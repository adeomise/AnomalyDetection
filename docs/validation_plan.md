# Validation Plan

## Completed Baseline Evidence

EXP-001 dataset validation, 50-epoch training, best-checkpoint validation, and result finalization are complete. The metrics and checkpoint checksum are recorded in [EXP-001-baseline.md](../experiments/EXP-001-baseline.md).

This does not establish real-time performance. FPS, latency, streaming stability, field false positives, and field false negatives remain unmeasured.

## A/B/C Integration Smoke Test

After model, environment, and real-time code are combined, record evidence for every item:

- [ ] provided `best.pt` exists and its SHA-256 matches the handoff;
- [ ] checkpoint loads with the configured model path;
- [ ] missing/unreadable checkpoint fails before capture begins;
- [ ] class mapping is exactly `0=fire`;
- [ ] sample image inference completes;
- [ ] a valid empty-detection result is handled without error;
- [ ] consecutive OpenCV video frames are processed;
- [ ] bounding boxes remain inside frame bounds and render correctly;
- [ ] confidence renders for each displayed detection;
- [ ] FPS or per-frame latency is measured and displayed/logged;
- [ ] end-of-stream and capture failure terminate or recover predictably;
- [ ] no API key, token, or credential-bearing stream URL is logged.

The real-time pipeline is not implemented, so this checklist is currently TODO.

## Later Validation Stages

1. Controlled video: representative distance, smoke/fire size, lighting, motion, and background.
2. Streaming reliability: reconnect, dropped frames, varying resolution, and sustained runtime.
3. Error analysis: false positives, false negatives, hard negatives, and detection stability.
4. Performance: FPS and latency on the actual integration laptop.

Acceptance thresholds must be agreed before claiming real-time readiness. EXP-006 threshold tuning is a candidate experiment, not completed work.
