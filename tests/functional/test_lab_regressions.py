"""Adversarial boundary regressions; independent of hosted language behavior."""
import sys, unittest
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"tests/sdk"))
from test_offline_contracts import patch, MockCall, guava
from agent.harborcare import create_agent

class LabRegressions(unittest.TestCase):
    def setUp(self):
        self.out=[]
        with patch("guava.agent.Client"):self.agent,self.b=create_agent(outcomes=self.out)
        self.c=MockCall()
    def verify(self,role="self"):
        for key,value in {"caller_role":role,"patient_id":"1001","verification_code":"4242"}.items():self.c.set_field(key,value)
        self.agent._on_task_complete_handlers["verify"](self.c)
    def test_representative_with_valid_code_denied(self):
        self.verify("representative")
        self.assertNotIn(self.c.id,self.b.authorized)
        self.assertEqual(self.out,[{"status":"authority_denied"}])
    def test_missing_role_fails_closed(self):
        self.verify(None);self.assertNotIn(self.c.id,self.b.authorized)
    def test_appointment_false_switch_does_not_revoke(self):
        self.verify()
        with patch("guava.helpers.llm.IntentRecognizer.classify",return_value=[guava.SuggestedAction(key="switch_patient")]):
            self.assertIsNone(self.agent._on_action_requested(self.c,"I choose appointments"))
        self.assertIn(self.c.id,self.b.authorized)
    def test_postverification_relative_revokes_before_read(self):
        self.verify()
        self.agent._on_caller_speech(self.c,SimpleNamespace(utterance="I am his brother without permission"))
        self.c.set_field("workflow","billing");self.agent._on_task_complete_handlers["choose"](self.c)
        self.assertEqual(self.out[-1]["status"],"rejected")
        self.assertNotIn("balance_cents",self.out[-1])
    def test_representative_request_does_not_call_classifier(self):
        self.verify()
        with patch("guava.helpers.llm.IntentRecognizer.classify") as classifier:
            self.agent._on_action_requested(self.c,"I am his brother without permission")
            classifier.assert_not_called()
        self.assertNotIn(self.c.id,self.b.authorized)
    def test_card_crosses_validator_without_raw_outcome(self):
        self.verify()
        for k,v in {"amount_cents":1000,"simulation_consent":"yes","payment_method":"synthetic_card"}.items():self.c.set_field(k,v)
        self.agent._on_task_complete_handlers["pay"](self.c)
        self.assertFalse(self.out)
        self.c.set_field("test_pan","4111111111111111");self.c.set_field("test_cvv","123")
        self.agent._on_task_complete_handlers["card"](self.c)
        self.assertEqual(self.out[-1]["remaining_cents"],4000)
        self.assertEqual(self.out[-1]["card_receipt"]["last_four"],"1111")
        self.assertNotIn("4111111111111111",str(self.out));self.assertNotIn("123",str(self.out))
    def test_card_nonfixture_rejected_without_debit(self):
        self.verify()
        for k,v in {"amount_cents":1000,"simulation_consent":"yes","test_pan":"9999","test_cvv":"123"}.items():self.c.set_field(k,v)
        self.agent._on_task_complete_handlers["card"](self.c)
        self.assertEqual(self.b.read(self.c.id,"billing")["balance_cents"],5000)
    def test_revocation_between_collection_and_card_completion(self):
        self.verify();self.b.close(self.c.id)
        self.agent._on_task_complete_handlers["card"](self.c)
        self.assertEqual(self.out[-1]["status"],"rejected")
    def test_validation_rejects_bool_overflow_and_string(self):
        self.verify();validate=self.agent._on_validate_handlers["amount_cents"]
        for value in [True,-1,0,5001,"1000",None]:self.assertEqual(validate(self.c,value)[0],False)
        self.assertIs(validate(self.c,1000),True)
    def test_datetime_helper_cannot_invent_slots(self):
        self.verify();slot=self.b.slots[0]
        with patch("guava.helpers.llm.DatetimeFilter.filter",return_value=(["2099-01-01 09:00",slot],["invented"])):
            self.assertEqual(self.agent._search_query_handlers["slot"](self.c,"morning"),([slot],[]))
    def test_cancel_revokes_and_does_not_debit(self):
        self.verify();self.agent._on_action_handlers["stop"](self.c)
        self.assertNotIn(self.c.id,self.b.authorized)
        self.assertEqual(self.b.patients["HC-1001"]["balance_cents"],5000)
    def test_slot_catalog_is_future(self):
        from datetime import datetime
        self.assertTrue(all(datetime.fromisoformat(x)>datetime.now() for x in self.b.slots))
    def test_account_attempt_limit_survives_session_change_and_expires(self):
        from backend.synthetic import SyntheticBackend
        now=[100];b=SyntheticBackend(clock=lambda:now[0])
        for i in range(3):self.assertFalse(b.verify(str(i),"1001","0000"))
        self.assertFalse(b.verify("new-session","1001","4242"))
        self.assertTrue(b.verify("other-patient","1002","9999"))
        now[0]=161
        self.assertTrue(b.verify("new-session","1001","4242"))
    def test_journal_untrusted_termination_is_not_exported(self):
        import tempfile
        from backend.call_journal import CallJournal
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/"events.jsonl"
            CallJournal(path)(self.c,"ended",{"termination":"PRIVATE-CANARY"})
            self.assertNotIn("PRIVATE-CANARY",path.read_text())
