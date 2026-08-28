/**
 * DiCompute quickstart — the OpenAI SDK, pointed at a different base URL.
 *
 *   npm i openai
 *   export DICO_KEY="sk-dico-..."
 *   npx tsx quickstart.ts
 */
import OpenAI from "openai";

const baseURL = process.env.DICO_BASE_URL ?? "https://dicompute.ai/openai/v1";
const apiKey = process.env.DICO_KEY;

if (!apiKey) {
  console.error(
    "Set DICO_KEY first. Mint one with:\n" +
      "  curl -sS -X POST https://dicompute.ai/api/signup \\\n" +
      "    -H 'content-type: application/json' -d '{\"email\":\"you@example.com\"}'",
  );
  process.exit(1);
}

const client = new OpenAI({ baseURL, apiKey });

// Resolve the model id at runtime rather than hardcoding it.
const { data: models } = await client.models.list();
const model = models[0]!.id;
console.log(`using model: ${model}\n`);

const stream = await client.chat.completions.create({
  model,
  messages: [{ role: "user", content: "In one sentence: what is decentralized inference?" }],
  stream: true,
});

for await (const chunk of stream) {
  process.stdout.write(chunk.choices[0]?.delta?.content ?? "");
}
process.stdout.write("\n");
