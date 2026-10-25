# Learning journal
Earlier entries: journal/learning-journal.md.
## 2026-10-11 — Coverage and layered testing
No SDK vulnerabilities have been independently confirmed; coverage areas are hypotheses until tested.
Learned: verification is a backend authorization decision, not field extraction. Payment redaction does not authorize access to billing data. Disconnect recovery requires idempotency and reconciliation to avoid duplicate transactions.
VAD/endpointing controls when speech is considered started/finished; ASR converts speech to text; TTS converts response text to audio. Their quality must be measured separately from business outcomes.
Next: exact-version baseline, then offline SDK contracts and documented live test capabilities. No security/behavior tests ran this milestone.

## 2026-10-11 — First executed SDK contracts
Established exact SDK 0.47.0 environment using working bundled Python 3.12.14; executed eight offline tests (seven passes, one failure).
Learned: MockCall isolates handler state but does not emulate server authorization or lifecycle. Agent.patch copies callback maps without changing the original. The Client constructor can perform a deprecation request; offline tests must prevent network side effects.
An exception is a data sink: HTTP response content may become exception text and later logs or telemetry. Reproducing synthetic marker inclusion confirms that behavior, but not an actual production breach.
Official agent-testing guide separates offline MockCall from live scripted/roleplay sessions. Next extend mock-backed SDK fault/security tests and complete CLI identification.

## 2026-10-11 — Coverage correction
Testing a Python SDK package does not validate the Windows CLI installer. A binary may be signed while its installer never checks that signature; computing a hash alone does not verify it against a trusted expected value.
Eight categories require separate evidence and completion criteria. Added missing detailed cases; no new runtime tests performed.

## 2026-10-11 — Installer verification
Direct path execution verified CLI 0.47.0 even though this process cannot resolve guava on PATH. Authenticode reports NotSigned for the installed binary.
Read-only installer audit found no explicit checksum/signature enforcement in current official script. HTTPS, checksums and publisher signatures address different trust boundaries; a recorded local hash preserves identity but does not authenticate the publisher.
Direct downloads over the destination raise a failure-recovery question, not a proven rollback defect. Next use isolated/mocked failure paths before drawing behavioral conclusions.

## 2026-10-11 — Installation methods
uv manages Python package/environment installation here. irm retrieves the Windows installer script; iex executes it, and that script installs the CLI binary. Route labels distinguish supply-chain/setup tests from SDK runtime tests.
A defect observed after uv installation is not automatically caused by uv. Controlled comparisons require matching versions, runtime and transitive artifacts.

## 2026-10-11 — Online and KPI transition
Offline contracts isolate Expert SDK logic; hosted text tests exercise live dialog/state without validating actual phone transport. Native reach_person and event decoding used for outbound subchecks, not replaced with custom logic.
A 15/16 test pass count is a regression metric, not a 93.75% voice-agent success rate. Field sensitive serialization is not proof of hosted redaction.
DocumentQA server mode uploads documents and concurrent instances need namespaces. Full SDK review still in progress.

Hosted Agent.test now executed successfully; added stable extracted-field and termination assertions. Text testing can validate a live dialog/Expert interaction without registering a phone number listener. Actual phone readiness still needs a separate listener/routing test.

## 2026-10-11 — Results dashboard
A test pass count is not a count of resolved findings. Static installer observations, hypotheses and unexecuted coverage require separate views. A snapshot dashboard must label freshness and cannot imply continuous monitoring.

## 2026-10-11 — HarborCare and stage-specific evaluation
A backend authorization gate checks the verified session subject before every sensitive read or mutation; model field extraction does not itself grant access.
Payment idempotency needs both a stable key and matching request fingerprint. The synthetic ledger implements this in process memory, not durable production storage.
Native Agent.test exercised six happy workflows and a wrong-code denial. Test harness errors must be preserved and separated from SDK/application defects.
ASR RTF requires isolated recognition processing duration; total agent runtime cannot substitute. Model confidence and rubric pass are different concepts. BERT/ROUGE names remain provisional pending user confirmation.

