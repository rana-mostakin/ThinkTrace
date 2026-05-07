# ThinkTrace

A Socratic reasoning diagnostic platform for students. Built with Python and Streamlit.

---

## What it does

Most study tools test whether you got the right answer. ThinkTrace does something different — it tests whether you can reason causally between concepts.

When you answer a question, the system does not tell you if you're right or wrong. It asks the next question. One level deeper. Until it finds the exact point in your reasoning chain where the logic breaks. Then it generates a targeted lesson for that specific gap.

The knowledge graph grows as you use it. Green nodes mean solid understanding. Red dashed edges mean broken causal links that need repair.

---

## Live demo

**[https://rana-mostakin-thinktrace.streamlit.app](https://rana-mostakin-thinktrace.streamlit.app)**

No account required to preview the interface. Create an account to start sessions and track your knowledge graph over time.

---

## Subjects covered

| Subject | Topics |
|---|---|
| Physics | Newton's Laws, Kinematics, Thermodynamics, Electrostatics, Optics, and 10 more |
| Chemistry | Atomic Structure, Bonding, Equilibrium, Electrochemistry, and 10 more |
| Higher Math | Calculus, Differential Equations, Linear Algebra, Probability, and 10 more |
| DSAT | Reading, Math, Writing and Grammar (all tested section types) |
| IELTS | Task 1, Task 2, Speaking, Listening, Academic Vocabulary |
| Biology | Cell Biology, Genetics, Evolution, Human Physiology, and 10 more |

Each subject has 15 topics. Each topic has pre-built diagnostic questions for the first two depth levels, so most sessions begin without an API call.

---

## How the cost works

ThinkTrace uses a hybrid question engine. The question bank handles the first two depth levels locally — no API call, no cost. Claude is only invoked from depth 3 onward, and for bridge lessons when a gap is found.

A typical session reaching depth 4 with a gap found costs approximately $0.004 in API usage.

```
Depth 1-2   →  local question bank    (0 API calls)
Depth 3-5   →  Claude API             (1 call per depth)
Bridge      →  Claude API             (1 call if gap found)
Upload      →  Claude API             (1 call per question analyzed)
```

---

## Features

**Socratic engine**
Every AI question has two parts: a warm conversational line, then the diagnostic question itself. The intro reduces defensiveness before the harder probe.

**Auto-generated figures**
Questions involving force, motion, chemical structure, or graphs automatically generate an inline SVG diagram. No images are stored — figures are generated from parameters at render time.

**User question upload**
Paste questions from your own exam papers or textbooks. The system extracts them, identifies the concept being tested, and generates a Socratic probe for each one. Supports plain text and image upload (Claude Vision reads handwritten or printed exam papers).

**Knowledge graph**
Built with NetworkX and rendered with Plotly. Each concept is a node. Each session adds or updates edges between concepts. Broken reasoning links show as dashed red edges. Repaired links turn solid green.

**Spaced repetition**
Concepts that were repaired get scheduled for review at 1-day, 3-day, 7-day, and 14-day intervals. The dashboard shows what is due today.

**Adaptive questioning**
After three sessions, the engine classifies your reasoning style as analytical, visual, procedural, or analogical. Subsequent questions are framed to match how you think.

**50+ languages**
The Socratic dialogue and bridge lessons are delivered in the student's chosen language. Mathematical notation stays in international standard form.

---

## Stack

```
Python 3.11
Streamlit
Anthropic Claude API  (claude-sonnet-4-20250514)
NetworkX
Plotly
SQLite
```

---

## Running locally

Requirements: Python 3.9 or newer, an Anthropic API key.

```bash
git clone https://github.com/rana-mostakin/ThinkTrace.git
cd ThinkTrace/thinktrace

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

export ANTHROPIC_API_KEY=your_key_here

streamlit run app.py
```

Open `http://localhost:8501` in your browser.

First run: the SQLite database is created automatically at `data/thinktrace.db`. Register an account and start a session.

---

## Project structure

```
thinktrace/
├── app.py
├── requirements.txt
│
├── auth/
│   ├── auth_ui.py
│   └── db.py
│
├── engine/
│   ├── socratic.py
│   ├── hybrid_engine.py        Bank first, Claude for depth 3+
│   ├── adaptive.py
│   └── figure_gen.py
│
├── pages/
│   ├── dashboard.py
│   ├── session.py
│   ├── graph.py
│   ├── upload_questions.py     Upload your own exam questions
│   ├── insights.py
│   └── schedule.py
│
├── data/
│   ├── subjects.py
│   ├── languages.py
│   └── question_bank.py        Pre-built questions, depth 1-2
│
└── utils/
    ├── styles.py
    └── graph_builder.py
```

---

## Configuration

| Variable | Required | Default | Description |
|---|---|---|---|
| `ANTHROPIC_API_KEY` | Yes | — | Your Anthropic API key |
| `TT_DB_PATH` | No | `data/thinktrace.db` | Custom SQLite path |
| `TT_MAX_DEPTH` | No | `5` | Maximum Socratic depth per session |

On Streamlit Cloud, set these under Settings → Secrets.

---

## Extending the question bank

The bank in `data/question_bank.py` covers depths 1 and 2 for all 90 topic slots. Adding more questions reduces API usage further.

```python
# Structure: BANK["Subject"]["Topic"][depth] = [question_dict, ...]
{
    "q_intro":        "Warm 1-sentence setup.",
    "q_topic":        "Short label",
    "q_text":         "The question. **Bold** key causal terms.",
    "q_needs_figure": False,
    "q_figure_type":  "none",
    "q_figure_params": {},
    "q_hint":         None,
    "gap_detected":   False,
    "gap_description": "",
    "gap_location":   "",
    "reasoning_style_signal": "unclear",
    "confidence":     0.75,
}
```

No API call is needed for bank questions. They are served instantly from memory.

---

## License

MIT. See `LICENSE`.

---

## Acknowledgements

- [Anthropic](https://anthropic.com) for the Claude API
- [Streamlit](https://streamlit.io) for the deployment platform
- [NetworkX](https://networkx.org) for graph operations
- [Plotly](https://plotly.com) for interactive visualisations
