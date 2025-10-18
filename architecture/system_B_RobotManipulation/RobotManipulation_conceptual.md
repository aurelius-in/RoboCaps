# Robot Manipulation — Conceptual (RM-ODP)

## Enterprise Viewpoint
- Goal: Reliable manipulation under uncertainty with explainable perception.
- Actors: Robot Operator, Process Engineer, Safety Officer.

## Information Viewpoint
- Entities: Object, Part, Pose, Affordance, Trajectory, Scene.

## Computational Viewpoint (conceptual)
- Services: Perception, Affordance Estimation, Planning, Control.
- Interactions: Perception → Planning → Control loop; feedback via sensors.

## Perception-to-Action Sequence
```mermaid
%%{init: { 'theme': 'dark', 'themeVariables': { 'background':'#000', 'primaryTextColor':'#FFF', 'textColor':'#FFF', 'fontSize':'14px' }}}%%
sequenceDiagram
    autonumber
    participant Cam as Camera
    participant Per as Perception (RoboCaps)
    participant Plan as Planner
    participant Ctrl as Controller
    Cam->>Per: RGB-D frames
    Per->>Plan: Poses + affordances
    Plan->>Ctrl: Trajectory
    Ctrl->>Robot: Execute
```
