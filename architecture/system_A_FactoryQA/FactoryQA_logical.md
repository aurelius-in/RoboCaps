# Factory QA — Logical (RM-ODP)

## Interfaces
- `/infer` (HTTP POST, FastAPI): image, config → part/pose outputs.
- ROS2 topics: `cam/image_raw`, `qa/poses`, `qa/defects`.
- MQTT topics: `qa/poses`, `qa/defects`, `qa/audit`.

## Contracts
- Pose schema: `{part_id, T_cam_part (SE3), confidence}`.
- Audit record: `{run_id, timestamps, inputs_hash, outputs, overlays_uri}`.

## Workflows
- Capture → Preprocess → Infer → Decide → Emit events → Persist artifacts.

## Reliability
- Backpressure via gateway buffers, at-least-once delivery, idempotent sink.

## Component/Data Flow
```mermaid
%%{init: { 'theme': 'dark', 'themeVariables': { 'background':'#000', 'primaryTextColor':'#FFF', 'textColor':'#FFF', 'fontSize':'14px' }}}%%
flowchart LR
    CAM[/cam/image_raw/] --> CAP[Capture Service]
    CAP --> PRE[Preprocess Node]
    PRE --> INF[RoboCaps Inference]
    INF --> POS[Pose Output]
    INF --> CONF[Part Confidence]
    POS --> MQTT{{mqtt: qa/poses}}
    CONF --> MQTT
    INF --> API[/POST /infer/]
```
