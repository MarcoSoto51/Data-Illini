#!/usr/bin/env bash
# =============================================================================
# run_all.sh — FARS 2023 Fatal Crash Analysis
# Executes the complete end-to-end pipeline from raw data to results.
# Usage:  bash run_all.sh
# =============================================================================

set -euo pipefail   # exit on error, undefined variable, or pipe failure


GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
info()    { echo -e "${GREEN}[INFO]${NC}  $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error()   { echo -e "${RED}[ERROR]${NC} $*" >&2; exit 1; }


info "Checking prerequisites..."

command -v python  >/dev/null 2>&1 || error "Python not found. Install Python 3.9+."
command -v snakemake >/dev/null 2>&1 || \
    warn "Snakemake not found — falling back to direct script execution."
HAVE_SNAKEMAKE=$(command -v snakemake >/dev/null 2>&1 && echo "yes" || echo "no")


info "Installing Python dependencies from requirements.txt..."
pip install -q -r requirements.txt


info "Creating output directories..."
mkdir -p data/processed
mkdir -p results/figures
mkdir -p results/tables
mkdir -p logs


info "Verifying raw data files..."
for f in \
    "data/raw/FARS2023NationalCSV/ACC_AUX.CSV" \
    "data/raw/FARS2023NationalCSV/PER_AUX.CSV" \
    "data/raw/FARS2023NationalCSV/VEH_AUX.CSV"
do
    [ -f "$f" ] || error "Required raw data file not found: $f"
done
info "All raw data files present."


if [ "$HAVE_SNAKEMAKE" = "yes" ]; then
    info "Running pipeline with Snakemake..."
    snakemake --cores 1 --rerun-incomplete
else
    warn "Running pipeline with direct Python invocation (no Snakemake)."

    info "Step 1/2 — Data integration and cleaning..."
    python scripts/integrate.py 2>&1 | tee logs/integrate.log

    info "Step 2/2 — Analysis and visualisation..."
    python scripts/DataAnalysis_Visualization.py \
        --data data/processed/fars_integrated_crash_level.csv \
        2>&1 | tee logs/analyze.log
fi


info "Pipeline complete. Outputs:"
echo ""
echo "  Processed data  →  data/processed/"
echo "  Figures         →  results/figures/"
echo "  Tables          →  results/tables/"
echo "  Logs            →  logs/"
echo ""
info "To inspect the workflow DAG (requires Snakemake + Graphviz):"
echo "  snakemake --dag | dot -Tpng -o dag.png"
