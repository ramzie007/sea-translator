from helpers import (
    download_text,
    chunk_text_sentences,
    build_translate_prompt,
    translate_chunk,
)
from dotenv import load_dotenv
import os
import typer
from rich.console import Console
from rich.progress import Progress
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI

console = Console()

# -------------------------
# Defaults
# -------------------------
GUTENBERG_URL = "https://www.gutenberg.org/cache/epub/16317/pg16317.txt"
EXAMPLE_URL = "https://example-files.online-convert.com/document/txt/example.txt"
DEFAULT_MODEL = "aisingapore/Gemma-SEA-LION-v4-27B-IT"
DEFAULT_CHUNK_CHAR = 3500
API_BASE_URL = "https://api.sea-lion.ai/v1"
DEFAULT_FILE_NAME = "translated.txt"
SUPPORTED_LANGS = ["indonesian", "filipino", "tamil", "thai", "vietnamese"]
SUPPORTED_MODELS = [
    "aisingapore/Gemma-SEA-LION-v4-27B-IT",
    "aisingapore/Llama-SEA-LION-v3-70B-IT",
]

def main(
    target_language: str = typer.Option(
        ...,
    help=f'Target SEA language for translation. Options: {", ".join(SUPPORTED_LANGS)}',
    ),
    input: str = typer.Option(GUTENBERG_URL, help="Input text file URL"),
    output: str = typer.Option(DEFAULT_FILE_NAME, help="Output file path"),
    model: str = typer.Option(
        DEFAULT_MODEL,
        help=f'SEA-LION model name. Options: {", ".join(SUPPORTED_MODELS)}',
    ),
    chunk_chars: int = typer.Option(
        DEFAULT_CHUNK_CHAR, help="Max characters per chunk"
    ),
    bilingual: bool = typer.Option(
        False, help="Output English + translation side by side"
    ),
):
    """
    CLI command to translate Project Gutenberg book to a Southeast Asian language using SEA-LION API.
    """

    load_dotenv()
    lang = target_language.strip().lower()
    if lang not in SUPPORTED_LANGS:
        console.print(f"[bold red]Unsupported target language:[/bold red] {lang}")
        raise typer.Exit(code=1)
    model = model.strip()
    if model not in SUPPORTED_MODELS:
        console.print(f"[bold red]Unsupported model:[/bold red] {model}")
        raise typer.Exit(code=1)

    api_key = os.environ.get("SEA_LION_API_KEY")
    if not api_key:
        console.print(
            "[bold red]Set SEA_LION_API_KEY environment variable first[/bold red]"
        )
        raise typer.Exit(code=1)

    client = OpenAI(api_key=api_key, base_url=API_BASE_URL)

    console.print(f"[bold green]Downloading book from {input}...[/bold green]")
    raw_text = download_text(input)

    chunks = chunk_text_sentences(raw_text, chunk_chars)

    out_path = output
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"Translated from {input}\nLanguage: {lang}\nModel: {model}\n\n")

    def translate_one(idx_chunk):
        """Translate a single chunk and return its index, original, and translation."""
        i, chunk = idx_chunk
        messages = build_translate_prompt(chunk, lang)
        translated = translate_chunk(client, model, messages)
        return i, chunk, translated.strip()

    results = {}
    max_workers = min(8, len(chunks))
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(translate_one, (i, chunk)): i
            for i, chunk in enumerate(chunks)
        }
        with Progress() as progress:
            task = progress.add_task("Translating", total=len(futures))
            for fut in as_completed(futures):
                i, chunk, translated = fut.result()
                results[i] = (chunk, translated)
                progress.update(task, advance=1)

    # Write results in order
    for i in range(len(chunks)):
        chunk, translated = results.get(i, ("", ""))
        with open(out_path, "a", encoding="utf-8") as f:
            # f.write(f"\n\n<!-- chunk {i+1}/{len(chunks)} -->\n\n")
            if bilingual:
                f.write("### English ###\n")
                f.write(chunk.strip() + "\n\n")
                f.write("### Translation ###\n")
            f.write(translated + "\n")

    console.print(f"[bold green]Done. Output:[/bold green] {out_path}")


app = typer.Typer()
app.command()(main)

if __name__ == "__main__":
    app()
