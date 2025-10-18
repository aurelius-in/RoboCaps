# Robot Manipulation — Implementable

## Components
- Perception Service: RoboCaps capsule head with SE(3) output; TensorRT runtime
- Affordance Module: generates grasp candidates from part poses
- Planner: MoveIt2/OMPL with collision checking
- Controller Interface: sends trajectories; monitors execution

## Deployment
- Workcell GPU node for perception; planner/controller co-located or on robot controller
- ROS2 network configured with QoS appropriate for real-time perception topics

## Configuration
- Model URIs and calibration parameters
- Grasp scoring thresholds and safety margins
- Timeouts for planning and execution

## Safety
- Safe stop integration; watchdogs on controller feedback
- Workspace and speed limits; emergency stop propagation

## Failure Modes
- Pose drift: re-observe and replan; add view change
- Planner failure: alternative grasps; fallback hand-off
- Controller faults: safe stop and notify operator

## Deployment Diagram
```mermaid
%%{init: { 'theme': 'dark', 'themeVariables': { 'background':'#000', 'primaryTextColor':'#FFF', 'fontSize':'16px' }}}%%
flowchart LR
  Cam[Camera] --> Per[Perception TRT]
  Per --> Aff[Affordance]
  Aff --> Plan[Planner MoveIt2]
  Plan --> Ctrl[Controller]
  Ctrl --> Robot[Robot HW]
```
