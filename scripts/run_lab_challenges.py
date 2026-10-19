"""Three sequential hosted challenges, each bounded at 90 seconds."""
import subprocess,sys,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
rows=[]
for case in (sys.argv[1:] or ("appointments","representative","card")):
    try:
        p=subprocess.run([sys.executable,"tests/integration/lab_challenges.py",case],cwd=root,capture_output=True,text=True,timeout=90)
        (root/"evidence"/f"lab-{case}.log").write_text(p.stdout+"\n"+p.stderr,encoding="utf-8")
        observations=[]
        for line in p.stdout.splitlines():
            try:
                obj=json.loads(line)
                if isinstance(obj,dict) and obj.get("case")==case:observations.append(obj)
            except ValueError:pass
        row={"case":case,"status":"PASS" if p.returncode==0 else "FAIL","exit_code":p.returncode,"observations":observations}
    except subprocess.TimeoutExpired as e:
        (root/"evidence"/f"lab-{case}.log").write_bytes((e.stdout or b"")+b"\n"+(e.stderr or b""))
        row={"case":case,"status":"TIMEOUT","limit_seconds":90}
    rows.append(row);print(json.dumps(row),flush=True)
(root/("reports/test-results/lab-hosted-followup-2026-10-18.json" if sys.argv[1:] else "reports/test-results/lab-hosted-2026-10-18.json")).write_text(json.dumps(rows,indent=2),encoding="utf-8")
