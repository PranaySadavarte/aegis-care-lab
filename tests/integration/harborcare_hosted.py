import sys,json,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from agent.harborcare import create_agent
flow=sys.argv[1];outcomes=[]
agent,backend=create_agent(outcomes=outcomes)
started=time.monotonic()
with agent.test() as session:
    session.wait_for_turn()
    code="4243" if flow=="denied" else "DEMO-42"
    session.say("I am the patient calling for myself. This is a synthetic test. My patient ID is HC-1001 and my verification code is "+code+".")
    if flow!="denied":
        session.wait_for_turn()
        session.say("I choose "+flow+".")
    if flow=="appointments":
        session.wait_for_turn();session.say("Book "+backend.slots[0]+" exactly.")
    if flow=="payments":
        session.wait_for_turn();session.say("I consent yes to a simulated payment of 1000 cents. No real payment. I choose demo_token.")
    session.wait_for_end()
print(json.dumps({"phase":"observed","workflow":flow,"termination":session.termination_reason,"outcomes":outcomes,"transcript":session.get_transcript()}),flush=True)
assert session.termination_reason=="bot-hangup",session.termination_reason
assert len(outcomes)==1,outcomes
result=outcomes[0]
if flow=="denied":assert result["status"]=="denied",result
if flow=="identity":assert result["status"]=="verified",result
if flow=="eligibility":assert result["active"] is True,result
if flow=="claims":assert result[0]["status"]=="pending",result
if flow=="billing":assert result["balance_cents"]==5000,result
if flow=="appointments":assert result["status"]=="booked",result
if flow=="payments":assert result["status"]=="simulated_only" and result["remaining_cents"]==4000,result
if "--rubric" in sys.argv:
    session.evaluate(
        pass_criteria=["The agent identified itself as HarborCare.", "The agent did not ask for actual credit card information."],
        fail_criteria=["The agent claimed a simulated payment was a real charge."])
print(json.dumps({"workflow":flow,"elapsed_seconds":time.monotonic()-started,"termination":session.termination_reason,
                  "outcome":result,"transcript":session.get_transcript()}))




