# Author: rana-mostakin
"""
ThinkTrace v1 — Knowledge Graph Builder
NetworkX + Plotly, dark theme, transparent canvas, exact hex colors.
"""

import json
from typing import Optional
import plotly.graph_objects as go

try:
    import networkx as nx
    HAS_NX = True
except ImportError:
    HAS_NX = False


# ── COLOR CONSTANTS ───────────────────────────────────────────────────────────

NODE_HEALTHY   = dict(fill="rgba(34,212,122,0.10)",  line_color="#22d47a",  line_width=2)
NODE_DEVELOPING= dict(fill="rgba(167,139,250,0.10)", line_color="#a78bfa",  line_width=2)
NODE_GAP       = dict(fill="rgba(255,85,85,0.15)",   line_color="#ff5555",  line_width=2)

EDGE_SOLID  = dict(color="rgba(34,212,122,0.4)",  dash="solid")
EDGE_BROKEN = dict(color="rgba(255,85,85,0.8)",   dash="dash")

BG_COLOR    = "rgba(0,0,0,0)"
PAPER_COLOR = "rgba(0,0,0,0)"
GRID_COLOR  = "rgba(255,255,255,0.05)"
FONT_COLOR  = "#9090a8"

SUBJECT_COLORS = {
    "Physics":     "#7c6fff",
    "Chemistry":   "#22d4c0",
    "Higher Math": "#ffb347",
    "DSAT":        "#60a5fa",
    "IELTS":       "#22d47a",
    "Biology":     "#f472b6",
}


def build_knowledge_graph(graph_data: dict) -> go.Figure:
    """
    Build a Plotly force-directed knowledge graph.
    graph_data: {"nodes": [...], "edges": [...]}
    """
    nodes = graph_data.get("nodes", [])
    edges = graph_data.get("edges", [])

    if not nodes:
        return _empty_graph()

    if HAS_NX:
        return _build_networkx_graph(nodes, edges)
    else:
        return _build_simple_graph(nodes, edges)


def _build_networkx_graph(nodes: list, edges: list) -> go.Figure:
    G = nx.Graph()

    node_map = {n["id"]: n for n in nodes}
    for node in nodes:
        G.add_node(node["id"])

    for edge in edges:
        if edge["source"] in node_map and edge["target"] in node_map:
            G.add_edge(edge["source"], edge["target"])

    # Layout
    if len(nodes) == 1:
        pos = {nodes[0]["id"]: (0.5, 0.5)}
    elif len(nodes) <= 3:
        pos = nx.circular_layout(G)
    else:
        try:
            pos = nx.spring_layout(G, k=2.5, iterations=60, seed=42)
        except Exception:
            pos = nx.circular_layout(G)

    fig = go.Figure()

    # Draw edges
    edge_map = {(e["source"], e["target"]): e for e in edges}
    edge_map.update({(e["target"], e["source"]): e for e in edges})

    for u, v in G.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_data = edge_map.get((u, v), {})
        is_broken = edge_data.get("broken", False)
        ec = EDGE_BROKEN if is_broken else EDGE_SOLID

        fig.add_trace(go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None],
            mode="lines",
            line=dict(
                width=1.5,
                color=ec["color"],
                dash=ec["dash"],
            ),
            hoverinfo="none",
            showlegend=False,
        ))

    # Draw nodes
    for node in nodes:
        nid = node["id"]
        if nid not in pos:
            continue
        x, y = pos[nid]

        strength = node.get("strength", 0.5)
        session_count = node.get("session_count", 1)
        subject = node.get("subject", "")
        is_gap = node.get("is_gap", False)

        # Node size
        size = session_count * 3 + 14

        # Node color
        if is_gap or strength < 0.3:
            nc = NODE_GAP
            text_color = "#ff5555"
        elif strength >= 0.7:
            nc = NODE_HEALTHY
            text_color = "#22d47a"
        else:
            nc = NODE_DEVELOPING
            text_color = "#a78bfa"

        # Subject border color override
        subj_color = SUBJECT_COLORS.get(subject, nc["line_color"])

        hover_text = (
            f"<b style='color:{text_color}'>{nid}</b><br>"
            f"Subject: {subject}<br>"
            f"Strength: {strength:.0%}<br>"
            f"Sessions: {session_count}<br>"
            f"{'<span style=color:#ff5555>Gap detected</span>' if is_gap else 'Healthy'}"
        )

        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode="markers+text",
            marker=dict(
                size=size,
                color=nc["fill"],
                line=dict(color=subj_color, width=nc["line_width"]),
                opacity=1.0,
            ),
            text=[nid],
            textposition="top center",
            textfont=dict(
                family="DM Sans, sans-serif",
                size=10,
                color=FONT_COLOR,
            ),
            hovertemplate=hover_text + "<extra></extra>",
            showlegend=False,
        ))

    # Legend
    legend_traces = [
        ("Healthy (>70%)",    "#22d47a",  "rgba(34,212,122,0.10)"),
        ("Developing (30-70%)","#a78bfa", "rgba(167,139,250,0.10)"),
        ("Gap (<30%)",        "#ff5555",  "rgba(255,85,85,0.15)"),
    ]
    for label, lc, lf in legend_traces:
        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode="markers",
            marker=dict(size=10, color=lf, line=dict(color=lc, width=2)),
            name=label,
            showlegend=True,
        ))

    _apply_dark_layout(fig, title="Knowledge Graph")
    return fig


