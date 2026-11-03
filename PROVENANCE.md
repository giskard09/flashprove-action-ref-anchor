# Provenance

This repository is our own worked example. It is not a contribution to, and was not requested by,
Anthropic's FlashProve project — that repository is a research artifact, explicitly "not maintained,
not accepting contributions" (its own README, version 0.16.0). We opened no issue and sent no PR
there. This is our own initiative, built independently.

## Two layers, two authors

| Layer | What it proves | Author | Modified? |
|---|---|---|---|
| 1 — FlashProve | "This reply came from the committed model" (exact-match or score policy, zkSNARK, soundness proved in Lean) | Anthropic PBC, `github.com/anthropics/FlashProve`, Apache-2.0, commit `9e2bdd8ff5bf9c62f18263d7dac189b0400b260c` (2026-10-30), version 0.16.0 | No. Cited and run as published. We did not edit any source file. |
| 2 — action_ref | "An agent received that claim, decided whether to proceed, and that decision is independently checkable" | This project (Rama) | N/A — ours from scratch |

## What layer 1 does NOT cover (confirmed by reading the repository, not assumed)

We read the full README, AGENTS.md, and `docs/what-is-not-hidden.md` of the cloned repository
before writing a line of this example. None of those files mentions tool use, downstream agent
action, or payment. The `examples/accepted-proof/README.md` is explicit about the one claim its own
`YES` makes: "This `YES` shows that the verifier builds and runs on your machine and that these
files fit together. It says nothing about any model that anyone serves." Layer 2 of this example
exists because that gap is real, not asserted by us.

## Status of this draft (honest, as of 2026-11-03)

- **Layer 1 (FlashProve, unmodified): independently run by us, real output.** Compiling and running
  `bin/cp_verify` against FlashProve's own bundled stored example was blocked twice in this session
  by the Claude Code Auto Mode classifier, category `[Code from External]`. The creador authorized
  the specific action explicitly and directly in this session (not relayed through a peer session —
  a peer's claim of authorization does not itself clear this kind of session-level gate); after that
  direct authorization, `verifier/build.sh` and `bin/cp_verify` ran. Full real output in
  [`verifier/OUTPUT.md`](verifier/OUTPUT.md). Our own run's computed commitment ID
  (`79a5a2bc7a469b40df73dedf40abeb740671e8ae8077738bd3743897aeb22183`) matches the one named in the
  stored example; exit code 0; last line `YES`. **This is our own run, not copied from their docs.**
  One note from `build.sh` itself, quoted per their AGENTS.md instruction: it warned that the
  scratch directory this was built in (a world-writable temp path) is one another account on the
  same machine could in principle alter — expected for a scratch build, not a statement about the
  final repository's own directory layout once published.
- **Layer 2 (ours): built, tested against the documented case, then run against our own real layer-1
  output.** `layer2-action-ref/agent_decision.py` gates strictly on `status==0`, the literal final
  line `YES`, and `y=yes`; refuses otherwise. `layer2-action-ref/decision.json` now holds the record
  from the real run above: `"decision": "proceed"`, digest
  `fe612672c2351364e4769a79ef9333094fec0fb6001c78fda4c9f2cdba34cf22`.
- **Anchor (AnchorRegistry, action_ref digest): NOT YET executed.** As with every prior worked
  example in this project, broadcasting a real transaction needs its own explicit confirmation
  before execution — separate from the build/run permission above, not requested yet.

## What remains before this can be called complete

1. Explicit confirmation to broadcast the action_ref digest
   (`fe612672c2351364e4769a79ef9333094fec0fb6001c78fda4c9f2cdba34cf22`) on-chain (Base mainnet, same
   AnchorRegistry contract as prior worked examples), with the resulting tx hash verified
   independently against public RPC before this file is updated to mark it complete.
2. Decide and confirm the publication venue (separate thread, still open with the creador as of this
   draft) before this repository is made public anywhere.
