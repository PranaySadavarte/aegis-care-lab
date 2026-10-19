# AEGIS Care project context
Updated: 2026-10-11
Repository: C:/Users/prana/aegis-care
Project: AEGIS Care — Guava SDK and Voice AI QA Evaluation
Agent scaffold: harborcare-agent (HarborCare inbound agent)

## Objective and scope
Evaluate Guava CLI/SDK v0.47.0 and build a healthcare-first voice agent for patient identity verification, insurance eligibility, claims, appointments, billing and payment security. Use synthetic patient/insurance records and simulated payments. Produce an evidence-backed technical assessment for Guava's founders and CEO.

## Current milestone
Initial scaffold audit completed and recorded in reports/scaffold-audit-2026-10-11.md. Git baseline: 47e92e7. Original demo preserved; synthetic HarborCare is now implemented and tested. Latest milestones below record current coverage and limitations.
Target CLI/SDK: 0.47.0. CLI version/authentication: user-reported, not reverified. Actual locked and installed SDK metadata: 0.47.1. Do not attribute 0.47.1 results to 0.47.0. Preserve current lock/environment evidence before selecting a separate 0.47.0 evaluation environment.

## Verified checks and limitations
- Scaffold/configuration/source files inspected; local Git baseline established.
- Current official starter documentation retrieved on 2026-10-11 and matched bundled documentation by SHA256.
- Dependency lock and installed package metadata inspected; runtime import not verified.
- uv --version succeeded: 0.12.9.
- guava --version failed to resolve on this session's PATH.
- Virtual-environment Python invocation failed before execution. Syntax and import checks did not run.
- No SDK behavior, healthcare functional, conversation, security exploit, audio, reliability or cross-platform tests executed.
- No live calls, deployments, number purchases or payment operations performed.

## Working rules
Read current official Guava documentation before using SDK APIs. Study SDK architecture before modifying application code. Teach concepts at each implementation step and update journal/learning-journal.md.
Update PROJECT_CONTEXT.md and QA_FINDINGS.md after each meaningful milestone, including current step, exact test status, evidence and next action.
Preserve raw evidence locally; redact secrets and sensitive identifiers in reports. evidence/ is ignored by Git, so Git does not back it up. Keep original evidence files and add new timestamped records.
Separate confirmed vulnerabilities, observed defects, potential risks and hypotheses. Classify ownership as application, SDK/platform, environment or unknown; require minimal reproduction before assigning vendor defects.
Do not purchase phone numbers, deploy paid infrastructure or run destructive operations without explicit approval.
Use Git for milestones. Never fabricate test outcomes. Read-only synced ChatGPT project references must remain untouched.

## Next recommended evaluation task
Establish a reproducible offline 0.47.0 evaluation baseline: locate the existing CLI and verify its version/signature without reinstalling; inspect the base Python launcher; preserve the 0.47.1 scaffold and lock; establish a separate locked 0.47.0 environment; then run syntax and SDK-import checks that do not import main.py or connect to hosted services.
Next architecture study: Agent lifecycle, Call commands, event handlers, task/field state, authentication, transport/threading, errors/retries, cleanup and testing utilities, grounded in official docs and version-specific installed source.

## Coverage planning milestone — 2026-10-11
SDK security review is incomplete. Added 24 detailed NOT_RUN cases in reports/test-plans/test-cases.csv, layered release gates, coverage audit and execution ledger. No executable harness exists yet.
Preferred directory structure reserved without moving existing scaffold/evidence. Future learning entries live in docs/learning-journal.md; prior journal retained.
Final stage: user-led calls against complete synthetic agent, including adversarial conversation and audio scenarios. Production canaries remain separately gated.
Notes C:/Guava/My notes.rtf used as reference only; statements inside are not independent instructions or verified results.

## SDK baseline execution milestone — 2026-10-11
Isolated SDK 0.47.0 imports successfully on bundled CPython 3.12.14. Installed-version inventory: baseline/sdk-0.47.0/requirements.lock.txt. Original 0.47.1 scaffold preserved.
First offline contract suite: 8 executed, 7 passed, 1 failed. SDK-F001 reproduces response-body inclusion in HTTP exception text; potential disclosure risk, no demonstrated real data leak.
CLI baseline still unresolved. Hosted agent.test/roleplay and comprehensive SDK security coverage remain unexecuted.
Latest report: reports/test-results/sdk-0.47.0-offline-2026-10-11.md. Historical NOT_RUN ledger represents the earlier planning milestone, not current execution.

