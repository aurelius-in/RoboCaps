# System A: Factory QA

Scope: Defect detection, part verification, and pose estimation on production lines. Edge-first with cloud-backed training.

- Inputs: Industrial cameras, conveyor encoders, PLC signals.
- Outputs: Part/pose assessments, defect classes, audit artifacts.
- Interfaces: ROS2/MQTT at edge, HTTPS to cloud API, Kafka for events.
