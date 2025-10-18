# Robot Manipulation Architecture Diagrams

## Sequence (Perception-to-Grasp)
```mermaid
%%{init: { 'theme': 'dark', 'themeVariables': { 'background':'#000', 'primaryTextColor':'#FFF', 'textColor':'#FFF', 'fontSize':'16px' }}}%%
sequenceDiagram
    autonumber
    participant Cam as Wrist/Overhead Cam
    participant Per as Perception Node
    participant Plan as Motion Planner
    participant Ctrl as Controller
    Cam->>Per: Frames
    Per->>Per: Capsules + Pose
    Per->>Plan: Object/part poses
    Plan->>Ctrl: Trajectory
    Ctrl->>Robot: Execute
```

## Container View (C4)
```mermaid
%%{init: { 'theme': 'dark', 'themeVariables': { 'background':'#000', 'primaryTextColor':'#FFF', 'textColor':'#FFF', 'fontSize':'16px' }}}%%
flowchart LR
  CAM[Camera]-->PER[Perception]
  PER-->AFF[Affordance]
  AFF-->PLAN[Planner]
  PLAN-->CTRL[Controller]
  CTRL-->ROBOT[(Robot HW)]
```

## Entity-Relationship (Manipulation Domain)
```mermaid
%%{init: { 'theme': 'dark', 'themeVariables': { 'background':'#000', 'primaryTextColor':'#FFF', 'textColor':'#FFF', 'fontSize':'16px' }}}%%
erDiagram
  SCENE ||--o{ OBJECT : contains
  OBJECT ||--o{ PART : has
  PART ||--|{ POSE : has
  GRASP_CANDIDATE }o--|| PART : for
  PLAN ||--o{ TRAJECTORY : produces
```

## State Machine (Grasp Attempt)
```mermaid
%%{init: { 'theme': 'dark', 'themeVariables': { 'background':'#000', 'primaryTextColor':'#FFF', 'textColor':'#FFF', 'fontSize':'16px' }}}%%
stateDiagram-v2
  [*] --> Observe
  Observe --> ProposeGrasps
  ProposeGrasps --> PlanPath
  PlanPath --> Execute
  Execute --> Verify
  Verify --> [*]
```

## Data Flow (ROS2 Topics)
```mermaid
%%{init: { 'theme': 'dark', 'themeVariables': { 'background':'#000', 'primaryTextColor':'#FFF', 'textColor':'#FFF', 'fontSize':'14px' }}}%%
flowchart LR
    CAM[/camera/color/] --> PER[perception_capsules]
    PER --> POSE[poses]
    POSE --> GRASP[grasp_candidates]
    GRASP --> PLAN[/move_group/goal/]
```

## Module Dependencies
```mermaid
%%{init: { 'theme': 'dark', 'themeVariables': { 'background':'#000', 'primaryTextColor':'#FFF', 'textColor':'#FFF', 'fontSize':'14px' }}}%%
graph TD
    B[Backbones] --> R[Routing Attention]
    R --> H[Capsule Head]
    H --> A[Affordance Decoder]
    A --> P[Planner Interface]
```
