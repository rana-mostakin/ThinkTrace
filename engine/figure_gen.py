# Author: rana-mostakin
"""
ThinkTrace v1 — SVG Figure Generator
Auto-generates inline SVG diagrams for physics, chemistry, math, and process questions.
All figures: viewBox="0 0 360 90", transparent bg, semi-transparent colors.
"""

from typing import Optional


def generate_figure(figure_type: str, params: dict) -> str:
    """
    Returns a complete SVG string for the given figure type and parameters.
    Types: force_diagram, velocity_diagram, molecular, graph_curve,
           process_flow, rocket_diagram, circuit_diagram
    """
    generators = {
        "force_diagram":    _force_diagram,
        "velocity_diagram": _velocity_diagram,
        "molecular":        _molecular,
        "graph_curve":      _graph_curve,
        "process_flow":     _process_flow,
        "rocket_diagram":   _rocket_diagram,
        "circuit_diagram":  _circuit_diagram,
        "none":             lambda p: "",
    }
    fn = generators.get(figure_type, lambda p: "")
    svg = fn(params)
    if not svg:
        return ""
    return f'<div style="margin:12px 0;opacity:0.9">{svg}</div>'


def _svg_wrap(content: str, viewbox: str = "0 0 360 90") -> str:
    return (
        f'<svg viewBox="{viewbox}" xmlns="http://www.w3.org/2000/svg" '
        + f'style="width:100%;max-width:360px;height:auto;display:block">'
        + f'{content}</svg>'
    )


def _arrow(x1, y1, x2, y2, color="rgba(124,111,255,0.7)", label="", label_color="rgba(144,144,168,0.9)"):
    """Render an arrow with optional label."""
    dx, dy = x2 - x1, y2 - y1
    # Arrowhead
    import math
    angle = math.atan2(dy, dx)
    aw = 7
    ax1 = x2 - aw * math.cos(angle - 0.4)
    ay1 = y2 - aw * math.sin(angle - 0.4)
    ax2 = x2 - aw * math.cos(angle + 0.4)
    ay2 = y2 - aw * math.sin(angle + 0.4)

    lx = (x1 + x2) / 2 + 6
    ly = (y1 + y2) / 2 - 4

    svg = (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        + f'stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>'
        + f'<polygon points="{x2},{y2} {ax1:.1f},{ay1:.1f} {ax2:.1f},{ay2:.1f}" '
        + f'fill="{color}"/>'
    )
    if label:
        svg += (
            f'<text x="{lx:.1f}" y="{ly:.1f}" font-family="JetBrains Mono,monospace" '
            + f'font-size="9" fill="{label_color}">{label}</text>'
        )
    return svg


