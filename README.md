# MLCLA-Net: A Multilayer Framework for COPD-LUAD Regulatory Module Discovery

This repository contains reproducibility material for the manuscript:

**MLCLA-Net: A Multilayer Systems-Biology Framework for Identifying Shared Regulatory Communities Between COPD and Lung Adenocarcinoma**

##

## Overview

MLCLA-Net is a multilayer transcriptomic framework for identifying shared regulatory communities between chronic obstructive pulmonary disease (COPD) and lung adenocarcinoma (LUAD). The workflow integrates:

- COPD miRNA-mRNA association networks
- COPD gene co-expression networks reconstructed from mRNA expression profiles
- LUAD miRNA-mRNA association networks
- LUAD gene co-expression networks reconstructed from mRNA expression profiles
- Three-layer supra-network construction
- Multilayer Cellular Learning Automata (MLCLA)-based community detection
- Baseline community-detection benchmarking
- Functional enrichment analysis
- External validation using independent GEO datasets
- TCGA-LUAD survival-support analysis
- Figure and supplementary table generation

## Repository structure

```text
MLCLA-Net-COPD-LUAD/
├── README.md
├── LICENSE
├── requirements.txt
├── environment.yml
├── data_availability.md
├── code_availability.md
├── citation.cff
├── config/
├── scripts/
├── example_data/
├── results/
└── supplementary/
```

Analysis workflow:

```text
scripts/
├── 01_preprocessing/
├── 02_differential_expression/
├── 03_network_reconstruction/
├── 04_mlcla_net/
├── 05_baseline_comparison/
├── 06_enrichment/
├── 07_external_validation/
├── 08_survival/
└── 09_figures/
```

## Main datasets

### Discovery datasets

- COPD: GEO accession **GSE38974**
  - miRNA platform: GPL7723
  - mRNA platform: GPL4133
- LUAD: **TCGA-LUAD**
  - miRNA-seq
  - mRNA RNA-seq
  - Clinical survival metadata from the Genomic Data Commons

### External validation datasets

- LUAD tumor versus normal: GSE32863 and GSE19804
- COPD versus control: GSE57148 and GSE76925

Raw TCGA and GEO data are not redistributed in this repository. See `data_availability.md`.

## Main MLCLA-Net parameters

```yaml
mlcla:
  interlayer_lambda: 0.1
  max_iterations: 1000
  best_iteration: 282
  reward_rate: 0.25
  penalty_rate: 0.05
  early_stopping_patience: 40
  random_seed: 42
```

The final three-layer supra-network contained:

- Node-layer objects: **24,150**
- Edges: **209,503**
- Nodes per layer: **8,050**
- Retained MLCLA communities: **5**
- Unique shared identifiers: **228**
- Final objective score: **0.8935**
- Average intralayer modularity: **0.3516**
- Interlayer alignment: **0.4264**

## Installation

### pip

```bash
git clone https://github.com/YOUR_USERNAME/MLCLA-Net-COPD-LUAD.git
cd MLCLA-Net-COPD-LUAD
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

### conda

```bash
git clone https://github.com/YOUR_USERNAME/MLCLA-Net-COPD-LUAD.git
cd MLCLA-Net-COPD-LUAD
conda env create -f environment.yml
conda activate mlcla-net
```

## Reproducing the workflow

Run scripts in numerical order after downloading the required datasets from GEO and GDC:

```bash
python scripts/01_preprocessing/preprocess_COPD_miRNA.py
python scripts/01_preprocessing/preprocess_COPD_mRNA.py
python scripts/01_preprocessing/preprocess_LUAD_miRNA.py
python scripts/01_preprocessing/preprocess_LUAD_mRNA.py
python scripts/02_differential_expression/differential_expression_COPD.py
python scripts/02_differential_expression/differential_expression_LUAD.py
python scripts/03_network_reconstruction/build_COPD_miRNA_mRNA_network.py
python scripts/03_network_reconstruction/build_COPD_gene_coexpression_network.py
python scripts/03_network_reconstruction/build_LUAD_miRNA_mRNA_network.py
python scripts/03_network_reconstruction/build_LUAD_gene_coexpression_network.py
python scripts/04_mlcla_net/build_supra_network.py
python scripts/04_mlcla_net/run_mlcla.py
python scripts/04_mlcla_net/extract_retained_communities.py
python scripts/04_mlcla_net/convergence_analysis.py
python scripts/05_baseline_comparison/compare_methods.py
python scripts/06_enrichment/run_enrichment_mlcla.py
python scripts/07_external_validation/validate_candidates.py
python scripts/08_survival/run_mrna_survival.py
python scripts/08_survival/run_mirna_survival.py
python scripts/09_figures/generate_all_figures.py
```

## Output structure

```text
results/
├── selected_mlcla_outputs/
├── baseline_comparison/
├── enrichment/
├── external_validation/
├── survival/
└── figures/
```

## Reproducibility notes

- Random seed: **42**
- Community retention criterion: all three layers and at least five shared identifiers
- Gene co-expression threshold: absolute Spearman correlation >= 0.6
- LUAD miRNA-mRNA association threshold: absolute Spearman correlation >= 0.4 and FDR <= 0.1
- Survival stratification: median expression
- Multiple-testing correction: Benjamini-Hochberg FDR

## Data and code availability

See `data_availability.md` and `code_availability.md`.

## License

This repository is released under the MIT License. See `LICENSE`.
