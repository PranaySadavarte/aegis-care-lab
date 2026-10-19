import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"tests/sdk"))
from test_offline_contracts import guava,MockCall,patch
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from agent.harborcare import create_agent
class HarborCareHandlers(unittest.TestCase):
    def setUp(self):
        self.results=[]
        with patch("guava.agent.Client"): self.agent,self.backend=create_agent(outcomes=self.results)
    def verify(self,call):
        self.agent._on_call_start(call)
        call.set_field("caller_role","self")
        call.set_field("patient_id","HC-1001");call.set_field("verification_code","DEMO-42")
        self.agent._on_task_complete_handlers["verify"](call)
    def test_all_six_workflow_handlers(self):
        for flow in ["identity","eligibility","claims","appointments","billing","payments"]:
            with self.subTest(flow=flow):
                self.setUp();call=MockCall();self.verify(call)
                call.set_field("workflow",flow);self.agent._on_task_complete_handlers["choose"](call)
                if flow=="appointments":
                    call.set_field("slot",self.backend.slots[0]);self.agent._on_task_complete_handlers["book"](call)
                if flow=="payments":
                    call.set_field("amount_cents",1000);call.set_field("simulation_consent","yes")
                    self.agent._on_task_complete_handlers["pay"](call)
                self.assertEqual(len(self.results),1)
                if isinstance(self.results[0],dict): self.assertNotIn(self.results[0].get("status"),["denied","rejected"])
                else: self.assertEqual(self.results[0][0]["status"],"pending")
    def test_unverified_handler_denied(self):
        call=MockCall();call.set_field("workflow","billing")
        self.agent._on_task_complete_handlers["choose"](call)
        self.assertEqual(self.results[0]["status"],"rejected")
    def test_wrong_code_denied(self):
        call=MockCall();call.set_field("caller_role","self");call.set_field("patient_id","HC-1001");call.set_field("verification_code","wrong")
        self.agent._on_task_complete_handlers["verify"](call)
        self.assertEqual(self.results[0]["status"],"denied")

