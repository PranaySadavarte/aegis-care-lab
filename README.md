# AEGIS Care Lab - Guava SDK and Voice AI QA Evaluation

AEGIS Care evaluates **Guava CLI/SDK 0.47.0** through an intentionally scrutinized **HarborCare** synthetic healthcare agent. The project contains layered tests, a local evidence dashboard, manual scripts and an evidence-backed leadership assessment. It is not a production healthcare/payment service.

## October 18 improvement lab

[All 22 findings and fix walkthrough](reports/test-results/fix-walkthrough-2026-10-18.md). WebRTC codes expire after one hour: use **Start / renew voice session** in the lab when needed; live readiness and expiry are checked before a Talk link is shown.

Independent development repository: https://github.com/PranaySadavarte/aegis-care-lab. Original baseline retained as upstream.

After starting the dashboard, open **http://127.0.0.1:8765/dashboard/lab.html** for fresh results, updated flowchart, card data boundaries, and the SDK feature inventory. A local WebRTC listener supplies the Talk link while it is running.

- [Improvement review: OS, actual SDK installation, fixes and remaining gaps](reports/leadership/AEGIS-Care-Improvement-Review-2026-10-18.md)
- Fresh core: **51/51 application PASS**, **47/53 SDK PASS** (six original failures retained).
- New optional synthetic-card path uses only designated PAN 4111111111111111 and CVV 123; no gateway.
- Hosted challenge runner: `baseline/sdk-0.47.0/.venv/Scripts/python.exe scripts/run_lab_challenges.py` (live usage).
- Temporary voice session links and raw evidence are ignored by Git.

## Start here

- [Plain-language faults, tests and flowchart](docs/understanding-aegis-care.md)
- [Leadership report](reports/leadership/AEGIS-Care-Guava-Assessment-2026-10-11.md)
- [Presentation PDF](reports/leadership/AEGIS-Care-Guava-Assessment-2026-10-11.pdf)
- [How to use the agent](docs/manual-validation-script.md)
- [Current context](PROJECT_CONTEXT.md) / [findings](QA_FINDINGS.md)
- [Finding-to-test map](reports/test-plans/finding-to-test-map.md)

## Windows setup

Supported evaluation baseline: Windows, Python 3.12, SDK 0.47.0. Install Git and uv from their official distributions first. Setup downloads pinned Python dependencies; it does not install the Guava CLI, buy a number or deploy anything.

```powershell
git clone https://github.com/PranaySadavarte/aegis-care-lab.git
Set-Location aegis-care-lab
.\scripts\setup-windows.ps1
.\scripts\start-dashboard.ps1
```

Open **http://127.0.0.1:8765/dashboard/**. Keep the dashboard terminal running. Stop it with Ctrl+C. If port 8765 is occupied, reuse the existing dashboard or stop its known process; do not terminate unrelated processes.

The repository includes a **sanitized historical snapshot**. Viewing it requires no Guava credentials. Raw call/installer evidence and virtual environments are intentionally excluded. Historical results do not claim that tests ran on your machine.

## Run core tests without Guava credentials

In a second PowerShell terminal:

```powershell
.\scripts\run-offline.ps1
```

This runs SDK contracts and deterministic application methods, blocks hosted network activity within the offline harness, and preserves new output under `evidence/portable-offline/`. Expected reference results are **47/53 SDK PASS with six retained discovery failures**, and **51/51 application PASS**. Your actual results may differ. A nonzero exit is expected while discovery failures remain unresolved.

This portable runner deliberately does **not** claim to rerun the original installer audit: its exact raw retrieved script is private evidence. Existing audit findings and proof limits are in the reports. `tests/run_all.py --suite offline` is the original investigator runner and requires that archived installer input; use the portable runner on a fresh clone.

## Hosted text, roleplay and audio tests

Authenticate through your own Guava account using **`guava login`** if the official CLI is already installed; check `guava --version` against the target before relying on CLI-version-specific results. The SDK can also use an API key according to Guava's current official SDK documentation. Do not commit keys, OAuth files, tokens or `.env` files.

```powershell
$taskPython = '.\baseline\sdk-0.47.0\.venv\Scripts\python.exe'
& $taskPython agent/harborcare.py --mode text
# Or browser microphone/audio:
& $taskPython agent/harborcare.py --mode webrtc
# Fixed hosted safety scenarios:
& $taskPython tests/run_all.py --suite security
& $taskPython tests/run_all.py --suite compliance
# Native persona and roleplay:
& $taskPython tests/run_all.py --suite extended
& $taskPython tests/run_all.py --suite adaptive
# Prerecorded noise/echo:
& $taskPython tests/run_all.py --suite robustness
```

Hosted modes use live services and may consume usage. Do not run `--suite all` unless you intend to execute every hosted suite. BERTScore/ROUGE need the optional separate metrics environment: `scripts/setup-windows.ps1 -WithMetrics`; model download and CPU time may be substantial.

Synthetic patient **1001**, code **4242**; speak digits individually. One workflow per call. No real patient information or cards. Payments use a simulated token and explicit simulation consent.

Phone mode reads `harborcare-agent/guava.toml`. This private repository retains the original evaluation configuration; **replace it with your own authorized Guava project/owned test number before using phone mode on another account**. Do not copy its routing identifiers into a new deployment. The listener must remain running. No automatic outbound calls, paid deployment or number purchase is part of setup.

## Dashboard pages and evidence

- **All test cases:** filter by use, stage, status; open method assertions, scenario and evidence details.
- **Defect discovery:** 20 reviewed findings with provenance and ownership; not 20 proven exploitable Guava vulnerabilities.
- **Audio comparison / Robustness:** clean versus noise/echo observations, samples and acceptance limits.
- **How to use the agent:** workflow prompts and manual appointment/defect tests.
- **Calls:** limited per-call metadata checks; a call does not automatically run the full regression suite.
- **Test runs:** investigator suite execution on demand. Fresh clones may lack historical raw inputs required by some page builders; sanitized historical pages remain the reference snapshot.

Do not equate process duration with ASR/LLM latency, rubric PASS with safety, or mocked commands with live telephony success. `OBSERVED`, `PARTIAL`, `NOT_RUN` and `TIMEOUT` remain explicit.

## Structure

```text
agent/                 HarborCare Expert using native Guava callbacks/tasks
backend/               Synthetic healthcare and isolated sensitive-data probes
tests/                 SDK, functional, security, audio, integration and metrics
fixtures/              Synthetic text/audio labels and public dataset provenance
dashboard/             Local pages, sanitized snapshots and page builders
reports/               Test plans, results, findings and leadership assessment
docs/                  Learning journal, architecture, profiles and operator guides
scripts/               Setup, launch, portable core test and publish-check helpers
evidence/              Local raw execution artifacts (Git-ignored)
```

## Reproducibility and sharing

Run `python scripts/check_publish.py` before sharing. It checks common secret patterns and tracked private-file mistakes; it is not a comprehensive security guarantee. Preserve raw originals locally and redact report copies. Recorded test cards are synthetic; selected published audio contains only reviewed synthetic output. Public audio attribution is in `docs/audio-datasets.md` and fixture manifests.

No general open-source license is assigned here. Third-party SDK, documentation and datasets retain their own licenses; consult source attribution before redistribution. Findings are intended for private technical review with Guava, not claims of a production incident or legal compliance certification.

[Guava CLI documentation](https://goguava.ai/docs/cli-reference) / [SDK architecture](https://goguava.ai/docs/architecture-overview) / [Action callbacks](https://goguava.ai/docs/on-action-request-execute).
