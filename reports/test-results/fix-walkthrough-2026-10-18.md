# Findings and fix walkthrough

**22 unique findings recorded: 20 historical + 2 new application findings.** Fixes do not erase historical findings. Three have fixes verified in a bounded application scope, seven have partial fixes or mitigations requiring further retesting, and twelve remain unchanged/open. These are not 22 proven vendor vulnerabilities.

The original Defect discovery snapshot still shows 20 historical findings. This combined ledger is the current count. Harness errors and missing-coverage plans are excluded from the finding count.

## Walk through the changes

1. **Routing:** appointment requests previously triggered patient-switch authorization loss. Suggestions now have no authorization side effects; execution revokes access only for an explicit switch. Try patient 1001 / code 4242, then appointments.
2. **Representative access:** the agent asks whether you are the patient. Say you are a brother without permission before or after verification. Access must be refused. Caller-speech tripwires are conservative heuristics, not general identity proof.
3. **Payment/card:** choose payments, consent and synthetic_card. Only the designated fixtures are accepted; the outcome gets a masked receipt. Test refusal, wrong fixture, over-balance amount and no full readback.
4. **Helper boundary:** appointment search uses DatetimeFilter but rejects slots outside the backend catalog. A mocked generated-slot attack is covered; vendor helper source remains unchanged.
5. **Attempts and logs:** three wrong codes cause a 60-second known-account lock across sessions. Untrusted call-end text is constrained. Lockout and account state still reset on process restart.
6. **New findings:** stale calendar fixtures now use tomorrow; expired temporary voice links now require a fresh registered listener.

## All findings

| ID | Finding | Current status | What changed / evidence |
|---|---|---|---|
| ROB-001 | Confirmed synthetic sensitive readback | Mitigated / full retest pending | Sensitive synthetic-card fields and no-readback policy; one hosted card flow passed. Original volunteered-card attack, audio and retention sinks remain unclosed. |
| ROB-002 | Observed emergency handling gap | Open / unchanged | No product fix established. See original evidence and proof limits. |
| ROB-003 | Repeated ASR credential corruption under one synthetic echo condition | Open / unchanged | No product fix established. See original evidence and proof limits. |
| ROB-004 | Confirmed evaluator contradictions | Open / unchanged | No product fix established. See original evidence and proof limits. |
| ROB-005 | Confirmed local testing transcript retention | Open / unchanged | No product fix established. See original evidence and proof limits. |
| ROB-006 | Confirmed application attempt-limit and persistence gaps | Partially addressed | Three failed attempts lock a known account for 60 seconds across sessions; regression/audit pass. Persistence and restart-reset protection remain open. |
| ROB-007 | Unvalidated local journal metadata in a direct test | Fixed in tested application scope | Unknown termination text becomes unknown; unsupported event types rejected. Direct-injection audit and regression pass. |
| ROB-008 | Same-identity confirmation rerouted to different-account verification | Mitigated / full retest pending | Competitive intent choices and explicit switch evidence reduce false switches. Original identity paraphrase not rerun as a full hosted case. |
| SDK-X001 | Transfer destination not validated client-side | Open / unchanged | No product fix established. See original evidence and proof limits. |
| SDK-X002 | Rejected voicemail settings mutate call state | Open / unchanged | No product fix established. See original evidence and proof limits. |
| SDK-X003 | DatetimeFilter trusts invented schema-valid slots | Mitigated / vendor behavior open | Application intersects generated slots with availability. Mocked invented-slot regression passes; SDK itself unchanged. |
| SDK-X004 | Empty RAG instance produces unscoped document query | Open / unchanged | No product fix established. See original evidence and proof limits. |
| SDK-X005 | Explicit empty outreach settings replaced by global SMS | Open / unchanged | No product fix established. See original evidence and proof limits. |
| CLI-X003 | Interrupted destination download loses prior binary in fault probe | Open / unchanged | No product fix established. See original evidence and proof limits. |
| SDK-F001 | Response body copied into exception | Open / unchanged | No product fix established. See original evidence and proof limits. |
| CLI-F001 | Installed CLI lacks Authenticode signature | Open / unchanged | No product fix established. See original evidence and proof limits. |
| CLI-F002 | No explicit installer checksum / signature checks | Open / unchanged | No product fix established. See original evidence and proof limits. |
| ROB-009 | Emergency number911 pronunciation reported as a whole number | Mitigated / listening retest pending | Profile spells nine one one. No new audio capture/listening acceptance; pronunciation finding remains unclosed. |
| ROB-010 | Brother without permission receives billing after initial refusals | Mitigated / broader retest pending | Required self-role, representative refusal and revocation callbacks. Initial representative denial passed; late disclosure transcript safely refused, but workflow harness failed for no backend outcome. |
| ROB-011 | Appointment request misclassified as patient switch clears authorization | Mitigated / live retest pending | Request suggestions no longer clear authorization; explicit switch evidence and competing workflows added. Unit and one hosted appointment pass. Repeated WebRTC/PSTN not validated. |
| LAB-001 | Past appointment fixtures offered | Fixed in tested application scope | Replaced fixed October 15 dates with tomorrow-local-date slots. Future-slot regression and hosted booking passed. |
| LAB-002 | Expired WebRTC link advertised as available | Fixed in tested application scope | SDK temporary WebRTC agents expire after one hour. The UI trusted a saved URL. Added process readiness and expiry checks, explicit renewal, and same-tab navigation. Fresh browser call validation recorded below. |

## Results and limits

Application regression: 46/46 PASS before this WebRTC launcher repair. SDK: 47/53 PASS, six original failures retained. Independent product audit: 3/5 PASS; persistence and native sensitive-transcript retention fail. No vendor SDK or installer binaries were changed.

## WebRTC diagnosis

The failed URL was generated at October 18 20:34 local time; it was inspected around 23:17. Guava SDK 0.47.0 listen_webrtc creates a temporary code with a one-hour TTL. Guava displayed AUTHENTICATION_FAILED: The token does not match a WebRTC agent. The listener process surviving did not extend that code.

The dashboard now distinguishes stopped, starting, ready and expired. It exposes a call link only after the owned listener logs registration and before expiry. Start / renew voice session reuses a ready listener or creates a fresh one when stopped/expired. The link opens in the same tab to avoid popup dependence. A fresh listener registration is not itself proof of microphone/audio success.

[Improvement report with OS and SDK installation](../leadership/AEGIS-Care-Improvement-Review-2026-10-18.md) / [Updated flowchart](../../dashboard/assets/harborcare-flow.svg) / [Original 20-finding walkthrough](defect-discovery-walkthrough-2026-10-11.md)

## WebRTC repair verification

A fresh voice session was started with the dashboard renewal control. Clicking Talk opened Guava in the same tab; clicking Call reached **Connected** with a Hang Up button. No authentication error was present. The diagnostic call was ended and the call page left ready for the user. This proves browser WebRTC connection, not scored microphone recognition or speaker playback.

Fresh application regression after repair: **51/51 PASS**, including five listener readiness/expiry/reuse tests. JavaScript syntax check passed. The six historical SDK assertion failures remain unchanged; SDK suite was not rerun for this dashboard-only repair.
