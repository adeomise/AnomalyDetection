# Architecture

The intended system boundary is:

```text
Smartphone / Drone Camera
        -> Streaming
        -> Laptop
        -> OpenCV
        -> YOLO
        -> Fire Detection
        -> Bounding Box / Confidence
        -> FPS / Latency
```

The camera device captures and transmits video. The laptop receives frames and performs inference. EXP-001 fixes the current model boundary to a YOLOv8m `.pt` checkpoint with class `0=fire`. Fire/smoke multi-class detection is only a future experiment candidate.

The streaming transport, capture application, real-time entry point, and deployment packaging are not fixed yet. Component ownership and the model interface are defined in the [project README](../README.md) and [real-time guide](realtime_guide.md).
