from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from threading import Lock
from pathlib import Path
import json,subprocess
from urllib.parse import urlsplit,parse_qs
from refresh_calls import refresh_calls
from voice_session import VoiceSession
root=Path(__file__).resolve().parents[1]
lock=Lock()
active_run=None
voice=VoiceSession(root)
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(root),**kwargs)
    def end_headers(self):
        self.send_header("Cache-Control","no-store")
        super().end_headers()
    def do_POST(self):
        global active_run
        port=self.server.server_port
        allowed_hosts=(f"127.0.0.1:{port}",f"localhost:{port}")
        origin=self.headers.get("Origin")
        if self.path not in ("/api/tests/start","/api/agent/start") or self.headers.get("Host") not in allowed_hosts or origin not in (None,f"http://127.0.0.1:{port}",f"http://localhost:{port}"):
            self.send_error(403);return
        if self.path=="/api/agent/start":
            try:
                with lock:data=voice.start()
                body=json.dumps(data).encode();self.send_response(202)
            except (OSError,subprocess.TimeoutExpired):
                body=json.dumps({'status':'error','message':'Could not start listener; inspect local evidence/managed-webrtc.log.'}).encode();self.send_response(503)
            self.send_header("Content-Type","application/json");self.end_headers();self.wfile.write(body);return
        try:
            length=int(self.headers.get("Content-Length","0"))
            if length<1 or length>1024: raise ValueError()
            request=json.loads(self.rfile.read(length))
            suite=request.get("suite")
            if suite not in ("offline","hosted","security","audio","adversarial","robustness","kpi","extended","adaptive","fixture-audio","fixture-text","compliance","review-audio","all"):raise ValueError()
            with lock:
                state_path=root/"dashboard/run-status.json"
                state=json.loads(state_path.read_text()) if state_path.exists() else {}
                if (active_run and active_run.poll() is None) or state.get("status")=="RUNNING":
                    body=json.dumps({"error":"A suite is already running"}).encode();code=409
                else:
                    active_run=subprocess.Popen([str(root/"baseline/sdk-0.47.0/.venv/Scripts/python.exe"),str(root/"tests/run_all.py"),"--suite",suite],
                                                cwd=root,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,
                                                creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0))
                    body=json.dumps({"started":True,"suite":suite}).encode();code=202
            self.send_response(code);self.send_header("Content-Type","application/json");self.end_headers();self.wfile.write(body)
        except (ValueError,json.JSONDecodeError):
            self.send_error(400,"Invalid fixed suite request")
    def do_GET(self):
        if self.path=="/api/agent/status":
            with lock:data=voice.status()
            body=json.dumps(data).encode();self.send_response(200);self.send_header("Content-Type","application/json");self.end_headers();self.wfile.write(body);return
        if self.path=="/api/calls/refresh":
            try:
                with lock:data=refresh_calls()
                body=json.dumps(data).encode()
                self.send_response(200)
            except Exception:
                body=json.dumps({"error":"Call refresh failed; retained previous snapshot. Check local evidence."}).encode()
                self.send_response(503)
            self.send_header("Content-Type","application/json");self.send_header("Cache-Control","no-store")
            self.end_headers();self.wfile.write(body)
        else:
            candidate=Path(self.translate_path(self.path)).resolve()
            if not any(candidate.is_relative_to(root/area) for area in ("dashboard","reports","docs")):
                self.send_error(403,"Only dashboard and sanitized reports are served")
                return
            if candidate.suffix.lower()==".md" and candidate.is_file():
                content=candidate.read_bytes()
                try:text=content.decode("utf-8-sig")
                except UnicodeDecodeError:text=content.decode("cp1252",errors="replace")
                # Repair historical display-only encoding artifacts without changing source/evidence.
                for bad,good in [("\u00c2\u00b7"," / "),("\u00e2\u2020\u2014",""),("\u00e2\u20ac\u201d","-"),("\u00e2\u20ac\u201c","-")]:text=text.replace(bad,good)
                raw=parse_qs(urlsplit(self.path).query).get("raw")==["1"]
                if raw:body=text.encode("utf-8");content_type="text/plain; charset=utf-8"
                else:
                    renderer=root/"baseline/dashboard/.venv/Scripts/python.exe"
                    try:
                        rendered=subprocess.run([str(renderer),str(root/"dashboard/render_report.py")],input=json.dumps({"text":text,"path":candidate.relative_to(root).as_posix()}),capture_output=True,text=True,encoding="utf-8",timeout=10)
                        if rendered.returncode:raise RuntimeError("Report renderer failed")
                        body=rendered.stdout.encode("utf-8");content_type="text/html; charset=utf-8"
                    except (OSError,subprocess.TimeoutExpired,RuntimeError):
                        self.send_error(503,"Report renderer unavailable; see operator guide for isolated reporting environment");return
                self.send_response(200);self.send_header("Content-Type",content_type)
                self.send_header("Content-Length",str(len(body)))
                self.send_header("X-Content-Type-Options","nosniff")
                self.send_header("Content-Security-Policy","default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; frame-ancestors 'none'")
                self.end_headers();self.wfile.write(body);return
            super().do_GET()
class LocalDashboardServer(ThreadingHTTPServer):
    allow_reuse_address=False

if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8765);args=parser.parse_args()
    print(f"Dashboard on http://127.0.0.1:{args.port}/dashboard/",flush=True)
    LocalDashboardServer(("127.0.0.1",args.port),Handler).serve_forever()