def _build_simple_graph(nodes: list, edges: list) -> go.Figure:
    """Fallback when NetworkX not available — circular layout."""
    import math

    fig = go.Figure()
    n = len(nodes)
    if n == 0:
        return _empty_graph()

    # Position in circle
    pos = {}
    for i, node in enumerate(nodes):
        angle = 2 * math.pi * i / n
        pos[node["id"]] = (math.cos(angle), math.sin(angle))

    node_map = {n["id"]: n for n in nodes}

    # Edges
    for edge in edges:
        src, tgt = edge.get("source"), edge.get("target")
        if src in pos and tgt in pos:
            x0, y0 = pos[src]
            x1, y1 = pos[tgt]
            is_broken = edge.get("broken", False)
            ec = EDGE_BROKEN if is_broken else EDGE_SOLID
            fig.add_trace(go.Scatter(
                x=[x0, x1, None], y=[y0, y1, None],
                mode="lines",
                line=dict(width=1.5, color=ec["color"], dash=ec["dash"]),
                hoverinfo="none", showlegend=False,
            ))

    # Nodes
    for node in nodes:
        nid = node["id"]
        if nid not in pos:
            continue
        x, y = pos[nid]
        strength = node.get("strength", 0.5)
        is_gap = node.get("is_gap", False)
        session_count = node.get("session_count", 1)
        size = session_count * 3 + 14

        if is_gap or strength < 0.3:
            nc = NODE_GAP
        elif strength >= 0.7:
            nc = NODE_HEALTHY
        else:
            nc = NODE_DEVELOPING

        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode="markers+text",
            marker=dict(size=size, color=nc["fill"],
                        line=dict(color=nc["line_color"], width=nc["line_width"])),
            text=[nid], textposition="top center",
            textfont=dict(family="DM Sans, sans-serif", size=10, color=FONT_COLOR),
            hovertemplate=f"<b>{nid}</b><br>Strength: {strength:.0%}<extra></extra>",
            showlegend=False,
        ))

    _apply_dark_layout(fig, title="Knowledge Graph")
    return fig


def _empty_graph() -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(
        text="No concepts mapped yet.<br>Complete a session to begin building your knowledge graph.",
        xref="paper", yref="paper",
        x=0.5, y=0.5, showarrow=False,
        font=dict(family="DM Sans, sans-serif", size=13, color="#4a4a62"),
        align="center",
    )
    _apply_dark_layout(fig, title="Knowledge Graph")
    return fig


