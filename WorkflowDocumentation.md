# Workflow Automation and Provenance

## Overview

This project uses [Snakemake](https://snakemake.readthedocs.io/) to automate the complete end-to-end analysis pipeline - from raw FARS data files through integration, cleaning, and statistical analysis to final figures and model outputs. A convenience shell script (`run_all.sh`) is also provided for environments where Snakemake is unavailable.

---

## Pipeline Structure

The workflow consists of two sequential rules:

```
data/raw/FARS2023NationalCSV/
  ACC_AUX.CSV
  PER_AUX.CSV       -> [Rule: integrate] -> data/processed/
  VEH_AUX.CSV                                      ├── acc_aux_cleaned.csv
                                                    ├── per_aux_cleaned.csv
                                                    ├── veh_aux_cleaned.csv
                                                    ├── per_summary_by_st_case.csv
                                                    ├── veh_summary_by_st_case.csv
                                                    └── fars_integrated_crash_level.csv
                                                              │
                                                              v
                                                    [Rule: analyze]
                                                              │
                                                    results/figures/   (10 plots)
                                                    results/tables/
                                                      ├── summary_statistics.csv
                                                      └── logistic_regression_report.txt
```

### Rule 1 — `integrate`

| Property | Detail |
|---|---|
| **Script** | `scripts/integrate.py` |
| **Inputs** | `data/raw/FARS2023NationalCSV/ACC_AUX.CSV`, `PER_AUX.CSV`, `VEH_AUX.CSV` |
| **Outputs** | 6 CSVs in `data/processed/` (see above) |
| **Log** | `logs/integrate.log` |
| **Purpose** | Merges the three FARS auxiliary tables, applies quality assessment and cleaning operations, produces person- and vehicle-level summaries, and writes the crash-level integrated dataset used by all downstream analysis. |

### Rule 2 — `analyze`

| Property | Detail |
|---|---|
| **Script** | `scripts/DataAnalysis_Visualization.py` |
| **Inputs** | `data/processed/fars_integrated_crash_level.csv` |
| **Outputs** | 10 PNG figures in `results/figures/`, summary statistics CSV, and logistic regression report in `results/tables/` |
| **Log** | `logs/analyze.log` |
| **Purpose** | Produces all descriptive statistics, visualisations (geographic, temporal, impairment, road-type, demographic patterns), a Random Forest feature-importance analysis, and a Logistic Regression model for predicting multi-fatality crashes. |

---

## How to Run

### Option A — Snakemake (recommended)

Snakemake tracks file dependencies and only re-runs rules whose inputs have changed since the last execution.

```bash
# Install dependencies
pip install -r requirements.txt

# Run the full pipeline (single core)
snakemake --cores 1

# Re-run everything from scratch
snakemake --cores 1 --forceall

# Preview what would run without executing
snakemake --dry-run

# Remove all generated outputs
snakemake clean
```

### Option B — `run_all.sh`

The convenience script runs the same steps without requiring Snakemake. It will use Snakemake automatically if it is installed, and fall back to direct Python invocation otherwise.

```bash
bash run_all.sh
```

---

## Workflow DAG

To visualise the directed acyclic graph (DAG) of the workflow (requires Snakemake and Graphviz):

```bash
snakemake --dag | dot -Tpng -o dag.png
```

The DAG confirms that `analyze` cannot begin until `integrate` has written `fars_integrated_crash_level.csv`, enforcing correct execution order and preventing use of stale intermediate files.

---

## Provenance

All workflow steps produce log files under `logs/` capturing stdout and stderr. These logs record:

- Timestamp of execution (via shell environment)
- Any warnings or errors raised during processing
- Counts and diagnostics printed by each script

Together, the Snakemake rule graph, the commit history, and the log files constitute a complete provenance record linking each output file back to its inputs, the code that produced it, and the person who committed that code.

| Artifact type | Location |
|---|---|
| Raw data | `data/raw/` |
| Processed / integrated data | `data/processed/` |
| Analysis results & figures | `results/` |
| Workflow definition | `Snakefile` |
| Convenience runner | `run_all.sh` |
| Execution logs | `logs/` |
| Software dependencies | `requirements.txt` |

---

## Software Dependencies

All Python package dependencies are listed in `requirements.txt`. To install:

```bash
pip install -r requirements.txt
```

The exact versions used during development are recorded in `requirements_freeze.txt` (generated via `pip freeze > requirements_freeze.txt`). Snakemake itself can be installed with:

```bash
pip install snakemake
```

Tested with Python 3.10+.
