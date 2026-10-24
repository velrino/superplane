Issue #8653 — Task log duration evidence

Issue: https://github.com/superplanehq/superplane/issues/8653
PR: https://github.com/superplanehq/superplane/pull/8869
Capture source commit: 95e76dc985cc8f7cb167d143ffc7b445b9add4a9
Current PR source commit: 0c6fe7f7b1b2e86f9f6c1398a790dcbeee9759d4
Reproduction baseline: a787101cae75b3c8acfc93527aaf81ef7b28a778
The contributed source files stayed byte-identical during the PR rebase.

These nine images are unedited Chromium screenshots of a controlled local
Storybook simulation. It uses real application components and the NDJSON
parser, simulated API responses, and a fixed browser clock.

The fixture defines a 28m 20s run and starts the agent 22m 50s later.
Checkout 1s, Prompt 29s, and Wait 5m total 5m 30s.
The interval before the agent starts is a simulation input. It does not
identify a setup, queue, or other cause for the production discrepancy.

Before: after completion in the open live view, the header shows agent time,
5m 30s. Reopening the same recorded run changes the header to run time,
28m 20s. Command durations require pointer hover.
After: both views show Run time 28m 20s. Command durations remain visible.

The private production task was not accessed. These images validate the
reproduced display fixes; they do not establish the cause or correctness
of the 28-minute total reported in the issue.

captions.txt explains each image. screenshots.json records dimensions and
SHA-256 checksums. The images are stored outside the source PR branch.
