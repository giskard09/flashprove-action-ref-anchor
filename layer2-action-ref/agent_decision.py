#!/usr/bin/env python3
"""
Layer 2 of this worked example: what an agent does AFTER a FlashProve verification.

FlashProve (layer 1, github.com/anthropics/FlashProve, Apache-2.0, cited unmodified) proves one
thing only: that a reply came from a committed model, under an exact-match or score policy. Its own
docs are explicit that this says nothing about any model that anyone serves in production, and
nothing at all about what happens to the reply afterward.

This script is OUR code, not FlashProve's. It takes the parsed `result-v1` line that `bin/cp_verify`
prints (see layer1-flashprove/README.md for how that line is produced from the repository's own
bundled example) and makes one small, named decision from it: whether to proceed with a downstream
action. The action itself is anchored with action_ref/AnchorRegistry, independent of FlashProve.

Honesty constraints this script is held to (per PROVENANCE.md):
- The decision is gated strictly on the verifier's own exit status and its `y=` field, nothing else.
- The downstream action is a real, modest, named action (a digest anchor), not a dramatized one
  (e.g. not "the agent paid a human" or "the agent took an irreversible real-world action") — this
  example's synthetic model carries no real-world weight, so the action it unlocks must not either.
- If the verification fails or is missing, the agent must refuse, not proceed with a default.
"""
import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone

RESULT_LINE_RE = re.compile(
    r"^result-v1\s+status=(?P<status>\d+)\s+claim=(?P<claim>\S+)\s+id=(?P<id>[0-9a-f]+)\b.*?\by=(?P<y>yes|no)\b"
)


def parse_result_line(line: str) -> dict:
    """Parse the `result-v1 ...` line that bin/cp_verify prints (verifier/docs/output.md)."""
    m = RESULT_LINE_RE.search(line.strip())
    if not m:
        raise ValueError(f"not a result-v1 line this script understands: {line!r}")
    d = m.groupdict()
    d["status"] = int(d["status"])
    return d


def decide(parsed: dict, final_line: str) -> dict:
    """
    The only decision this agent makes: proceed or refuse.

    Gate (all three required — any missing or false value refuses):
      1. cp_verify exited 0 (parsed['status'] == 0)
      2. the final printed line is exactly "YES" (not inferred from status alone)
      3. the claim's own y= field is "yes" for the checked token

    This mirrors verifier/docs/output.md: status and the YES/NO line are two independent signals
    from the same run, and this script refuses unless both agree. It does not re-derive, soften or
    second-guess what the verifier said.
    """
    ok = (
        parsed["status"] == 0
        and final_line.strip() == "YES"
        and parsed["y"] == "yes"
    )
    return {
        "decision": "proceed" if ok else "refuse",
        "gate": {
            "cp_verify_exit_status_zero": parsed["status"] == 0,
            "final_line_is_YES": final_line.strip() == "YES",
            "claim_y_is_yes": parsed["y"] == "yes",
        },
        "flashprove_claim": parsed,
    }


def build_action_record(decision: dict, agent_id: str) -> dict:
    """
    The downstream action this example unlocks: NOT a payment, NOT a real-world effect — a named,
    modest action proportional to what a toy synthetic-model proof can honestly support: the agent
    commits (anchors) its own decision record, so that *that it decided, and on what claim* is
    independently checkable later, the same way action_ref anchors have always worked in this
    project's other worked examples (turnkey-action-ref-anchor, dapr-history-anchor,
    lightning-wavelength-action-ref-anchor).

    If this example is extended to a real served model and a real FlashProve deployment, the same
    gate could reasonably unlock a real tool call or payment — this script deliberately does not,
    so as not to overclaim what a toy synthetic-model proof backs.
    """
    record = {
        "action_ref_version": "v1",
        "agent_id": agent_id,
        "upstream_verification": {
            "system": "FlashProve",
            "repo": "https://github.com/anthropics/FlashProve",
            "license": "Apache-2.0",
            "note": "cited unmodified; this record does not alter or re-run FlashProve's own output",
        },
        "decision": decision["decision"],
        "gate": decision["gate"],
        "flashprove_claim": decision["flashprove_claim"],
        "decided_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
    }
    payload = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    record["digest_sha256"] = hashlib.sha256(payload).hexdigest()
    return record


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--result-line",
        required=True,
        help="the exact result-v1 line printed by bin/cp_verify (quote it whole)",
    )
    ap.add_argument(
        "--final-line",
        required=True,
        help='the last line cp_verify printed (expected "YES" or "NO")',
    )
    ap.add_argument("--agent-id", default="rama-worked-example-agent")
    ap.add_argument("--out", help="write the action record JSON here instead of stdout")
    args = ap.parse_args()

    try:
        parsed = parse_result_line(args.result_line)
    except ValueError as e:
        print(f"refuse: {e}", file=sys.stderr)
        return 2

    decision = decide(parsed, args.final_line)
    record = build_action_record(decision, args.agent_id)

    out = json.dumps(record, indent=2, sort_keys=True)
    if args.out:
        with open(args.out, "w") as f:
            f.write(out + "\n")
    else:
        print(out)

    return 0 if decision["decision"] == "proceed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
