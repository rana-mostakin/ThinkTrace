# Author: rana-mostakin
"""
ThinkTrace v1 — Complete Subjects & Topics Data
"""

SUBJECTS: dict[str, list[str]] = {
    "Physics": [
        "Newton's Laws", "Kinematics", "Work & Energy", "Momentum",
        "Waves & Sound", "Thermodynamics", "Electrostatics", "Magnetism",
        "Optics", "Quantum Basics", "Circular Motion", "Gravitation",
        "Simple Harmonic Motion", "Fluid Mechanics", "Rotational Motion",
    ],
    "Chemistry": [
        "Atomic Structure", "Periodic Table", "Chemical Bonding", "Stoichiometry",
        "Acids & Bases", "Redox Reactions", "Thermochemistry", "Organic Basics",
        "Equilibrium", "Electrochemistry", "Gas Laws", "Nuclear Chemistry",
        "Reaction Rates", "Solution Chemistry", "Coordination Compounds",
    ],
    "Higher Math": [
        "Limits & Continuity", "Differentiation", "Integration",
        "Differential Equations", "Complex Numbers", "Matrices & Determinants",
        "Vectors", "Probability & Statistics", "Sequences & Series",
        "Conic Sections", "3D Geometry", "Linear Algebra",
        "Number Theory", "Mathematical Induction", "Fourier Basics",
    ],
    "DSAT": [
        "Reading Comprehension", "Evidence Analysis", "Vocabulary in Context",
        "Math: Algebra I", "Math: Algebra II", "Math: Advanced Math",
        "Math: Problem Solving", "Math: Geometry & Trig", "Data Analysis",
        "Writing & Grammar", "Text Structure", "Central Ideas",
        "Cross-text Connections", "Quantitative Reasoning", "Inference & Implication",
    ],
    "IELTS": [
        "Reading Strategies", "Listening Skills", "Writing Task 1 — Graphs",
        "Writing Task 2 — Essay", "Speaking Part 1", "Speaking Part 2 — Cue Card",
        "Speaking Part 3", "Vocabulary Building", "Grammar Accuracy",
        "Cohesion & Coherence", "Academic Word List", "Paraphrasing",
        "Skimming & Scanning", "Note-taking Skills", "Band 7+ Strategies",
    ],
    "Biology": [
        "Cell Biology", "DNA & Genetics", "Evolution", "Human Physiology",
        "Ecology", "Photosynthesis", "Cellular Respiration", "Nervous System",
        "Immune System", "Reproductive Biology", "Biotechnology",
        "Plant Biology", "Protein Synthesis", "Enzymes & Metabolism", "Homeostasis",
    ],
}

SUBJECT_ICONS = {
    "Physics":     "⚛",
    "Chemistry":   "⚗",
    "Higher Math": "∑",
    "DSAT":        "📖",
    "IELTS":       "🌐",
    "Biology":     "🧬",
}

SUBJECT_COLORS = {
    "Physics":     "var(--accent)",
    "Chemistry":   "var(--teal)",
    "Higher Math": "var(--amber)",
    "DSAT":        "var(--blue)",
    "IELTS":       "var(--green)",
    "Biology":     "var(--pink)",
}

MIN_TOPICS = 3


def validate_topics(topics: list[str]) -> tuple[bool, str]:
    """Returns (is_valid, message)."""
    if len(topics) < MIN_TOPICS:
        needed = MIN_TOPICS - len(topics)
        return False, f"Select {needed} more topic{'s' if needed > 1 else ''} to begin ({len(topics)}/{MIN_TOPICS})"
    return True, f"{len(topics)} topics selected — ready to start"
