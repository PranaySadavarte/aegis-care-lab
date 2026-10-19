"""HarborCare synthetic prototype; native Guava tasks/fields/callbacks."""
import argparse
import json
import logging
import re
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import guava
from backend.synthetic import SyntheticBackend, AccessDenied, Conflict

def create_agent(backend=None, outcomes=None, recorder=None):
    backend=backend or SyntheticBackend()
    from agent.profile import load_profile
    profile=load_profile()
    def assign_task(call,*args,**kwargs):
        kwargs["objective"]=kwargs.get("objective","")+"\n"+"\n".join(profile[key] for key in ("scope","safety","verification","payments"))
        call.set_task(*args,**kwargs)
    from guava.helpers.llm import IntentRecognizer
    identity_intents=IntentRecognizer({"switch_patient":"Explicit request to change patient account; not selecting a workflow.",
        "appointments":"Book an appointment for the verified patient.","billing":"Check own balance.",
        "eligibility":"Check own coverage.","claims":"Check own claims.","payments":"Simulate a payment.",
        "stop":"Stop or cancel the conversation.","human":"Request human support."})
    agent=guava.Agent(name="HarborCare",organization="HarborCare",
                      purpose=profile["persona"])
    def finish(call, result):
        if recorder: recorder(call,"finished",{"workflow":call.get_field("workflow") or "verification","result_status":result.get("status","returned") if isinstance(result,dict) else "returned","verified":call.id in backend.authorized})
        if outcomes is not None: outcomes.append(result)
        call.set_variable("qa_result",result)
        if isinstance(result,dict) and result.get("status")=="authority_denied":
            message="This demo supports only the patient calling for their own account. I cannot share another person's records."
        elif isinstance(result,dict) and result.get("status")=="denied":
            message="I could not verify those details. Please check your patient ID and code and call again."
        elif isinstance(result,dict) and "balance_cents" in result:
            message="Your account balance is "+format(result["balance_cents"]/100,".2f")+" dollars."
        elif isinstance(result,dict) and "plan" in result:
            message="Your plan is "+result["plan"]+". Coverage is "+("active." if result["active"] else "inactive.")
        elif isinstance(result,list):
            message="Your claim "+result[0]["id"]+" is "+result[0]["status"]+"." if result else "There are no claims on this account."
        elif isinstance(result,dict) and result.get("status") in ("booked","already_booked"):
            message="Your appointment is confirmed for "+result["slot"]+"."
        elif isinstance(result,dict) and result.get("status")=="simulated_only":
            message="Your demo payment of "+format(result["amount_cents"]/100,".2f")+" dollars is recorded. No real charge was made."
        elif isinstance(result,dict) and result.get("status")=="verified":
            message="Your identity check is complete."
        else: message="I am unable to complete this request right now. Please try again."
        call.hangup("Tell the caller this result naturally, then close courteously: "+message)
    @agent.on_call_start
    def start(call):
        if recorder: recorder(call,"started")
        assign_task(call,"verify",objective="Welcome the caller. Mention demo data once, briefly. Verify identity before discussing records. Never request real personal or card details.",
                       checklist=[guava.Say("Welcome to HarborCare. This demo uses sample records. I can help with your coverage, claims, appointments, or account."),
                                  guava.Field(key="caller_role",field_type="multiple_choice",choices=["self","representative"],description="Ask whether the caller is the patient themselves or calling for another person. Representatives are unsupported, even with the patient's code."),
                                  guava.Field(key="patient_id",description="Collect synthetic patient ID as digits, such as 1001. Legacy HC-prefixed IDs also work."),
                                  guava.Field(key="verification_code",description="Collect the four-digit synthetic verification code as digits, preserving zeros. Do not guess or disclose a code. Legacy DEMO-prefixed codes also work.",sensitive=True)])
    @agent.on_task_complete("verify")
    def verified(call):
        if call.get_field("caller_role")!="self":
            backend.close(call.id)
            finish(call,{"status":"authority_denied"});return
        if not backend.verify(call.id,str(call.get_field("patient_id") or "").strip(),str(call.get_field("verification_code") or "").strip()):
            logging.getLogger("harborcare").info("Synthetic verification denied; exact accepted credentials did not match. No credential values logged.")
            finish(call,{"status":"denied","message":"Synthetic verification failed."})
            return
        assign_task(call,"choose",objective="Ask how you can help with coverage, claims, appointments, billing or a demo payment. Use the matching workflow without naming internal test labels.",
                       checklist=[guava.Field(key="workflow",field_type="multiple_choice",
                         choices=["identity","eligibility","claims","appointments","billing","payments"],
                         description="Choose one workflow for this call.")])
    @agent.on_task_complete("choose")
    def choose(call):
        workflow=call.get_field("workflow")
        try:
            backend.subject(call.id)
            if workflow=="identity": finish(call,{"status":"verified","synthetic_only":True})
            elif workflow in ("eligibility","claims","billing"): finish(call,backend.read(call.id,workflow))
            elif workflow=="appointments":
                available=backend.read(call.id,"appointments")["available"]
                if not available: finish(call,{"status":"no_slots"}); return
                assign_task(call,"book",objective="Book one of the available synthetic appointment slots.",
                               checklist=[guava.Field(key="slot",field_type="multiple_choice",choices=available,searchable=True)])
            elif workflow=="payments":
                balance=backend.read(call.id,"billing")["balance_cents"]
                assign_task(call,"pay",objective="Simulate payment only. Current synthetic balance in cents: "+str(balance),
                               checklist=[guava.Field(key="amount_cents",field_type="integer",description="Positive whole cents, no greater than the synthetic balance."),
                                          guava.Field(key="simulation_consent",field_type="multiple_choice",choices=["yes","no"],
                                                      description="Explicit consent to a simulated payment only."),
                                          guava.Field(key="payment_method",field_type="multiple_choice",choices=["demo_token","synthetic_card"],description="Choose existing demo token or designated synthetic-card SDK test. Never use a real card.")])
            else: finish(call,{"status":"unsupported"})
        except (AccessDenied,ValueError,Conflict):
            finish(call,{"status":"rejected","message":"Synthetic request could not be completed."})
    @agent.on_task_complete("book")
    def book(call):
        try: finish(call,backend.book(call.id,call.get_field("slot")))
        except (AccessDenied,ValueError,Conflict): finish(call,{"status":"rejected"})
    @agent.on_task_complete("pay")
    def pay(call):
        try:
            backend.subject(call.id)
            if call.get_field("simulation_consent")!="yes":
                finish(call,{"status":"rejected"});return
            if call.get_field("payment_method")=="synthetic_card":
                assign_task(call,"card",objective="SDK synthetic-card test only. Collect the designated fixture 4111111111111111 and CVV 123. Never repeat either value. No real charge. Sensitive fields do not guarantee transcript redaction.",checklist=[
                    guava.Field(key="test_pan",field_type="digit_sequence",sensitive=True,description="Designated synthetic test PAN only."),
                    guava.Field(key="test_cvv",field_type="cvv",sensitive=True,description="Designated synthetic CVV only.")]);return
            finish(call,backend.pay(call.id,call.get_field("amount_cents"),"SIMULATED-TOKEN",
                                   call.get_field("simulation_consent")=="yes",call.id+":payment"))
        except (AccessDenied,ValueError,Conflict): finish(call,{"status":"rejected","message":"No simulated payment completed."})
    @agent.on_task_complete("card")
    def card(call):
        from backend.sensitive_demo import SyntheticSensitiveProcessor
        try:
            backend.subject(call.id)
            if call.get_field("simulation_consent")!="yes":raise ValueError("Consent required")
            receipt=SyntheticSensitiveProcessor().card_receipt(call.get_field("test_pan"),call.get_field("test_cvv"))
            result=backend.pay(call.id,call.get_field("amount_cents"),"SIMULATED-TOKEN",True,call.id+":payment")
            result["card_receipt"]={"last_four":receipt["last_four"],"synthetic_only":True}
            finish(call,result)
        except (AccessDenied,ValueError,Conflict):finish(call,{"status":"rejected"})
    @agent.on_validate("amount_cents")
    def amount_valid(call,value):
        try:
            return True if type(value) is int and 0<value<=backend.read(call.id,"billing")["balance_cents"] else (False,"Use positive whole cents within the balance.")
        except AccessDenied:return (False,"Verification required.")
    @agent.on_search_query("slot")
    def search_slots(call,query):
        from guava.helpers.llm import DatetimeFilter
        try:
            available=backend.read(call.id,"appointments")["available"]
            matches,alternatives=DatetimeFilter(available).filter(query)
            # SDK-X003: distrust generated slot values, even with a constrained prompt.
            return ([x for x in matches if x in available],[x for x in alternatives if x in available])
        except AccessDenied:return ([],[])
    @agent.on_caller_speech
    def caller_speech(call,event):
        # Conservative tripwire supplements explicit role collection; no speech is journaled.
        text=getattr(event,"utterance","") or ""
        if re.search(r"\b(brother|sister|husband|wife|father|mother|on behalf|without permission|not the patient)\b",text,re.I):
            backend.close(call.id)
            call.send_instruction("Do not disclose account information. Representative access is unsupported. End with a refusal.")
    @agent.on_escalate
    def escalate(call,event):
        backend.close(call.id)
        call.hangup("Explain that this local demo has no connected human queue. Ask the caller to contact their clinic directly.")
    @agent.on_action_request
    def action_request(call,request):
        if re.search(r"\b(brother|sister|husband|wife|on behalf|without permission|not the patient)\b",request,re.I):
            backend.close(call.id)
            return [guava.SuggestedAction(key="deny_representative",description="Refuse unsupported representative access.")]
        actions=identity_intents.classify(request)
        if actions and any(item.key=="switch_patient" for item in actions):
            # A single-choice classifier can overmatch. Require explicit lexical evidence too.
            if not re.search(r"\b(different patient|another patient|switch patient|change patient|different account|another account)\b",request,re.I):return None
            return [guava.SuggestedAction(key="switch_patient",description="Verify the different patient before any account access.")]
        return actions
    @agent.on_action("deny_representative")
    def deny_representative(call):
        backend.close(call.id);finish(call,{"status":"authority_denied"})
    for workflow_key in ("appointments","billing","eligibility","claims","payments"):
        def route(call,key=workflow_key):
            call.set_variable("requested_workflow",key)
            # Native fields remain authoritative; a suggestion cannot overwrite collected state.
            if call.id not in backend.authorized:
                start(call);return
            assign_task(call,"choose",objective="The caller requests "+key+". Confirm that workflow.",checklist=[guava.Field(key="workflow",field_type="multiple_choice",choices=["identity","eligibility","claims","appointments","billing","payments"])])
        agent.on_action(workflow_key)(route)
    @agent.on_action("stop")
    def stop(call):
        backend.close(call.id);call.hangup("Confirm cancellation. No further action will be taken.")
    @agent.on_action("human")
    def human(call):escalate(call,None)
    @agent.on_action("switch_patient")
    def switch_patient(call):
        backend.close(call.id)
        assign_task(call,"switch_verify",objective="Explain that access to a different account requires fresh verification. Do not reuse the earlier code.",
                      checklist=[guava.Field(key="new_patient_id",description="The different patient ID."),
                                 guava.Field(key="new_caller_role",field_type="multiple_choice",choices=["self","representative"],description="Only the patient themselves is supported."),
                                 guava.Field(key="new_verification_code",description="The code for that patient; never guess it.",sensitive=True)])
    @agent.on_task_complete("switch_verify")
    def switch_verified(call):
        if call.get_field("new_caller_role")!="self":
            backend.close(call.id);finish(call,{"status":"authority_denied"});return
        if not backend.verify(call.id,str(call.get_field("new_patient_id") or ""),str(call.get_field("new_verification_code") or "")):
            finish(call,{"status":"denied"});return
        assign_task(call,"choose",objective="Ask how you can help with coverage, claims, appointments, billing or a demo payment.",
                      checklist=[guava.Field(key="workflow",field_type="multiple_choice",choices=["identity","eligibility","claims","appointments","billing","payments"])])
    @agent.on_question
    def question(call, question):
        from agent.sdk_knowledge import answer_sdk_question
        sdk_answer=answer_sdk_question(question)
        if sdk_answer:return sdk_answer
        return profile["question-fallback"]
    @agent.on_session_end
    def ended(call, event):
        if recorder: recorder(call,"ended",{"termination":event.termination_reason})
        backend.close(call.id)
    return agent, backend

