# Public deployment

Target: Streamlit Community Cloud, Python **3.12**, CPU. The public app URL is
**UNVERIFIED** until a real deployment is opened without an owner session.
`http://localhost:8501` is only a local preview.

Deployment inputs are ready in the repository:

| Setting | Value |
|---|---|
| Repository | `deeps2710/MemoryForge` |
| Branch | `main` |
| Main file | `app.py` |
| Python | `3.12` in Advanced settings |
| Secrets | None; leave empty |
| Dependencies | Root `requirements.txt` with `requirements-lock.txt` constraints |
| Checkpoint | Checked-in `artifacts/encoder.pt`; no startup training |
| Port / process | Host-managed Streamlit server |

The root requirements select the official PyTorch 2.6.0 CPU wheel on Windows and
Linux. The numerical versions and training settings are unchanged. Constraints
record the tested transitive versions; they are not a cross-platform wheel lock.
The provider runs Linux, so the Windows verification alone is insufficient to
claim public deployment success.

1. Sign in at [Streamlit Community Cloud](https://share.streamlit.io/). The owner
   must handle any account terms or new GitHub permissions. Use an account with
   access to the repository; do not grant access to unrelated private repositories.
2. Choose **Create app**, then **Yup, I have an app**. Enter the values above.
   A custom subdomain is optional and subject to availability; no address has
   been reserved or invented here.
3. Under **Advanced settings**, select Python 3.12, leave Secrets empty, save and
   deploy. Inspect build logs for a successful install and app startup.
4. Open the assigned URL in a separate browser without a Streamlit owner login.
   Confirm the preset, logo and real prediction render. Rehearse DEMO_SCRIPT.md:
   teach, query, conflict, clear and open Research & evidence. Confirm encoder
   delta 0 throughout, nonzero taught memory and zero memory after reset.
5. Reboot the app once and measure time from navigation to the usable preset.
   Record observed cold-start and interaction timings; do not substitute the
   local health endpoint for this check. A sleeping free app may need waking.
6. Put the verified URL in README.md and SUBMISSION_READINESS_REPORT.md, update
   the requirement evidence and rebuild the submission ZIP. Only then mark
   public access and cold-start checks PASS.

The app requires no API key, dataset download or background training. Browser
sessions own separate temporary memory. Refreshing the browser resets the lab.
`fileWatcherType = "none"` avoids unnecessary file watching; reboot a running
server after Python-module changes. CORS and XSRF protections remain enabled.
`.streamlit/secrets.toml` is ignored as a precaution; no secrets file is needed.

If installation fails, inspect the actual provider log and preserve pinned
numerical versions. Community Cloud tries uv and falls back to pip for a
requirements file. Do not switch the app to static screenshots or remove the
real checkpoint to make a failed deployment appear successful.

Primary deployment references, checked 2026-09-07:
[deploying an app](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy),
[dependency discovery](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies),
[official PyTorch version/CPU install commands](https://pytorch.org/get-started/previous-versions/).

Observed account state: the browser reached Streamlit's sign-in page, which
states that signing in accepts its Terms of Service. No deployment or new
account agreement has been completed by the agent.
