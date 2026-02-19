#!/usr/bin/env bash
# Download open-access healthcare research PDFs for the demo.
# These are freely available from PubMed Central (PMC).
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
echo "Downloading sample papers to $DIR ..."

# 1. "Machine Learning for the Prediction of Sepsis: A Systematic Review"
#    Fleuren et al., 2020 - Critical Care
curl -sL "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7045910/pdf/13054_2020_Article_2749.pdf" \
  -o "$DIR/sepsis_ml_systematic_review.pdf"
echo "  [1/3] sepsis_ml_systematic_review.pdf"

# 2. "Development and Validation of a Machine Learning Model for Early Sepsis Prediction"
#    Barton et al., 2019 - International Journal of Medical Informatics
curl -sL "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6857506/pdf/main.pdf" \
  -o "$DIR/sepsis_early_prediction_model.pdf"
echo "  [2/3] sepsis_early_prediction_model.pdf"

# 3. "Artificial Intelligence and Machine Learning in Clinical Development"
#    Harrer et al., 2019 - Translational Medicine Communications
curl -sL "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7325854/pdf/41231_2019_Article_25.pdf" \
  -o "$DIR/ai_ml_clinical_development.pdf"
echo "  [3/3] ai_ml_clinical_development.pdf"

echo ""
echo "Done! 3 papers downloaded. Run:"
echo "  python synthesize.py papers/"
