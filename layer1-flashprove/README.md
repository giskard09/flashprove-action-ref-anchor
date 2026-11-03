# Layer 1 — FlashProve (cited, unmodified)

Everything in this directory is pointers and commands, not FlashProve's code. We clone it fresh
rather than vendoring it, so this example never drifts from what Anthropic actually published.

## What we cite

- Repo: https://github.com/anthropics/FlashProve
- Commit: `9e2bdd8ff5bf9c62f18263d7dac189b0400b260c` (2026-10-30T20:56:11Z)
- Version: `0.16.0`
- License: Apache-2.0
- Primary announcement: https://www.anthropic.com/research/provable-inference

## What we checked before using it

```sh
git clone --depth 1 https://github.com/anthropics/FlashProve.git
cd FlashProve/examples/accepted-proof
sha256sum -c SHA256SUMS
```

All nine files (`ID.txt`, `config/*`, `example.proof`, `example.req`, `example.y`, `ivk/*`) check
out `OK` against the repository's own published `SHA256SUMS` — confirms we have the files Anthropic
published, unaltered, before building or running anything.

## Reproducing the stored example (route 1 of their README — no GPU, under 2 minutes)

```sh
verifier/build.sh
bin/cp_verify examples/accepted-proof/config examples/accepted-proof/ivk \
  examples/accepted-proof/example.req examples/accepted-proof/example.y \
  examples/accepted-proof/example.proof \
  -id 79a5a2bc7a469b40df73dedf40abeb740671e8ae8077738bd3743897aeb22183 -q
```

Expected: exit code 0, last line `YES`, preceded by a `result-v1 ...` line (see
`examples/accepted-proof/README.md` in the FlashProve checkout for what every field means).

**Our output from running this ourselves** goes in [`../verifier/OUTPUT.md`](../verifier/OUTPUT.md)
once produced — see that file and `PROVENANCE.md` for whether it has been run yet in this draft.

## What this example is, and is not, evidence of

Quoting FlashProve's own `examples/accepted-proof/README.md` directly: "This `YES` shows that the
verifier builds and runs on your machine and that these files fit together... It says nothing about
any model that anyone serves." The model here is synthetic (8 layers, 4 routed experts, a 512-word
vocabulary) — this is FlashProve demonstrating its own verifier, not a claim about Llama 4 Maverick
or any served model. That is the right scope for this example too: layer 2 of this repository gates
on *that the verifier's own stored demonstration passed*, nothing more.
