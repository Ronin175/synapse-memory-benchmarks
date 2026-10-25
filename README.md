# Synapse Memory: LoCoMo Results

**82.7% on LoCoMo (all 1,540 scored questions), answered by a 20B open model running on a laptop.**

AI assistants forget. Each conversation starts from zero unless something stores what was said and hands the right parts back later. Most memory systems that do this run in the cloud and answer with large cloud models, which rules them out for teams whose data cannot leave the building: law firms, hospitals, defense contractors.

Synapse Memory is a memory engine built for those teams. It runs entirely on the user's own machine. On LoCoMo, the standard benchmark for long-term conversational memory, it scores 82.7% with a 20B open model on a MacBook Pro. That is within half a point of the best published result on the same answer model, and ahead of several systems that answer with cloud models.

This repo publishes the results, how they were measured, and enough detail for anyone to check them. The engine code is not public. Every run records the SHA-256 fingerprint of the exact engine file it tested.

Built and tested by Grant McElroy, solo, since April 2026.

---

## Headline result

| | |
|---|---|
| Benchmark | LoCoMo, categories 1 to 4 (1,540 questions across 10 long conversations) |
| Engine | Synapse 0.1.5 |
| Answer model | gpt-oss-20b, run locally with Ollama |
| Hardware | 14-inch MacBook Pro, M4 Pro (14-core CPU, 20-core GPU), 48 GB |
| Judge | GPT-4o (gpt-4o-2024-08-06), Mem0 paper judge prompt |
| **Score (LLM judge, J)** | **82.7%** |
| Official LoCoMo token F1 | 53.5% |
| Date | 2026-10-23 |

Everything except the judge runs on the laptop. The judge only sees LoCoMo's public question, the answer key, and the model's answer.

---

## Progress

Four full runs, every one on all 1,540 questions, same dataset, same judge and judge prompt.

| Date | Engine | Answer model (local) | Overall J | Single-hop | Temporal | Multi-hop | Open-domain | Evidence shown | F1 |
|---|---|---|---|---|---|---|---|---|---|
| 2026-10-18 | 0.1.3 | qwen3.5:9b | 71.0% | 77.4% | 73.8% | 58.5% | 41.7% | 74.8% | 52.5% |
| 2026-10-19 | 0.1.4 | qwen3.5:9b | 79.7% | 89.1% | 76.3% | 66.7% | 47.9% | 87.1% | 59.9% |
| 2026-10-20 | 0.1.4 | gpt-oss-20b | 81.6% | 87.3% | 81.3% | 72.0% | 60.4% | 87.1% | 54.1% |
| 2026-10-23 | **0.1.5** | gpt-oss-20b | **82.7%** | **89.2%** | 81.3% | 72.0% | **61.5%** | **90.4%** | 53.5% |

What changed at each step:
- **0.1.3 to 0.1.4 (+8.7):** the engine shows the model the turns said around each memory it finds, ranks memories said near a date the question names higher, and fixes a date-reading bug. New answer prompt. Retrieval went from 74.8% to 87.1% of evidence shown.
- **9B to 20B (+1.9):** only the answer model changed. Same engine file, same fingerprint.
- **0.1.4 to 0.1.5 (+1.1):** the engine hands the model 48 memories instead of 24. Nothing else in the engine changed.

"Evidence shown" is the share of the answer key's evidence turns that were in the context the model saw. It separates what the engine found from what the model did with it.

---

## By category (0.1.5)

LoCoMo's dataset uses category codes 1 to 4. Some papers, including Mem0 and Hindsight, print these under different names, so the question counts are listed to make matching easy.

| Category (dataset code) | Questions | J (strict) | Token F1 | Evidence shown |
|---|---|---|---|---|
| Single-hop (4) | 841 | 89.2% | 58.8% | 95.0% |
| Temporal (2) | 321 | 81.3% | 57.5% | 93.0% |
| Multi-hop (1) | 282 | 72.0% | 38.8% | 79.1% |
| Open-domain / reasoning (3) | 96 | 61.5% | 37.1% | 74.6% |
| **Overall** | **1,540** | **82.7%** | **53.5%** | **90.4%** |

