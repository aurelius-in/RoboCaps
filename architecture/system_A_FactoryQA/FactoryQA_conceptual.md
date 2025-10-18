# Factory QA — Conceptual (RM-ODP)

## Enterprise Viewpoint
- Goal: Zero-defect throughput with explainable perception and auditability.
- Actors: Operator, QA Engineer, Line Controller, Data Steward.
- Policies: Traceability, latency SLAs, safety interlocks.

## Information Viewpoint
- Core entities: Part, Feature, Pose, Defect, InspectionRun, Artifact.
- Invariants: Each InspectionRun binds a Part to a Pose set and decision.

## Computational Viewpoint (conceptual)
- Services: Capture, Preprocess, Perception, Decisioning, Audit.
- Interactions: Event-driven; edge-local decision with cloud sync.

## Context Diagram
```mermaid
%%{init: { 'theme': 'dark', 'themeVariables': { 'background':'#000', 'primaryTextColor':'#FFF', 'textColor':'#FFF', 'fontSize':'14px' }}}%%
flowchart LR
    Operator((Operator)) -->|Start/Stop| Capture[Capture]
    PLC((PLC)) -->|Triggers| Capture
    Capture --> Pre[Preprocess]
    Pre --> Perception[Perception (RoboCaps)]
    Perception --> Decision[Decisioning]
    Decision --> Audit[(Audit Store)]
    Decision --> Bus[(Events)]
```