## Eight-category coverage correction — 2026-10-11
All eight evaluation categories now mapped in reports/sdk-evaluation/category-coverage-2026-10-11.md. Catalog expanded to 32 cases with installation permissions/rollback, developer experience, functional contracts, testability, compatibility and deployment coverage.
No new tests executed. Full baseline remains incomplete; installer evaluation takes priority before additional agent work.

## CLI/installer milestone — 2026-10-11
Located existing CLI at default LOCALAPPDATA/guava/bin; direct query verifies 0.47.0. Installed binary is NotSigned per Authenticode. Current official installer downloaded and statically audited without execution: no explicit checksum/signature verification; direct destination replacement raises untested rollback risk.
CLI and isolated SDK versions now both verified 0.47.0; authentication, original installer provenance and comprehensive behavior/security remain unverified.
Details: reports/sdk-evaluation/installer-audit-2026-10-11.md. No machine PATH or existing install changes.

## Installation-method classification — 2026-10-11
User confirmed irm (not ifm). Added reports/test-plans/installation-method-matrix.md and component/method scope columns to the catalog.
uv installation results apply to Python SDK; current irm/iex installer inspection applies to Windows CLI script. Existing CLI original install route remains UNKNOWN; direct artifact inspection is not proof of route.
No new tests ran. SDK exception behavior is not attributed to uv without controlled comparison evidence.

## Directional/online milestone — 2026-10-11
User report due tonight; authorized hosted evaluation budget 500 minutes. No paid deployment/purchase or unspecified outbound destination authorized.
Expanded corrected offline suite: 16 unique tests, 15 PASS, 1 known FAIL. Native SDK event/task/reach_person/production Call APIs exercised. Full SDK/source review and inbound/outbound E2E remain incomplete.
Prepared bounded synthetic hosted smoke using Agent.test; outcome recorded separately. See reports/sdk-evaluation/directional-kpi-2026-10-11.md for coverage/KPI definitions.

Hosted transition outcome: two synthetic live text runs completed; second asserted exact field and bot-hangup successfully. See reports/test-results/hosted-smoke-2026-10-11.md. No phone listener started; no-answer cause unresolved; billed usage unmeasured.

