"""Append-only sanitized manual call outcomes; no credentials, numbers or transcript."""
import json,hashlib
from datetime import datetime,timezone
from threading import Lock
from backend.evaluation import evaluate_observation
class CallJournal:
    def __init__(self,path,channel="unknown"):self.path=path;self.channel=channel;self.lock=Lock();self.finished=set()
    def __call__(self,call,event,detail=None):
        if event not in ("started","finished","ended"):raise ValueError("Unsupported journal event")
        if event=="ended":
            allowed={"caller-hangup","bot-hangup","error","timeout","unknown"}
            termination=(detail or {}).get("termination")
            detail={"termination":termination if termination in allowed else "unknown"}
        row={"call":"call-"+hashlib.sha256(call.id.encode()).hexdigest()[:10],
             "at_utc":datetime.now(timezone.utc).isoformat(),"event":event,"detail":detail,"channel":self.channel}
        if event=="finished": row["evaluation"]=evaluate_observation(detail or {})
        with self.lock:
            if event=="finished": self.finished.add(row["call"])
            if event=="ended":
                if row["call"] not in self.finished:
                    row["evaluation"]={"authorization_gate":"INCONCLUSIVE","workflow_outcome":"NO_RESULT","semantic_accuracy":"NOT_EVALUATED","asr_accuracy":"NOT_MEASURED","scope":"Call ended before an Expert result"}
                self.finished.discard(row["call"])
            self.path.parent.mkdir(parents=True,exist_ok=True)
            with self.path.open("a",encoding="utf-8") as out:out.write(json.dumps(row)+"\n")
