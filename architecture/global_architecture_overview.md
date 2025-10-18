# Global Architecture Overview

RoboCaps spans edge perception, cloud training/evaluation, and enterprise integration. This overview summarizes cross-system patterns, interfaces, and governance.

## Assumptions
- Edge nodes have GPU acceleration and reliable power; connectivity may be intermittent.
- Camera triggering, part catalogs, and acceptance criteria are under change control.
- Data retention policies permit storage of overlays and anonymized frames for audit.

## Non-Functional Requirements
- Latency: edge p50 < 60 ms, p99 < 120 ms (224×224 inference).
- Availability: > 99.5% for API and edge agents during shifts.
- Security: mTLS, signed artifacts, SBOM/scans, least-privilege identities.
- Observability: metrics, logs, traces with trace ID propagation.

## C4 Context
```mermaid
%%{init: { 'theme': 'dark', 'themeVariables': { 'background':'#000000', 'primaryTextColor':'#FFFFFF', 'fontSize':'16px' }}}%%
flowchart LR
    E[Edge Robots<br/>Cameras + Jetson / RTX] -- MQTT / ROS2 --> G[Edge Gateway<br/>QoS, buffering]
    G -- gRPC / HTTPS --> A[Perception API<br/>FastAPI + TensorRT]
    A -- events --> B[Event Bus<br/>Kafka or Redpanda]
    B -- features --> T[Training Pipeline<br/>PyTorch + S3]
    T -- models --> R[Registry<br/>Model, Config, Artifacts]
    R -- deploy --> A
    A -- insights --> BI[Enterprise Apps<br/>MES / ERP / QMS]
```

## C4 Container View
The platform comprises edge nodes, an ingress/API layer, an event backbone, a data lake, a training pipeline, and a model registry that feeds deployments.

```mermaid
%%{init: { 'theme': 'dark', 'themeVariables': { 'background':'#000', 'primaryTextColor':'#FFF', 'textColor':'#FFF', 'fontSize':'16px' }}}%%
flowchart LR
    subgraph Edge[Edge Nodes]
      E1[Edge Inference]
      Cap[Capture]
      Pre[Preprocess]
      Cap-->Pre-->E1
    end
    Ingress[Perception API]
    Bus[(Event Bus)]
    Lake[(Data Lake / S3)]
    Train[Training Pipeline]
    Reg[(Model Registry)]
    E1 -- infer --> Ingress
    Ingress -- publish --> Bus
    Ingress -- artifacts --> Lake
    Train -- models --> Reg
    Reg -- deploy --> Ingress
```

## Information Model (ER)
`InspectionRun` ties input frames to decisions and artifacts for audit.

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

## Data Lifecycle
```mermaid
%%{init: { 'theme': 'dark', 'themeVariables': { 'background':'#000', 'primaryTextColor':'#FFF', 'textColor':'#FFF', 'fontSize':'16px' }}}%%
sequenceDiagram
    autonumber
    participant Edge as Edge Inference
    participant API as API
    participant Bus as Event Bus
    participant Lake as Data Lake S3
    participant Train as Trainer
    participant Reg as Model Registry
    Edge->>API: Inference + metadata
    API->>Bus: Events
    API->>Lake: Artifacts overlays
    Train->>Reg: Register model
    Reg->>API: Deploy new model
```

## Trust Zones and Deployment
Separate concerns to minimize blast radius and meet compliance requirements.

```mermaid
%%{init: { 'theme': 'dark', 'themeVariables': { 'background':'#000000', 'primaryTextColor':'#FFFFFF', 'fontSize':'16px' }}}%%
flowchart LR
  subgraph Z1[Zone 1 Edge]
    EdgeNode[Edge Node<br/>Capture + Inference]
  end
  subgraph Z2[Zone 2 DMZ]
    GW[Edge Gateway]
  end
  subgraph Z3[Zone 3 Cloud]
    API[Perception API]
    BUS[Event Bus]
    S3[Data Lake]
    REG[Model Registry]
  end
  EdgeNode -- mTLS --> GW
  GW -- mTLS --> API
  API --> BUS
  API --> S3
  REG --> API
```

## Data Contracts (Global)
- Pose: `{part_id, tx, ty, theta | tz, qw, qx, qy, qz, confidence}`
- Decision event: `{run_id, parts, poses, decision, model_version, trace_id}`
- Artifact: `{run_id, overlay_uri, created_at}`

## Security Model
- Artifact signing; verify on load; SBOM for images
- mTLS with short-lived credentials (rotated)
- RBAC for API and artifact store

## Observability
- Prometheus: latency, throughput, errors, GPU metrics
- Structured logs with trace IDs and run IDs
- Tracing: capture→decision correlation via OTLP

## Failure Modes and Mitigations
- Connectivity loss: local buffering and reconciliation
- Model regression: canary deploy with automated rollback criteria
- Resource saturation: autoscaling, rate limiting, reduced resolution fallback

## Capacity and Versioning
- Version models/configs with semver + git SHA
- Capacity plan using peak frames per second and object count per frame
