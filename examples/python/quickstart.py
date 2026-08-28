"""DiCompute quickstart — the OpenAI SDK, pointed at a different base URL.

    pip install openai
    export DICO_KEY="sk-dico-..."
    python quickstart.py
"""

import os

from openai import OpenAI

BASE_URL = os.environ.get("DICO_BASE_URL", "https://dicompute.ai/openai/v1")
api_key = os.environ.get("DICO_KEY")
if not api_key:
    raise SystemExit(
        "Set DICO_KEY first. Mint one with:\n"
        "  curl -sS -X POST https://dicompute.ai/api/signup \\\n"
        "    -H 'content-type: application/json' -d '{\"email\":\"you@example.com\"}'"
    )

client = OpenAI(base_url=BASE_URL, api_key=api_key)

# Resolve the model id at runtime. The catalog changes; a hardcoded id is the
# most common way an integration breaks.
model = client.models.list().data[0].id
print(f"using model: {model}\n")

stream = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "In one sentence: what is decentralized inference?"}],
    stream=True,
)

for chunk in stream:
    delta = chunk.choices[0].delta.content
    if delta:
        print(delta, end="", flush=True)
print()
