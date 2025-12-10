# Swordfish - Dark Web OSINT Tool

A CLI tool for dark web intelligence gathering. Searches 17 Tor search engines, exports results for manual review, and scrapes selected links.

## Features

- Search 17 dark web search engines in parallel
- Export all results to JSON for manual review
- Scrape selected links via Tor
- No LLM dependency - use your preferred LLM for analysis

## Requirements

- Python 3.10+
- Tor daemon running on localhost:9050

## Installation

```bash
# Clone the repository
git clone https://github.com/jalalhussein/swordfish.git
cd swordfish

# Install Python dependencies
pip install -r requirements.txt

# Install and start Tor
# macOS:
brew install tor
tor

# Linux:
sudo apt install tor
sudo service tor start
```

## Usage

### Step 1: Search

Search dark web engines and export all results:

```bash
python main.py search -q "your search query" -o results.json
```

Options:
- `-q, --query` (required): Search query
- `-t, --threads` (default: 5): Number of parallel threads
- `-o, --output`: Output JSON file (default: `results_<timestamp>.json`)

### Step 2: Select Links

Review `results.json` and create a text file with links you want to scrape (one per line):

```
http://example1.onion/page
http://example2.onion/page
# Comments are ignored
http://example3.onion/page
```

### Step 3: Scrape

Scrape content from selected links:

```bash
python main.py scrape -i selected_links.txt -o content.json
```

Options:
- `-i, --input` (required): File with links to scrape
- `-t, --threads` (default: 5): Number of parallel threads
- `-o, --output`: Output JSON file (default: `scraped_<timestamp>.json`)

### Step 4: Analyze

Use your preferred LLM to analyze the scraped content in `content.json`.

See `prompts/query_refinement_prompt.md` for a prompt template to refine your search queries.

## Output Formats

### Search Results (results.json)

```json
{
  "query": "search query",
  "timestamp": "2025-12-10T10:30:00",
  "total_results": 150,
  "results": [
    {"index": 1, "title": "Result Title", "link": "http://xxx.onion/page"}
  ]
}
```

### Scraped Content (content.json)

```json
{
  "timestamp": "2025-12-10T10:45:00",
  "total_scraped": 10,
  "content": [
    {"link": "http://xxx.onion/page", "title": "Page Title", "text": "Scraped content..."}
  ]
}
```

## Search Engines

Swordfish searches 17 Tor search engines:

1. Ahmia
2. OnionLand
3. DarkHunt
4. Torgle
5. Amnesia
6. Kaizer
7. Anima
8. Tornado
9. TorNet
10. Torland
11. Find Tor
12. Excavator
13. Onionway
14. Tor66
15. OSS
16. Torgol
17. The Deep Searches

## License

MIT License - See [LICENSE](LICENSE) for details.

## Author

Jalal Hussein <jalalhussein@gmail.com>
