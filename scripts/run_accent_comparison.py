"""Run each prerecorded voice once, with bounded processes and preserved provenance."""
import sys,subprocess,json,uuid,hashlib,platform
from pathlib import Path
from datetime import datetime,timezone
from importlib.metadata import version
ROOT=Path(__file__).resolve().parents[1]
stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:6]
folder=ROOT/'evidence/accent-comparison'/stamp;folder.mkdir(parents=True)
manifest=ROOT/'fixtures/audio/accents/manifest.json';rows=[]
for fixture in json.loads(manifest.read_text())['rows']:
    process=subprocess.Popen([sys.executable,str(ROOT/'tests/audio/accent_probe.py'),fixture['id'],str(folder)],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8')
    try:out,err=process.communicate(timeout=90);status='EXITED'
    except subprocess.TimeoutExpired:
        subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],capture_output=True);out,err=process.communicate(timeout=10);status='TIMEOUT'
    (folder/(fixture['id']+'.log')).write_text(out+'\n'+err,encoding='utf-8')
    result_path=folder/(fixture['id']+'.json')
    result=json.loads(result_path.read_text()) if result_path.exists() else {**fixture,'scoring_status':status if status=='TIMEOUT' else 'ERROR','literal_wer':None,'numeral_wer':None,'hypothesis':None}
    result.update(process_status=status,exit_code=process.returncode);rows.append(result)
    print(json.dumps({key:result.get(key) for key in ['id','scoring_status','literal_wer','numeral_wer','exact_test_sequences']}),flush=True)
    (folder/'partial-summary.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
baseline=rows[0]
for row in rows:
    row['literal_wer_delta_vs_david_pp']=round((row['literal_wer']-baseline['literal_wer'])*100,2) if row.get('literal_wer') is not None and baseline.get('literal_wer') is not None else None
summary={'run_id':stamp,'created_at_utc':datetime.now(timezone.utc).isoformat(),'sdk_version':version('guava-sdk'),'python':platform.python_version(),'os':platform.platform(),'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'manifest_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),'repetitions_per_voice':1,'scope':'Six synthetic voice samples with one matched neutral script. No independent human speakers; accent, voice and synthesis-engine effects are confounded. No population accuracy or healthcare workflow claim.','rows':rows}
(folder/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
target=ROOT/'reports/test-results/accent-comparison-2026-10-25.json';target.write_text(json.dumps(summary,indent=2),encoding='utf-8')
(ROOT/'dashboard/accent-comparison.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print('Saved '+str(target),flush=True)
sys.exit(1 if any(x['scoring_status']!='OBSERVED' or x.get('exit_code')!=0 for x in rows) else 0)
