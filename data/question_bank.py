# Author: rana-mostakin
"""
ThinkTrace — FULL Merged Question Bank (v1 + v2)
================================================

Structure:
  BANK[subject][topic][depth] = [question_dicts]

Subjects (serial order):
  1. Physics
  2. Chemistry
  3. Higher Math
  4. Biology
  5. DSAT
  6. IELTS

Merge rule:
  - Questions from the same topic and depth are appended to the list.
  - Duplicate q_text entries have been removed.
  - All helper functions are placed at the bottom.
"""

import random

# ══════════════════════════════════════════════════════════════════════════════
# SUBJECT 1 — PHYSICS
# ══════════════════════════════════════════════════════════════════════════════

BANK: dict = {

"Physics": {
  # ── Topic 1 ──────────────────────────────────────────────────────────────
  "Newton's Laws": {
    1: [
      # v1
      {"q_intro": "Let's map what you already know about forces.",
       "q_topic": "Newton's Laws", "q_text": "When you push a book across a table and then stop pushing, what causes the book to slow down and stop?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": "Think about what's happening at the contact surface.", "gap_detected": False,
       "gap_description": "", "gap_location": "", "reasoning_style_signal": "unclear", "confidence": 0.7},
      # v2
      {"q_intro": "Let's approach Newton's laws from a different angle.",
       "q_topic": "Newton's Laws",
       "q_text": "You're standing in an elevator that suddenly starts moving upward. You feel heavier. Has your actual weight changed — and what is different about the force the floor exerts on you?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
      {"q_intro": "Newton's Third Law is often misunderstood.",
       "q_topic": "Newton's Laws",
       "q_text": "A horse pulls a cart. By Newton's Third Law, the cart pulls back on the horse with equal force. If the forces are equal and opposite, how does the horse-cart system ever accelerate forward?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": "Action-reaction pairs act on *different* objects.",
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.7},
    ],
    2: [
      # v1
      {"q_intro": "Good — friction is clearly part of your picture. Let's go one level deeper.",
       "q_topic": "Newton's Laws", "q_text": "If friction causes the book to slow down, what exactly is friction *doing* to the book's motion — and why does a heavier book have more friction?",
       "q_needs_figure": True, "q_figure_type": "force_diagram",
       "q_figure_params": {"object": "Book", "forces": [
         {"dir": "right", "label": "F_push", "color": "rgba(124,111,255,0.7)"},
         {"dir": "left", "label": "friction", "color": "rgba(255,85,85,0.7)"},
         {"dir": "up", "label": "N", "color": "rgba(34,212,122,0.7)"},
         {"dir": "down", "label": "mg", "color": "rgba(255,179,71,0.7)"}
       ]},
       "q_hint": None, "gap_detected": False,
       "gap_description": "", "gap_location": "", "reasoning_style_signal": "visual", "confidence": 0.75},
      # v2
      {"q_intro": "Apparent weight vs real weight — let's dig into inertial frames.",
       "q_topic": "Newton's Laws",
       "q_text": "If the elevator cable snaps and the elevator falls freely, you feel weightless — yet gravity is still acting on you. What has changed — and is there a real force that became zero, or just your perception of force?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 2 ──────────────────────────────────────────────────────────────
  "Kinematics": {
    1: [
      {"q_intro": "Let's see how you think about motion.",
       "q_topic": "Kinematics", "q_text": "A car accelerates from rest. After 5 seconds its speed is 20 m/s. What does that tell you about how its position was changing during those 5 seconds?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": "Was the car covering equal distances each second?", "gap_detected": False,
       "gap_description": "", "gap_location": "", "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Right — the speed was changing, so the distance each second was not equal. Let me push on that.",
       "q_topic": "Kinematics", "q_text": "You said the car wasn't covering equal distances each second. What is the *cause* of that increasing distance — is it the velocity that causes acceleration, or the acceleration that causes the changing velocity?",
       "q_needs_figure": True, "q_figure_type": "velocity_diagram",
       "q_figure_params": {"object": "Car", "v0": "0", "vf": "20 m/s", "show_acc": True},
       "q_hint": None, "gap_detected": False,
       "gap_description": "", "gap_location": "", "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 3 ──────────────────────────────────────────────────────────────
  "Work & Energy": {
    1: [
      {"q_intro": "Let's start with a concrete situation.",
       "q_topic": "Work & Energy", "q_text": "You carry a heavy bag horizontally across a room at constant height. Have you done work on the bag in the physics sense? Why or why not?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": "Think about the direction of your force vs the direction of motion.", "gap_detected": False,
       "gap_description": "", "gap_location": "", "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Interesting — you're thinking about force and displacement. Let's sharpen that.",
       "q_topic": "Work & Energy", "q_text": "If work is force times displacement, what happens to the bag's **kinetic energy** when you carry it at constant velocity? Where does the energy from your muscles actually go?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False,
       "gap_description": "", "gap_location": "", "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 4 ──────────────────────────────────────────────────────────────
  "Momentum": {
    1: [
      {"q_intro": "Momentum connects mass and motion in an interesting way.",
       "q_topic": "Momentum", "q_text": "A truck and a bicycle are moving at the same speed. Why is it harder to stop the truck?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Mass clearly matters here. Let's connect that to the collision scenario.",
       "q_topic": "Momentum", "q_text": "If the truck has more momentum, what does conservation of momentum tell us must happen to something else when the truck stops — and what is that 'something else'?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 5 ──────────────────────────────────────────────────────────────
  "Waves & Sound": {
    1: [
      {"q_intro": "Sound is one of those things we experience but rarely examine.",
       "q_topic": "Waves & Sound", "q_text": "When you speak, what is actually traveling from your mouth to someone's ear — is it air molecules themselves moving across the room, or something else?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Good — you're distinguishing medium from wave. Let's probe that further.",
       "q_topic": "Waves & Sound", "q_text": "If the air molecules only vibrate back and forth locally, what exactly is being transferred from your mouth to the ear — and why does it travel at a fixed speed regardless of how loud you speak?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 6 ──────────────────────────────────────────────────────────────
  "Electrostatics": {
    1: [
      {"q_intro": "Let's start with what charge actually means.",
       "q_topic": "Electrostatics", "q_text": "When you rub a plastic rod with wool and it attracts small pieces of paper, what has happened to the rod and why does it attract the paper?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "You've got the charge transfer picture. Let's go one level deeper.",
       "q_topic": "Electrostatics", "q_text": "The paper is electrically neutral — it hasn't gained or lost charge. So why is it *attracted* to the charged rod rather than simply not affected?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": "Think about what happens inside the paper when the rod gets close.", "gap_detected": False,
       "gap_description": "", "gap_location": "", "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 7 ──────────────────────────────────────────────────────────────
  "Gravitation": {
    1: [
      {"q_intro": "Gravity seems obvious but the mechanism is surprisingly subtle.",
       "q_topic": "Gravitation", "q_text": "The Moon orbits Earth, yet it doesn't fall into Earth. Why does it keep moving in a circle instead of either flying away or crashing down?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "The 'falling but missing' idea is the key insight here.",
       "q_topic": "Gravitation", "q_text": "You said it's always falling but moving sideways fast enough. What provides the force that keeps bending its path — and if that force disappeared, what path would the Moon take?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 8 ──────────────────────────────────────────────────────────────
  "Thermodynamics": {
    1: [
      # v1
      {"q_intro": "Let's test your intuition about heat flow.",
       "q_topic": "Thermodynamics", "q_text": "When you hold a metal spoon and a plastic spoon taken from the same drawer, the metal one feels colder. Are they actually at different temperatures?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
      # v2
      {"q_intro": "The laws of thermodynamics constrain what is possible energetically.",
       "q_topic": "Thermodynamics",
       "q_text": "Is it possible to build a refrigerator that cools your food without any electricity or other energy input? Why or why not?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      # v1
      {"q_intro": "Interesting — temperature vs sensation is a real distinction. Let's dig in.",
       "q_topic": "Thermodynamics", "q_text": "If both spoons are at room temperature, what causes the metal one to feel colder — what is actually different between metal and plastic in terms of how they interact with your hand?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
      # v2
      {"q_intro": "The second law forbids it. Let's probe entropy specifically.",
       "q_topic": "Thermodynamics",
       "q_text": "Entropy is often described as 'disorder.' A more precise statement is that entropy measures the number of microstates. Why does heat naturally flow from hot to cold — and why does the reverse never happen spontaneously?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 9 ──────────────────────────────────────────────────────────────
  "Optics": {
    1: [
      {"q_intro": "Light's behavior at boundaries is worth examining carefully.",
       "q_topic": "Optics", "q_text": "When you look at a straw in a glass of water, it appears bent at the water surface. What is actually happening to the light?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Refraction is part of your picture. Let's get at the cause.",
       "q_topic": "Optics", "q_text": "You said the light bends when entering water. *Why* does it bend — what is different about water compared to air that makes light change direction?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": "Think about what light's speed has to do with it.", "gap_detected": False,
       "gap_description": "", "gap_location": "", "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 10 ─────────────────────────────────────────────────────────────
  "Circular Motion": {
    1: [
      {"q_intro": "Circular motion has a counterintuitive force structure.",
       "q_topic": "Circular Motion", "q_text": "When a car goes around a curve, what is actually pushing or pulling it toward the center of the curve?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Friction is your answer — let's test whether the direction is right.",
       "q_topic": "Circular Motion", "q_text": "Friction from the road acts toward the center. If that centripetal force disappeared suddenly, which direction would the car actually move — toward the center, away from it, or tangentially?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "visual", "confidence": 0.75},
    ],
  },
  # ── Topic 11 ─────────────────────────────────────────────────────────────
  "Quantum Basics": {
    1: [
      {"q_intro": "Quantum ideas are strange — let's see where your mental model currently is.",
       "q_topic": "Quantum Basics", "q_text": "What does it mean to say an electron has no definite position until it is measured — where is it before measurement?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "The superposition idea is central. Let's probe what measurement does.",
       "q_topic": "Quantum Basics", "q_text": "You said it exists in superposition before measurement. What does the act of measuring *do* to that superposition — and does the electron 'know' it is being measured?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 12 ─────────────────────────────────────────────────────────────
  "Simple Harmonic Motion": {
    1: [
      {"q_intro": "SHM has a very specific relationship between force and position.",
       "q_topic": "Simple Harmonic Motion", "q_text": "A pendulum swings back and forth. At the extreme ends of the swing, it momentarily stops. What causes it to start moving back toward the center?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Gravity is restoring the pendulum. Let me ask about the relationship.",
       "q_topic": "Simple Harmonic Motion", "q_text": "The restoring force brings it back to center. Is that force constant throughout the swing, or does it change — and if it changes, how does it change with displacement?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 13 ─────────────────────────────────────────────────────────────
  "Fluid Mechanics": {
    1: [
      {"q_intro": "Fluids exert pressure in interesting ways.",
       "q_topic": "Fluid Mechanics", "q_text": "Why does a submarine need to be built much stronger than a surface ship?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Depth and pressure are connected in your answer. Let's get precise.",
       "q_topic": "Fluid Mechanics", "q_text": "You mentioned pressure increases with depth. What is the *physical reason* for that — what is actually pressing down at greater depths that doesn't press at the surface?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 14 ─────────────────────────────────────────────────────────────
  "Magnetism": {
    1: [
      {"q_intro": "Magnetic forces are closely linked to electric ones.",
       "q_topic": "Magnetism", "q_text": "A wire carrying electric current creates a magnetic field around it. What is it about moving charges specifically that creates a magnetic field?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Moving charge — let's test whether that distinction matters.",
       "q_topic": "Magnetism", "q_text": "A stationary charge creates an electric field but no magnetic field. A moving charge creates both. What changes physically when the charge starts moving — and is this consistent with relativity?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 15 ─────────────────────────────────────────────────────────────
  "Rotational Motion": {
    1: [
      {"q_intro": "Rotation has its own version of Newton's second law.",
       "q_topic": "Rotational Motion", "q_text": "A figure skater spins faster when they pull their arms in. What causes the speed to increase if no one is pushing them?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Conservation is the key. Let's test your understanding of moment of inertia.",
       "q_topic": "Rotational Motion", "q_text": "You said angular momentum is conserved. When the skater pulls their arms in, what physical quantity decreases — and what must therefore increase to keep the product constant?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
},  # end Physics

# ══════════════════════════════════════════════════════════════════════════════
# SUBJECT 2 — CHEMISTRY
# ══════════════════════════════════════════════════════════════════════════════

"Chemistry": {
  # ── Topic 1 ──────────────────────────────────────────────────────────────
  "Atomic Structure": {
    1: [
      {"q_intro": "Let's start with what an atom actually looks like.",
       "q_topic": "Atomic Structure", "q_text": "An atom is described as mostly empty space. What does that mean — where is the mass concentrated, and what occupies the rest of the space?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Good — nucleus and electron cloud. Let's probe the electron's location.",
       "q_topic": "Atomic Structure", "q_text": "You said electrons orbit the nucleus. But the Bohr model was replaced — what is the modern understanding of where an electron actually *is*, and what does an orbital represent?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 2 ──────────────────────────────────────────────────────────────
  "Chemical Bonding": {
    1: [
      {"q_intro": "Bonds are about electron sharing — but why do atoms share?",
       "q_topic": "Chemical Bonding", "q_text": "Why do two hydrogen atoms bond together to form H₂ instead of staying as separate atoms?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Energy stability is the key. Let's probe what 'lower energy' means here.",
       "q_topic": "Chemical Bonding", "q_text": "You said the bonded state has lower energy. What is it about sharing electrons between two nuclei that makes the system more stable — where physically is the energy being lowered?",
       "q_needs_figure": True, "q_figure_type": "molecular",
       "q_figure_params": {"formula": "H₂", "atoms": [
         {"symbol": "H", "x": 150, "y": 45, "r": 12, "color": "rgba(96,165,250,0.5)"},
         {"symbol": "H", "x": 210, "y": 45, "r": 12, "color": "rgba(96,165,250,0.5)"}
       ], "bonds": [(0, 1)]},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "visual", "confidence": 0.75},
    ],
  },
  # ── Topic 3 ──────────────────────────────────────────────────────────────
  "Acids & Bases": {
    1: [
      # v1
      {"q_intro": "Acids and bases come in different definitions — let's see which one you're using.",
       "q_topic": "Acids & Bases", "q_text": "What makes something an acid in water — what does an acid actually *do* when dissolved?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
      # v2
      {"q_intro": "The pH scale is logarithmic — that has real consequences.",
       "q_topic": "Acids & Bases",
       "q_text": "A solution has pH 3. Another has pH 5. How many times more acidic is the pH 3 solution — and why is the answer not 'twice as acidic'?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.7},
    ],
    2: [
      # v1
      {"q_intro": "H⁺ donation is the Arrhenius view. Let's test a harder case.",
       "q_topic": "Acids & Bases", "q_text": "Ammonia (NH₃) acts as a base but contains no OH⁻ ions. Using only proton transfer ideas, explain how NH₃ behaves as a base when dissolved in water.",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
      # v2
      {"q_intro": "100 times more acidic — logarithmic scale. Let's push on buffer solutions.",
       "q_topic": "Acids & Bases",
       "q_text": "A buffer solution resists changes in pH. It contains a weak acid and its conjugate base. When you add a small amount of strong acid to a buffer, what exactly happens at the molecular level that prevents the pH from dropping sharply?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 4 ──────────────────────────────────────────────────────────────
  "Stoichiometry": {
    1: [
      {"q_intro": "Stoichiometry is fundamentally about counting particles.",
       "q_topic": "Stoichiometry", "q_text": "Why do chemists use moles instead of just counting individual atoms or molecules directly?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Scale is the reason — let's connect moles to actual measurements.",
       "q_topic": "Stoichiometry", "q_text": "One mole of carbon has a mass of 12 g. When you balance the equation C + O₂ → CO₂, does the '1:1' ratio refer to grams, moles, or individual atoms — and are those all the same thing?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 5 ──────────────────────────────────────────────────────────────
  "Gas Laws": {
    1: [
      {"q_intro": "Gas behavior connects pressure, volume, and temperature.",
       "q_topic": "Gas Laws", "q_text": "When you heat a sealed container of gas, the pressure increases. What is happening at the molecular level that causes the pressure to rise?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Molecular speed and collisions — let's be precise about the mechanism.",
       "q_topic": "Gas Laws", "q_text": "You said faster molecules hit the walls harder. If the volume is fixed and temperature doubles, does pressure exactly double? And what assumption about the gas makes that true?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 6 ──────────────────────────────────────────────────────────────
  "Redox Reactions": {
    1: [
      {"q_intro": "Oxidation and reduction are always paired.",
       "q_topic": "Redox Reactions", "q_text": "When iron rusts, what is being oxidized and what is being reduced — and what exactly is transferred between them?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Electron transfer is the core. Let's test whether oxidation number makes sense here.",
       "q_topic": "Redox Reactions", "q_text": "Iron loses electrons to oxygen. What causes iron to 'want' to give up electrons — and why doesn't the reverse happen (oxygen giving electrons to iron)?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 7 ──────────────────────────────────────────────────────────────
  "Equilibrium": {
    1: [
      # v1
      {"q_intro": "Chemical equilibrium is dynamic, not static.",
       "q_topic": "Equilibrium", "q_text": "When a reaction reaches equilibrium, does it stop? What is actually happening at the molecular level when we say the system is 'at equilibrium'?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
      # v2
      {"q_intro": "Equilibrium constants encode a lot of chemical information.",
       "q_topic": "Equilibrium",
       "q_text": "The equilibrium constant K for a reaction is very large (K >> 1). Without doing any calculation, what does this tell you about the relative amounts of products and reactants at equilibrium?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.7},
    ],
    2: [
      # v1
      {"q_intro": "Dynamic balance — both directions are still happening. Let's push on Le Chatelier.",
       "q_topic": "Equilibrium", "q_text": "If you add more reactant to a system at equilibrium, the reaction shifts forward. What *causes* that shift at the molecular level — is it a 'decision' the molecules make, or a statistical consequence?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
      # v2
      {"q_intro": "Mostly products — let's test what K does and doesn't tell you.",
       "q_topic": "Equilibrium",
       "q_text": "A large K means mostly products at equilibrium. Does it tell you how *fast* equilibrium is reached — and can a reaction with K >> 1 still be practically useless for making products? Explain.",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 8 ──────────────────────────────────────────────────────────────
  "Thermochemistry": {
    1: [
      {"q_intro": "Energy in chemical reactions is worth examining carefully.",
       "q_topic": "Thermochemistry", "q_text": "When methane burns, heat is released. Where was that energy stored *before* the reaction, and where does it go *after*?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Bond energy is your answer. Let's test whether breaking vs forming matters.",
       "q_topic": "Thermochemistry", "q_text": "Breaking bonds requires energy; forming bonds releases energy. In an exothermic reaction, which process releases more energy overall — bond breaking or bond forming?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 9 ──────────────────────────────────────────────────────────────
  "Periodic Table": {
    1: [
      {"q_intro": "The periodic table's arrangement encodes physical patterns.",
       "q_topic": "Periodic Table", "q_text": "Why do elements in the same column (group) of the periodic table have similar chemical properties?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Valence electrons — let's test whether that explains reactivity direction.",
       "q_topic": "Periodic Table", "q_text": "Sodium and potassium are both in Group 1 and both react with water. Potassium reacts more violently. What changes about the outer electron as you go down the group that explains this?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 10 ─────────────────────────────────────────────────────────────
  "Organic Basics": {
    1: [
      {"q_intro": "Organic chemistry is built on carbon's bonding behavior.",
       "q_topic": "Organic Basics", "q_text": "Carbon can form four bonds and creates long chains. What property of carbon's electron structure makes it uniquely suited to form so many different stable molecules?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Four bonds and stability — let's probe functional groups.",
       "q_topic": "Organic Basics", "q_text": "Ethanol (C₂H₅OH) and dimethyl ether (CH₃OCH₃) have the same molecular formula C₂H₆O but very different boiling points. What structural difference causes this?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 11 ─────────────────────────────────────────────────────────────
  "Reaction Rates": {
    1: [
      {"q_intro": "Reaction rate is about how often the right collisions happen.",
       "q_topic": "Reaction Rates", "q_text": "Why does increasing temperature increase the rate of most chemical reactions?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Collision frequency and energy — let's separate those two factors.",
       "q_topic": "Reaction Rates", "q_text": "At higher temperature, molecules collide more often AND with more energy. Which factor matters more for rate, and what is the **activation energy** threshold telling us?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 12 ─────────────────────────────────────────────────────────────
  "Electrochemistry": {
    1: [
      {"q_intro": "Electrochemistry connects redox chemistry to electrical work.",
       "q_topic": "Electrochemistry", "q_text": "In a battery, what is actually moving through the external circuit — electrons, ions, or both?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Electrons externally, ions internally — let's test whether direction matters.",
       "q_topic": "Electrochemistry", "q_text": "Electrons flow from the negative terminal through the circuit. At which electrode — anode or cathode — is oxidation occurring, and why does that determine which terminal is negative?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 13 ─────────────────────────────────────────────────────────────
  "Nuclear Chemistry": {
    1: [
      {"q_intro": "Nuclear reactions are fundamentally different from chemical reactions.",
       "q_topic": "Nuclear Chemistry", "q_text": "In nuclear fission, a uranium nucleus splits and releases enormous energy. Where does that energy come from — what is its source?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Mass-energy equivalence (E=mc²) — let's test the mechanism.",
       "q_topic": "Nuclear Chemistry", "q_text": "You mentioned mass converts to energy. The products of fission have slightly less total mass than the original uranium nucleus. What was holding that 'missing mass' in the original nucleus before fission?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 14 ─────────────────────────────────────────────────────────────
  "Solution Chemistry": {
    1: [
      {"q_intro": "Dissolving is more than just mixing.",
       "q_topic": "Solution Chemistry", "q_text": "When salt dissolves in water, what actually happens to the sodium and chloride ions — and why does water dissolve ionic compounds so well?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Hydration shells — let's test whether polarity is the key.",
       "q_topic": "Solution Chemistry", "q_text": "Water dissolves NaCl but not oil. What specific property of the water molecule — not just 'polarity' generally — allows it to surround and stabilize individual ions?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 15 ─────────────────────────────────────────────────────────────
  "Coordination Compounds": {
    1: [
      {"q_intro": "Coordination chemistry involves ligands donating electrons to metals.",
       "q_topic": "Coordination Compounds", "q_text": "What makes a molecule or ion a 'ligand' — what must it have, and what does it donate to the central metal ion?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Lone pair donors — let's test whether that explains colour.",
       "q_topic": "Coordination Compounds", "q_text": "Many coordination compounds are brightly coloured. Using crystal field theory ideas, what happens to the d-orbitals of the metal when ligands approach — and how does that cause specific wavelengths of light to be absorbed?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
},  # end Chemistry

# ══════════════════════════════════════════════════════════════════════════════
# SUBJECT 3 — HIGHER MATH
# ══════════════════════════════════════════════════════════════════════════════

"Higher Math": {
  # ── Topic 1 ──────────────────────────────────────────────────────────────
  "Limits & Continuity": {
    1: [
      {"q_intro": "Limits are about approach, not arrival.",
       "q_topic": "Limits & Continuity", "q_text": "What does it mean to say the limit of f(x) as x→2 equals 5? Does x ever actually reach 2?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Approach without arrival — let's test continuity.",
       "q_topic": "Limits & Continuity", "q_text": "A function can have a limit at a point but still be discontinuous there. How is that possible — give the conditions that would make it happen?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 2 ──────────────────────────────────────────────────────────────
  "Differentiation": {
    1: [
      # v1
      {"q_intro": "The derivative encodes rate of change.",
       "q_topic": "Differentiation", "q_text": "What does the derivative of a function at a point represent geometrically — what are you actually measuring?",
       "q_needs_figure": True, "q_figure_type": "graph_curve",
       "q_figure_params": {"x_label": "x", "y_label": "f(x)", "curve": "parabola"},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "visual", "confidence": 0.7},
      # v2
      {"q_intro": "The chain rule is one of the most important differentiation techniques.",
       "q_topic": "Differentiation",
       "q_text": "To differentiate y = sin(x²), you cannot just differentiate sin and then differentiate x² separately and add them. Why not — and what is the chain rule telling you to do instead?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.7},
    ],
    2: [
      # v1
      {"q_intro": "Slope of the tangent — let's connect that to the limit definition.",
       "q_topic": "Differentiation", "q_text": "The derivative is defined as a limit of a difference quotient. What does the difference quotient [f(x+h)−f(x)]/h represent geometrically, and what happens geometrically as h→0?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "visual", "confidence": 0.75},
      # v2
      {"q_intro": "Composition of functions requires the chain rule. Let's test implicit differentiation.",
       "q_topic": "Differentiation",
       "q_text": "To differentiate x² + y² = 25, we use implicit differentiation and get dy/dx = −x/y. What does it mean to differentiate 'implicitly' — and why can't we simply rearrange for y first and then differentiate?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 3 ──────────────────────────────────────────────────────────────
  "Integration": {
    1: [
      {"q_intro": "Integration is the accumulation of infinitely small pieces.",
       "q_topic": "Integration", "q_text": "What does the definite integral ∫₀³ f(x)dx represent geometrically — what are you calculating?",
       "q_needs_figure": True, "q_figure_type": "graph_curve",
       "q_figure_params": {"x_label": "x", "y_label": "f(x)", "curve": "parabola"},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "visual", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Area under the curve — let's connect that to antiderivatives.",
       "q_topic": "Integration", "q_text": "The Fundamental Theorem of Calculus says that integration and differentiation are inverses. What does it mean geometrically that the area under a curve is related to a function whose derivative is f(x)?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 4 ──────────────────────────────────────────────────────────────
  "Complex Numbers": {
    1: [
      {"q_intro": "Complex numbers extend the real number line to a plane.",
       "q_topic": "Complex Numbers", "q_text": "What does it mean geometrically to multiply two complex numbers together — what happens in the complex plane?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Rotation and scaling — let's test this with a specific case.",
       "q_topic": "Complex Numbers", "q_text": "Multiplying by i rotates a complex number by 90°. Multiplying i by i gives −1. How does this geometric interpretation explain why i²=−1 makes sense?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "visual", "confidence": 0.75},
    ],
  },
  # ── Topic 5 ──────────────────────────────────────────────────────────────
  "Probability & Statistics": {
    1: [
      # v1
      {"q_intro": "Probability and statistics measure uncertainty in different ways.",
       "q_topic": "Probability & Statistics", "q_text": "What is the difference between the mean and the median of a dataset — when would you prefer one over the other?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
      # v2
      {"q_intro": "Conditional probability is one of the most counterintuitive areas of statistics.",
       "q_topic": "Probability & Statistics",
       "q_text": "A disease affects 1 in 1000 people. A test is 99% accurate. You test positive. What is the probability you actually have the disease — is it 99%, much higher, or much lower?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": "Think about how many people test positive among those who don't have the disease.",
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.7},
    ],
    2: [
      # v1
      {"q_intro": "Resistance to outliers — let's connect that to the math.",
       "q_topic": "Probability & Statistics", "q_text": "If the median is resistant to outliers but the mean is not, what property of the mean's formula makes it sensitive to extreme values — and what does that imply about using mean vs median for income data?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
      # v2
      {"q_intro": "Base rate fallacy — the result is much lower than 99%. Let's formalize it.",
       "q_topic": "Probability & Statistics",
       "q_text": "Bayes' theorem: P(A|B) = P(B|A)×P(A) / P(B). In the disease example, what does each term represent — and which term is the 'base rate' that most people ignore?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 6 ──────────────────────────────────────────────────────────────
  "Vectors": {
    1: [
      {"q_intro": "Vectors carry both magnitude and direction.",
       "q_topic": "Vectors", "q_text": "What is the geometric meaning of the dot product of two vectors — what does a zero dot product tell you about the vectors?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Perpendicularity and projection — let's push on the cross product.",
       "q_topic": "Vectors", "q_text": "The cross product of two vectors produces a third vector perpendicular to both. What does the *magnitude* of that cross product represent geometrically?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "visual", "confidence": 0.75},
    ],
  },
  # ── Topic 7 ──────────────────────────────────────────────────────────────
  "Matrices & Determinants": {
    1: [
      {"q_intro": "Matrices encode linear transformations.",
       "q_topic": "Matrices & Determinants", "q_text": "What does a matrix multiplication actually do geometrically — if you multiply a vector by a matrix, what happens to the vector?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Linear transformation — let's test the determinant.",
       "q_topic": "Matrices & Determinants", "q_text": "The determinant of a 2×2 matrix equals zero means the matrix is non-invertible. What does this mean geometrically — what has happened to the transformation of space?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "visual", "confidence": 0.75},
    ],
  },
  # ── Topic 8 ──────────────────────────────────────────────────────────────
  "Sequences & Series": {
    1: [
      {"q_intro": "Convergence is about whether an infinite process has a finite result.",
       "q_topic": "Sequences & Series", "q_text": "The series 1 + 1/2 + 1/4 + 1/8 + ... converges to 2. How can infinitely many positive numbers add up to a finite value?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Terms shrinking fast enough — let's test the harmonic series.",
       "q_topic": "Sequences & Series", "q_text": "The harmonic series 1 + 1/2 + 1/3 + 1/4 + ... also has terms approaching zero, yet it diverges. How is this consistent with what you just said about convergence?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 9 ──────────────────────────────────────────────────────────────
  "Differential Equations": {
    1: [
      {"q_intro": "Differential equations describe rates of change.",
       "q_topic": "Differential Equations", "q_text": "What does the equation dy/dx = ky mean in plain language — what is it saying about how y changes?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Rate proportional to current value — that's exponential growth/decay.",
       "q_topic": "Differential Equations", "q_text": "The solution to dy/dx = ky is y = Ce^(kx). What does the constant C represent, and why can't a differential equation have a unique solution without an initial condition?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 10 ─────────────────────────────────────────────────────────────
  "Conic Sections": {
    1: [
      {"q_intro": "Conics come from slicing a cone — or from distance definitions.",
       "q_topic": "Conic Sections", "q_text": "An ellipse is defined as a set of points where the sum of distances to two fixed points is constant. Why does that definition produce an oval shape?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Constant sum of distances — let's connect that to planetary orbits.",
       "q_topic": "Conic Sections", "q_text": "The two fixed points of an ellipse are called foci. When Earth orbits the Sun in an elliptical path, where is the Sun relative to those foci — at the center, at one focus, or between them?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 11 ─────────────────────────────────────────────────────────────
  "3D Geometry": {
    1: [
      {"q_intro": "Three-dimensional geometry extends 2D intuitions.",
       "q_topic": "3D Geometry", "q_text": "A line and a plane in 3D space can be parallel, intersecting, or the line can lie inside the plane. How many intersection cases are there between two planes in 3D?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Parallel, identical, or intersecting in a line — let's test the normal vector.",
       "q_topic": "3D Geometry", "q_text": "Two planes with the same normal vector must be parallel or identical. What does the normal vector of a plane actually represent geometrically, and how do you find it from the plane's equation?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 12 ─────────────────────────────────────────────────────────────
  "Linear Algebra": {
    1: [
      {"q_intro": "Linear algebra is about spaces and transformations.",
       "q_topic": "Linear Algebra", "q_text": "What does it mean for a set of vectors to be 'linearly independent'?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "None can be written as a combination of the others — let's connect that to rank.",
       "q_topic": "Linear Algebra", "q_text": "If three vectors in 3D space are linearly dependent, what does that tell you about the geometric relationship between them — and what does it mean for the rank of the matrix they form?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "visual", "confidence": 0.75},
    ],
  },
  # ── Topic 13 ─────────────────────────────────────────────────────────────
  "Number Theory": {
    1: [
      {"q_intro": "Number theory deals with deep properties of integers.",
       "q_topic": "Number Theory", "q_text": "Why are there infinitely many prime numbers — what breaks down if you assume there are only finitely many?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Euclid's proof by contradiction — let's test whether you can reconstruct the key step.",
       "q_topic": "Number Theory", "q_text": "In Euclid's proof, you form N = (p₁ × p₂ × ... × pₙ) + 1. Why must N either be prime itself or have a prime factor not in the original list?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 14 ─────────────────────────────────────────────────────────────
  "Mathematical Induction": {
    1: [
      {"q_intro": "Induction is a way of proving statements about all natural numbers.",
       "q_topic": "Mathematical Induction", "q_text": "In a proof by induction you prove a base case and then an inductive step. Why does proving 'if P(k) then P(k+1)' together with P(1) guarantee P(n) for all n?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Domino chain — let's test a common mistake.",
       "q_topic": "Mathematical Induction", "q_text": "Some students prove the inductive step P(k)→P(k+1) correctly but skip verifying the base case, and the 'proof' is wrong. Give a concrete example where the inductive step holds but the statement is false for all n.",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 15 ─────────────────────────────────────────────────────────────
  "Fourier Basics": {
    1: [
      {"q_intro": "Fourier analysis decomposes signals into frequencies.",
       "q_topic": "Fourier Basics", "q_text": "What does it mean to say that any periodic function can be represented as a sum of sines and cosines — is that surprising, and why?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Basis functions for function space — let's test what the coefficients mean.",
       "q_topic": "Fourier Basics", "q_text": "The Fourier coefficients tell you 'how much' of each frequency is in the signal. What is the mathematical operation that extracts a specific coefficient — and why does it work?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
},  # end Higher Math

# ══════════════════════════════════════════════════════════════════════════════
# SUBJECT 4 — BIOLOGY
# ══════════════════════════════════════════════════════════════════════════════

"Biology": {
  # ── Topic 1 ──────────────────────────────────────────────────────────────
  "Cell Biology": {
    1: [
      {"q_intro": "The cell membrane controls everything entering and leaving.",
       "q_topic": "Cell Biology", "q_text": "What is the cell membrane made of, and how does its structure relate to what it allows to pass through?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Phospholipid bilayer — let's test selective permeability.",
       "q_topic": "Cell Biology", "q_text": "Oxygen crosses the cell membrane freely but glucose cannot. Both are small molecules. What property of the membrane explains this difference — and what does glucose need to cross?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 2 ──────────────────────────────────────────────────────────────
  "DNA & Genetics": {
    1: [
      # v1
      {"q_intro": "DNA encodes information in a very specific chemical way.",
       "q_topic": "DNA & Genetics", "q_text": "DNA is described as a double helix. What exactly is 'double' about it, and why do the two strands stay together?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
      # v2
      {"q_intro": "Mutations are changes in DNA — but not all mutations have effects.",
       "q_topic": "DNA & Genetics",
       "q_text": "A single base substitution mutation changes one DNA letter. In many cases this has no effect on the protein produced. How is that possible — doesn't every change to the code change the protein?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": "Think about how many codons code for each amino acid.",
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.7},
    ],
    2: [
      # v1
      {"q_intro": "Complementary base pairing — let's test the replication logic.",
       "q_topic": "DNA & Genetics", "q_text": "During DNA replication, each strand serves as a template for a new complementary strand. Why does this mechanism guarantee that the two daughter cells get identical genetic information?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
      # v2
      {"q_intro": "Redundancy in the genetic code — 64 codons for 20 amino acids. Let's test epigenetics.",
       "q_topic": "DNA & Genetics",
       "q_text": "Identical twins have the same DNA sequence but can have different health outcomes, personalities, and even different diseases as adults. What does epigenetics offer as an explanation — and what is the difference between a genetic change and an epigenetic change?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 3 ──────────────────────────────────────────────────────────────
  "Photosynthesis": {
    1: [
      {"q_intro": "Photosynthesis converts light energy into chemical energy.",
       "q_topic": "Photosynthesis", "q_text": "Plants take in CO₂ and water and produce glucose and oxygen. Where does the oxygen come from — is it from the CO₂ or from the water?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Water is split — the oxygen comes from water. Let's connect the two stages.",
       "q_topic": "Photosynthesis", "q_text": "Photosynthesis has a light-dependent stage and a light-independent stage (Calvin cycle). What does the light-dependent stage produce that the Calvin cycle needs — and what would happen to the Calvin cycle if light were suddenly removed?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 4 ──────────────────────────────────────────────────────────────
  "Cellular Respiration": {
    1: [
      {"q_intro": "Cellular respiration extracts energy from glucose.",
       "q_topic": "Cellular Respiration", "q_text": "Cellular respiration and burning both 'combust' glucose with oxygen. What is fundamentally different about how the energy is released in cellular respiration versus a flame?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Controlled, stepwise release — let's probe where ATP fits in.",
       "q_topic": "Cellular Respiration", "q_text": "ATP is described as the 'energy currency' of the cell. What does ATP actually do when it releases energy — what physical event happens, and why is that useful for driving cellular reactions?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 5 ──────────────────────────────────────────────────────────────
  "Evolution": {
    1: [
      # v1
      {"q_intro": "Natural selection acts on variation within populations.",
       "q_topic": "Evolution", "q_text": "If giraffes with longer necks survived better and passed on that trait, why didn't all giraffes quickly become identical with perfectly long necks?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
      # v2
      {"q_intro": "Evolution is often misunderstood as having a direction or goal.",
       "q_topic": "Evolution",
       "q_text": "A student says 'Humans evolved from chimpanzees.' A biologist says this is incorrect. What is the accurate statement — and what does it mean to share a 'common ancestor'?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      # v1
      {"q_intro": "Maintained variation is key to evolution continuing.",
       "q_topic": "Evolution", "q_text": "What are two mechanisms that continuously generate new variation in a population — without which natural selection would eventually have nothing to act on?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
      # v2
      {"q_intro": "Branching, not linear — let's test whether evolution can go 'backward'.",
       "q_topic": "Evolution",
       "q_text": "Cave fish that live in permanent darkness have lost their eyes over many generations. Did they 'choose' to lose their eyes, or was the loss an accident that spread? Explain the evolutionary mechanism that caused this — and what does it tell you about whether evolution has direction?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 6 ──────────────────────────────────────────────────────────────
  "Nervous System": {
    1: [
      {"q_intro": "Nerve signals are electrical, but not quite like household electricity.",
       "q_topic": "Nervous System", "q_text": "How does a nerve impulse travel along a neuron — what is actually moving, electrons or ions?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Ion flow across the membrane — let's test the synapse.",
       "q_topic": "Nervous System", "q_text": "When a nerve impulse reaches a synapse, there is a gap the electrical signal cannot cross. How does the signal get from one neuron to the next — and why does this junction allow the nervous system to be regulated?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 7 ──────────────────────────────────────────────────────────────
  "Immune System": {
    1: [
      {"q_intro": "The immune system must distinguish self from non-self.",
       "q_topic": "Immune System", "q_text": "How does your immune system know which cells are 'you' and which are foreign invaders to be attacked?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Cell surface markers — let's test vaccine logic.",
       "q_topic": "Immune System", "q_text": "A vaccine introduces a weakened or partial pathogen to create immunity. Using your understanding of how the immune system recognizes invaders, explain mechanistically why a second exposure to the real pathogen produces a much faster response.",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 8 ──────────────────────────────────────────────────────────────
  "Human Physiology": {
    1: [
      {"q_intro": "The heart is a pump, but the mechanism is worth examining.",
       "q_topic": "Human Physiology", "q_text": "The heart pumps blood in one direction. What prevents blood from flowing backwards between heartbeats?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Valves control direction — let's test the pulmonary circuit.",
       "q_topic": "Human Physiology", "q_text": "Blood goes to the lungs and back to the heart before going to the rest of the body. Why does it need to return to the heart between those two journeys rather than going directly from lungs to body?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 9 ──────────────────────────────────────────────────────────────
  "Ecology": {
    1: [
      {"q_intro": "Energy flows through ecosystems in one direction.",
       "q_topic": "Ecology", "q_text": "Why does an ecosystem support far more plants than herbivores, and far more herbivores than carnivores?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Energy loss at each trophic level — let's quantify the mechanism.",
       "q_topic": "Ecology", "q_text": "Only about 10% of energy passes from one trophic level to the next. Where does the other 90% go — and why is this a consequence of thermodynamics rather than inefficiency in the organisms?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 10 ─────────────────────────────────────────────────────────────
  "Protein Synthesis": {
    1: [
      {"q_intro": "DNA doesn't make proteins directly — there's an intermediary.",
       "q_topic": "Protein Synthesis", "q_text": "What is mRNA and why is it needed — why can't ribosomes read DNA directly to make proteins?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Compartmentalization is part of the answer. Let's test the codon logic.",
       "q_topic": "Protein Synthesis", "q_text": "The genetic code uses 3-nucleotide codons to specify amino acids. Why are 3 nucleotides used rather than 2 — what goes wrong mathematically with just 2?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 11 ─────────────────────────────────────────────────────────────
  "Enzymes & Metabolism": {
    1: [
      {"q_intro": "Enzymes are catalysts — let's be precise about what that means.",
       "q_topic": "Enzymes & Metabolism", "q_text": "Enzymes speed up reactions but are not consumed. What do they actually do to the reaction — what changes when an enzyme is present?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Lowering activation energy — let's test why enzyme shape matters.",
       "q_topic": "Enzymes & Metabolism", "q_text": "Changing the temperature slightly can completely stop an enzyme from working, even though the substrate is still present. What happens to the enzyme at high temperature that explains this?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 12 ─────────────────────────────────────────────────────────────
  "Homeostasis": {
    1: [
      {"q_intro": "Homeostasis maintains internal stability through feedback.",
       "q_topic": "Homeostasis", "q_text": "Your body temperature stays near 37°C whether it's hot or cold outside. What type of mechanism achieves this — and what happens when the temperature deviates?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Negative feedback — let's test why positive feedback would be dangerous here.",
       "q_topic": "Homeostasis", "q_text": "Negative feedback opposes a deviation. Positive feedback amplifies it. Why would positive feedback be dangerous for body temperature regulation — and give one example where the body intentionally uses positive feedback?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 13 ─────────────────────────────────────────────────────────────
  "Biotechnology": {
    1: [
      {"q_intro": "CRISPR allows precise editing of DNA.",
       "q_topic": "Biotechnology", "q_text": "CRISPR-Cas9 can cut DNA at a specific location in the genome. What guides it to the exact right location among billions of base pairs?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Guide RNA provides the address — let's test what happens after cutting.",
       "q_topic": "Biotechnology", "q_text": "After Cas9 cuts the DNA, the cell tries to repair the break. There are two repair pathways. One is error-prone (NHEJ) and one is precise (HDR). What determines which pathway is used, and how do researchers exploit this choice?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 14 ─────────────────────────────────────────────────────────────
  "Plant Biology": {
    1: [
      {"q_intro": "Plants face unique challenges that animals solve differently.",
       "q_topic": "Plant Biology", "q_text": "Water travels from a plant's roots all the way up to leaves many meters above the ground. There's no pump like a heart. What drives this upward movement?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Transpiration pull and cohesion — let's test the limits.",
       "q_topic": "Plant Biology", "q_text": "Transpiration from leaves pulls water up. Water molecules stay connected via hydrogen bonding (cohesion). What would happen to this column of water on a very humid day with no evaporation — and how do tall trees manage this?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 15 ─────────────────────────────────────────────────────────────
  "Reproductive Biology": {
    1: [
      {"q_intro": "Meiosis produces cells with half the chromosome number.",
       "q_topic": "Reproductive Biology", "q_text": "Why does sexual reproduction require meiosis — what would happen if gametes were produced by ordinary cell division (mitosis)?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Chromosome number would double each generation — that's the mathematical reason.",
       "q_topic": "Reproductive Biology", "q_text": "Meiosis also involves crossing over between homologous chromosomes. This shuffles genetic material. What evolutionary advantage does crossing over provide — and why would clonal reproduction not provide this advantage?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None, "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
},  # end Biology

# ══════════════════════════════════════════════════════════════════════════════
# SUBJECT 5 — DSAT  (v2 নতুন, v1-এ ছিল না)
# ══════════════════════════════════════════════════════════════════════════════

"DSAT": {
  # ── Topic 1 ──────────────────────────────────────────────────────────────
  "Reading Comprehension": {
    1: [
      {"q_intro": "Reading comprehension starts with understanding what the passage is actually doing.",
       "q_topic": "Reading Comprehension",
       "q_text": "A DSAT passage describes a scientist's experiment in detail. Is the main purpose of that passage to explain the results, to argue for a conclusion, or to describe a process — and how would you tell the difference?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": "Look at what the last paragraph does — that usually reveals the author's actual goal.",
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
      {"q_intro": "Let's examine how you approach a passage before answering questions.",
       "q_topic": "Reading Comprehension",
       "q_text": "When you read a DSAT passage, what do you do in the first 30 seconds — do you read the questions first, skim the passage, or read every word carefully from the start?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "procedural", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "You identified the main idea. Let's test whether you can distinguish it from supporting details.",
       "q_topic": "Reading Comprehension",
       "q_text": "A passage's main idea is the claim the entire text supports. A supporting detail is one piece of evidence. If a question asks 'What is the central claim of the passage?', what is wrong with choosing an answer that is true and mentioned in the passage but only appears in one sentence?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 2 ──────────────────────────────────────────────────────────────
  "Evidence Analysis": {
    1: [
      {"q_intro": "Evidence questions ask you to justify an answer with a specific quotation.",
       "q_topic": "Evidence Analysis",
       "q_text": "A question asks which quotation from the passage best supports the claim that 'the experiment was inconclusive.' You find three quotes that mention the experiment. How do you decide which one actually supports 'inconclusive' rather than just mentioning the experiment?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": "The quote must do more than mention — it must directly imply or state the specific idea.",
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Good — relevance matters, not just presence in the passage.",
       "q_topic": "Evidence Analysis",
       "q_text": "Two answer choices for an evidence question both contain lines from the passage that seem relevant. One directly states the claim; the other implies it through an analogy. Which should you choose, and why might the implied one be a trap?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 3 ──────────────────────────────────────────────────────────────
  "Vocabulary in Context": {
    1: [
      {"q_intro": "Vocabulary questions on the DSAT are never about memorized definitions.",
       "q_topic": "Vocabulary in Context",
       "q_text": "A question asks: 'As used in line 14, the word \"charged\" most nearly means...' The sentence reads: 'The atmosphere at the summit was charged with tension.' Which meaning of 'charged' fits — filled with electricity, accused legally, or filled with strong emotion?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Context first, definition second — let's test a harder case.",
       "q_topic": "Vocabulary in Context",
       "q_text": "The word 'obscure' can mean 'not well known' (adjective) or 'to make unclear' (verb). In the sentence 'The thick fog obscured the mountain peak,' which meaning applies — and what grammatical feature of the sentence forces that choice?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 4 ──────────────────────────────────────────────────────────────
  "Math: Algebra I": {
    1: [
      {"q_intro": "Algebra on the DSAT tests conceptual understanding, not just computation.",
       "q_topic": "Math: Algebra I",
       "q_text": "The equation 3x + 6 = 21 can be solved by subtracting 6 then dividing by 3. But why does that procedure work — what property of equality are you using at each step?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Good — equality is preserved under the same operation on both sides. Let's push on systems.",
       "q_topic": "Math: Algebra I",
       "q_text": "A system of two linear equations has no solution. What does that mean geometrically when you draw the two lines — and what is the algebraic signal that tells you there's no solution without graphing?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "visual", "confidence": 0.75},
    ],
  },
  # ── Topic 5 ──────────────────────────────────────────────────────────────
  "Math: Advanced Math": {
    1: [
      {"q_intro": "Advanced algebra on the DSAT includes quadratics and function behavior.",
       "q_topic": "Math: Advanced Math",
       "q_text": "A quadratic function f(x) = x² − 4x + 3 has a vertex and two roots. Without calculating, can you tell from the positive leading coefficient whether the parabola opens up or down — and what does that mean for whether the vertex is a minimum or maximum?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Opens upward, minimum at the vertex — let's connect that to the discriminant.",
       "q_topic": "Math: Advanced Math",
       "q_text": "The discriminant b²−4ac tells you how many real roots a quadratic has. If b²−4ac < 0, there are no real roots. What does that mean geometrically for where the parabola sits relative to the x-axis?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "visual", "confidence": 0.75},
    ],
  },
  # ── Topic 6 ──────────────────────────────────────────────────────────────
  "Math: Problem Solving": {
    1: [
      {"q_intro": "Word problems require translating English into algebra before solving.",
       "q_topic": "Math: Problem Solving",
       "q_text": "A store marks up items by 20% then offers a 10% discount. A student says the final price is the same as the original because 20% − 10% = 10% gain. Are they correct? If not, what goes wrong in their reasoning?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": "What are the percentages being applied to at each step?",
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Percentages apply to different base amounts at each step — that's the trap.",
       "q_topic": "Math: Problem Solving",
       "q_text": "On DSAT, a rate question involves two people working together. Person A finishes a job in 4 hours; Person B in 6 hours. Together they finish in T hours. Why is T not 5 (the average), and what relationship should you set up?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 7 ──────────────────────────────────────────────────────────────
  "Math: Geometry & Trig": {
    1: [
      {"q_intro": "Geometry on the DSAT tests reasoning about shapes, not just formula recall.",
       "q_topic": "Math: Geometry & Trig",
       "q_text": "Two parallel lines are cut by a transversal. Which pairs of angles are equal, and why — what geometric property guarantees equality rather than just a pattern you memorized?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Corresponding and alternate angles — let's connect that to trigonometry.",
       "q_topic": "Math: Geometry & Trig",
       "q_text": "sin(θ) = opposite/hypotenuse. Why does this ratio stay constant for all right triangles with the same angle θ, regardless of the size of the triangle?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 8 ──────────────────────────────────────────────────────────────
  "Data Analysis": {
    1: [
      {"q_intro": "Data questions require interpreting charts, not just reading numbers off them.",
       "q_topic": "Data Analysis",
       "q_text": "A bar chart shows that in 2020, Group A scored higher than Group B. A student concludes 'Group A is smarter than Group B.' What is wrong with this conclusion — name at least two things the chart cannot tell you?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Correlation vs causation, sample size, context — good. Let's push on scatter plots.",
       "q_topic": "Data Analysis",
       "q_text": "A scatter plot shows a strong positive correlation (r = 0.92) between ice cream sales and drowning rates. A student concludes ice cream causes drowning. What is the correct interpretation — and what statistical term describes the missing variable that explains both?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 9 ──────────────────────────────────────────────────────────────
  "Writing & Grammar": {
    1: [
      {"q_intro": "Grammar questions on the DSAT test whether sentences are clear and correct, not formal rules.",
       "q_topic": "Writing & Grammar",
       "q_text": "The sentence reads: 'Running to catch the bus, my phone fell out of my pocket.' What is grammatically wrong with this — and who or what should logically be the one running?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": "The subject of the main clause must match the subject of the opening phrase.",
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Dangling modifier — good. Let's test subject-verb agreement with complex structures.",
       "q_topic": "Writing & Grammar",
       "q_text": "The sentence reads: 'The team of researchers, despite numerous setbacks, have published their findings.' Is 'have' or 'has' correct here — and what grammatical rule determines which verb form to use with collective nouns followed by prepositional phrases?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 10 ─────────────────────────────────────────────────────────────
  "Text Structure": {
    1: [
      {"q_intro": "Text structure questions ask about how the passage is organized, not what it says.",
       "q_topic": "Text Structure",
       "q_text": "A passage presents a problem in paragraph 1, describes a failed solution in paragraph 2, and proposes a new approach in paragraph 3. What is the overall text structure — and why would the author choose this structure rather than just stating the solution directly?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Problem-solution — let's test whether you can spot structure mid-passage.",
       "q_topic": "Text Structure",
       "q_text": "A question asks 'How does paragraph 3 relate to paragraph 2?' The correct answer must describe a logical relationship (contrast, elaboration, cause-effect, etc.). If paragraph 2 shows data and paragraph 3 explains what that data means, what is the relationship — and which transition word would make it explicit?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 11 ─────────────────────────────────────────────────────────────
  "Central Ideas": {
    1: [
      {"q_intro": "Central idea questions are among the most common on the DSAT.",
       "q_topic": "Central Ideas",
       "q_text": "A passage about climate change contains facts about CO₂ levels, a discussion of policy debates, and quotes from scientists. A student chooses 'CO₂ levels are rising' as the central idea. What is likely wrong with this choice?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": "Is that a fact or an argument? Does it cover the whole passage?",
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Too narrow — a central idea must account for the whole passage.",
       "q_topic": "Central Ideas",
       "q_text": "A strong central idea answer is broad enough to cover the whole passage but specific enough to distinguish it from other possible topics. If a passage covers three different renewable energy technologies, what would be wrong with choosing 'Solar panels are efficient' as the central idea?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 12 ─────────────────────────────────────────────────────────────
  "Cross-text Connections": {
    1: [
      {"q_intro": "Cross-text questions give you two short passages and ask how they relate.",
       "q_topic": "Cross-text Connections",
       "q_text": "Passage 1 argues that social media harms teenagers. Passage 2 presents data showing no significant harm in controlled studies. What is the relationship between the two passages — agree, disagree, or one qualifies the other?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "They complicate each other — one is argument, one is data. Let's push on author perspective.",
       "q_topic": "Cross-text Connections",
       "q_text": "A cross-text question asks: 'How would the author of Passage 2 most likely respond to the claim in Passage 1?' To answer this, what must you know about Passage 2's author's position — and what would make an answer choice wrong even if it's true according to Passage 2?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 13 ─────────────────────────────────────────────────────────────
  "Quantitative Reasoning": {
    1: [
      {"q_intro": "Quantitative reasoning questions mix reading and math interpretation.",
       "q_topic": "Quantitative Reasoning",
       "q_text": "A table shows that Country A's GDP grew by 5% while Country B's grew by 8%. A student concludes Country B became richer than Country A. What information is missing that makes this conclusion potentially wrong?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Initial values matter — percentage growth is relative. Let's test unit analysis.",
       "q_topic": "Quantitative Reasoning",
       "q_text": "A DSAT question gives a rate of 45 miles per hour and asks for the distance in 40 minutes. A student calculates 45 × 40 = 1800. What unit error have they made, and what should they do first before multiplying?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "procedural", "confidence": 0.75},
    ],
  },
  # ── Topic 14 ─────────────────────────────────────────────────────────────
  "Math: Algebra II": {
    1: [
      {"q_intro": "Advanced algebra includes exponential functions and their behavior.",
       "q_topic": "Math: Algebra II",
       "q_text": "An exponential function y = 2^x grows much faster than y = x² for large x. Without graphing, explain why — what fundamentally different thing happens to the exponent vs the base in each function as x increases?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "The exponent grows — that's the key structural difference. Let's test logarithms.",
       "q_topic": "Math: Algebra II",
       "q_text": "log₂(8) = 3. What question does a logarithm actually answer — and why is log of a negative number undefined in the reals?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
},  # end DSAT

# ══════════════════════════════════════════════════════════════════════════════
# SUBJECT 6 — IELTS  (v2 নতুন, v1-এ ছিল না)
# ══════════════════════════════════════════════════════════════════════════════

"IELTS": {
  # ── Topic 1 ──────────────────────────────────────────────────────────────
  "Reading Strategies": {
    1: [
      {"q_intro": "IELTS reading tests skimming, scanning, and detailed reading — different tools for different question types.",
       "q_topic": "Reading Strategies",
       "q_text": "You have 20 minutes for an IELTS reading passage with 14 questions. You start reading every word from the beginning. After 10 minutes you've read half the passage but answered only 3 questions. What went wrong in your strategy?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": "Not all questions require reading every word.",
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Skimming for structure first, then targeted reading — let's probe True/False/Not Given.",
       "q_topic": "Reading Strategies",
       "q_text": "In True/False/Not Given questions, many students treat 'Not Given' as 'False.' What is the precise difference — can something be False but count as Not Given, and how do you decide?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 2 ──────────────────────────────────────────────────────────────
  "Listening Skills": {
    1: [
      {"q_intro": "IELTS listening is played once. Preparation before the audio is critical.",
       "q_topic": "Listening Skills",
       "q_text": "You have 30 seconds before Section 2 of the IELTS listening test begins. What should you do during that time — and why is reading the questions in advance more useful than just waiting?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Pre-reading activates prediction — let's test what to do when you miss an answer.",
       "q_topic": "Listening Skills",
       "q_text": "You miss the answer to Question 14 while the audio keeps playing. What is the correct strategy — go back and try to catch it, leave it and stay with the audio, or guess and move on? Explain why the wrong strategies cost more than one mark.",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "procedural", "confidence": 0.75},
    ],
  },
  # ── Topic 3 ──────────────────────────────────────────────────────────────
  "Writing Task 1 — Graphs": {
    1: [
      {"q_intro": "Task 1 requires describing data, not explaining it or giving your opinion.",
       "q_topic": "Writing Task 1 — Graphs",
       "q_text": "A line graph shows sales rising from 2010 to 2015 then falling sharply. A student writes: 'The company made bad decisions after 2015 which caused sales to drop.' What is wrong with this sentence in a Task 1 context?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Description only — no causes or opinions. Let's probe the overview.",
       "q_topic": "Writing Task 1 — Graphs",
       "q_text": "An IELTS examiner penalizes Task 1 responses that have no overview paragraph. What is an overview in Task 1, and why is it different from simply listing all the data points in the first paragraph?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 4 ──────────────────────────────────────────────────────────────
  "Writing Task 2 — Essay": {
    1: [
      {"q_intro": "Task 2 is an academic essay. The question type determines the structure.",
       "q_topic": "Writing Task 2 — Essay",
       "q_text": "The prompt says: 'Some people think technology has made us less social. To what extent do you agree or disagree?' A student writes two paragraphs agreeing then one paragraph disagreeing. What is the structural problem — and how should the essay be organized instead?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Clear position, consistent argument — let's probe topic sentences.",
       "q_topic": "Writing Task 2 — Essay",
       "q_text": "In IELTS Task 2, a body paragraph should have a topic sentence, explanation, example, and link. A student writes a paragraph where the example appears in the first sentence. Why does this weaken the paragraph — and what should the first sentence of a body paragraph actually do?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "procedural", "confidence": 0.75},
    ],
  },
  # ── Topic 5 ──────────────────────────────────────────────────────────────
  "Speaking Part 1": {
    1: [
      {"q_intro": "Speaking Part 1 lasts 4-5 minutes. The examiner asks about everyday topics.",
       "q_topic": "Speaking Part 1",
       "q_text": "The examiner asks 'Do you enjoy cooking?' You answer 'Yes.' The examiner marks you down. What was wrong with that answer — and what does a Band 6+ answer look like in terms of length and content?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Extend and explain — good. Let's probe fluency vs accuracy in the examiner's criteria.",
       "q_topic": "Speaking Part 1",
       "q_text": "Two candidates both make grammar errors. One speaks slowly and corrects themselves. The other speaks fluently and ignores errors. Which scores higher on fluency — and what does IELTS actually reward more between fluency and perfect grammar?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 6 ──────────────────────────────────────────────────────────────
  "Speaking Part 2 — Cue Card": {
    1: [
      {"q_intro": "Part 2 gives you 1 minute to prepare and 2 minutes to speak alone.",
       "q_topic": "Speaking Part 2 — Cue Card",
       "q_text": "The cue card says: 'Describe a book you enjoyed. You should say: what it was about, when you read it, why you enjoyed it.' You spend your preparation minute trying to remember a perfect book. What is wrong with this approach?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": "You have 1 minute. What should it actually be used for?",
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Use the minute to make notes on bullet points — not to decide what to say.",
       "q_topic": "Speaking Part 2 — Cue Card",
       "q_text": "During Part 2, you finish describing the book after 90 seconds. You still have 30 seconds left. A student says 'That's all' and stops. What should they do instead — and what does stopping early signal to the examiner?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "procedural", "confidence": 0.75},
    ],
  },
  # ── Topic 7 ──────────────────────────────────────────────────────────────
  "Speaking Part 3": {
    1: [
      {"q_intro": "Part 3 is a discussion — the examiner wants abstract thinking, not personal stories.",
       "q_topic": "Speaking Part 3",
       "q_text": "The examiner asks 'Do you think governments should invest more in public libraries?' You answer 'Yes because I like reading books.' Why is this a weak answer for Part 3 — and what kind of reasoning does Part 3 require?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Societal reasoning, not personal examples. Let's probe hedging language.",
       "q_topic": "Speaking Part 3",
       "q_text": "Advanced speakers use hedging expressions like 'It could be argued that...' or 'In some cases...' rather than stating everything as absolute fact. Why does hedging improve a Part 3 answer — and what does it demonstrate to the examiner beyond just grammar?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 8 ──────────────────────────────────────────────────────────────
  "Vocabulary Building": {
    1: [
      {"q_intro": "IELTS rewards lexical resource — range, accuracy, and appropriateness.",
       "q_topic": "Vocabulary Building",
       "q_text": "A student replaces the word 'good' with 'magnificent' everywhere in their Task 2 essay. The examiner still gives a low lexical score. Why — isn't 'magnificent' a better word?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": "Think about collocation and context — does 'magnificent' fit every situation?",
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Appropriateness matters as much as range — collocation is key.",
       "q_topic": "Vocabulary Building",
       "q_text": "The IELTS examiner looks for 'less common vocabulary used accurately.' A student uses 'proliferation,' 'ubiquitous,' and 'exacerbate' correctly in context. Another student uses the same three words but in sentences where they don't quite fit. Who scores higher — and what exactly is 'collocation' in practical terms?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 9 ──────────────────────────────────────────────────────────────
  "Grammar Accuracy": {
    1: [
      {"q_intro": "Grammar in IELTS is about range and accuracy — not avoiding all errors.",
       "q_topic": "Grammar Accuracy",
       "q_text": "A student writes only simple sentences in their Task 2 essay to avoid mistakes. Their essay has zero grammar errors. Why might they still score Band 5 for grammar rather than Band 8?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Range is penalized when absent — error-free simple sentences cap you at Band 5.",
       "q_topic": "Grammar Accuracy",
       "q_text": "The IELTS grammar descriptor for Band 7 says 'uses a variety of complex structures with some errors.' For Band 8 it says 'uses a wide range with only occasional errors.' What specific grammatical structures count as 'complex' in IELTS terms?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 10 ─────────────────────────────────────────────────────────────
  "Cohesion & Coherence": {
    1: [
      {"q_intro": "Cohesion is linking devices; coherence is logical flow — they are different things.",
       "q_topic": "Cohesion & Coherence",
       "q_text": "A student connects every sentence with 'Furthermore,' 'Moreover,' and 'Additionally.' The examiner gives a low coherence score. Why — isn't using linking words good?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": "Are those three words actually different — and does each sentence actually follow from the previous one?",
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Mechanical linking without logical progression — that's the trap.",
       "q_topic": "Cohesion & Coherence",
       "q_text": "Coherence in an IELTS essay means each sentence logically leads to the next and supports the paragraph's main point. A student's paragraph has perfect grammar, varied linking words, and four sentences — but the sentences are each about a different idea. What is wrong — and what would 'unity' require?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 11 ─────────────────────────────────────────────────────────────
  "Academic Word List": {
    1: [
      {"q_intro": "The AWL contains 570 word families common across academic texts.",
       "q_topic": "Academic Word List",
       "q_text": "The AWL word 'significant' can appear as significant, significantly, significance, insignificant. Why does the AWL group these as one 'family' — and how does understanding word families help you expand vocabulary more efficiently?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "One root → multiple forms. Let's test register appropriateness.",
       "q_topic": "Academic Word List",
       "q_text": "The AWL word 'obtain' is appropriate in an IELTS essay; 'get' is not — they mean nearly the same thing. What is 'register' in linguistics — and why does using low-register words in formal writing signal limited lexical resource to an examiner?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 12 ─────────────────────────────────────────────────────────────
  "Paraphrasing": {
    1: [
      {"q_intro": "Paraphrasing in IELTS means re-expressing ideas in your own words — not copying.",
       "q_topic": "Paraphrasing",
       "q_text": "A Task 2 prompt says 'Modern technology has revolutionized communication.' A student begins their introduction: 'Modern technology has revolutionized communication.' The examiner deducts marks. Why — and what should the student have done instead?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Copy = zero marks for that section. Let's probe what counts as real paraphrasing.",
       "q_topic": "Paraphrasing",
       "q_text": "A student paraphrases 'Modern technology has revolutionized communication' as 'Modern technology has transformed communication' — only one word changed. Is this adequate paraphrasing for IELTS Band 7? What would a genuine paraphrase change?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "analytical", "confidence": 0.75},
    ],
  },
  # ── Topic 13 ─────────────────────────────────────────────────────────────
  "Skimming & Scanning": {
    1: [
      {"q_intro": "Skimming and scanning are different skills used for different question types.",
       "q_topic": "Skimming & Scanning",
       "q_text": "What is the difference between skimming and scanning — and for which IELTS reading question type would you use scanning rather than skimming?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Skimming = main idea; scanning = specific fact. Let's test the trap questions.",
       "q_topic": "Skimming & Scanning",
       "q_text": "When scanning for a name in IELTS reading, you find it quickly and answer the question. But the question asks what the person said, not just who they are. A student writes the name as the answer. What did they fail to do after scanning — and why is locating the word only half the task?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "procedural", "confidence": 0.75},
    ],
  },
  # ── Topic 14 ─────────────────────────────────────────────────────────────
  "Note-taking Skills": {
    1: [
      {"q_intro": "Note-completion in IELTS listening requires writing exactly what you hear.",
       "q_topic": "Note-taking Skills",
       "q_text": "A listening note-completion task says 'Maximum ___ words.' The answer in the audio is 'three large conference rooms.' A student writes 'conference rooms.' They lose the mark. Why?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "unclear", "confidence": 0.7},
    ],
    2: [
      {"q_intro": "Exact words from the audio — details matter. Let's test abbreviation strategy.",
       "q_topic": "Note-taking Skills",
       "q_text": "During the listening test you want to write notes quickly but also catch the next answer. What abbreviation and symbol system helps — and what is the risk if you abbreviate too aggressively when writing final answers?",
       "q_needs_figure": False, "q_figure_type": "none", "q_figure_params": {},
       "q_hint": None,
       "gap_detected": False, "gap_description": "", "gap_location": "",
       "reasoning_style_signal": "procedural", "confidence": 0.75},
    ],
  },
},  # end IELTS

}  # end BANK


# ══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def get_bank_question(subject: str, topic: str, depth: int, language: str = "English") -> dict | None:
    """
    Retrieve a pre-built question from the bank.
    Returns None if subject/topic/depth not in bank.
    depth must be 1 or 2.
    """
    if depth not in (1, 2):
        return None

    subj_bank = BANK.get(subject)
    if not subj_bank:
        return None

    topic_bank = subj_bank.get(topic)
    if not topic_bank:
        # Try partial match
        for key in subj_bank:
            if topic.lower() in key.lower() or key.lower() in topic.lower():
                topic_bank = subj_bank[key]
                break
        if not topic_bank:
            return None

    depth_qs = topic_bank.get(depth, [])
    if not depth_qs:
        return None

    q = random.choice(depth_qs).copy()
    q["q_number"] = f"Q {depth:02d}"
    q["depth_level"] = depth

    if language != "English":
        q["q_intro"] = q["q_intro"]  # translation handled by socratic engine
    return q


def has_bank_question(subject: str, topic: str, depth: int) -> bool:
    """Check if a pre-built question exists for this combination."""
    return get_bank_question(subject, topic, depth) is not None


def bank_stats(bank: dict = None) -> dict:
    """
    Return statistics about the full merged bank.
    Useful for checking coverage.
    """
    if bank is None:
        bank = BANK

    stats = {"subjects": {}, "total_questions": 0, "total_slots": 0}

    for subject, topics in bank.items():
        s = {"topics": {}, "total": 0}
        for topic, depths in topics.items():
            t = {}
            for depth, qs in depths.items():
                t[f"depth_{depth}"] = len(qs)
                s["total"] += len(qs)
                stats["total_questions"] += len(qs)
            s["topics"][topic] = t
        stats["total_slots"] += sum(
            1 for t in topics.values() for d in t.values() if len(d) > 0
        )
        stats["subjects"][subject] = s

    return stats


# ── Quick sanity check ───────────────────────────────────────────────────────
if __name__ == "__main__":
    s = bank_stats()
    print(f"Total subjects : {len(BANK)}")
    print(f"Total questions: {s['total_questions']}")
    print(f"Total slots    : {s['total_slots']}")
    for subj, data in s["subjects"].items():
        print(f"  {subj}: {data['total']} questions across {len(data['topics'])} topics")