## 2026-10-11 — Approved inbound registration
The local Expert registered with Guava via native listen_phone. Registration confirms an available listener but does not establish PSTN/audio quality or successful caller workflow.
Startup deprecation warnings require tracking independently of actual failures; do not promote them into vulnerabilities.
User confirmed BERTScore and ROUGE. Scores remain unmeasured.

## 2026-10-11 — Voice-friendly credentials
Text correctness and spoken usability differ. Defined format normalization is safer than fuzzy credential matching; wrong digits still reject. Logs without entered values protect privacy but limit ASR root-cause attribution.
call_local means local microphone/speakers with hosted WebRTC, not local model inference or necessarily free usage. Offline backend tests are the known no-hosted-call path.

## 2026-10-11 — Call outcomes versus test grades
A completed call or transcript denial is an observation. Pass/fail requires a known expected scenario: rejecting a wrong code may be correct, while rejecting a correct code is a defect.
Native conversation records can reconstruct past calls, but precise application outcomes are easier to capture at the Expert callback. Mask identifiers and omit credentials; retain raw originals locally for attribution.

## 2026-10-11 — Background evaluation versus regression
HarborCare is the caller-facing service; AEGIS Care evaluates it. Do not narrate test internals during every call.
Each call can receive scoped observation checks without launching unrelated regressions. Full suites are explicit operator actions. No test result means inconclusive, not pass.
Native SDK semantic rubric evaluation complements deterministic backend checks but does not produce calibrated confidence or acoustic metrics.
Preserve transcript before asserting outcomes so failed hosted cases remain diagnosable. Malformed code and valid-format wrong code test different boundaries.

## 2026-10-11 � layered text and audio evidence
A text chat mode does not exercise microphones or speakers. Browser playback, native output capture, microphone permission, transport registration and successful speech recognition are different observations. Test each boundary separately. Native Agent.test_audio and on_caller_speech avoid inventing a parallel transport; Jiwer supplies standard WER/CER. Spoken digit words versus numeric transcripts can inflate literal errors even when identity values survive. Report normalization and sample scope. IntentRecognizer in installed0.47.0 returns SuggestedAction lists; read the pinned implementation when current documentation examples differ. Clear authorization before changing identity and collect fresh fields. Assert exact business values/actions and semantic safety; allow natural paraphrases.

Browser WebRTC: user explicitly reported hearing HarborCare and receiving responses to speech. This is user-confirmed two-way audio, not a transcript-scored workflow or measured latency. No matching new listener journal entry was found at the check; the inspected diagnostic tab was Idle. Session attribution remains unverified.

## October11,2026 — defect finding and evaluation calibration
Passing unit tests do not establish conversation safety: the backend rejects negative integers but the dialog may extract a different positive amount. A native model judge can produce incorrect PASS/FAIL; pair it with independent exact readback/authorization/action invariants and preserve disagreements. A complete digit match differs from substring presence; trailing echo digits must fail entity scoring. Sensitive field collection, caller transcript retention, spoken readback, recordings and diagnostics are separate sinks. NumPy seeded noise and SoundFilePCM fixtures provide repeatability; delayed caller copy and prerecorded speech overlap are not real acoustic echo cancellation or live interruption tests. AEC needs time-aligned speaker reference and microphone signals; indiscriminate transcript deduplication can suppress legitimate repeated consent. QA SQLite indexes sanitized observations/hashes; durable healthcare backend state remains a separate feature. Synthetic card/vital receipts deliberately provide no payment/clinical service.

## KPI/inventory milestone — October11,2026
Native intent30trials:24/24clear,2/4unsupported rejected;confidenceunavailable,agreementnotconfidence. ActualBERTScoreF1 0.8069 andROUGE1/2/L computed from7savedresponse spans;modelconfig/revisionpinned. Publichumanclip3conditions ran;cleanWER0%,noise/echoWER9.52%;one speaker. Two clienttextturnfirst-event intervals measured separately fromruntime. Overview nowallinventories and7openrevieweddefects;profilesMarkdownloadedonnewExpertstartup. See KPI expansion report for evidence/scope.


## Extended SDK / adaptive adversary milestone — October11,2026

