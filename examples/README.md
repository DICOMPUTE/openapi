# Examples

Runnable against the live API. Each one resolves the model id from `/v1/models`
rather than hardcoding it.

| File | Run it |
|---|---|
| [`curl.sh`](curl.sh) | `./curl.sh` |
| [`python/quickstart.py`](python/quickstart.py) | `pip install openai && python quickstart.py` |
| [`typescript/quickstart.ts`](typescript/quickstart.ts) | `npm i openai && npx tsx quickstart.ts` |

All three read `DICO_KEY` from the environment. To get one:

```bash
curl -sS -X POST https://dicompute.ai/api/signup \
  -H 'content-type: application/json' -d '{"email":"you@example.com"}'
export DICO_KEY="sk-dico-..."
```
