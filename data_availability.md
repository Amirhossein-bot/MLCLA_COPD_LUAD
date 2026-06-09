# Data Availability

The datasets analyzed in this study are publicly available from GEO and the Genomic Data Commons.

## Discovery datasets

### COPD dataset

- Dataset: GSE38974
- Repository: Gene Expression Omnibus
- miRNA platform: GPL7723
- mRNA platform: GPL4133
- Sample context: lung tissue from COPD and control samples
- Use in this study:
  - differential-expression analysis
  - COPD miRNA-mRNA association network reconstruction
  - COPD gene co-expression network reconstruction

### LUAD dataset

- Dataset: TCGA-LUAD
- Repository: Genomic Data Commons
- Data types:
  - miRNA-seq
  - mRNA RNA-seq
  - clinical survival metadata
- Use in this study:
  - differential-expression analysis
  - LUAD miRNA-mRNA association network reconstruction
  - LUAD gene co-expression network reconstruction
  - TCGA-LUAD survival-support analysis

## External validation datasets

The following independent GEO datasets were used for external validation:

- GSE32863
- GSE19804
- GSE57148
- GSE76925

## Raw data redistribution

Raw TCGA and GEO data are not redistributed in this repository due to database usage policies, file-size constraints, and reproducibility best practice. Users should download raw and processed input files directly from GEO and the Genomic Data Commons using the accession numbers listed above.

## Processed outputs

Selected processed outputs supporting the manuscript may be provided in the `results/` and `supplementary/` folders, including:

- MLCLA-Net retained community outputs
- baseline comparison workbooks
- enrichment output summaries
- external validation summaries
- survival-support analysis outputs
- figure source data

## Reproducibility note

The repository is intended to provide scripts, configuration files, example inputs, and selected processed outputs sufficient to reproduce the analytical workflow after users download the publicly available source datasets.