How I read this: on single-hop and temporal questions, the engine finds the evidence more than 93% of the time, so most remaining misses are the model's. Multi-hop and open-domain are where the engine still misses pieces, and they are what I'm working on next.

---

## How it compares

Published LoCoMo scores, with the answer model and judge each one used. Most published results use a cloud model to answer. Synapse answers with a local open model.

| System | LoCoMo J | Answer model | Judge | Source |
|---|---|---|---|---|
| Hindsight | 83.2% | GPT-OSS-20B | GPT-OSS-120B | [arXiv 2512.12818](https://arxiv.org/abs/2512.12818), Table 4 |
| **Synapse 0.1.5** | **82.7%** | **gpt-oss-20b, local** | **GPT-4o, Mem0 paper prompt** | this repo |
| Memobase | 75.8% | not stated | not stated | cited in [arXiv 2512.12818](https://arxiv.org/abs/2512.12818) |
| MemOS | 75.8% | GPT-4o-mini | not stated | [arXiv 2507.03724](https://arxiv.org/abs/2507.03724) |
| Zep (Zep's own re-run) | 75.1% | not stated | not stated | [Zep blog](https://www.getzep.com/blog/lies-damn-lies-statistics-is-mem0-really-sota-in-agent-memory/) |
| Letta Filesystem | 74.0% | GPT-4o-mini | not stated | [Letta blog](https://www.letta.com/blog/benchmarking-ai-agent-memory) |
| Full conversation in context | 72.9% | GPT-4o-mini | GPT-4o-mini (per Mem0's released code) | [Mem0 paper, arXiv 2504.19413](https://arxiv.org/abs/2504.19413), Table 2 |
| Mem0 | 66.9% | GPT-4o-mini | GPT-4o-mini (per Mem0's released code) | [Mem0 paper, arXiv 2504.19413](https://arxiv.org/abs/2504.19413), Table 2 |

Judges and judge prompts differ between systems, so small gaps (a point or two) are not decisive. Large gaps are.

### Closest comparison: Hindsight on the same answer model

Hindsight and Synapse both answer with GPT-OSS-20B. Categories are matched by dataset code. Hindsight's paper uses different category names, and the match is confirmed by question-count weighting, which reproduces their 83.18% overall.

| Category (dataset code) | Questions | Synapse 0.1.5 | Hindsight (OSS-20B) |
|---|---|---|---|
| Single-hop (4) | 841 | 89.2% | 91.0% |
| Temporal (2) | 321 | **81.3%** | 76.3% |
| Multi-hop (1) | 282 | 72.0% | 74.1% |
| Open-domain / reasoning (3) | 96 | 61.5% | 64.6% |
| **Overall** | **1,540** | **82.7%** | **83.2%** |

Synapse leads on time questions by 5 points and trails on the other three. The overall gap is about 8 questions out of 1,540.

---

## Strict vs. lenient judge

Mem0 has published two judge prompts: the one from their paper, and a newer one used for their 2026 results. I graded the same 1,540 saved answers from the 0.1.4 gpt-oss-20b run with both. The 0.1.5 run has only been graded with the strict prompt.

| Category | J, Mem0 paper prompt (strict, headline) | J, Mem0 current prompt (lenient) |
|---|---|---|
| Single-hop | 87.3% | 89.1% |
| Temporal | 81.3% | 88.5% |
| Multi-hop | 72.0% | 87.6% |
| Open-domain / reasoning | 60.4% | 65.6% |
| **Overall** | **81.6%** | **87.2%** |

The two judges disagree on 91 answers. In 89 of them, the lenient prompt passed an answer the strict prompt failed. Some of those answers are wrong:

| Answer key | Model's answer | Lenient judge |
|---|---|---|
| six months | Five months. | passed |
| The week before 9 June 2023 | 9 June 2023 | passed |

So I report the strict prompt as the headline. A higher number isn't worth much if it passes wrong answers.

---

## How the runs work

- **Dataset:** LoCoMo (`locomo10.json`), categories 1 to 4. Category 5 (adversarial) is not scored, following the Mem0 paper.
- **Process:** each conversation is fed into a fresh engine turn by turn, in order. Then every question is asked once. The engine picks what to show the model; the model answers.
- **Answer prompt:** one prompt for every category, since a real system never knows a question's category. It contains no LoCoMo questions, answers or names, and an automated test checks for that.
- **Answer model settings:** gpt-oss-20b at medium reasoning, temperature 1.0 (OpenAI's recommended setting for this model), up to 2,048 output tokens, 16,384-token context window. Context given to the model in 0.1.5: median about 13,100 characters (about 3,400 tokens) per question, roughly 15% of an average LoCoMo conversation.
- **Judge:** GPT-4o (gpt-4o-2024-08-06). The strict prompt is called the way the Mem0 paper called it (temperature 0, JSON output), copied byte for byte from Mem0 (`evaluation/metrics/llm_judge.py`, tag v0.1.99). The lenient prompt is from `mem0ai/memory-benchmarks`, commit 4b61c5d.
- **F1:** LoCoMo's official token F1 code (snap-research/locomo, commit 3eb6f2c). F1 counts matching words, so fuller answers score a little lower on it even when they're right. That's why F1 dipped slightly in the last two runs while J went up.
- **Fingerprinting:** every run records the SHA-256 of the engine file it tested, so a result always points to one exact version.

| Engine | SHA-256 (first 12) | Runs |
|---|---|---|
| 0.1.3 | `8a277967a5f4` | 2026-10-18 |
| 0.1.4 | `5d986093f8fc` | 2026-10-19, 2026-10-20 |
| 0.1.5 | `fc33f440de9c` | 2026-10-23 |

### Speed and cost (0.1.5 run)

| | |
|---|---|
| Answer time, median / 95th percentile | 10.3 s / 27.1 s |
| Retrieval time, median | 0.05 s |
| Writing speed | about 50 tokens/s |
| Input per answer, average | about 3,400 tokens |
| Model memory | 12.9 GB |
| Judge cost, full run (strict prompt) | about $1.69 |

---

## What these results do not show

- **One run per version.** At temperature 1.0 the model answers a little differently each time. Between the last two runs, about 140 answers flipped right or wrong with the same evidence shown. A rerun could land several tenths of a point higher or lower.
- **Different judges across systems.** See the judge column above. Hindsight used GPT-OSS-120B; Synapse used GPT-4o.
- **18 answers ran out of room.** In the 0.1.5 run, 18 answers hit the 2,048-token output cap before finishing and were graded wrong. They're counted as misses in the 82.7%.
- **LoCoMo only.** LongMemEval is next.

---

## Check it yourself

Every answer and every grade from all four runs is in `results/`, one file per run, one line per question:

| File | Run |
|---|---|
| `results/2026-10-18_synapse-0.1.3_qwen3.5-9b.jsonl` | 0.1.3, qwen3.5:9b |
| `results/2026-10-19_synapse-0.1.4_qwen3.5-9b.jsonl` | 0.1.4, qwen3.5:9b |
| `results/2026-10-20_synapse-0.1.4_gpt-oss-20b.jsonl` | 0.1.4, gpt-oss-20b |
| `results/2026-10-23_synapse-0.1.5_gpt-oss-20b.jsonl` | 0.1.5, gpt-oss-20b (headline) |

Each line holds the question ID, category, question, answer key, the model's full reply, the answer graded, the strict judge's verdict (and the lenient one, where that was run), official F1, the answer key's evidence turns, the share of them shown to the model, whether the reply hit the token cap, and timing and token counts.

To rebuild every table in this README (Python 3, standard library only):

```
python3 scripts/score.py results/*.jsonl
```

To re-grade the answers with your own judge, take `question`, `gold` and `answer` from each line. `MANIFEST.sha256` lists the fingerprint of every file here.

Not published: the engine code, and the memory text the engine handed the model for each question, since that shows how the engine works.

---

## Contact

Grant McElroy
[LinkedIn](https://www.linkedin.com/in/grant-m-a564a8220/)

Build log: [TikTok @_ronin175](https://www.tiktok.com/@_ronin175) · [Instagram @_ronin175](https://www.instagram.com/_ronin175/) · [X @ronin175_](https://x.com/ronin175_)
