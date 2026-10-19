"""Own one temporary WebRTC listener; never treat a saved URL as readiness."""
import json,subprocess,os
from datetime import datetime,timezone
from pathlib import Path

class VoiceSession:
    def __init__(self,root):
        self.root=Path(root);self.process=None
        self.manifest=self.root/'dashboard/agent-session.json'
        self.log=self.root/'evidence/managed-webrtc.log'
    def status(self):
        if self.process is None or self.process.poll() is not None:return {'status':'stopped'}
        try:
            data=json.loads(self.manifest.read_text())
            if datetime.fromisoformat(data['expires_at'])<=datetime.now(timezone.utc):return {'status':'expired'}
            if 'Started listing on WebRTC code' not in self.log.read_text(errors='replace'):return {'status':'starting'}
            return {'status':'ready','url':data['url'],'expires_at':data['expires_at']}
        except (OSError,ValueError,KeyError):return {'status':'starting'}
    def start(self):
        state=self.status()
        if state['status'] in ('ready','starting'):return state
        if self.process is not None and self.process.poll() is None:
            # Windows venv Python launches a runtime child; stop only our owned tree.
            if os.name=='nt':
                subprocess.run(['taskkill','/PID',str(self.process.pid),'/T','/F'],capture_output=True,timeout=10,check=True)
            else:self.process.terminate()
            self.process.wait(timeout=10)
        self.log.parent.mkdir(parents=True,exist_ok=True)
        self.manifest.unlink(missing_ok=True)
        with self.log.open('w',encoding='utf-8') as output:
            self.process=subprocess.Popen([str(self.root/'baseline/sdk-0.47.0/.venv/Scripts/python.exe'),str(self.root/'scripts/voice_listener.py')],cwd=self.root,stdout=output,stderr=output,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        return {'status':'starting'}
