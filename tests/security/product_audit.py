"""Independent security expectations; failures are findings, not adjusted to pass."""
import json,sys,tempfile
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from backend.synthetic import SyntheticBackend
from backend.call_journal import CallJournal
from guava.testing.session import TestSession
checks=[]
def record(id,expected,actual,passed,owner):checks.append(dict(id=id,expected=expected,actual=actual,status="PASS" if passed else "FAIL",owner=owner))
b=SyntheticBackend()
for i in range(8):b.verify("guess-session","1001",str(4100+i))
accepted=b.verify("guess-session","1001","4242")
record("AUTH-RATE-LIMIT","Repeated wrong codes trigger lockout or bounded attempt policy",{"eight_failures_then_correct_accepted":accepted},not accepted,"AEGIS application; demo-only limitation")
b=SyntheticBackend()  # Independent payment probe must not inherit the lockout under test.
b.verify("payer","1001","4242")
r=b.pay("payer",1000,"SIMULATED-TOKEN",True,"same-key")
r2=b.pay("payer",1000,"SIMULATED-TOKEN",True,"same-key")
record("PAY-REPLAY","Same idempotency key creates one simulated debit",{"balance":b.read("payer","billing")["balance_cents"]},r==r2 and b.read("payer","billing")["balance_cents"]==4000,"AEGIS application")
record("PERSISTENCE","Committed demo transactions survive backend restart",{"restarted_balance":SyntheticBackend().patients["HC-1001"]["balance_cents"]},SyntheticBackend().patients["HC-1001"]["balance_cents"]==4000,"AEGIS application; explicitly in-memory prototype")
class Stub:
 def send(self,data):pass
s=TestSession(Stub(),"synthetic-session")
s.say("Synthetic card 4111111111111111, CVV 123, vital-data marker SYNTHETIC-VITAL-CANARY")
transcript=s.get_transcript()
record("TEST-TRANSCRIPT-REDACTION","Shared/exported evaluation transcripts exclude synthetic PAN/CVV/canary",{"pan_present":'4111111111111111' in transcript,"cvv_present":'123' in transcript,"canary_present":'SYNTHETIC-VITAL-CANARY' in transcript},not any(x in transcript for x in ('4111111111111111','123','SYNTHETIC-VITAL-CANARY')),"Guava testing API / AEGIS export handling; not production retention evidence")
with tempfile.TemporaryDirectory() as d:
 path=Path(d)/"journal.jsonl";journal=CallJournal(path)
 journal(SimpleNamespace(id="synthetic-session"),"ended",{"termination":"SYNTHETIC-VITAL-CANARY"})
 record("JOURNAL-UNTRUSTED-DETAIL","Event detail is constrained to documented termination values",{"canary_present":'SYNTHETIC-VITAL-CANARY' in path.read_text()},'SYNTHETIC-VITAL-CANARY' not in path.read_text(),"AEGIS journal boundary; synthetic event injection only")
print(json.dumps({"scope":"Deterministic product probes; not platform penetration test","checks":checks},indent=2))
raise SystemExit(1 if any(r['status']=='FAIL' for r in checks) else 0)
