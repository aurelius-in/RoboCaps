# Global Architecture Overview

RoboCaps spans edge perception, cloud training/evaluation, and enterprise integration. This overview summarizes cross-system patterns, interfaces, and governance.

## C4 Context
```mermaid
%%{init: { 'theme': 'dark', 'themeVariables': { 'background':'#000', 'primaryTextColor':'#FFF', 'textColor':'#FFF', 'fontSize':'14px' }}}%%
flowchart LR
    E[Edge Robots\nCameras + Jetson/RTX] -- MQTT/ROS2 --> G[Edge Gateway\nQoS, buffering]
    G -- gRPC/HTTPs --> A[Perception API\nFastAPI + TensorRT]
    A -- events --> B[Event Bus\nKafka/Redpanda]
    B -- features --> T[Training Pipeline\nPyTorch + S3]
    T -- models --> R[Registry\nModel/Config/Artifacts]
    R -- deploy --> A
    A -- insights --> BI[Enterprise Apps\nMES/ERP/QMS]
```

## Cross-Cutting Concerns
- Observability: metrics (Prometheus), traces (OTLP), logs (JSON).
- Security: mTLS, JWT/OIDC, least-privilege IAM, SBOMs, image scanning.
- Data: S3-compatible object store, data retention, PII redaction.
- Model lifecycle: versioning (semver+git sha), canary, rollback, A/B.

## Governance
- Change management: RFCs, risk gates, model cards, datasheets.
- Compliance: ISO 26262 (as applicable), IEC 62443, SOC2-friendly controls.
