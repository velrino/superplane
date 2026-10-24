# SuperPlane architecture diagram sources

This artifact branch contains the renderer and symbols for the architecture documentation.
It is separate from the source contribution to SuperPlane.

## Layout

```text
source/
├── README.md
├── architecture_graphviz.py
├── symbols/                  # All technology and neutral icons
└── output/                   # Two final 3840 × 2160 PNGs
    ├── system-architecture.png
    └── design-system.png
```

## Render

Requirements: Graphviz (`dot` on PATH) and `uv`.
The Python script declares its Python and package requirements inline.

```sh
uv run architecture_graphviz.py
```

The script renders both diagrams and writes PNGs only.
Each icon, title, and description occupies a separate table row.
Graphviz lays out the logical graph; Pillow fits it onto a 16:9 canvas.
Technology icons come from the `diagrams` package. Neutral symbols are drawn by the script.
All symbols are collected in `symbols/` and can be regenerated.

## Scope

The diagrams describe source main at `bfb220601dae150e1f635a840ac597c0d6ad669d`.
The system map follows the integrated runner path and shows selected relationships.
The design system map describes existing composition, not a proposed replacement.
See the documentation README for optional paths and source references.

Only the documentation and final PNGs belong in the SuperPlane contribution.
The renderer and individual symbols remain in this artifact branch.
