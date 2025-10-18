# Sim2Real — Implementable (RM-ODP)

## Technical Stack
- Simulation: Isaac Sim or Unreal-based pipelines.
- Training: PyTorch DDP, mixed precision.
- Storage: S3-compatible; metadata DB for runs.

## Config Samples
```yaml
training:
  batch_size: 64
  lr: 3e-4
  epochs: 50
sim:
  domain_randomization: true
  params: [lighting, texture, pose, occlusion]
```

## Deployment Notes
- Use containerized sim workers on GPU nodes.
- Track provenance for synthetic assets and seeds.
- Automate regression against real eval suites.

## Deployment Diagram
```mermaid
%%{init: { 'theme': 'dark', 'themeVariables': { 'background':'#000', 'primaryTextColor':'#FFF', 'textColor':'#FFF', 'fontSize':'14px' }}}%%
flowchart LR
    subgraph Cloud[Cloud]
      Sim[Sim Workers]
      Train[Trainer]
      Eval[Evaluator]
      Sim --> Train
      Train --> Eval
    end
    Store[(S3 + Metadata DB)]
    Train --> Store
    Eval --> Store
```
