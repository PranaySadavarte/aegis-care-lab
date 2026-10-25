# Prerecorded accent comparison against David

Date: October 25, 2026. One hosted native file-audio run per synthetic voice. SDK 0.47.0.

## What changed

Added six matched recordings: Windows SAPI David (US), Microsoft neural Guy (US control), Ryan (British), Prabhat (Indian), William (Australian), and Abeo (Nigerian). These are synthetic locale-labelled voice samples, not recordings of independent human speakers.

Every voice reads the same neutral sentence. No patient records, verification credentials, financial context or personal data were sent to the external TTS service. The script tests a weekday, time-of-day phrase, two arbitrary digit sequences and a negative preference.

> Please schedule a meeting on Tuesday morning. The first test reference is one two three four. The second test reference is five six seven eight. I do not want a reminder.

Pipeline: shared script -> selected TTS voice -> prerecorded PCM16 WAV -> common 16 kHz mono format -> 8 seconds leading / 3 seconds trailing silence -> native Guava Agent.test_audio -> caller-speech events -> independent scoring.

The new probe is isolated from HarborCare healthcare workflows and does not replace the main agent or live phone listener. It measures file-audio transcription, not business workflow completion.

## Actual results

| Voice / locale | Raw WER | Numeral-normalized WER | Delta vs David (raw, pp) | Exact digit sequences | Negative cue observed |
|---|---:|---:|---:|---|---|
| US English / David | 25.81% | 0.00% | +0.00 | 2/2, correct order | Yes |
| US English / Guy | 25.81% | 0.00% | +0.00 | 2/2, correct order | Yes |
| British English / Ryan | 25.81% | 0.00% | +0.00 | 2/2, correct order | Yes |
| Indian English / Prabhat | 29.03% | 16.00% | +3.23 | 1/2; mismatch | Yes |
| Australian English / William | 25.81% | 0.00% | +0.00 | 2/2, correct order | Yes |
| Nigerian English / Abeo | 41.94% | 24.00% | +16.13 | 1/2; mismatch | Yes |

Raw WER compares normalized words without converting spoken number words to digits. Numeral-normalized WER applies the same digit-word joining to reference and hypothesis. The two exact sequences must be 1234 and 5678 in order, with no extra digit sequence. The negative cue is a lexical observation, not proof of semantic consent handling.

In this run, David, US Guy, British Ryan and Australian William matched after numeral normalization. Indian Prabhat returned the first sequence as "1 to 34" and omitted "The" before "first". Nigerian Abeo omitted the entire first-reference sentence from the captured transcript. Both retained 5678 and the negative cue. These are script-to-captured-transcript differences, not isolated proof of an accent-specific ASR defect: synthesis, endpointing and event capture have not been independently separated.

## Transcripts

### US English / David

Recognized: Please schedule a meeting on Tuesday morning. The first test reference is 1234. The second test reference is 5678. I do not want a reminder.

### US English / Guy

Recognized: Please schedule a meeting on Tuesday morning. The first test reference is 1234. The second test reference is 5678. I do not want a reminder.

### British English / Ryan

Recognized: Please schedule a meeting on Tuesday morning. The first test reference is 1234. The second test reference is 5678. I do not want a reminder.

### Indian English / Prabhat

Recognized: Please schedule a meeting on Tuesday morning. First test reference is 1 to 34. The second test reference is 5678. I do not want a reminder.

### Australian English / William

Recognized: Please schedule a meeting on Tuesday morning. The first test reference is 1234. The second test reference is 5678. I do not want a reminder.

### Nigerian English / Abeo

Recognized: Please schedule a meeting on Tuesday morning. The second test reference is 5678. I do not want a reminder.

## Interpretation and limits

This is one identical script and one trial per voice; it cannot establish that any accent is generally easier or harder. A zero numeral-normalized score means the normalized reference matched in this sample, not general perfect recognition. Raw numeral-format differences are not necessarily lost information.

David uses Windows SAPI; the others use Microsoft online neural synthesis, including MP3 decoding and linear resampling to 16 kHz. The US neural control helps show a possible engine effect but does not isolate accent from speaker, pace, timbre or codec. Default rates were retained and speech durations differ. No added noise, repeated trials, human-accent population, live microphone or carrier path was tested. Voice locale labels were not independently validated by a human listening panel.

## Reproduce

1. Run scripts/setup-windows.ps1 for the pinned SDK/reporting environments.
2. Create baseline/audio-fixtures/.venv with uv and sync baseline/audio-fixtures/requirements.lock.txt into it.
3. Run scripts/build_accent_fixtures.py with that generator interpreter. David requires the installed Windows David SAPI voice; other voices use Microsoft online TTS via edge-tts 7.3.1.
4. With your Guava authentication available, run scripts/run_accent_comparison.py using baseline/sdk-0.47.0/.venv/Scripts/python.exe. This makes six hosted audio tests and may consume usage. Each has a 90-second process limit; errors/timeouts remain explicit.
5. Run scripts/build_accent_report.py with the SDK interpreter to rebuild the report/listening page.

## Files and provenance

- fixtures/audio/accents/manifest.json: exact voice IDs, shared reference, PCM format, padding, duration and SHA-256 for each file.
- tests/audio/accent_probe.py: native file-audio harness and utterance-event capture.
- tests/audio/accent_scoring.py: literal/numeric normalization and exact digit checks.
- scripts/run_accent_comparison.py: sequential one-trial execution with timestamped preserved raw logs/audio.
- dashboard/accent-comparison.html: scores, playback and recognized transcripts.
- reports/test-results/accent-comparison-2026-10-25.json: actual observations and provenance.
- Raw local evidence: evidence/accent-comparison/20261025T224812Z-a84070/ (ignored by Git).

Run ID: `20261025T224812Z-a84070`. Locked source baseline commit: `3460dd9321bf7e9dbfbb95a1fffd8346674a82f0`; the newly added harness is a working-tree extension to that baseline. Input manifest SHA-256: `92b2cdc3a72bbc90a08cf689c32a3fcc90b2a9cd1e2fed32de709aecfeb35106`.

Voice generation package: [edge-tts project](https://github.com/rany2/edge-tts). Locale background: [Microsoft speech language support](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support). Generated fixture reuse remains subject to applicable provider terms; no human dataset license is claimed.
