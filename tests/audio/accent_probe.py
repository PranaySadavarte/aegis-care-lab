"""One native hosted file-audio observation, separate from healthcare workflows."""
import sys,json,time,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
import guava
from accent_scoring import score
row=next(r for r in json.loads((ROOT/'fixtures/audio/accents/manifest.json').read_text())['rows'] if r['id']==sys.argv[1])
folder=Path(sys.argv[2]);source=ROOT/row['padded_path']
assert hashlib.sha256(source.read_bytes()).hexdigest()==row['padded_sha256'],'Input hash differs from manifest'
heard={};agent=guava.Agent(name='AccentASRProbe',purpose='Listen to a neutral prerecorded meeting-and-test-reference sentence. Do not guess missing words or digits.')
@agent.on_call_start
def start(call):call.set_task('listen',objective='Ask the caller to read their sample sentence and listen without interrupting.',checklist=[guava.Field(key='sample',description='The sample sentence spoken by the caller; do not infer missing content.')])
@agent.on_caller_speech
def speech(call,event):heard[event.utterance_id or str(len(heard))]=event.utterance
begin=time.monotonic()
agent.test_audio(source,folder/(row['id']+'-agent.wav'))
hypothesis=' '.join(heard.values())
result={**row,**score(row['reference_text'],hypothesis),'hypothesis':hypothesis,'speech_events':len(heard),'process_seconds':round(time.monotonic()-begin,3),'scope':'Native Guava SDK file-audio observation. Synthetic voice comparison; not a scored healthcare call, isolated ASR latency, live microphone or population accent benchmark.'}
(folder/(row['id']+'.json')).write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({'id':row['id'],'status':result['scoring_status'],'literal_wer':result['literal_wer'],'numeral_wer':result['numeral_wer'],'exact_test_sequences':result['exact_test_sequences']}),flush=True)
