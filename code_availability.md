# Code Availability

The code supporting the MLCLA-Net workflow is provided in this repository.

## Repository

GitHub repository:

```text
https://github.com/YOUR_USERNAME/MLCLA-Net-COPD-LUAD
```

Replace the URL above with the final public repository URL before manuscript submission.

## Contents

The repository includes scripts for:

- COPD and LUAD preprocessing
- differential-expression analysis
- miRNA-mRNA association network reconstruction
- gene co-expression network reconstruction
- three-layer supra-network construction
- MLCLA-Net community detection
- convergence analysis
- baseline community-detection comparison
- functional enrichment analysis
- external validation
- TCGA-LUAD survival-support analysis
- figure generation

## Software environment

The Python environment can be recreated using either:

```bash
pip install -r requirements.txt
```

or:

```bash
conda env create -f environment.yml
conda activate mlcla-net
```

## Versioning

Before manuscript submission, create a stable repository release, for example `v1.0.0`.

For archival reproducibility, the release may also be deposited in Zenodo to obtain a DOI.

## Notes

Raw TCGA and GEO data are not redistributed in this repository. See `data_availability.md` for dataset access information.

Some scripts may require local file paths to be updated in configuration files before execution.
