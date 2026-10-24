Issue #8653 — Task log duration evidence

Issue: https://github.com/superplanehq/superplane/issues/8653
Source commit: 95e76dc985cc8f7cb167d143ffc7b445b9add4a9
Baseline: a787101cae75b3c8acfc93527aaf81ef7b28a778

These nine images are unedited Chromium screenshots of a controlled local
Storybook simulation. It uses the real task console components and NDJSON
parser, simulated API responses, and a fixed browser clock.

Before: the same finished run shows 5m 30s while viewed live, then 28m 20s
after reopening. Step durations require pointer hover.
After: both views show Run time 28m 20s. Command durations remain visible.

The private production task was not accessed. These images do not establish
the exact cause of its reported duration.

captions.txt explains each image. screenshots.json records dimensions and
SHA-256 checksums. The images are stored outside the source PR branch.
