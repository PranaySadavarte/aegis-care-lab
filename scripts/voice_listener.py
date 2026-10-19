"""Dashboard-owned listener with explicit one-hour expiry metadata."""
import json,os,sys
from datetime import datetime,timedelta,timezone
from pathlib import Path
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
import guava
from agent.harborcare import create_agent
from backend.call_journal import CallJournal
from guava import logging_utils
logging_utils.configure_logging()
agent,_=create_agent(recorder=CallJournal(root/'evidence/2026-10-11/call-history/manual-events.jsonl',channel='webrtc'))
created=datetime.now(timezone.utc)
code=guava.Client().create_webrtc_agent(ttl=timedelta(hours=1))
manifest=root/'dashboard/agent-session.json'
temporary=manifest.with_suffix('.tmp')
temporary.write_text(json.dumps({'pid':os.getpid(),'url':'https://app.goguava.ai/debug-webrtc?webrtc_code='+code,'expires_at':(created+timedelta(minutes=59)).isoformat()}))
temporary.replace(manifest)
agent.listen_webrtc(code)
