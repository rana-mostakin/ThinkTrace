# Author: rana-mostakin
"""
ThinkTrace v1 — Knowledge Graph Page
Interactive Plotly graph with node/edge analysis and stats.
"""

import streamlit as st
from auth.db import get_knowledge_graph, get_user_sessions
from utils.graph_builder import build_knowledge_graph
from data.subjects import SUBJECT_COLORS


def show_graph():
    user = st.session_state.get("user", {})
    user_id = user.get("id")

    st.markdown("""
    <div style="margin-bottom:1.5rem">
      <div class="tt-h2">Knowledge Graph</div>
      <div style="font-size:13px;color:var(--text2);font-family:'DM Sans',sans-serif;margin-top:4px">
        Spatial map of your conceptual understanding. Red nodes = gaps. Green = healthy.
      </div>
    </div>
    """, unsafe_allow_html=True)

    graph_data = get_knowledge_graph(user_id)
    nodes = graph_data.get("nodes", [])
    edges = graph_data.get("edges", [])

    # Stats bar
    healthy   = sum(1 for n in nodes if not n.get("is_gap") and n.get("strength", 0.5) >= 0.7)
    developing= sum(1 for n in nodes if not n.get("is_gap") and 0.3 <= n.get("strength", 0.5) < 0.7)
    gap_nodes = sum(1 for n in nodes if n.get("is_gap") or n.get("strength", 0.5) < 0.3)
    broken_edges = sum(1 for e in edges if e.get("broken"))
    solid_edges  = len(edges) - broken_edges

    stat_col1, stat_col2, stat_col3, stat_col4, stat_col5 = st.columns(5, gap="small")
    stats = [
        (len(nodes),    "Concepts",       "var(--text2)"),
        (healthy,       "Healthy",        "var(--green)"),
        (developing,    "Developing",     "var(--accent2)"),
        (gap_nodes,     "Gaps",           "var(--red)"),
        (broken_edges,  "Broken Links",   "var(--amber)"),
    ]
    for col, (val, label, color) in zip(
        [stat_col1, stat_col2, stat_col3, stat_col4, stat_col5], stats
    ):
        with col:
            st.markdown(f"""
            <div style="background:var(--glass);border:1px solid var(--border2);
                        border-radius:10px;padding:10px 14px">
              <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;
                          color:{color}">{val}</div>
              <div style="font-size:11px;color:var(--text3);font-family:'DM Sans',sans-serif">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Filter by subject
    subjects_in_graph = list({n.get("subject", "") for n in nodes if n.get("subject")})
    filter_col, _ = st.columns([2, 3])
    with filter_col:
        if subjects_in_graph:
            filter_subject = st.multiselect(
                "Filter by subject",
                options=["All"] + subjects_in_graph,
                default=["All"],
                key="graph_filter",
            )
        else:
            filter_subject = ["All"]

    # Apply filter
    if filter_subject and "All" not in filter_subject:
        filtered_nodes = [n for n in nodes if n.get("subject") in filter_subject]
        filtered_node_ids = {n["id"] for n in filtered_nodes}
        filtered_edges = [e for e in edges
                          if e["source"] in filtered_node_ids and
                          e["target"] in filtered_node_ids]
        filtered_data = {"nodes": filtered_nodes, "edges": filtered_edges}
    else:
        filtered_data = graph_data

    # Main graph
    fig = build_knowledge_graph(filtered_data)
    st.plotly_chart(fig, use_container_width=True,
                    config={"displayModeBar": True,
                            "modeBarButtonsToRemove": ["toImage"],
                            "displaylogo": False})

    # Gap nodes detail
    gap_list = [n for n in filtered_data.get("nodes", [])
                if n.get("is_gap") or n.get("strength", 0.5) < 0.3]

    if gap_list:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            '<div class="tt-h3" style="margin-bottom:0.75rem">Gap Nodes</div>',
            unsafe_allow_html=True,
        )
        for node in gap_list:
            subj = node.get("subject", "")
            color = SUBJECT_COLORS.get(subj, "var(--red)")
            str_pct = int(node.get("strength", 0.1) * 100)
            st.markdown(f"""
            <div style="display:flex;align-items:center;justify-content:space-between;
                        padding:10px 14px;background:rgba(255,85,85,.06);
                        border:1px solid rgba(255,85,85,.15);border-radius:8px;margin-bottom:6px">
              <div>
                <div style="font-family:'DM Sans',sans-serif;font-size:13px;
                            color:var(--text);font-weight:500">{node['id']}</div>
                <div style="font-size:11px;color:{color};margin-top:2px">{subj}</div>
              </div>
              <div style="text-align:right">
                <div style="font-family:'JetBrains Mono',monospace;font-size:11px;
                            color:var(--red)">str {str_pct}%</div>
                <div style="font-size:10px;color:var(--text3);margin-top:2px">
                  {node.get('session_count', 1)} session{"s" if node.get('session_count', 1) != 1 else ""}
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # Broken edges
    broken_list = [e for e in filtered_data.get("edges", []) if e.get("broken")]
    if broken_list:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            '<div class="tt-h3" style="margin-bottom:0.75rem">Broken Causal Links</div>',
            unsafe_allow_html=True,
        )
        for edge in broken_list:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding:8px 14px;
                        background:rgba(255,85,85,.04);border:1px solid rgba(255,85,85,.12);
                        border-radius:8px;margin-bottom:4px">
              <span style="font-family:'JetBrains Mono',monospace;font-size:12px;
                           color:var(--text2)">{edge['source']}</span>
              <span style="color:var(--red);font-size:14px">⟶</span>
              <span style="font-family:'JetBrains Mono',monospace;font-size:12px;
                           color:var(--red)">{edge['target']}</span>
              <span style="font-size:10px;color:var(--text3);margin-left:auto">broken link</span>
            </div>
            """, unsafe_allow_html=True)
