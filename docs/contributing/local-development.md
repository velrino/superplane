---
title: Local Development Guide
---

# Local Development Guide

This guide covers everyday development workflows, runner environments, and advanced configuration for working on SuperPlane.

## Everyday Development Workflow

### Starting and Stopping the Server

Once you have completed the initial setup from [CONTRIBUTING.md](../../CONTRIBUTING.md), you do not need to run `make dev.setup` for every session.

- **Start containers and server:**
  ```sh
  make dev.up
  make dev.server
  ```
- **Foreground logs:** To view server logs directly in your terminal (air, Vite, and worker processes) instead of running detached:
  ```sh
  make dev.server.fg
  ```
- **Stop containers:**
  ```sh
  make dev.down
  ```

### When to Re-run Setup

Re-run `make dev.setup` when you pull changes or switch branches that include:
- New or updated Go modules (`go.mod`, `go.sum`).
- New or updated npm dependencies in `web_src/package.json`.
- Modified Protocol Buffer definitions in `protos/` (re-runs `pb.gen`).
- New database migrations in `db/migrations/`.

## Runner Fleets and Worker Tools

SuperPlane uses ephemeral runner containers managed by the Docker Fleet Manager to execute integrated tasks and factory line workflows.

### Automatic Fleet and Token Configuration

During local development:
- `make dev.setup` and `make dev.server` automatically seed the default installation runner fleet (`e1-large-amd64`).
- Once you complete owner onboarding at `http://localhost:8000`, the local Fleet Manager detects the owner account and provisions its API credentials automatically.
- You do not need to create fleets or generate `INSTALLATION_ADMIN_TOKEN` manually in `.env` for standard local development.

### Bundled Worker CLIs

The local worker image includes Claude Code, Codex, OpenCode, git, `gh`, and `jq` so factory line apps can run in isolated containers.
- Do not install these CLIs on your host machine.
- Connect GitHub and Claude integrations in the organization before dispatching factory tasks. Factory nodes use those organization integrations rather than a host `.env` `ANTHROPIC_API_KEY`.
- OpenCode must be available on the runner `PATH` for the Run OpenRouter Agent.

### Rebuilding Runner Images

If you modify `release/runner/Dockerfile`, rebuild the runner images with:

```sh
make dev.up
```

### Checking Runner Health

To verify that all required CLI binaries, browser engines, and models are available on the runner image:

```sh
make doctor-local
```

## Advanced Configuration

### Database Snapshots

A local dump lets you initialize a new environment without repeating owner setup or GitHub connection. This is useful when working with scripts or automated setups. See [Local database snapshot](local-database-snapshot.md).

### External Integrations and Hosted OpenRouter

- To configure webhooks from external services (GitHub, Slack, Jira, Linear) via public tunnels (ngrok or cloudflared), see [Connecting to third-party services during development](connecting-to-3rdparty-services-from-development.md).
- To seed the SuperPlane-hosted OpenRouter provider, set `SUPERPLANE_DEV_HOSTED_OPENROUTER=yes` in `.env` as documented in [Connecting to third-party services](connecting-to-3rdparty-services-from-development.md).

### Legacy Task Broker Routing

`make dev.up`, `make dev.setup`, and `make dev.server` use the integrated runner API and Docker Fleet Manager. Set `TASK_BROKER_*` environment variables in `.env` only when testing legacy or remote broker routing (see `.env.example`).
