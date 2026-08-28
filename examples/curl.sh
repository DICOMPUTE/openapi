#!/usr/bin/env bash
# DiCompute API quickstart. Requires: curl, and DICO_KEY for the authed calls.
set -euo pipefail

BASE="${DICO_BASE_URL:-https://dicompute.ai/openai}"

echo "== public: the live catalog (no key needed) =="
curl -sS "$BASE/v1/models"

echo
echo "== public: current rates =="
curl -sS "$BASE/v1/pricing"

if [ -z "${DICO_KEY:-}" ]; then
  echo
  echo "Set DICO_KEY to run the authenticated calls. Mint one with:"
  echo "  curl -sS -X POST https://dicompute.ai/api/signup \\"
  echo "    -H 'content-type: application/json' -d '{\"email\":\"you@example.com\"}'"
  exit 0
fi

# Resolve a model id from the live catalog rather than hardcoding one.
# grep -o emits one match per line, so head -1 is genuinely the FIRST id
# (a greedy sed on this single-line JSON would silently return the LAST).
MODEL="$(curl -sS "$BASE/v1/models" \
  | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)"
echo
echo "== streaming a completion with model: $MODEL =="
curl -sS -N "$BASE/v1/chat/completions" \
  -H "authorization: Bearer $DICO_KEY" \
  -H 'content-type: application/json' \
  -d "{\"model\":\"$MODEL\",\"stream\":true,
       \"messages\":[{\"role\":\"user\",\"content\":\"say OK\"}]}"

echo
echo "== what that cost =="
curl -sS "$BASE/v1/account/balance" -H "authorization: Bearer $DICO_KEY"