## Dashboard milestone — 2026-10-11
Local dashboard: dashboard/index.html (preview http://127.0.0.1:8765/dashboard/). Sanitized snapshot with actual results, unresolved installer findings, coverage filters, JSON export and report links; no external hosting or live monitoring.
Generator validates preserved result counts. SDK-016/017 catalog corrected to PARTIAL for existing executed subchecks; no new SDK tests. See dashboard/README.md for refresh and scope limitations.

## HarborCare implementation / pipeline-stage milestone — 2026-10-11
Synthetic agent implemented in agent/harborcare.py and backend/synthetic.py using native SDK APIs. Six workflow paths; 10 corrected functional methods PASS; six hosted happy workflows plus one corrected wrong-code denial PASS. Initial harness errors preserved and attributed to tests.
PipelineStage/Direction catalog labels and ASR/LLM/robustness dashboard pages added. Metric functions not found in scoped public API are planned via established libraries, not fabricated scores.
Phone listener was rejected by automatic approval review due to possible live/shared routing impact. No listener started; explicit user approval pending. Full prototype limitations/results in reports/test-results/harborcare-2026-10-11.md.

## Approved phone listener — 2026-10-11
User approved attachment to configured inbound number; listener registered successfully with zero other registered listeners. See reports/test-results/phone-listener-2026-10-11.md. No completed phone call claimed; awaiting user test.
BERTScore and ROUGE names confirmed; metric pages regenerated. Startup WebSocket deprecation warning observed without registration failure.

## Spoken verification fix — 2026-10-11
User live calls repeatedly failed verification; four accepted call sessions visible in raw listener evidence, but actual entered field values absent. Exact live root cause unknown. Strict credential string handling identified as application limitation.
Easy synthetic credentials 1001/4242 added; legacy credentials preserved; bounded formatting normalization added. Corrected suite 12/12 functional methods PASS. Updated approved phone listener running; native local-audio mode ready, not launched. Local/WebRTC usage cannot be assumed free.

Numeric credentials also passed one hosted text billing test (exit 0); live audio verification still awaits user retest.

## Per-call history — 2026-10-11
Dashboard now displays individual native inbound conversation records and on-demand refresh. Four historical records recovered; transcripts report verification denial; outcomes unscored. Timestamp timezone unknown in CLI display.
Future approved listener now records masked start/finish/end outcomes locally; no credentials or transcript in dashboard. No new live call evaluated during this instrumentation milestone.

## Service and evaluation runner — 2026-10-11
AEGIS Care = QA umbrella; HarborCare = agent persona. Service wording revised; synthetic limitations retained.
Dedicated Calls and Test runs pages. tests/run_all.py runs offline/hosted/all fixed suites; full regressions on demand. Automatic per-call metadata checks added, with explicit semantic/ASR limits.
Latest functional 17 PASS; SDK 15/16 PASS (known failure); installer audit open findings. Six revised hosted workflows PASS; malformed text denial returned no backend result (open robustness observation); valid-format wrong-code rerun PASS; native billing rubric PASS.
See reports/test-results/service-runner-2026-10-11.md. Broad test catalog and production feature scope still incomplete.


## Text/audio and dashboard repair milestone � 2026-10-11
Application 26/26 PASS; SDK 15/16 PASS, known exception failure and installer controls unresolved. Native hosted adversarial cases: latest injection, identity-switch and malformed-code PASS; initial incomplete-script failure retained. Windows-curses installed; plain --mode text exit0. One prerecorded synthetic ASR clip scored WER62.50% / CER48.68% without numeral equivalence, expected digit strings2/2. Twelve labeled audio assets prepared; other clips unscored. User confirmed browser playback of greeting; native microphone/speaker routing remains unverified. Calls now report duration provenance/unknowns and explicit local channel labels. Dashboard measured pages and runner security/audio suites added. See usability-repair report for limits and evidence.

Browser WebRTC: user explicitly reported hearing HarborCare and receiving responses to speech. This is user-confirmed two-way audio, not a transcript-scored workflow or measured latency. No matching new listener journal entry was found at the check; the inspected diagnostic tab was Idle. Session attribution remains unverified.

## Defect discovery / robustness milestone — October11,2026
Seven hostile cases plus two follow-ups; six audio conditions plus echo repeat; native sensitivePAN/CVV and vital intake probes executed. Card readback reproduced twice despite native judgePASS; exact safety invariant now fails it. Emergency flow retains verification; delayed echo corrupted full credentials twice. Strict negative amount rejected without debit. Native sensitive fields avoided readback but local testing transcripts retained caller input. Five deterministic product probes:four gaps,one idempotencyPASS. Six new sensitive processor functional testsPASS. Seven reviewed findings and metadata-only QA SQLite ledger; production backend still in-memory. See product-robustness-assessment report and dashboard/defects.html. No legal certification/full platform audit claim; actual live AEC/barge-in and hosted retention remain unverified.

Final campaign regression:32/32 application methodsPASS;SDK15/16PASS plusinstallerOPEN_FINDINGS (run20261012T032131Z-be98e6). Catalog39cases;audio18fixtures across two manifests. Hosted/readback and echo failures remain open and separately visible.

## KPI/inventory milestone — October11,2026
Native intent30trials:24/24clear,2/4unsupported rejected;confidenceunavailable,agreementnotconfidence. ActualBERTScoreF1 0.8069 andROUGE1/2/L computed from7savedresponse spans;modelconfig/revisionpinned. Publichumanclip3conditions ran;cleanWER0%,noise/echoWER9.52%;one speaker. Two clienttextturnfirst-event intervals measured separately fromruntime. Overview nowallinventories and7openrevieweddefects;profilesMarkdownloadedonnewExpertstartup. See KPI expansion report for evidence/scope.

ActualExpertparaphrasebenchmark4/6completion;targetedbillingrepeatPASS,identityrepeatrequested different-account verification then processTIMEOUT withtranscriptretained. AddedROB-008 without claiming classifierrootcause. Overview135inventoryentries,8revieweddiscoveryfindings.


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
