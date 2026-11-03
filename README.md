# flashprove-action-ref-anchor

A worked example combining two independent layers of evidence around one AI reply:

1. **Which model answered** — [FlashProve](https://github.com/anthropics/FlashProve) (Anthropic
   PBC, Apache-2.0), cited and run unmodified. Proves, with a zkSNARK checked in Lean, that a reply
   came from a committed model under an exact-match or score policy.
2. **What an agent did with that answer** — `action_ref`, this project's own pattern (same one used
   in `turnkey-action-ref-anchor`, `dapr-history-anchor`, `lightning-wavelength-action-ref-anchor`).
   An agent reads FlashProve's verdict, makes one gated decision (proceed/refuse), and that decision
   is anchored on-chain so it is independently checkable afterward.

FlashProve's own documentation is explicit that its guarantee stops at "this reply came from the
committed model" — nothing about what happens to the reply next. This example exists to show that
second half concretely, not to claim FlashProve is missing something it was ever meant to cover.

This is our own initiative. We are not contributors to FlashProve (that repository states
explicitly it accepts none) and no one at Anthropic asked for this. See [PROVENANCE.md](PROVENANCE.md)
for exactly what is cited, what is ours, and the current build status.

## Layout

```
layer1-flashprove/    pointers + exact commands to reproduce FlashProve's own stored example
layer2-action-ref/    agent_decision.py — our code, gates on layer 1's verdict
verifier/             where the compiled cp_verify binary and its real output go once built
PROVENANCE.md         what is cited vs. ours, and current (honest) build status
```

## Status

See [PROVENANCE.md](PROVENANCE.md) — this repository is a work in progress, not yet published.
