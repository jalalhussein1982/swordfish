# Swordfish - Dark Web OSINT Tool

## Project Overview

Swordfish is a CLI tool for dark web intelligence gathering. It searches multiple Tor search engines, exports results for manual review, and scrapes selected links. No LLM dependency - you use your preferred LLM externally for analysis.

## Tech Stack

- **Language**: Python 3.10+
- **CLI Framework**: Click
- **Web Scraping**: BeautifulSoup, Requests
- **Proxy**: Tor SOCKS5 (127.0.0.1:9050)

## Directory Structure

```
swordfish/
├── main.py              # CLI entry point (search + scrape commands)
├── search.py            # Dark web search across 17 Tor engines
├── scrape.py            # Web content scraping with Tor
├── requirements.txt     # Python dependencies (minimal)
├── prompts/
│   └── query_refinement_prompt.md  # Manual LLM prompt for query refinement
├── LICENSE              # MIT License
└── README.md            # User documentation
```

## Two-Step Workflow

```
Step 1: Search
    User Query → Search 17 engines → Deduplicate → Export JSON

Step 2: Scrape
    User selects links → Scrape via Tor → Export JSON → Manual LLM analysis
```

## CLI Commands

### `swordfish search` - Search dark web and export results

```bash
python main.py search -q "ransomware payments" -t 10 -o results.json
```

Options:
- `-q/--query` (required): Search query
- `-t/--threads` (default 5): Parallel search threads
- `-o/--output`: Output JSON file (default: `results_<timestamp>.json`)

Output format (`results.json`):
```json
{
  "query": "ransomware payments",
  "timestamp": "2025-12-10T10:30:00",
  "total_results": 150,
  "results": [
    {"index": 1, "title": "Result title", "link": "http://xxx.onion/page"},
    {"index": 2, "title": "Another result", "link": "http://yyy.onion/page"}
  ]
}
```

### `swordfish scrape` - Scrape selected links

```bash
python main.py scrape -i selected_links.txt -t 10 -o content.json
```

Options:
- `-i/--input` (required): File with links (one per line)
- `-t/--threads` (default 5): Parallel scraping threads
- `-o/--output`: Output JSON file (default: `scraped_<timestamp>.json`)

Input format (`selected_links.txt`):
```
http://xxx.onion/page
http://yyy.onion/page
# Comments are ignored
http://zzz.onion/page
```

Output format (`content.json`):
```json
{
  "timestamp": "2025-12-10T10:45:00",
  "total_scraped": 3,
  "content": [
    {"link": "http://xxx.onion/page", "title": "Page Title", "text": "Scraped content..."},
    {"link": "http://yyy.onion/page", "title": "Page Title", "text": "Scraped content..."}
  ]
}
```

## Key Files & Functions

### main.py
- `swordfish search`: Search command
- `swordfish scrape`: Scrape command

### search.py
- `SEARCH_ENGINE_ENDPOINTS`: List of 17 Tor search engine URL templates
- `get_tor_proxies()`: Returns SOCKS5 proxy config
- `fetch_search_results(engine, query)`: Scrapes single search engine
- `get_search_results(query, max_workers)`: Parallel multi-engine search
- `export_results(results, query, output_path)`: Export to JSON

### scrape.py
- `get_tor_session()`: Creates requests.Session with Tor proxy and retry
- `scrape_single(url_data)`: Scrapes one URL (45s timeout, 2000 char limit)
- `scrape_multiple(urls_data, max_workers)`: Parallel scraping
- `read_links_from_file(file_path)`: Read links from text file
- `export_scraped_content(scraped_results, output_path)`: Export to JSON

### prompts/query_refinement_prompt.md
Manual prompt for refining search queries with your preferred LLM.

## Running the App

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start Tor daemon
# Linux: sudo apt install tor && sudo service tor start
# macOS: brew install tor && tor

# 3. Search
python main.py search -q "your query" -t 5 -o results.json

# 4. Review results.json, create selected_links.txt with chosen links

# 5. Scrape
python main.py scrape -i selected_links.txt -o content.json

# 6. Analyze content.json with your preferred LLM
```

## Common Modification Patterns

### Adding a New Search Engine
Add URL template to `search.py:SEARCH_ENGINE_ENDPOINTS`:
```python
"http://new-engine.onion/search?q={query}"
```

### Changing Scraping Behavior
Edit `scrape.py`:
- Timeout: Change `timeout=45` in `scrape_single()`
- Content limit: Change `max_chars = 2000` in `scrape_multiple()`
- Retry strategy: Modify `HTTPAdapter` parameters in `get_tor_session()`

## Architecture Notes

- **Parallel Processing**: Uses `ThreadPoolExecutor` for concurrent search and scraping
- **Tor Proxy**: All `.onion` requests go through SOCKS5 proxy at 127.0.0.1:9050
- **No LLM Dependency**: All LLM operations are manual/external

## Requirements

- **Tor daemon** must be running on localhost:9050
  - Linux: `apt install tor && sudo service tor start`
  - macOS: `brew install tor && tor`

## Search Engines (17 total)

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
15. OSS (Onion Search Server)
16. Torgol
17. The Deep Searches
