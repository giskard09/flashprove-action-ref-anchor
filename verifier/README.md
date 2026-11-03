# Verifier output

This directory holds this example's own run of FlashProve's `bin/cp_verify`, built from their
unmodified `verifier/src/cp_verify.cpp` (see `../layer1-flashprove/README.md`) — not vendored here,
produced fresh from the cloned repository at build time.

- `OUTPUT.md` — not yet created in this draft. Once `bin/cp_verify` is built and run against
  `examples/accepted-proof/` in this environment, its full stdout (the `result-v1` line and the
  final `YES`/`NO`) goes here verbatim, with the exact command and exit code.

Until `OUTPUT.md` exists, `run_example.sh` in the repository root cannot complete step 2 — see
`PROVENANCE.md` for why (a session-level permission gate on compiling/running third-party source,
cleared by the creador for this specific action but not yet exercised).
