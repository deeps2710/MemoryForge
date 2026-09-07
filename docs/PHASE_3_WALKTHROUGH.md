# Phase 3 browser and robustness walkthrough

Verified 2026-09-07 at http://127.0.0.1:8501/ using the fresh isolated
`.local/phase3-clean` installation. This is a local preview, not deployment.

1. Cold-started Streamlit with the saved checkpoint. Health endpoint returned
   `ok`; the real one-shot preset appeared without a training action.
2. Taught a second round: actual writes changed from 3 to 6, query accuracy
   from 23/30 to 27/30, and encoder delta remained 0.
3. Opened Research & evidence through the guided-lab button. Its heading
   reported the actual episode 1000, 6 writes and encoder delta 0.
4. Inspected the BDH/CQ claims with adjacent primary links, role comparison,
   DeltaNet/Titans cards, limits and source ledger. The app distinguishes the
   toy from each published architecture.
5. Inspected the actual outer-product increment, one-hot label, key norm,
   count averaging and matrix-query derivation. AppTest independently checks
   equality and that this inspection leaves memory unchanged.
6. Inspected the saved mean/population-deviation chart on desktop and mobile:
   clean, one wrong-label write and three wrong-label writes are labelled with
   distinct line styles. The chance reference, numeric table and sampling
   limitations are visible. Chart payloads are verified against raw results.
7. At 390×844, shortened navigation labels fit together (last tab right edge
   268.86 px); document width equals viewport width, 390 px. Research cards and
   the learning feedback wrap. The legend stacks; wide numeric dataframes use
   their own horizontal scrolling. Desktop inspection used 1280×720.
8. Selected No in the research check and observed immediate explanatory
   feedback. Returned to the experiment and verified the same 6 memory writes.
   Both answers and navigation state preservation are also covered by AppTest.

The server was restarted after the final navigation-label change because the
development configuration disables file watching. A stale preview tab earlier
reported ERR_NETWORK_IO_SUSPENDED; a fresh local tab loaded successfully.
Radio inputs in Streamlit use styled labels; clicking their visible labels
worked when automation's direct setChecked call could not operate them.

The fresh-install robustness record includes missing-checkpoint handling,
regeneration, exact tensor/core replay, seed/shot boundaries, repeated conflict
and reset, and offline app actions with fresh caches and blocked socket-connect
functions. This does not claim a browser-wide disconnected-network audit,
formal WCAG conformance, a human learning study or public-service performance.
