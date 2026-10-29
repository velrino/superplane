# Factory architecture diagram source

This source generates the PNG used for superplanehq/superplane#8997.
It follows the visual style of PR #8880 and describes source revision
`e2cb3dbe868fde28b8c9053c01c1642915571c98`.

## Render

Install Graphviz (`dot` on PATH) and `uv`, then run:

```sh
uv run architecture.py
```

The script declares its Python dependencies inline. It collects technology
icons from the `diagrams` package and draws neutral symbols itself.
Graphviz lays out the logical graph. Pillow fits it onto a 3840 × 2160 canvas.
The PNG is written to `output/factory-architecture.png`.

Only the guide and final PNG belong in the contribution. This source package
is kept separately so contributors can inspect and regenerate the diagram.
