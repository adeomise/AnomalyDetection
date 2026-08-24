# Validation Plan

## Stage 1 - Dataset Test

Evaluate Precision, Recall, mAP@0.5, mAP@0.5:0.95, and the Confusion Matrix on a test set that was not used for training or tuning.

## Stage 2 - Controlled Validation

Use safely obtained controlled or field-validation video to check behavior on realistic input. Record the input conditions, model version, dataset version, and observations.

## Stage 3 - Realtime Pipeline

Measure FPS, latency, detection stability, false positives, and false negatives across representative streaming conditions.

TODO: Define acceptance criteria and test cases. No measurements are available yet.