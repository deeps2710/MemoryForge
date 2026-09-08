# Public deployment

**PASS — verified 2026-09-08:** [Open MemoryForge](https://memoryforge.streamlit.app/).
The real application was opened and operated in a separate browser without an
owner login. This is a public deployment; localhost remains a development preview.

| Setting | Verified value |
|---|---|
| Provider | Streamlit Community Cloud |
| Repository / branch | deeps2710/MemoryForge / main |
| Main file | app.py |
| Python | 3.12 selected; provider installed 3.12.14 |
| Core runtime | CPU PyTorch 2.6.0+cpu; Streamlit 1.45.1 |
| Table serialization | PyArrow 24.0.0 |
| Dependencies | Root requirements.txt with requirements-lock.txt constraints |
| Model | Checked-in artifacts/encoder.pt; no startup training |
| Secrets | None required |

## Repair and reproduction

The owner-created app selected Python 3.14.7. Its log failed because the pinned
PyTorch 2.6.0 CPU wheel has no matching Python 3.14 ABI. In the existing app's
**Settings → General**, Python was changed to **3.12** and **Save changes** was
clicked. The rebuild installed Python 3.12.14 and loaded the application. No
model upgrade, retraining, app deletion or new account permission was necessary.
For a new deployment, choose Python 3.12 explicitly in **Advanced settings**.
Repository files alone do not replace this provider runtime setting.

The first successful build also replaced PyArrow 25.0.1 with 24.0.0 under the
provider's compatibility workaround. The project now pins 24.0.0 to match that
observed runtime. The upstream [Arrow issue #50471](https://github.com/apache/arrow/issues/50471)
describes an import-thread crash in 25.0.0 and identifies 24.0.0 as unaffected;
this project does not independently establish the provider's diagnosis of 25.0.1.
The final fresh cloud install directly installed the pinned 24.0.0.

The provider's uv attempt reported an unresolved setuptools 84.0.0 with the
configured indexes. On the fresh build, its standard pip fallback succeeded.
This is recorded as successful pip installation, not successful uv resolution.
Use the documented pip command locally. A provider warning also lists
pyproject.toml, which contains only pytest configuration; requirements.txt was
the actual dependency source. No Poetry application lock is claimed.

## Observed public behavior

The anonymous seed-1000 session started with 3 writes and 23/30 correct queries.
Teaching produced 6 writes and 27/30; Test Query advanced to held-out sample 1328
(digit 4, prediction/truth GAMMA). A conflicting write produced 7 writes and
26/30. Reset gave zero writes, zero memory and abstention. Encoder parameter
delta stayed zero. The owner's separate session retained its three-write preset
while the anonymous session was cleared.

Research & evidence preserved the cleared state, displayed the BDH/CQ boundaries
and adjacent primary citations, and rendered the saved 650-condition/19,500-outcome
chart with its saved-computation label. The supplied logo and expanded release
credits exposed the repository, demo, both PDFs, provenance and AI disclosure.
Desktop research and 390×844 mobile hero/controls/metrics were visually checked.
These checks are not a full accessibility certification.

One observed click-to-feedback interval for teach/query/conflict/reset was
1,001/959/1,017/952 ms, including automation and network overhead. This establishes
roughly one-second observed feedback; it does not promise subsecond performance.

A fresh reboot was initiated at **04:44:42.587 UTC on 2026-09-08**. Provider logs
finished dependency processing at 04:46:24; the anonymous usable preset was
observed within **130 seconds**, then a real teach again produced 27/30. This is
a polling upper bound covering provisioning and reinstall, not isolated encoder
load time. An earlier interrupted timing was discarded. The delay is acceptable
for this free-host demo when woken before judging; it is material and not an
instant-start claim. No concurrent-user throughput study was performed.

Structured evidence: artifacts/phase4_deployment.json. Final local compatibility
checks: artifacts/phase4_final_installation.json and phase4_final_robustness.json.
Full bitwise retraining was verified on Windows; Linux received install and
browser checks, not an independent bitwise training reproduction.

## Before presenting or maintaining

Open the public URL early and follow DEMO_SCRIPT.md. A sleeping app may need
waking. Keep Python 3.12 selected; inspect the end of current logs rather than
mistaking an older failed attempt for the final outcome. Reboot after changes
if the running process has not refreshed. Memory is scoped to browser sessions;
refresh starts a new lab. No API key or dataset download is required by the app.
CORS/XSRF protections remain enabled; .streamlit/secrets.toml is ignored.

Primary provider references checked during Phase 4:
[deployment settings](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy),
[dependency discovery](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies),
[PyTorch version and CPU commands](https://pytorch.org/get-started/previous-versions/).
