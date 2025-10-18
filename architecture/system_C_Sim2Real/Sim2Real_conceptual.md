# Sim2Real — Conceptual (RM-ODP)

## Enterprise Viewpoint
- Goal: Reduce deployment risk by validating models against realistic variations.
- Stakeholders: Research, QA, Operations.

## Information Viewpoint
- Entities: Scenario, DomainParams, Model, Metric, GapReport.

## Computational Viewpoint (conceptual)
- Services: Synthetic Data Gen, Training, Evaluation, Adaptation.
- Interactions: Iterative loop to shrink sim-to-real gap.

## Iterative Loop
```mermaid
%%{init: { 'theme': 'dark', 'themeVariables': { 'background':'#000', 'primaryTextColor':'#FFF', 'textColor':'#FFF', 'fontSize':'14px' }}}%%
flowchart LR
    RAND[Domain Randomization] --> TRAIN[Train]
    TRAIN --> EVAL[Evaluate]
    EVAL --> GAP[Gap Analysis]
    GAP -->|tune| RAND
```
