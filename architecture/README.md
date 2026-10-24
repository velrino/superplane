# Architecture and design system materials

This branch stores supporting materials for the SuperPlane architecture documentation.
The diagrams describe existing code at main revision `bfb220601`.

## Layout

```text
architecture/
├── README.md
├── research/                 # Existing docs, related issues, and base revision
├── review/                   # Image validation and tracking-issue description
└── source/
    ├── README.md             # Reproduction instructions
    ├── architecture_graphviz.py
    ├── symbols/              # All 16 icons
    └── output/               # Two final PNGs, 3840 × 2160
```

## Diagrams

[System architecture](source/output/system-architecture.png) · [Design system](source/output/design-system.png)

All output images are PNGs. Icons, titles, and descriptions have separate layout rows.
The diagrams are proposed in [PR #8880](https://github.com/superplanehq/superplane/pull/8880).
Feedback and the purpose of this contribution are tracked in [issue #8879](https://github.com/superplanehq/superplane/issues/8879).

## Contribution boundary

This `artifacts/architecture` branch contains the renderer, symbols, and review materials.
It has an independent history and is not the source branch for an upstream pull request.

The [documentation branch](https://github.com/velrino/superplane/tree/docs/architecture-overview/docs/architecture)
starts from the upstream main revision and contains the documentation and final PNGs.
It also corrects outdated statements in the existing architecture guide.
The upstream PR is open for review and contains documentation and final PNGs only.

See [source/README.md](source/README.md) to regenerate the diagrams.