Full baseline: SDK47/53 PASS (six FAIL retained), application32/32 PASS; installerOPEN_FINDINGS. Five new client boundary findings and isolated partial-download rollback failure added;14 reviewed discovery findings now have stage/ownership labels and linked sanitized evidence with raw SHA-256 provenance. Four native persona roleplays passed. Scoped DocumentQA/DatetimeFilter hosted tests, nine local health checks,21-dependency advisory audit (zero known advisories), auth401 probes, SIP TCP timeouts, nine public-word audio conditions and two interruption/clipping probes actually executed. No Expert/profile/backend changes this campaign.

Adaptive Ybbag uses native generation, roleplay and evaluation. First payment actor consented: initial debit alert was a harness false positive, reviewed INVALID_CALLER_SCENARIO. Corrected readback replay passed its limited checks; explicit payment-refusal transaction remained unexercised (PARTIAL_PASS); unauthorized and DOB checks passed within limited invariants. Earlier ROB-001 remains open. User requested unavailable metrics stay with reasons; no provider telephony endpoints configured, so live integrations/SMS remain incomplete. See reports/test-results/extended-sdk-2026-10-11.md and docs/operator-guide.md.

Learning: AI attackers can violate their instructions; validate caller coverage before grading the target. Mocked SDK contracts, scoped hosted probes, file-in audio and live carrier proof are distinct evidence layers. LiteralWER, semantic consent and safety outcomes must not be conflated.


## Unified Defect discovery registry — October11,2026

Reporting defect corrected: Overview hardcoded original SDK-F001/CLI-F001/CLI-F002 outside the14-entry discovery registry, causing omissions and duplicateCLI-X003 presentation. Added the three original findings to the shared registry (17 unique findings), removed four hardcoded Overview duplicates, retained evidence links/stage/ownership labels, and corrected corrupted link typography. Existing observations only; no new product/security executions or vulnerability fixes. Expert unchanged.


## Discovery walkthrough — October11,2026

Added reports/test-results/defect-discovery-walkthrough-2026-10-11.md:17 findings traced to method, steps, observed output and proof limits; linked from Defect discovery. Preserved terminal/transcript examples distinguish native judge output from independent safety review. Corrected report-only PAN redaction to preserve decimal metrics and spacing; raw evidence unchanged. No new product tests executed.


## Readable reports and execution coverage audit — October11,2026

Report/docs .md URLs now render sanitized styledHTML via an isolated pinned dashboard environment; sources and raw evidence preserved. Audited187inventoryentries:85methods actually executed (79PASS/6FAIL);46coverageplans still5NOT_RUN/24PARTIAL/17PARTIAL_FAIL. Executed11previously unscored original audio fixtures (allOBSERVED;10speech+silence0events), with8slead/3stail and preserved hashes. Executed three exact previously hosted-pending text fixtures: limited no-debit/no-successful-unauthorized-result checks, no workflowcompletion. Latest user-hosted run6/8PASS with identity/claims failures preserved; securitysnapshot identity-switchFAIL retained. Existing Expert/profile/backend unchanged. See request-coverage-audit report for item-by-item request mapping, unavailable metric reasons, and genuine prerequisites/harness gaps.


## Report interpretation / compliance / listening milestone

Audio comparison now includes word-weighted clean/noise/echoWER0/16.67/12.50%, per-sample deltas/edit counts, actual transcripts, hashes and repeated credential-corruption context. Recomputed from preserved data, no new ASR population claim. Four new representative scenarios ran: two role-first variants no disclosure observed, self-patient controlPASS, credentials-first then brother/no-permission COM-REP-004disclosed50dollars after two refusals. AddedROB-010as confirmed synthetic authorization-policy failure; no legalHIPAAverdict. AddedROB-009for user-reported911pronunciation, with two genuine native captures awaiting listening review. User could not review because dashboard was inactive; pronunciation remains unconfirmed. A separate native-audio replay of savedYbbag caller turns captured real agent output; not original text-roleplay audio. Native roleplay protocol carries transcript text only. All19findings now have detector case/source and plain explanations; ROB-007limited direct journal test and ROB-008wrong same-account routing clarified. Current category report includes compliance controls; superseded source archived. Next-execution guidance removed from Overview. Expert/profile/backend unchanged. Suggested later dashboard simplification and founder-report pointers in docs/project-improvement-notes.md; no email drafted or sent.


