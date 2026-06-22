# Statistical Analysis

## Committed Metrics Used in This Release

- Experiment 1 trajectory kappa: `1.000`
- Experiment 1 snapshot kappa: `0.464`
- Experiment 2 trajectory kappa: `0.900`
- Experiment 2 snapshot kappa: `0.444`
- second-model robustness kappa: `0.900`
- baseline ladder kappas: `0.444`, `0.231`, `0.700`, `0.900`

## Interpretation

The release emphasis is comparative rather than universal. In both experiments, full-trajectory evaluation is stronger than final-step-only evaluation using the committed metrics. Experiment 2 adds a second-model robustness check and a baseline ladder showing that broader context improves performance in this synthetic setting.

## Caution

These numbers are derived from synthetic, author-generated benchmark data. They should not be treated as field-validation estimates.