def _force_diagram(params: dict) -> str:
    obj = params.get("object", "Block")
    forces = params.get("forces", [
        {"dir": "up",    "label": "N", "color": "rgba(34,212,122,0.75)"},
        {"dir": "down",  "label": "mg", "color": "rgba(255,85,85,0.75)"},
        {"dir": "right", "label": "F", "color": "rgba(124,111,255,0.75)"},
    ])

    cx, cy = 180, 45
    box_size = 22

    content = (
        # Object box
        f'<rect x="{cx - box_size/2}" y="{cy - box_size/2}" '
        + f'width="{box_size}" height="{box_size}" rx="3" '
        + f'fill="rgba(124,111,255,0.12)" stroke="rgba(124,111,255,0.4)" stroke-width="1.5"/>'
        + f'<text x="{cx}" y="{cy + 4}" font-family="DM Sans,sans-serif" '
        + f'font-size="9" fill="rgba(144,144,168,0.9)" text-anchor="middle">{obj}</text>'
    )

    dir_map = {
        "up":    (cx, cy - box_size // 2, cx, cy - 40),
        "down":  (cx, cy + box_size // 2, cx, cy + 40),
        "right": (cx + box_size // 2, cy, cx + 55, cy),
        "left":  (cx - box_size // 2, cy, cx - 55, cy),
    }

    for f in forces:
        direction = f.get("dir", "up")
        if direction in dir_map:
            x1, y1, x2, y2 = dir_map[direction]
            content += _arrow(x1, y1, x2, y2,
                              color=f.get("color", "rgba(124,111,255,0.7)"),
                              label=f.get("label", ""))

    return _svg_wrap(content)


def _velocity_diagram(params: dict) -> str:
    obj = params.get("object", "Object")
    v0 = params.get("v0", "v₀")
    vf = params.get("vf", "v")
    show_acc = params.get("show_acc", True)

    content = (
        # Timeline
        f'<line x1="30" y1="55" x2="330" y2="55" stroke="rgba(144,144,168,0.25)" stroke-width="1"/>'
        # Initial velocity arrow
        + _arrow(30, 45, 120, 45, color="rgba(124,111,255,0.75)", label=v0)
        # Final velocity arrow
        + _arrow(200, 45, 320, 45, color="rgba(34,212,122,0.75)", label=vf)
        # Object dot
        + f'<circle cx="160" cy="45" r="5" fill="rgba(124,111,255,0.5)"/>'
        + f'<text x="160" y="35" font-family="DM Sans,sans-serif" font-size="9" '
        + f'fill="rgba(144,144,168,0.9)" text-anchor="middle">{obj}</text>'
    )

    if show_acc:
        content += _arrow(30, 75, 180, 75, color="rgba(255,179,71,0.65)", label="a")

    # Time labels
    content += (
        f'<text x="30" y="68" font-family="JetBrains Mono,monospace" font-size="8" '
        + f'fill="rgba(74,74,98,0.9)" text-anchor="middle">t=0</text>'
        + f'<text x="330" y="68" font-family="JetBrains Mono,monospace" font-size="8" '
        + f'fill="rgba(74,74,98,0.9)" text-anchor="middle">t</text>'
    )

    return _svg_wrap(content)


def _molecular(params: dict) -> str:
    formula = params.get("formula", "H₂O")
    atoms = params.get("atoms", [
        {"symbol": "O", "x": 180, "y": 40, "r": 14, "color": "rgba(255,85,85,0.5)"},
        {"symbol": "H", "x": 130, "y": 65, "r": 9,  "color": "rgba(96,165,250,0.5)"},
        {"symbol": "H", "x": 230, "y": 65, "r": 9,  "color": "rgba(96,165,250,0.5)"},
    ])
    bonds = params.get("bonds", [(0, 1), (0, 2)])

    content = ""

    # Draw bonds first
    for b in bonds:
        if b[0] < len(atoms) and b[1] < len(atoms):
            a1, a2 = atoms[b[0]], atoms[b[1]]
            content += (
                f'<line x1="{a1["x"]}" y1="{a1["y"]}" x2="{a2["x"]}" y2="{a2["y"]}" '
                + f'stroke="rgba(124,111,255,0.35)" stroke-width="2" stroke-linecap="round"/>'
            )

    # Draw atoms
    for atom in atoms:
        content += (
            f'<circle cx="{atom["x"]}" cy="{atom["y"]}" r="{atom["r"]}" '
            + f'fill="{atom["color"]}" stroke="rgba(255,255,255,0.15)" stroke-width="1"/>'
            + f'<text x="{atom["x"]}" y="{atom["y"]+4}" font-family="DM Sans,sans-serif" '
            + f'font-size="10" fill="rgba(238,238,245,0.9)" text-anchor="middle" font-weight="500">'
            + f'{atom["symbol"]}</text>'
        )

    # Formula label
    content += (
        f'<text x="180" y="85" font-family="JetBrains Mono,monospace" font-size="11" '
        + f'fill="rgba(167,139,250,0.85)" text-anchor="middle">{formula}</text>'
    )

    return _svg_wrap(content)


def _graph_curve(params: dict) -> str:
    x_label = params.get("x_label", "x")
    y_label = params.get("y_label", "y")
    curve_type = params.get("curve", "sine")  # sine, parabola, exponential, linear

    # Axes
    content = (
        f'<line x1="40" y1="10" x2="40" y2="80" stroke="rgba(144,144,168,0.4)" stroke-width="1"/>'
        + f'<line x1="40" y1="80" x2="330" y2="80" stroke="rgba(144,144,168,0.4)" stroke-width="1"/>'
        + _arrow(40, 10, 40, 5, color="rgba(144,144,168,0.4)")
        + _arrow(330, 80, 336, 80, color="rgba(144,144,168,0.4)")
        + f'<text x="345" y="84" font-family="JetBrains Mono,monospace" font-size="10" fill="rgba(144,144,168,0.8)">{x_label}</text>'
        + f'<text x="44" y="10" font-family="JetBrains Mono,monospace" font-size="10" fill="rgba(144,144,168,0.8)">{y_label}</text>'
    )

    # Generate curve points
    import math
    pts = []
    width = 280
    height = 60
    ox, oy = 50, 75

    for i in range(101):
        t = i / 100
        x_px = ox + t * width
        if curve_type == "sine":
            y_px = oy - height * 0.4 * (math.sin(t * 2 * math.pi) + 1) / 2 - height * 0.1
        elif curve_type == "parabola":
            y_px = oy - height * 0.7 * (1 - (2 * t - 1) ** 2)
        elif curve_type == "exponential":
            y_px = oy - height * 0.6 * (math.exp(t * 2) - 1) / (math.e ** 2 - 1)
        elif curve_type == "linear":
            y_px = oy - height * 0.6 * t
        else:
            y_px = oy - height * 0.5 * t
        pts.append(f"{x_px:.1f},{y_px:.1f}")

    points_str = " ".join(pts)
    content += (
        f'<polyline points="{points_str}" fill="none" '
        + f'stroke="rgba(124,111,255,0.7)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
    )

    return _svg_wrap(content)


def _process_flow(params: dict) -> str:
    steps = params.get("steps", ["Input", "Process", "Output"])
    colors = [
        "rgba(124,111,255,0.15)", "rgba(34,212,192,0.15)", "rgba(34,212,122,0.15)",
        "rgba(255,179,71,0.15)", "rgba(244,114,182,0.15)",
    ]
    border_colors = [
        "rgba(124,111,255,0.4)", "rgba(34,212,192,0.4)", "rgba(34,212,122,0.4)",
        "rgba(255,179,71,0.4)", "rgba(244,114,182,0.4)",
    ]

    n = len(steps)
    total_width = 320
    step_w = min(80, (total_width - (n - 1) * 20) // n)
    step_h = 36
    start_x = 20
    cy = 40

    content = ""
    for i, step in enumerate(steps):
        x = start_x + i * (step_w + 25)
        color = colors[i % len(colors)]
        border = border_colors[i % len(border_colors)]

        content += (
            f'<rect x="{x}" y="{cy - step_h // 2}" width="{step_w}" height="{step_h}" rx="6" '
            + f'fill="{color}" stroke="{border}" stroke-width="1.2"/>'
            + f'<text x="{x + step_w // 2}" y="{cy + 4}" font-family="DM Sans,sans-serif" '
            + f'font-size="9" fill="rgba(238,238,245,0.85)" text-anchor="middle">{step}</text>'
        )

        # Arrow between steps
        if i < n - 1:
            ax = x + step_w
            content += _arrow(ax, cy, ax + 22, cy,
                              color="rgba(124,111,255,0.4)")

    return _svg_wrap(content)


def _rocket_diagram(params: dict) -> str:
    content = (
        # Rocket body
        '<path d="M 180 15 L 160 50 L 160 70 L 200 70 L 200 50 Z" '
        + 'fill="rgba(124,111,255,0.15)" stroke="rgba(124,111,255,0.5)" stroke-width="1.5"/>'
        # Nose cone
        '<path d="M 180 15 L 165 50 L 195 50 Z" '
        + 'fill="rgba(124,111,255,0.25)" stroke="rgba(124,111,255,0.4)" stroke-width="1"/>'
        # Fins
        '<path d="M 160 65 L 145 78 L 160 72 Z" '
        + 'fill="rgba(34,212,192,0.2)" stroke="rgba(34,212,192,0.4)" stroke-width="1"/>'
        + '<path d="M 200 65 L 215 78 L 200 72 Z" '
        + 'fill="rgba(34,212,192,0.2)" stroke="rgba(34,212,192,0.4)" stroke-width="1"/>'
        # Thrust arrow
        + _arrow(180, 78, 180, 88, color="rgba(255,179,71,0.7)", label="F_thrust")
        # Weight arrow
        + _arrow(175, 50, 175, 20, color="rgba(255,85,85,0.6)", label="W")
    )
    return _svg_wrap(content)


def _circuit_diagram(params: dict) -> str:
    parts = [
        '<rect x="30" y="20" width="300" height="55" rx="0" fill="none" stroke="rgba(124,111,255,0.3)" stroke-width="1.5"/>',
        '<line x1="30" y1="35" x2="30" y2="60" stroke="rgba(255,179,71,0.7)" stroke-width="3" stroke-linecap="round"/>',
        '<line x1="30" y1="40" x2="20" y2="40" stroke="rgba(255,179,71,0.5)" stroke-width="1.5"/>',
        '<line x1="30" y1="55" x2="20" y2="55" stroke="rgba(255,179,71,0.5)" stroke-width="1"/>',
        '<text x="12" y="50" font-family="JetBrains Mono,monospace" font-size="8" fill="rgba(255,179,71,0.8)">V</text>',
        '<rect x="140" y="16" width="60" height="12" rx="2" fill="rgba(34,212,122,0.1)" stroke="rgba(34,212,122,0.5)" stroke-width="1.2"/>',
        '<text x="170" y="26" font-family="DM Sans,sans-serif" font-size="8" fill="rgba(34,212,122,0.8)" text-anchor="middle">R</text>',
        _arrow(80, 20, 110, 20, color="rgba(96,165,250,0.55)", label="I"),
        '<text x="165" y="88" font-family="DM Sans,sans-serif" font-size="9" fill="rgba(144,144,168,0.7)" text-anchor="middle">Simple DC Circuit</text>',
    ]
    content = "".join(parts)
    return _svg_wrap(content)

def figure_html(figure_type: str, params: dict) -> str:
    """Returns HTML-wrapped SVG or empty string."""
    return generate_figure(figure_type, params)
