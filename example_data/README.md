# Example Data

This folder contains small toy files that demonstrate the expected input format for the MLCLA-Net workflow.

These files are synthetic examples only. They are not the real COPD, LUAD, TCGA, or GEO data used in the manuscript.

## Files

- `toy_expression_miRNA.csv`: toy miRNA expression matrix
- `toy_expression_mRNA.csv`: toy mRNA-derived gene expression matrix
- `toy_metadata.csv`: sample metadata with case/control labels
- `toy_supra_edges.csv`: toy three-layer supra-network edge list

## Format notes

Expression matrices use:

- first column = feature identifier
- remaining columns = sample identifiers

The toy supra-network uses:

- `source`
- `target`
- `weight`
- `layer`
- `edge_type`

Layer-specific node labels follow the pattern:

```text
LayerPrefix::BaseIdentifier
```

Example:

```text
COPD_gene::TP53
miRNA_cross::hsa-miR-34a
LUAD_gene::TP53
```

For real analysis, download the public datasets described in `data_availability.md` and configure local paths in `config/config.yaml`.