def plain_text_chat(agent):
    """Simple terminal view built on native TestSession, not a new dialog engine."""
    from websockets.exceptions import ConnectionClosedOK
    with agent.test() as session:
        printed=0
        while True:
            try: session.wait_for_turn()
            except ConnectionClosedOK:
                print(session.get_transcript()[printed:]);break
            transcript=session.get_transcript();print(transcript[printed:]);printed=len(transcript)
            try:message=input("You: ").strip()
            except EOFError:break
            if message.lower() in ("quit","exit"):break
            if message:session.say(message)

if __name__=="__main__":
    import tomllib
    args=argparse.ArgumentParser()
    args.add_argument("--mode",choices=["chat","text","phone","webrtc","local"],default="chat")
    options=args.parse_args()
    from guava import logging_utils
    logging_utils.configure_logging()
    from backend.call_journal import CallJournal
    journal=CallJournal(Path(__file__).resolve().parents[1]/"evidence/2026-10-11/call-history/manual-events.jsonl",channel=options.mode)
    agent,_=create_agent(recorder=journal)
    if options.mode=="phone":
        config=tomllib.loads((Path(__file__).resolve().parents[1]/"harborcare-agent/guava.toml").read_text())
        agent.listen_phone(config["phone_number"])
    elif options.mode=="webrtc": agent.listen_webrtc()
    elif options.mode=="local": agent.call_local()
    elif options.mode=="text": plain_text_chat(agent)
    else: agent.chat()
