"""Extract structured methodology from a healthcare research PDF using Ollama."""

import json
import os
import sys
from pathlib import Path

import ollama

from tools.pdf_reader import read_pdf

DEFAULT_MODEL = os.environ.get("SYNTH_MODEL", "glm-4.7-flash:bf16")

EXTRACTION_PROMPT = """You are a healthcare research methodology extractor.
Read the following text from a clinical research paper and extract the methodology.

Return ONLY valid JSON with these fields:
{
  "title": "paper title",
  "study_type": "e.g. retrospective cohort, RCT, meta-analysis",
  "population": "who was studied, sample size, data source",
  "method": "primary analytical method or intervention",
  "comparison": "what baselines or comparators were used",
  "primary_outcome": "main result with metric and value",
  "validation": "how results were validated",
  "strengths": ["list of strengths"],
  "limitations": ["list of limitations"],
  "gaps": ["what this study did NOT address"]
}

If a field is not found in the text, use "not reported".

Paper text:
"""


def extract_methodology(pdf_path: str, model: str = DEFAULT_MODEL) -> dict:
    """Read a PDF and extract its methodology via Ollama."""
    chunks = read_pdf(pdf_path)
    full_text = "\n\n".join(c["text"] for c in chunks)

    # Trim to fit context window (~6000 chars keeps it safe for 8k models)
    if len(full_text) > 6000:
        full_text = full_text[:6000]

    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": EXTRACTION_PROMPT + full_text}],
        format="json",
    )

    result = json.loads(response["message"]["content"])

    # Save to output directory
    out_dir = Path("output/methodologies")
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = Path(pdf_path).stem
    out_path = out_dir / f"{stem}.json"
    out_path.write_text(json.dumps(result, indent=2))

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tools/methodology_extractor.py <pdf>", file=sys.stderr)
        sys.exit(1)

    model = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_MODEL
    result = extract_methodology(sys.argv[1], model)
    print(json.dumps(result, indent=2))
