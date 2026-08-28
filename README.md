# DiCompute API — OpenAPI specification

The machine-readable contract for the [DiCompute](https://dicompute.ai) inference
API: one OpenAI-compatible endpoint over independent GPU operators, metered in
micro-USD and settled on XDC.

**Base URL:** `https://dicompute.ai/openai`

[`openapi.json`](openapi.json) describes 20 endpoints. Point Postman, Insomnia,
Stoplight, or any OpenAPI code generator at it.

```bash
npx @redocly/cli preview-docs \
  https://raw.githubusercontent.com/DICOMPUTE/openapi/main/openapi.json
```

## Two minutes to a first call

No account, no password, no credit card. Signup mints a key with real starting credit.

```bash
curl -sS -X POST https://dicompute.ai/api/signup \
  -H 'content-type: application/json' \
  -d '{"email":"you@example.com"}'
# => {"apiKey":"sk-dico-...","account":"signup-...","startingBalanceUusd":100000}
```

> The key is returned **exactly once** — there is no recovery flow. Copy it now.
> `startingBalanceUusd` is micro-USD: 100,000 µUSD = $0.10.

```bash
export DICO_KEY="sk-dico-..."

curl -sS -N https://dicompute.ai/openai/v1/chat/completions \
  -H "authorization: Bearer $DICO_KEY" \
  -H 'content-type: application/json' \
  -d '{"model":"qwen2.5-3b-instruct","stream":true,
       "messages":[{"role":"user","content":"say OK"}]}'
```

Runnable versions in [`examples/`](examples) — curl, Python, and TypeScript.

## Already using another SDK?

The endpoint is OpenAI-compatible, so most clients need only a base URL change.
An Anthropic-shaped surface (`/v1/messages`) is served from the same base.

```python
from openai import OpenAI

client = OpenAI(base_url="https://dicompute.ai/openai/v1", api_key="sk-dico-...")
```

## Endpoints

Resolve model ids from `/v1/models` at runtime — the catalog changes, and
hardcoding an id is the most common integration break.

| Endpoint | Auth | What it does |
|---|---|---|
| `POST /v1/chat/completions` | yes | OpenAI-compatible chat, streaming supported |
| `POST /v1/responses` | yes | OpenAI Responses-shaped surface |
| `POST /v1/messages` | yes | Anthropic-shaped surface |
| `POST /v1/messages/count_tokens` | yes | Token count without spending |
| `POST /v1/embeddings` | yes | Embeddings |
| `POST /v1/rerank` | yes | Reranking |
| `GET /v1/models` · `GET /v1/models/{id}` | no | Live catalog, capabilities, pricing |
| `GET /v1/models/capacity` | no | Serving capacity per model |
| `GET /v1/pricing` | no | Per-token rates, batch discount, minimum charge |
| `GET /v1/stats` | no | Network stats — upstreams, metered requests |
| `GET /v1/account/balance` · `GET /v1/account/usage` | yes | Your balance and usage |
| `GET /v1/me` | yes | Identity for the presented key |
| `POST /v1/keys/revoke` | yes | Revoke a key |
| `GET /v1/provider/earnings` | yes | GPU operator earnings |
| `POST /v1/sessions` | yes | Session exchange |
| `/v1/oauth/authorize` · `/v1/oauth/token` · `/v1/oauth/clients/{id}` | mixed | OAuth flow |

The four unauthenticated `GET`s are the quickest way to confirm connectivity:

```bash
curl -sS https://dicompute.ai/openai/v1/models
curl -sS https://dicompute.ai/openai/v1/pricing
```

## Billing model

Usage is metered in **integer micro-USD** end to end — no floating-point drift
between what the router measures and what your balance is charged. `/v1/pricing`
returns the live per-model rates, the batch discount, and the minimum charge per
request. Current rates are also published at [dicompute.ai/models](https://dicompute.ai/models).

## How this file is maintained

`openapi.json` is **generated**, not hand-written — it is derived from the API's
own endpoint list and shared request/response schemas in the DiCompute monorepo,
then published here. Two consequences:

- **Don't send PRs that edit `openapi.json` directly.** They would be overwritten
  by the next sync. Open an issue describing the mismatch instead.
- **The spec follows the deployed API**, so a field appearing here means it exists
  in the running service, not that it is merely planned.

Corrections to `examples/` and this README are very welcome.

## Links

[Website](https://dicompute.ai) ·
[Console](https://dicompute.ai/console) ·
[Models & pricing](https://dicompute.ai/models) ·
[API console](https://dicompute.ai/api-console) ·
[Live stats](https://dicompute.ai/stats) ·
[Whitepaper](https://dicompute.ai/whitepaper) ·
[Run a GPU](https://dicompute.ai/earn)

## Security

Never open a public issue for a vulnerability — see
[DICOMPUTE/.github/SECURITY.md](https://github.com/DICOMPUTE/.github/blob/main/SECURITY.md)
or email `security@dicompute.ai`.

## License

[MIT](LICENSE).
