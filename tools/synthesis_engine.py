"""Synthesize methodologies across multiple papers using Ollama."""

import json
import os
import sys
from pathlib import Path

import ollama

DEFAULT_MODEL = os.environ.get("SYNTH_MODEL", "glm-4.7-flash:bf16")

SYNTHESIS_PROMPT = """You are a healthcare research synthesis expert.
Given the following methodology extractions from multiple papers, produce a synthesis.

Return ONLY valid JSON with these fields:
{
  "papers_analyzed": ["list of paper titles"],
  "comparison": [
    {
      "dimension": "e.g. Study Design, Population, Method, Outcome Metric",
      "findings": {"Paper A title": "value", "Paper B title": "value"}
    }
  ],
  "what_agrees": ["common findings across all papers"],
  "what_differs": ["key differences and why they matter"],
  "gaps_found": ["what NO paper addressed"],
  "suggested_next_study": {
    "design": "recommended study type",
    "population": "who to study",
    "method": "suggested approach",
    "rationale": "why this fills the gaps"
  }
}

Paper methodologies:
"""


def synthesize(methodologies_dir: str, model: str = DEFAULT_MODEL, question: str = "") -> dict:
    """Load all methodology JSONs and synthesize across them."""
    meth_dir = Path(methodologies_dir)
    papers = {}
    for f in sorted(meth_dir.glob("*.json")):
        papers[f.stem] = json.loads(f.read_text())

    if not papers:
        print("No methodology files found.", file=sys.stderr)
        sys.exit(1)

    prompt = SYNTHESIS_PROMPT
    if question:
        prompt += f"\nResearch question: {question}\n\n"

    for name, data in papers.items():
        prompt += f"\n--- {name} ---\n{json.dumps(data, indent=2)}\n"

    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        format="json",
    )

    result = json.loads(response["message"]["content"])

    out_path = Path("output/synthesis.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2))

    return result


if __name__ == "__main__":
    meth_dir = sys.argv[1] if len(sys.argv) > 1 else "output/methodologies"
    model = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_MODEL
    result = synthesize(meth_dir, model)
    print(json.dumps(result, indent=2))
