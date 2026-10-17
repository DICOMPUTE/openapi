# Examples

Runnable against the live API. Each one resolves the model id from `/v1/models`
rather than hardcoding it.

| File | Run it |
|---|---|
| [`curl.sh`](curl.sh) | `./curl.sh` |
| [`python/quickstart.py`](python/quickstart.py) | `pip install openai && python quickstart.py` |
| [`typescript/quickstart.ts`](typescript/quickstart.ts) | `npm i openai && npx tsx quickstart.ts` |

All three read `DICO_KEY` from the environment. To get one, sign up in the console
(<https://dicompute.ai/console#onboarding>: email, 6-digit code, accept the
terms; the key is shown once). Scripted signup is a multi-step flow, see the
[top-level README](../README.md).

```bash
export DICO_KEY="sk-dico-..."
```
