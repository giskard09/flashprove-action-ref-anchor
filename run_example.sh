#!/bin/bash
# Runs this worked example end to end: layer 1 (FlashProve's own stored example, unmodified) then
# layer 2 (our agent_decision.py). Expects a fresh clone of github.com/anthropics/FlashProve at
# $FLASHPROVE_CHECKOUT (default: ./FlashProve, as cloned by layer1-flashprove's instructions).
set -euo pipefail

FLASHPROVE_CHECKOUT="${FLASHPROVE_CHECKOUT:-./FlashProve}"
COMMITMENT_ID="79a5a2bc7a469b40df73dedf40abeb740671e8ae8077738bd3743897aeb22183"

if [[ ! -d "$FLASHPROVE_CHECKOUT" ]]; then
  echo "run_example.sh: $FLASHPROVE_CHECKOUT not found. Clone it first:" >&2
  echo "  git clone --depth 1 https://github.com/anthropics/FlashProve.git $FLASHPROVE_CHECKOUT" >&2
  exit 2
fi

echo "--- step 0: confirm the stored example is byte-identical to what Anthropic published ---"
( cd "$FLASHPROVE_CHECKOUT/examples/accepted-proof" && sha256sum -c SHA256SUMS )

echo
echo "--- step 1: build FlashProve's own verifier (their code, unmodified) ---"
( cd "$FLASHPROVE_CHECKOUT" && verifier/build.sh )

echo
echo "--- step 2: run it against their own stored example ---"
OUTPUT=$( cd "$FLASHPROVE_CHECKOUT" && bin/cp_verify \
  examples/accepted-proof/config examples/accepted-proof/ivk \
  examples/accepted-proof/example.req examples/accepted-proof/example.y \
  examples/accepted-proof/example.proof \
  -id "$COMMITMENT_ID" -q )
echo "$OUTPUT"
{
  echo "# Verifier output"
  echo
  echo "Command: \`bin/cp_verify examples/accepted-proof/{config,ivk,example.req,example.y,example.proof} -id $COMMITMENT_ID -q\`"
  echo "Run from: $FLASHPROVE_CHECKOUT (commit \`$(cd "$FLASHPROVE_CHECKOUT" && git rev-parse HEAD)\`)"
  echo "Run at (UTC): $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo
  echo '```'
  echo "$OUTPUT"
  echo '```'
} > verifier/OUTPUT.md
echo "wrote verifier/OUTPUT.md"

RESULT_LINE=$(echo "$OUTPUT" | grep '^result-v1 ')
FINAL_LINE=$(echo "$OUTPUT" | tail -n1)

echo
echo "--- step 3: our agent decides, based only on that output ---"
python3 layer2-action-ref/agent_decision.py \
  --result-line "$RESULT_LINE" \
  --final-line "$FINAL_LINE" \
  --out layer2-action-ref/decision.json
cat layer2-action-ref/decision.json