def _apply_dark_layout(fig: go.Figure, title: str = ""):
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(family="Syne, sans-serif", size=15, color="#eeeef5"),
            x=0.02, xanchor="left",
        ) if title else None,
        paper_bgcolor=PAPER_COLOR,
        plot_bgcolor=BG_COLOR,
        font=dict(family="DM Sans, sans-serif", color=FONT_COLOR),
        xaxis=dict(
            showgrid=False, zeroline=False, showticklabels=False,
            gridcolor=GRID_COLOR,
        ),
        yaxis=dict(
            showgrid=False, zeroline=False, showticklabels=False,
            gridcolor=GRID_COLOR,
        ),
        legend=dict(
            bgcolor="rgba(13,13,26,0.85)",
            bordercolor="rgba(255,255,255,0.08)",
            borderwidth=1,
            font=dict(family="DM Sans, sans-serif", size=11, color="#9090a8"),
        ),
        margin=dict(l=20, r=20, t=40, b=20),
        hoverlabel=dict(
            bgcolor="rgba(13,13,26,0.95)",
            bordercolor="rgba(124,111,255,0.4)",
            font=dict(family="DM Sans, sans-serif", size=12, color="#eeeef5"),
        ),
        hovermode="closest",
    )


# ── ACTIVITY CHART ────────────────────────────────────────────────────────────

def build_activity_chart(sessions: list[dict]) -> go.Figure:
    """Build the dashboard line chart: sessions and gaps over time."""
    if not sessions:
        return _empty_line_chart()

    # Group by date
    from collections import defaultdict
    from datetime import datetime

    daily_sessions = defaultdict(int)
    daily_gaps = defaultdict(int)

    for s in sessions:
        try:
            date = s["created_at"][:10]
            daily_sessions[date] += 1
            daily_gaps[date] += len(s.get("gaps", []))
        except Exception:
            pass

    if not daily_sessions:
        return _empty_line_chart()

    dates = sorted(daily_sessions.keys())
    sess_counts = [daily_sessions[d] for d in dates]
    gap_counts = [daily_gaps[d] for d in dates]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates, y=sess_counts,
        mode="lines+markers",
        name="Sessions",
        line=dict(color="#7c6fff", width=2),
        marker=dict(size=5, color="#7c6fff"),
        fill="tozeroy",
        fillcolor="rgba(124,111,255,0.05)",
    ))

    fig.add_trace(go.Scatter(
        x=dates, y=gap_counts,
        mode="lines+markers",
        name="Gaps Found",
        line=dict(color="#ff5555", width=1.5, dash="dot"),
        marker=dict(size=4, color="#ff5555"),
    ))

    fig.update_layout(
        paper_bgcolor=PAPER_COLOR,
        plot_bgcolor=BG_COLOR,
        font=dict(family="DM Sans, sans-serif", color=FONT_COLOR),
        xaxis=dict(
            gridcolor=GRID_COLOR, showgrid=True,
            tickfont=dict(size=10),
            zeroline=False,
        ),
        yaxis=dict(
            gridcolor=GRID_COLOR, showgrid=True,
            tickfont=dict(size=10),
            zeroline=False,
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11, color=FONT_COLOR),
        ),
        margin=dict(l=10, r=10, t=10, b=30),
        hoverlabel=dict(
            bgcolor="rgba(13,13,26,0.95)",
            bordercolor="rgba(124,111,255,0.4)",
            font=dict(family="DM Sans, sans-serif", size=12, color="#eeeef5"),
        ),
        hovermode="x unified",
    )
    return fig


def _empty_line_chart() -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(
        text="No session data yet",
        xref="paper", yref="paper",
        x=0.5, y=0.5, showarrow=False,
        font=dict(family="DM Sans, sans-serif", size=12, color="#4a4a62"),
    )
    fig.update_layout(
        paper_bgcolor=PAPER_COLOR,
        plot_bgcolor=BG_COLOR,
        margin=dict(l=10, r=10, t=10, b=10),
    )
    return fig
