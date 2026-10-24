# /// script
# requires-python = ">=3.11"
# dependencies = ["diagrams>=0.25,<0.26", "pillow>=11,<13"]
# ///
"""Render SuperPlane runtime and UI maps from reviewed source topology.

Inspired by the user's ClassGame architecture_graphviz.py reference.
Run: uv run architecture_graphviz.py
Outputs: two 4K PNGs in output/. All icons are stored in symbols/.
The topology describes source main bfb220601, not a deployed environment.
"""

import html
import textwrap
import shutil
import re
from pathlib import Path

import diagrams
from diagrams import Cluster, Diagram, Edge, Node
from diagrams.generic.storage import Storage
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.queue import RabbitMQ
from diagrams.programming.framework import React
from diagrams.programming.language import Bash, Go
from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
SYMBOLS = ROOT / "symbols"
OUTPUTS = ROOT / "output"
SYMBOLS.mkdir(exist_ok=True)
OUTPUTS.mkdir(exist_ok=True)
RAW_OUTPUT = OUTPUTS / "system-architecture-raw"
OUTPUT = OUTPUTS / "system-architecture.png"

LOGICAL_SIZE = (1920, 1080)
PNG_SCALE = 2
CANVAS_SIZE = tuple(dimension * PNG_SCALE for dimension in LOGICAL_SIZE)
# Slide header band (logical px). The graph is fitted into the space below it.
HEADER_HEIGHT = 112
FRAME_MARGIN_X = 48
FRAME_MARGIN_BOTTOM = 74

TITLE = "SuperPlane · System architecture"
SUBTITLE = "Logical modules and the integrated runner path"

