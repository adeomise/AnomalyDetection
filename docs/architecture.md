# Architecture

The intended system boundary is:

```text
Smartphone / Drone Camera
        -> Streaming
        -> Laptop
        -> OpenCV
        -> YOLO
        -> Fire / Smoke Detection
        -> Bounding Box / Confidence
        -> FPS / Latency
```

The camera device captures and transmits video. The laptop receives frames and performs inference. The streaming transport, application, model variant, and deployment details are not fixed yet.