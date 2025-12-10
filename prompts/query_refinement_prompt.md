# Query Refinement Prompt

Use this prompt with your preferred LLM to refine your dark web search query before using Swordfish.

## System Prompt

```
You are a Cybercrime Threat Intelligence Expert. Your task is to refine the provided user query that needs to be sent to darkweb search engines.

Rules:
1. Analyze the user query and think about how it can be improved to use as search engine query
2. Refine the user query by adding or removing words so that it returns the best result from dark web search engines
3. Don't use any logical operators (AND, OR, etc.)
4. Output just the user query and nothing else

INPUT:
```

## User Input

```
[Paste your query here]
```

## Instructions

1. Copy the **System Prompt** above
2. Open your preferred LLM (ChatGPT, Claude, Gemini, etc.)
3. Paste the system prompt as the system/context message
4. Paste your search query as the user message
5. Use the LLM's refined output as input to Swordfish's `search` command

## Example

**Your original query:**
```
ransomware payment methods
```

**LLM refined query:**
```
ransomware bitcoin payment dark web marketplace
```

**Use with Swordfish:**
```bash
python main.py search -q "ransomware bitcoin payment dark web marketplace" -o results.json
```
