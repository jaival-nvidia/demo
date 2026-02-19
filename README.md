# Methodology Synthesis

**Synthesize healthcare research methodologies from PDFs in minutes, not months.**

Healthcare systematic reviews take 6-18 months. Even a quick literature comparison means weeks of reading, manual extraction, and spreadsheet wrangling. This tool automates the hard parts: drop your PDFs, run one command, get a structured methodology comparison with evidence gaps and next-study recommendations.

Runs 100% locally with Ollama. No cloud APIs, no data leaves your machine.

---

## How It Works

```
papers/*.pdf                          You drop research PDFs here
       |
       v
 pdf_reader.py                        Extracts text, splits into chunks
       |
       v
 methodology_extractor.py             Ollama extracts structured methodology per paper
       |
       v
 synthesis_engine.py                  Ollama cross-compares all papers
       |
       v
 report_writer.py                     Renders a clean Markdown report
       |
       v
output/synthesis_report.md            Your finished synthesis
```

Each step is a standalone script. Run them individually, chain them in Claude Code, or use the all-in-one CLI.

---

## Quick Start

```bash
# 1. Clone and install
git clone https://github.com/jaival-nvidia/demo.git
cd demo
pip install -r requirements.txt

# 2. Make sure Ollama is running with a model
ollama pull glm-4.7-flash:bf16

# 3. Download sample papers (or drop your own PDFs into papers/)
bash papers/download_samples.sh

# 4. Run
python synthesize.py papers/
```

Your report will be at `output/synthesis_report.md`.

### Options

```bash
# Ask a specific research question
python synthesize.py papers/ --question "Best ML approach for early sepsis detection?"

# Use a different model (default is glm-4.7-flash:bf16)
python synthesize.py papers/ --model mistral

# Custom output location
python synthesize.py papers/ --output my_report.md
```

---

## Using with Claude Code

Claude Code can orchestrate the tools directly. Just tell it:

> "Synthesize the methodologies from the papers in the papers folder"

Claude Code will call each script in sequence:

```
python tools/pdf_reader.py papers/paper1.pdf
python tools/methodology_extractor.py papers/paper1.pdf
python tools/methodology_extractor.py papers/paper2.pdf
python tools/synthesis_engine.py output/methodologies/
python tools/report_writer.py output/synthesis.json
```

Each tool reads from files and writes to `output/`, so Claude Code can inspect intermediate results and adapt.

---

## What Gets Extracted

For each paper, the tool extracts a flat, structured JSON:

```json
{
  "title": "Machine Learning for Early Prediction of Sepsis",
  "study_type": "retrospective cohort",
  "population": "42,808 ED visits, adults >= 18",
  "method": "XGBoost on vitals + labs",
  "comparison": "SOFA, qSOFA, SIRS",
  "primary_outcome": "AUROC 0.87 at 4-hour prediction window",
  "validation": "temporal split + external site",
  "strengths": ["large cohort", "multi-site", "temporal validation"],
  "limitations": ["retrospective", "no deployment study"],
  "gaps": ["no pediatric data", "no fairness analysis"]
}
```

---

## Example Output

See the full pre-generated example: **[example_output/synthesis_report.md](example_output/synthesis_report.md)**

Here's a preview of what the final report looks like (synthesizing 3 sepsis detection papers):

### Evidence Gaps Found

- No study tested on pediatric populations
- No study evaluated fairness across racial/ethnic demographic groups
- No RCT comparing ML-augmented care vs standard care on patient outcomes
- No study addressed model drift over time
- Cost-effectiveness of ML deployment was not analyzed

### Recommended Next Study

- **Design:** Pragmatic cluster-randomized trial
- **Population:** Mixed adult ED/ICU patients across academic and community hospitals
- **Method:** Lightweight gradient-boosted model integrated into EHR, randomized vs standard qSOFA
- **Rationale:** Fills the three biggest gaps -- no RCT evidence, no fairness analysis, no community hospital data

---

## Project Structure

```
methodology-synthesis/
├── README.md                          # This file
├── requirements.txt                   # pymupdf, ollama, rich, typer
├── .gitignore
├── synthesize.py                      # All-in-one CLI entry point
├── tools/
│   ├── pdf_reader.py                  # PDF -> text chunks
│   ├── methodology_extractor.py       # Text -> structured methodology (Ollama)
│   ├── synthesis_engine.py            # N methodologies -> synthesis (Ollama)
│   └── report_writer.py              # Synthesis JSON -> Markdown report
├── papers/                            # Drop your PDFs here
├── output/                            # Generated files appear here
└── example_output/
    └── synthesis_report.md            # Pre-generated example
```

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com) running locally
- Any Ollama model (default: `glm-4.7-flash:bf16`)

## Model Recommendations

| Model | Speed | Quality | Notes |
|-------|-------|---------|-------|
| `glm-4.7-flash:bf16` | Fast | Very Good | Default, strong structured extraction |
| `llama3.1:8b` | Fast | Good | Lightweight alternative |
| `mistral` | Fast | Good | Solid general-purpose option |
| `qwen2.5:14b` | Medium | Very Good | Good balance of speed and quality |

Set with `--model` flag or `SYNTH_MODEL` environment variable.

---

## License

MIT
