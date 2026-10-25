"""Generate matched synthetic English voice fixtures; never label them human accents."""
import asyncio,hashlib,json,subprocess,shutil
from datetime import datetime,timezone
from pathlib import Path
import edge_tts,numpy as np,soundfile as sf
ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/'fixtures/audio/accents'
TEXT='Please schedule a meeting on Tuesday morning. The first test reference is one two three four. The second test reference is five six seven eight. I do not want a reminder.'
VOICES=[('david','US English / David','Microsoft David Desktop - English (United States)'),('us-guy','US English / Guy','en-US-GuyNeural'),('uk-ryan','British English / Ryan','en-GB-RyanNeural'),('india-prabhat','Indian English / Prabhat','en-IN-PrabhatNeural'),('australia-william','Australian English / William','en-AU-WilliamMultilingualNeural'),('nigeria-abeo','Nigerian English / Abeo','en-NG-AbeoNeural')]
async def main():
    FOLDER.mkdir(parents=True,exist_ok=True);scratch=ROOT/'work/accent-generation';scratch.mkdir(parents=True,exist_ok=True)
    rows=[]
    for key,label,voice in VOICES:
        source=scratch/(key+('.wav' if key=='david' else '.mp3'))
        if key=='david':
            request=scratch/'david-request.json';request.write_text(json.dumps({'text':TEXT,'voice':voice,'output':str(source)}),encoding='utf-8')
            subprocess.run(['powershell.exe','-NoProfile','-File',str(ROOT/'scripts/synthesize_accent_david.ps1'),'-RequestJson',str(request)],check=True)
        else:await edge_tts.Communicate(TEXT,voice,rate='+0%',volume='+0%',pitch='+0Hz').save(str(source))
        samples,sr=sf.read(source,dtype='float32')
        if samples.ndim>1:samples=samples.mean(axis=1)
        if sr!=16000:
            # Deterministic linear resampling, identical target format; no denoising/voice alteration.
            samples=np.interp(np.arange(round(len(samples)*16000/sr))*sr/16000,np.arange(len(samples)),samples)
        clean=FOLDER/(key+'.wav');sf.write(clean,samples,16000,subtype='PCM_16')
        preview=ROOT/'dashboard/assets/accents';preview.mkdir(parents=True,exist_ok=True);shutil.copyfile(clean,preview/clean.name)
        padded=FOLDER/(key+'-padded.wav');sf.write(padded,np.concatenate([np.zeros(8*16000),samples,np.zeros(3*16000)]),16000,subtype='PCM_16')
        rows.append({'id':key,'label':label,'voice_id':voice,'generator':'Windows SAPI' if key=='david' else 'edge-tts Microsoft online TTS','synthetic':True,'reference_text':TEXT,'target_entities':{'first_test_reference':'1234','second_test_reference':'5678'},'path':clean.relative_to(ROOT).as_posix(),'padded_path':padded.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(clean.read_bytes()).hexdigest(),'padded_sha256':hashlib.sha256(padded.read_bytes()).hexdigest(),'speech_seconds':round(len(samples)/16000,3),'sample_rate':16000,'channels':1,'sample_width':2,'padding_seconds':{'leading':8,'trailing':3}})
        print(label,'generated',flush=True)
    (FOLDER/'manifest.json').write_text(json.dumps({'created_at_utc':datetime.now(timezone.utc).isoformat(),'scope':'Six synthetic voices, one identical script, no human-accent representativeness. David is a different synthesizer; US Guy is a neural-engine control, not a full confound removal.','rows':rows},indent=2),encoding='utf-8')
asyncio.run(main())
