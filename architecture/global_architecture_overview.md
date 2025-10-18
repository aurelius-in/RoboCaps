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

## Data Lifecycle
```mermaid
%%{init: { 'theme': 'dark', 'themeVariables': { 'background':'#000', 'primaryTextColor':'#FFF', 'textColor':'#FFF', 'fontSize':'14px' }}}%%
sequenceDiagram
    autonumber
    participant Edge as Edge Inference
    participant API as API
    participant Bus as Event Bus
    participant Lake as Data Lake (S3)
    participant Train as Trainer
    participant Reg as Model Registry
    Edge->>API: Inference + metadata
    API->>Bus: Events
    API->>Lake: Artifacts (images/overlays)
    Train->>Reg: Register model
    Reg->>API: Deploy new model
```

## C4 Container View
The platform comprises edge nodes, an ingress/API layer, an event backbone, a data lake, a training pipeline, and a model registry that feeds deployments.

```mermaid
%%{init: { 'theme': 'dark', 'themeVariables': { 'background':'#000', 'primaryTextColor':'#FFF', 'textColor':'#FFF', 'fontSize':'16px' }}}%%
flowchart LR
    subgraph Edge[Edge Nodes]
      E1[Edge Inference]
    end
    Ingress[Perception API]
    Bus[(Event Bus)]
    Lake[(Data Lake/S3)]
    Train[Training Pipeline]
    Reg[(Model Registry)]
    E1 -- infer --> Ingress
    Ingress -- publish --> Bus
    Ingress -- artifacts --> Lake
    Train -- models --> Reg
    Reg -- deploy --> Ingress
```

## Information Model (ER)
This model underpins event schemas and storage. `InspectionRun` ties input frames to decisions and artifacts for audit.

```mermaid
%%{init: { 'theme': 'dark', 'themeVariables': { 'background':'#000', 'primaryTextColor':'#FFF', 'textColor':'#FFF', 'fontSize':'16px' }}}%%
erDiagram
  PART ||--o{ FEATURE : has
  PART ||--o{ POSE : exhibits
  INSPECTION_RUN ||--o{ ARTIFACT : produces
  INSPECTION_RUN ||--o{ DEFECT : flags
  INSPECTION_RUN }o--|| PART : inspects
  POSE ||--|| CAMERA : in_frame_of
```
