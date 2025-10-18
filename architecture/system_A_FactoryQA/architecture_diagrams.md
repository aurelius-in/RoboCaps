# Factory QA Architecture Diagrams

## Sequence (Inspection Cycle)
```mermaid
%%{init: { 'theme': 'dark', 'themeVariables': { 'background':'#000', 'primaryTextColor':'#FFF', 'textColor':'#FFF', 'fontSize':'16px' }}}%%
sequenceDiagram
    autonumber
    participant Cam as Camera
    participant Edge as Edge Inference
    participant GW as Edge Gateway
    participant API as Perception API
    participant Bus as Event Bus
    Cam->>Edge: Frame + Trigger
    Edge->>Edge: Preprocess + RoboCaps infer
    Edge->>GW: Results + Artifacts
    GW->>API: HTTPS /infer
    API->>Bus: Publish QA events
```

The inspection cycle starts on hardware triggers, runs local inference for latency, publishes decisions upstream, and persists overlays for audit.

## Data Flow (ROS2/MQTT Topics)
```mermaid
%%{init: { 'theme': 'dark', 'themeVariables': { 'background':'#000', 'primaryTextColor':'#FFF', 'textColor':'#FFF', 'fontSize':'16px' }}}%%
flowchart LR
    CAM[/cam/image_raw/] --> PRE[preprocess]
    PRE --> INF[infer_capsules]
    INF --> P[poses]
    INF --> C[part_confidence]
    P --> OUT{{mqtt: qa/poses}}
    C --> OUT
```

## Container View (C4)
```mermaid
%%{init: { 'theme': 'dark', 'themeVariables': { 'background':'#000', 'primaryTextColor':'#FFF', 'textColor':'#FFF', 'fontSize':'16px' }}}%%
flowchart LR
  subgraph Edge[Edge]
    cap[Capture]
    pre[Preprocess]
    inf[Inference (TRT)]
  end
  api[Perception API]:::svc
  bus[(Events)]:::queue
  art[(Artifacts/S3)]:::store
  cap-->pre-->inf-->api
  api-->bus
  api-->art
  classDef svc fill:#111,stroke:#888,color:#FFF;
  classDef queue fill:#000,stroke:#888,color:#FFF;
  classDef store fill:#000,stroke:#888,color:#FFF;
```

## Entity-Relationship (QA Domain)
```mermaid
%%{init: { 'theme': 'dark', 'themeVariables': { 'background':'#000', 'primaryTextColor':'#FFF', 'textColor':'#FFF', 'fontSize':'16px' }}}%%
erDiagram
  INSPECTION_RUN ||--o{ FRAME : includes
  FRAME }o--|| CAMERA : captured_by
  INSPECTION_RUN ||--o{ RESULT : yields
  RESULT }o--|| PART : about
  RESULT ||--|{ POSE : has
  RESULT ||--|{ DEFECT : has
```

## State Machine (Run Lifecycle)
```mermaid
%%{init: { 'theme': 'dark', 'themeVariables': { 'background':'#000', 'primaryTextColor':'#FFF', 'textColor':'#FFF', 'fontSize':'16px' }}}%%
stateDiagram-v2
  [*] --> Idle
  Idle --> Capturing: trigger
  Capturing --> Inferring: frame_ready
  Inferring --> Deciding: outputs_ready
  Deciding --> Emitting: publish
  Emitting --> [*]
```

## Module Dependencies
```mermaid
%%{init: { 'theme': 'dark', 'themeVariables': { 'background':'#000', 'primaryTextColor':'#FFF', 'textColor':'#FFF', 'fontSize':'14px' }}}%%
graph TD
    B[Backbone Adapters] --> R[Routing Attention]
    R --> H[Capsule Head]
    H --> L[Pose Loss]
    H --> V[Visualization]
    H --> S[API Server]
```
