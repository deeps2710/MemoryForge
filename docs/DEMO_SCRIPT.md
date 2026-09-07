# One-minute concept demonstration

Open a freshly loaded **Guided lab** on episode **1000**, after the model has
loaded. Browser refresh resets to this preset. These are target narration slots,
not a measured human completion time. All values below come from the recorded
seed-1000 lab protocol, not the different Phase 1 benchmark.

| Time | Action and narration | Observable check |
|---|---|---|
| 0–8 s | “Temporary associations can change while every encoder parameter stays fixed.” Point to the digit-to-symbol demonstrations and frozen encoder. | Digit 1 → ALPHA, 4 → GAMMA, 8 → BETA; three real writes. |
| 8–18 s | Click **Teach demonstrations**. “A new image writes its normalized embedding into the row for its symbol.” | Six writes; the actual 3 × 16 matrix changes; encoder delta stays 0, memory delta is positive. |
| 18–28 s | Click **Test Query**. Point to prediction beside ground truth and the score bars. “This held-out image only reads memory; it does not train the encoder or become a demonstration.” | Six writes remain; measured score is a row–query dot product. Across the fixed queries, accuracy rose from 23/30 to 27/30. |
| 28–40 s | Click **Inject Conflict**. “The same key can be written under a wrong symbol. The memory accepts it.” | Seven writes; accuracy 90.0% → 86.7%; five predictions change. A changed prediction need not always become incorrect. |
| 40–48 s | Click **Clear Memory**. “These associations are temporary.” | Zero matrix, zero writes, abstention; encoder delta still 0. |
| 48–60 s | Open **Research & evidence**, BDH connection. “BDH also separates trained structure from dynamic associative state. BDH-CQ adds a separate iterative reasoning workspace. This toy implements neither system: it tests names for familiar digits, not new visual concepts.” | Source links and system distinctions are visible. |

If a cold start delays loading, wait for the usable preset before timing the
concept check. Do not claim a universal subsecond network response or hide a
failure. Use the local command `python -m streamlit run app.py` as an explicitly
local fallback if the public service is unavailable.

Optional follow-up: in Playground, compare five clean demonstrations/class
(22/30) with ten (29/30). Explain that class means can move in an unhelpful
direction, so additional examples do not guarantee monotonic accuracy. The
slider rebuilds clean memory and removes conflicts.

Defense preparation: derive `S += v k^T`, `c += v`, `M[i] = S[i]/c[i]`, `scores = Mq`;
trace one support ID and one disjoint query ID; explain why the digit head cannot
produce the random symbols; distinguish saved 50-seed charts from live writes.
See TECHNICAL_WALKTHROUGH.md and the immediate-feedback **60-second check** in
the app. Human understanding and live defense have not been verified by tests.