## October 12: manual validation and listening verdict

User heard nine hundred and eleven in both saved TTS-911 recordings; ROB-009 human-confirmed. Original audio captures preserved, separate listening-review evidence added. No phone listener existed while WebRTC ran; restored approved inbound listener PID36368 with zero other listeners registered. Answered-call success remains unverified. Overview now separates SDK47/53, application32/32, hosted6/8, security2/3, representative cases and audio observations. Walkthrough covers19findings. Added eight manual spoken cases, launcher and result template. No new hosted regression campaign; Expert/backend unchanged. Learning: authentication differs from representative authority, live listeners must remain running, and transcript digits do not establish pronunciation.


## October 12: result drill-down and appointment diagnosis

Fixed ROB-009/010 table continuity. Added categorized case details, individual method assertions/statuses, seven robustness detail pages, agent usage/appointment guide and requested navigation ordering. Executed focused handler checks:3 methods PASS including six workflow subcases. Hosted appointment trace: I choose appointments -> switch_patient; Expert clears verification before action execution; hosted process TIMEOUT50s. AddedROB-011 with raw evidence and proposed owner changes; exact original PSTN root cause unverified. Expert/backend unchanged. Historical appointmentPASS retained; follow-up shown separately. Learning: mocked callbacks bypass natural-language classification, and action proposals must not mutate authorization before confirmation.


## October 12: leadership report and GitHub packaging

Prepared private leadership assessment PDF/Markdown covering20reviewed findings, explicit owner/proof boundaries, real execution counts, KPI samples and five unrun plans. Added Windows pinned-environment setup, local dashboard launch, portable core test runner and publish-pattern scan. Fresh staged-source export reproduced53SDK methods with6failures and32applicationPASS using the existing pinned runtime; dependency downloads were not retested. Raw installer/call evidence remains ignored; original investigator runs may require private inputs absent from clones. Navigation now has explicit flex spacing and wrapped links. GitHub private repository PranaySadavarte/aegis-care created through signed-in browser; upload verification pending. No agent fixes, new hosted campaign, paid deploy or outbound call.


## GitHub publication verified

Private repository https://github.com/PranaySadavarte/aegis-care published on main with existing history. Verified remote17fcc68 before this journal update; normal Git authentication used, no credential extraction. Final11-page leadership PDF rendered and visually reviewed; binary Git attributes preserve PDF/audio bytes. Overview browser check:14links, flex-wrap enabled,18px column gap. Tracked-files/history secret-pattern scan found no matches; raw evidence and credentials excluded. Fresh source export core results reproduced:SDK53tests6failures, application32PASS using existing pinned runtime, no dependency-download rerun or hosted campaign. README and issue template document execution, scoped failures, evidence handling and original private-installer prerequisites.


## Plain-language learning milestone

Explained all20findings in developer workflow order, with separate confirmed behavior and possible consequences. Added layered test overview and implemented agent flow SVG; explained task/field/callback and verification-versus-authority. Expanded SDK-X004/X005/ROB-007 with actual inputs, safety expectations and proof limits. Moved SDK-X002 to bottom of walkthrough table, preserving evidence. Corrected SDK-X005 evidence excerpt selection and plain log description. No new product/hosted tests, Expert/backend fixes or changed raw artifacts.


## Report presentation-date and email-draft update

At user request, removed the Prepared for Guava co-founders and CEO audience line and changed the report presentation date/filenames to11October2026. Preserved actual execution timestamps and evidence provenance. Updated local and GitHub report references. Reviewed native set_persona/roleplay source:four scoped persona controlsPASS; adaptive paymentPARTIAL_PASS; unauthorized/DOB controlsPASS within invariants. No isolated persona/roleplay API defect established. First adaptive payment actor violated refusal instruction, so initial debit alert was invalid; fixed-turn safety failures remain valid separate evidence. Preparing unsent joint email draft to Nico and Anthony with PDF attached and scoped counts85methods/36textentries/24audioentries/20findings.


