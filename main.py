import click
import json
from yaspin import yaspin
from datetime import datetime
from scrape import scrape_multiple, read_links_from_file, export_scraped_content
from search import get_search_results, export_results


@click.group()
@click.version_option()
def swordfish():
    """Swordfish: Dark Web OSINT Tool.

    A two-step CLI tool for dark web intelligence gathering:

    Step 1: Search dark web engines and export results
    Step 2: Scrape selected links and export content
    """
    pass


@swordfish.command()
@click.option("--query", "-q", required=True, type=str, help="Dark web search query")
@click.option(
    "--threads",
    "-t",
    default=5,
    show_default=True,
    type=int,
    help="Number of threads for parallel searching",
)
@click.option(
    "--output",
    "-o",
    type=str,
    help="Output JSON filename. Default: results_<timestamp>.json",
)
def search(query, threads, output):
    """Search dark web engines and export all results.

    Example:
        swordfish search -q "ransomware payments" -t 10 -o results.json

    This searches 17 Tor search engines in parallel and exports
    all deduplicated results to a JSON file for manual review.
    """
    click.echo(f"[*] Searching for: {query}")

    with yaspin(text="Searching dark web engines...", color="cyan") as sp:
        search_results = get_search_results(
            query.replace(" ", "+"), max_workers=threads
        )
        sp.ok("✔")

    click.echo(f"[*] Found {len(search_results)} unique results")

    # Generate output filename
    if not output:
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output = f"results_{now}.json"
    elif not output.endswith(".json"):
        output = output + ".json"

    # Export results
    export_results(search_results, query, output)
    click.echo(f"[+] Results saved to {output}")
    click.echo(f"\n[*] Next steps:")
    click.echo(f"    1. Review {output} and select links to scrape")
    click.echo(f"    2. Create a text file with selected links (one per line)")
    click.echo(f"    3. Run: swordfish scrape -i <links_file> -o <output_file>")


@swordfish.command()
@click.option(
    "--input",
    "-i",
    "input_file",
    required=True,
    type=click.Path(exists=True),
    help="Input file with links to scrape (one per line)",
)
@click.option(
    "--threads",
    "-t",
    default=5,
    show_default=True,
    type=int,
    help="Number of threads for parallel scraping",
)
@click.option(
    "--output",
    "-o",
    type=str,
    help="Output JSON filename. Default: scraped_<timestamp>.json",
)
def scrape(input_file, threads, output):
    """Scrape content from selected links.

    Example:
        swordfish scrape -i selected_links.txt -t 10 -o content.json

    Reads links from the input file (one per line) and scrapes
    content from each via Tor, exporting to a JSON file.
    """
    # Read links from input file
    links = read_links_from_file(input_file)

    if not links:
        click.echo("[!] No valid links found in input file")
        return

    click.echo(f"[*] Loaded {len(links)} links to scrape")

    # Convert to format expected by scrape_multiple
    urls_data = [{"link": link, "title": ""} for link in links]

    with yaspin(text="Scraping content via Tor...", color="cyan") as sp:
        scraped_results = scrape_multiple(urls_data, max_workers=threads)
        sp.ok("✔")

    # Count successful scrapes
    successful = sum(1 for content in scraped_results.values() if content and not content.startswith("Error"))
    click.echo(f"[*] Successfully scraped {successful}/{len(links)} links")

    # Generate output filename
    if not output:
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output = f"scraped_{now}.json"
    elif not output.endswith(".json"):
        output = output + ".json"

    # Export scraped content
    export_scraped_content(scraped_results, output)
    click.echo(f"[+] Scraped content saved to {output}")
    click.echo(f"\n[*] Next steps:")
    click.echo(f"    1. Review {output} for intelligence analysis")
    click.echo(f"    2. Use your preferred LLM to analyze the content")
    click.echo(f"    3. See prompts/query_refinement_prompt.md for prompt templates")


if __name__ == "__main__":
    swordfish()