BLUE = "#3b63f3"
PURPLE = "#8b5cf6"
ORANGE = "#ed8b00"
TEAL = "#0ea5b7"
GREEN = "#16a368"
RED = "#dc382d"
INK = "#211833"
MUTED = "#645b73"
PANEL_FILL = "#f6f7fb"
PANEL_LINE = "#d8dce8"
SANS = "Helvetica Neue, Helvetica, Arial, sans-serif"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Load the same title fonts used by the hand-laid-out architecture."""
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
        if bold
        else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica Bold.ttf"
        if bold
        else "/System/Library/Fonts/Supplemental/Helvetica.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


FONT_TITLE = font(36 * PNG_SCALE, bold=True)
FONT_SUBTITLE = font(17 * PNG_SCALE)

# No `ratio`/`size`: Graphviz lays the graph out at its natural density and we
# fit the result onto the slide afterwards, so spacing and type scale together.
graph_attr = {
    "bgcolor": "white",
    "dpi": "192",
    "pad": "0.3",
    "nodesep": "0.38",
    "ranksep": "0.72",
    "splines": "spline",
    "newrank": "true",
    "compound": "true",
    # Best effort only: dot keeps a node's out-edges in declaration order, but
    # heads inside different clusters may still be reordered.
    "ordering": "out",
    "fontname": "Helvetica",
}
node_attr = {
    "fontname": "Helvetica",
    "fontcolor": INK,
}
edge_attr = {
    "color": BLUE,
    "fontcolor": MUTED,
    "fontname": "Helvetica",
    "fontsize": "11.5",
    "penwidth": "1.6",
    "arrowsize": "0.75",
    "labeldistance": "1.2",
}
cluster_attr = {
    "style": "rounded,filled",
    "fillcolor": PANEL_FILL,
    "bgcolor": PANEL_FILL,
    "pencolor": PANEL_LINE,
    "penwidth": "1.2",
    "fontname": "Helvetica-Bold",
    "fontsize": "13",
    "fontcolor": MUTED,
    "labeljust": "l",
    "margin": "26",
}


def card(icon: type[Node], title: str, subtitle: str, **attrs) -> Node:
    """Copy technology icons into the same folder as the neutral symbols."""
    original = Path(diagrams.__file__).resolve().parent.parent / icon._icon_dir / icon._icon
    path = SYMBOLS / f"{icon.__name__.lower()}.png"
    shutil.copy2(original, path)
    return icon_card(path, title, subtitle, **attrs)


def icon_card(path: Path, title: str, subtitle: str, **attrs) -> Node:
    """Use separate table rows so an icon can never overlap its label."""
    title_lines = "<br/>".join(html.escape(line) for line in textwrap.wrap(title, 23))
    sub_lines = "<br/>".join(html.escape(line) for line in textwrap.wrap(subtitle, 28))
    label = (
        '<<table border="0" cellborder="0" cellspacing="0" cellpadding="0">'
        '<tr><td width="180" height="80" fixedsize="true">'
        f'<img src="{html.escape(str(path))}" scale="true"/></td></tr>'
        '<tr><td height="12"></td></tr>'
        f'<tr><td width="180"><font point-size="17"><b>{title_lines}</b></font></td></tr>'
        '<tr><td height="5"></td></tr>'
        f'<tr><td><font point-size="12" color="{MUTED}">{sub_lines}</font></td></tr>'
        '</table>>'
    )
    node_id = re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")
    return Node(label, nodeid=node_id, shape="plain", fixedsize="false", width="0", height="0", margin="0", **attrs)


def panel(title: str) -> Cluster:
    return Cluster(title, graph_attr=cluster_attr)


def flow(color: str = BLUE, label: str = "", **attrs) -> Edge:
    both = attrs.pop("dir", None) == "both"
    return Edge(color=color, label=label, forward=True, reverse=both, **attrs)


def pulse(color: str, label: str = "", **attrs) -> Edge:
    """Realtime / telemetry traffic: same weight, dashed."""
    both = attrs.pop("dir", None) == "both"
    return Edge(color=color, label=label, forward=True, reverse=both, style="dashed", **attrs)


def frame_box(scale: int) -> tuple[int, int, int, int]:
    """Slide area reserved for the graph (left, top, right, bottom), in canvas px."""
    return (
        FRAME_MARGIN_X * scale,
        HEADER_HEIGHT * scale,
        (LOGICAL_SIZE[0] - FRAME_MARGIN_X) * scale,
        (LOGICAL_SIZE[1] - FRAME_MARGIN_BOTTOM) * scale,
    )


def write_slide_png() -> None:
    """Fit the native Graphviz render under the header on an exact 4K 16:9 canvas."""
    raw_png = RAW_OUTPUT.with_suffix(".png")
    left, top, right, bottom = frame_box(PNG_SCALE)
    frame = (right - left, bottom - top)
    with Image.open(raw_png) as source:
        fitted = ImageOps.contain(
            source.convert("RGB"), frame, method=Image.Resampling.LANCZOS
        )

    canvas = Image.new("RGB", CANVAS_SIZE, "white")
    canvas.paste(
        fitted,
        (left + (frame[0] - fitted.width) // 2, top + (frame[1] - fitted.height) // 2),
    )
    draw = ImageDraw.Draw(canvas)
    draw.text((42 * PNG_SCALE, 22 * PNG_SCALE), TITLE, fill=INK, font=FONT_TITLE)
    draw.text((44 * PNG_SCALE, 66 * PNG_SCALE), SUBTITLE, fill=MUTED, font=FONT_SUBTITLE)
    draw.text((44 * PNG_SCALE, 1034 * PNG_SCALE), FOOTNOTE, fill=MUTED, font=font(14 * PNG_SCALE))
    canvas.save(OUTPUT, quality=95)
    raw_png.unlink()


def symbol(name: str, color: str = BLUE) -> str:
    """Draw small neutral symbols instead of implying a vendor dependency."""
    path = SYMBOLS / f"{name}.png"
    canvas = Image.new("RGBA", (256, 256), (255, 255, 255, 0))
    d = ImageDraw.Draw(canvas)
    if name in ("tokens", "theme"):
        for x, y, fill in [(40, 40, BLUE), (142, 40, PURPLE), (40, 142, TEAL), (142, 142, ORANGE)]:
            d.rounded_rectangle((x, y, x + 74, y + 74), radius=18, fill=fill)
    elif name == "typography":
        d.text((32, 44), "Aa", font=font(136, bold=True), fill=INK)
    elif name == "checks":
        d.rounded_rectangle((44, 28, 212, 224), radius=20, outline=color, width=12)
        for y in (75, 125, 175):
            d.line((68, y, 79, y + 12, 100, y - 12), fill=color, width=9, joint="curve")
            d.line((122, y, 184, y), fill=color, width=9)
    elif name == "storybook":
        d.rounded_rectangle((45, 28, 211, 226), radius=20, fill="#ff4785")
        d.text((80, 52), "S", font=font(130, bold=True), fill="white")
    elif name == "providers":
        for x, y in [(128, 52), (52, 184), (204, 184)]:
            d.line((128, 128, x, y), fill=color, width=12)
            d.ellipse((x - 27, y - 27, x + 27, y + 27), fill="white", outline=color, width=10)
        d.ellipse((93, 93, 163, 163), fill=color)
    else:
        for x, y in [(40, 35), (142, 35), (40, 140), (142, 140)]:
            d.rounded_rectangle((x, y, x + 74, y + 74), radius=14, outline=color, width=10)
    canvas.save(path)
    return str(path)


def neutral(name: str, title: str, subtitle: str, color: str = BLUE) -> Node:
    return icon_card(Path(symbol(name, color)), title, subtitle)


def system_map() -> None:
    with panel("CLIENTS & EVENTS"):
        web = card(React, "Web UI", "canvases · workspaces")
        cli = card(Bash, "CLI / webhooks", "API clients · event intake")
    with panel("SUPERPLANE GO APPLICATION · LOGICAL MODULES"):
        public = card(Go, "Public HTTP API", "REST gateway · auth · live hub")
        services = card(Go, "Application services", "organizations · factories · canvases")
        workers = neutral("workers", "Workers + registry", "workflow engine · integrations")
        runner_api = card(Go, "Runner API", "registration · control · log ingress")
        public >> flow(label="in-process handlers", weight="5") >> services
        services >> Edge(style="invis", weight="2") >> workers
        workers >> Edge(style="invis", weight="2") >> runner_api
    with panel("DURABLE STATE & MESSAGING"):
        postgres = card(PostgreSQL, "PostgreSQL", "domain state · work · runner tasks")
        rabbit = card(RabbitMQ, "RabbitMQ", "wake-ups · state notifications")
        files = card(Storage, "Files & logs", "active filesystem · blob archives")
    with panel("RUNNER INFRASTRUCTURE"):
        fleet = card(Go, "Fleet Manager", "admin HTTP · capacity drivers")
        runners = card(Server, "Runner hosts", "host / Docker · shell / agents")
        fleet >> flow(ORANGE, label="provision / remove", weight="2") >> runners
    with panel("EXTERNAL PROVIDERS"):
        providers = neutral("providers", "APIs & models", "Git · SaaS · CI/CD · LLMs", PURPLE)

    web >> flow(label="REST + WebSocket", dir="both", weight="6") >> public
    cli >> flow(label="HTTPS", weight="4") >> public
    services >> flow(TEAL, label="persist / read", dir="both", weight="2") >> postgres
    workers >> flow(TEAL, label="durable work", dir="both") >> postgres
    workers >> pulse(ORANGE, label="publish / wake", dir="both") >> rabbit
    services >> pulse(ORANGE, label="state changes", constraint="false") >> rabbit
    runner_api >> flow(TEAL, label="reserve / persist", dir="both", constraint="false") >> postgres
    rabbit >> pulse(ORANGE, label="task wake-up", constraint="false") >> runner_api
    runner_api >> flow(TEAL, label="store log chunks", weight="2") >> files
    workers >> flow(TEAL, label="compact / archive", constraint="false") >> files
    runner_api >> flow(ORANGE, label="HTTP + control WebSocket", dir="both", weight="4") >> runners
    workers >> flow(PURPLE, label="integration calls", weight="2") >> providers
    runners >> flow(PURPLE, label="Git / tools / models", weight="2") >> providers


def design_map() -> None:
    with panel("FOUNDATIONS"):
        tokens = neutral("tokens", "Tokens & themes", "App.css · light / dark / workspace")
        visuals = neutral("typography", "Type & icons", "contextual scales · Lucide · logos")
    with panel("REUSABLE UI FAMILIES · COEXISTING"):
        shadcn = neutral("shadcn", "shadcn primitives", "components/ui · forms · Radix")
        reui = neutral("reui", "ReUI components", "components/reui · Frame · Badge", TEAL)
        existing = neutral("existing", "Existing UI", "ui · primitives + compositions", PURPLE)
    with panel("PRODUCT COMPOSITION"):
        components = card(React, "Pages & components", "hooks · state · view models")
        canvases = card(React, "Canvas experience", "nodes · mappers · execution details")
        factories = card(React, "Workspace experience", "tasks · lines · run console")
        components >> flow(label="compose") >> canvases
        components >> flow(label="compose") >> factories
    with panel("REVIEW & VERIFICATION"):
        stories = neutral("storybook", "Storybook", "tokens · states · fixtures")
        checks = neutral("checks", "Behavior checks", "Bun · Happy DOM · Testing Library", GREEN)
    for family in (shadcn, reui, existing):
        tokens >> flow(TEAL, label="theme" if family == shadcn else "", weight="3") >> family
        visuals >> flow(TEAL, label="shared conventions" if family == existing else "", weight="2") >> family
        family >> flow(label="compose / import", weight="3") >> components
    components >> pulse(PURPLE, label="visual scenarios", weight="2") >> stories
    components >> pulse(GREEN, label="observable behavior", weight="2") >> checks


def render(name: str, title: str, subtitle: str, footer: str, build) -> None:
    global RAW_OUTPUT, OUTPUT, TITLE, SUBTITLE, FOOTNOTE
    RAW_OUTPUT = OUTPUTS / f"{name}-raw"
    OUTPUT = OUTPUTS / f"{name}.png"
    TITLE, SUBTITLE, FOOTNOTE = title, subtitle, footer
    with Diagram("", filename=str(RAW_OUTPUT), direction="LR", show=False,
                 outformat="png", graph_attr=graph_attr,
                 node_attr=node_attr, edge_attr=edge_attr):
        build()
    write_slide_png()
    print(f"Wrote {OUTPUT} (3840x2160)")


if __name__ == "__main__":
    render(
        "system-architecture", "SuperPlane · System architecture",
        "Logical modules, durable execution and the integrated runner path",
        "Source: main bfb220601 · Roles and storage depend on configuration · Optional legacy and managed-agent paths are described in the README",
        system_map,
    )
    render(
        "design-system", "SuperPlane · Design system map",
        "Shared foundations, coexisting UI families and product composition",
        "Source: main bfb220601 · Arrows show composition and review relationships, not strict import boundaries · No new design system is proposed",
        design_map,
    )
