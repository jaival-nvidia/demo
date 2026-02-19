"""Render a synthesis JSON into a polished Markdown report."""

import json
import sys
from datetime import datetime
from pathlib import Path


def render_report(synthesis_path: str, methodologies_dir: str = "output/methodologies") -> str:
    """Turn synthesis.json + per-paper JSONs into a Markdown report."""
    synth = json.loads(Path(synthesis_path).read_text())

    # Load individual paper methodologies for the summary section
    papers = {}
    meth_dir = Path(methodologies_dir)
    if meth_dir.exists():
        for f in sorted(meth_dir.glob("*.json")):
            papers[f.stem] = json.loads(f.read_text())

    lines = []
    lines.append("# Methodology Synthesis Report")
    lines.append(f"\n*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")

    # --- Overview ---
    analyzed = synth.get("papers_analyzed", list(papers.keys()))
    lines.append("## Overview\n")
    lines.append(f"**Papers analyzed:** {len(analyzed)}\n")
    for title in analyzed:
        lines.append(f"- {title}")
    lines.append("")

    # --- Individual Paper Summaries ---
    if papers:
        lines.append("## Paper Summaries\n")
        for name, data in papers.items():
            lines.append(f"### {data.get('title', name)}\n")
            lines.append(f"| Field | Detail |")
            lines.append(f"|-------|--------|")
            for field in ["study_type", "population", "method", "comparison", "primary_outcome", "validation"]:
                val = data.get(field, "not reported")
                lines.append(f"| **{field.replace('_', ' ').title()}** | {val} |")
            lines.append("")
            if data.get("strengths"):
                lines.append("**Strengths:** " + ", ".join(data["strengths"]))
            if data.get("limitations"):
                lines.append("**Limitations:** " + ", ".join(data["limitations"]))
            lines.append("")

    # --- Comparison ---
    comparisons = synth.get("comparison", [])
    if comparisons:
        lines.append("## Cross-Study Comparison\n")
        for comp in comparisons:
            lines.append(f"### {comp.get('dimension', 'Dimension')}\n")
            findings = comp.get("findings", {})
            for paper, val in findings.items():
                lines.append(f"- **{paper}:** {val}")
            lines.append("")

    # --- Agreement ---
    agrees = synth.get("what_agrees", [])
    if agrees:
        lines.append("## What Agrees Across Studies\n")
        for item in agrees:
            lines.append(f"- {item}")
        lines.append("")

    # --- Differences ---
    differs = synth.get("what_differs", [])
    if differs:
        lines.append("## What Differs\n")
        for item in differs:
            lines.append(f"- {item}")
        lines.append("")

    # --- Gaps ---
    gaps = synth.get("gaps_found", [])
    if gaps:
        lines.append("## Evidence Gaps\n")
        for item in gaps:
            lines.append(f"- {item}")
        lines.append("")

    # --- Suggested Next Study ---
    suggestion = synth.get("suggested_next_study", {})
    if suggestion:
        lines.append("## Recommended Next Study\n")
        for key, val in suggestion.items():
            lines.append(f"- **{key.replace('_', ' ').title()}:** {val}")
        lines.append("")

    report = "\n".join(lines)

    out_path = Path("output/synthesis_report.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report)

    return report


if __name__ == "__main__":
    synth_path = sys.argv[1] if len(sys.argv) > 1 else "output/synthesis.json"
    report = render_report(synth_path)
    print(report)
