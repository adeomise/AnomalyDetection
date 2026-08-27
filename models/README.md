# Models

Model weights are excluded from Git because pretrained and trained weights can be large and may have separate distribution or licensing requirements.

- Put externally obtained weights in `models/pretrained/`.
- Put project-generated checkpoints such as `best.pt` and `last.pt` in `models/checkpoints/`.
- Do not commit either location's `.pt` files. Transfer checkpoints through the team-approved artifact channel and inject the local path through config or CLI.

The validated EXP-001 `best.pt` SHA-256 is:

```text
7b1fe847ea81bf5cd3647da1d457510b4a87d956be9eed4ab61c92db817f5ef2
```

Verify the checksum after transfer. A permanent team artifact location and the real-time model-path configuration remain TODO; no public checkpoint download URL is defined.
