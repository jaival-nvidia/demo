"""
Methodology Synthesis CLI
Drop healthcare PDFs into papers/, run this script, get a structured report.

Usage:
    python synthesize.py papers/
    python synthesize.py papers/ --question "Best ML approach for early sepsis detection?"
    python synthesize.py papers/ --model mistral
"""

import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

from tools.pdf_reader import read_pdf
from tools.methodology_extractor import extract_methodology
from tools.synthesis_engine import synthesize
from tools.report_writer import render_report

app = typer.Typer(add_completion=False)
console = Console()


@app.command()
def main(
    papers_dir: str = typer.Argument("papers", help="Directory containing PDF files"),
    question: str = typer.Option("", "--question", "-q", help="Research question to guide the synthesis"),
    model: str = typer.Option("glm-4.7-flash:bf16", "--model", "-m", help="Ollama model to use"),
    output: str = typer.Option("output/synthesis_report.md", "--output", "-o", help="Output report path"),
):
    """Synthesize methodologies from healthcare research PDFs."""
    import os
    os.environ["SYNTH_MODEL"] = model

    pdfs = list(Path(papers_dir).glob("*.pdf"))
    if not pdfs:
        console.print(f"[red]No PDFs found in {papers_dir}/[/red]")
        raise typer.Exit(1)

    console.print(Panel(f"[bold]Methodology Synthesis[/bold]\n"
                        f"Papers: {len(pdfs)} | Model: {model}", title="Starting"))

    # Step 1: Extract methodology from each paper
    for pdf in pdfs:
        console.print(f"\n[bold cyan]Extracting:[/bold cyan] {pdf.name}")
        with console.status("Reading PDF and calling Ollama..."):
            result = extract_methodology(str(pdf), model)
        title = result.get("title", pdf.stem)
        console.print(f"  [green]Done:[/green] {title}")

    # Step 2: Synthesize across all papers
    console.print(f"\n[bold cyan]Synthesizing[/bold cyan] across {len(pdfs)} papers...")
    with console.status("Running cross-paper analysis..."):
        synth = synthesize("output/methodologies", model, question)
    console.print("  [green]Synthesis complete[/green]")

    # Step 3: Generate report
    console.print(f"\n[bold cyan]Writing report...[/bold cyan]")
    report = render_report("output/synthesis.json")
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    Path(output).write_text(report)
    console.print(f"  [green]Report saved to {output}[/green]")

    # Summary
    gaps = synth.get("gaps_found", [])
    console.print(Panel(
        f"[bold green]Done![/bold green]\n\n"
        f"Papers analyzed: {len(pdfs)}\n"
        f"Evidence gaps found: {len(gaps)}\n"
        f"Report: {output}",
        title="Synthesis Complete"
    ))


if __name__ == "__main__":
    app()