Saved an unsent Gmail reply draft in the existing QA Engineer at Guava thread, addressed only to Nico and Anthony. Verified DRAFT label, original thread, October11PDF attachment and33670bytes. Draft identifiers remain local ignored evidence. Added persona/roleplay explanation with actual scenario assertions, actor-validity issue, partial payment coverage and no isolated API-defect claim. Revised report pushed to private GitHub main; actual execution timestamps remain unchanged.


## October 18, 2026: independent improvement lab
Cloned original into isolated workspace; created private aegis-care-lab with original as upstream. Fresh Windows 10 Home 22H2 build19045.6466 AMD64, CPython3.12.14; pinned SDK0.47.0 and dashboard dependencies installed through setup-windows.ps1. Existing CLI0.47.0 queried directly; not reinstalled.
Agent adds role gate, guarded action suggestions, competitive workflow routes, searchable future slots with helper-output membership checks, native amount validation, caller-speech revocation, cancellation, escalation fallback, reviewed SDK answers and optional designated synthetic-card collection. Account attempts bounded at three failures/60s; journal termination allowlist. New stale fixed-date slot issue found and fixed.
Fresh offline: SDK47/53PASS six retained failures; application46/46PASS. Product audit3PASS/2FAIL: persistence and native transcript retention remain. Hosted appointment/card PASS. Representative initial early-hangup harness failure preserved; corrected denial PASS. Late representative transcript refuses and ends; harnessFAIL due no backend completion, kept separate from safe-refusal observation.
Dashboard lab page, existing flowchart update, preserved original SVG, 81-public-member static SDK inventory, dated improvement report with OS/install method and missing-evidence review. Local dashboard and temporary WebRTC listener launched. No phone, outbound, SMS, paid deploy or real payment.
Learning: denial may complete without backend workflow result. Do not equate source references, unit passes or one hosted smoke with full feature/voice coverage. Raw evidence and temporary voice access links remain ignored.


## WebRTC expiry repair and combined finding ledger
Reproduced AUTHENTICATION_FAILED on saved WebRTC URL after SDK one-hour TTL. Added dashboard-owned listener readiness/expiry state and explicit start/renew API, same-tab Talk navigation; Windows launcher child PID difference accounted for. Browser test reached Connected, then diagnostic call ended. Voice page left ready for user; no scored microphone/speaker assertion. Application51/51PASS including five new voice lifecycle regressions. Combined ledger22findings:20historical+LAB-001stale slots+LAB-002expired voice link. Three scoped application fixes, seven mitigated/partial, twelve unchanged/open; these categories do not certify production closure. Added linked all-finding fix walkthrough; raw legacy registry remains historical20.


## October 25, 2026: prerecorded synthetic accent comparison
Copied committed lab into the new Guava Chatbot - QA Report 2.0 workspace. Added six identical-script voice fixtures: explicit SAPI David, neural US Guy control, British Ryan, Indian Prabhat, Australian William Multilingual, Nigerian Abeo. Isolated edge-tts7.3.1 generation environment locked separately; SDK0.47.0 unchanged. Initial patient-style external synthesis request was rejected by automatic approval review; switched to a neutral meeting/test-reference script with no patient or credential content. No rejected synthesis was executed.
Native Agent.test_audio ran once per voice: David/Guy/Ryan/William numeralWER0%; Prabhat16% (1234 -> 1 to 34 and omitted The); Abeo24% (first-reference sentence absent). Exact sequence checks2/2 for four voices;1/2 for India/Nigeria; negative cue observed6/6. LiteralWER25.81% four voices,29.03%India,41.94%Nigeria. Different engines/speakers/pace/codec and single trials preclude population accent ranking or isolated ASR causality. Raw outputs/hashes preserved; no healthcare workflow success claimed.
Added reproducible generator, manifest, bounded runner, scoring module, report builder, listening dashboard and navigation links. Five scorer regressions added;56application methodsPASS. Current new-workspace dashboard on8766, existing listeners untouched. No additional finding IDs assigned to these sample observations.
