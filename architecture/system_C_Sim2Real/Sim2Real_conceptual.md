# Sim2Real — Conceptual

## Goals and Scope
Shrink the gap between simulated and real deployments by designing training and evaluation loops that emphasize pose stability, compositional understanding, and auditability.

## Stakeholders
- Research: dataset curation, domain randomization
- QA/Operations: confidence in transfer and performance envelopes

## Assumptions
- Access to a simulator (Isaac/Unreal) with controllable domain parameters
- Real-world evaluation datasets with pose ground truth or proxies

## NFRs
- Reproducibility: seeds and configs tracked; artifacts versioned
- Comparability: standardized metrics (ADD/ADD-S, equivariance error)

## Risks
- Over-randomization reducing relevance: monitor gap metrics
- Simulator bias: incorporate real captures into evaluation

## Iterative Loop
```mermaid
%%{init: { 'theme': 'dark', 'themeVariables': { 'background':'#000', 'primaryTextColor':'#FFF', 'fontSize':'16px' }}}%%
flowchart LR
    RAND[Domain Randomization] --> TRAIN[Train]
    TRAIN --> EVAL[Evaluate]
    EVAL --> GAP[Gap Analysis]
    GAP --> RAND
```

## Domain Model (Class Diagram)
```mermaid
%%{init: { 'theme': 'dark', 'themeVariables': { 'background':'#000', 'primaryTextColor':'#FFF', 'fontSize':'16px' }}}%%
classDiagram
  class Scenario {+id: string\n+params: dict}
  class Run {+id: string\n+seed: int}
  class Metric {+name: string\n+value: float}
  class Checkpoint {+uri: string\n+hash: string}
  Scenario "1" --> "*" Run : generates
  Run "1" --> "*" Metric : logs
  Run "1" --> "*" Checkpoint : creates
```
