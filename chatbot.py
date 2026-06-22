#!/usr/bin/env python3
"""
AI Chatbot — Conversational Q&A System
========================================
A rule-based chatbot using regex pattern matching and conditional logic.
Handles general Q&A, tech topics, science, and casual conversation.

Usage:  python chatbot.py
Exit:   type  quit / exit / bye  or press Ctrl+C
"""

import re
import random
from datetime import datetime

# ──────────────────────────────────────────────────────────────────────────────
# RESPONSE PATTERNS
# Each entry: (regex_pattern, [list_of_possible_responses])
# The engine picks a random response from the matched list.
# ──────────────────────────────────────────────────────────────────────────────

PATTERNS: list[tuple[str, list[str]]] = [

    # ── Greetings ─────────────────────────────────────────────────────────────
    (
        r'\b(hi|hello|hey|howdy|greetings|good\s*(morning|afternoon|evening|day))\b',
        [
            "Hello! How can I help you today?",
            "Hi there! What can I assist you with?",
            "Hey! Ask me anything — I'm here to help.",
            "Greetings! What's on your mind?",
        ]
    ),

    # ── How are you ───────────────────────────────────────────────────────────
    (
        r"how are you|how's it going|how do you do|what's up|you good",
        [
            "I'm running smoothly and ready to help! What do you need?",
            "All good on my end — what can I do for you?",
            "Doing great, thanks! What's your question?",
        ]
    ),

    # ── Thank you ─────────────────────────────────────────────────────────────
    (
        r'\b(thanks|thank you|thank you so much|appreciate it|cheers|thx|ty)\b',
        [
            "You're welcome! Let me know if you need anything else.",
            "Happy to help! Anything else on your mind?",
            "Of course! Feel free to ask more questions anytime.",
        ]
    ),

    # ── Farewells ─────────────────────────────────────────────────────────────
    (
        r'\b(bye|goodbye|see you|farewell|take care|later|cya|good night)\b',
        [
            "Goodbye! Have a wonderful day!",
            "See you later — feel free to return anytime!",
            "Take care! It was great chatting with you.",
        ]
    ),

    # ── Positive acknowledgments ──────────────────────────────────────────────
    (
        r'^(yes|yeah|yep|sure|ok|okay|alright|got it|perfect|great|sounds good)\.?$',
        [
            "Great! What else can I help with?",
            "Awesome! Feel free to ask anything.",
            "Perfect — what's next?",
        ]
    ),

    # ── Negative acknowledgments ──────────────────────────────────────────────
    (
        r'^(no|nope|nah|not really|never mind|nevermind)\.?$',
        [
            "No worries! Let me know if anything comes up.",
            "That's fine — I'm here whenever you need me.",
        ]
    ),

    # ──────────────────────────────────────────────────────────────────────────
    # IDENTITY & META
    # ──────────────────────────────────────────────────────────────────────────

    (
        r"what'?s? your name|who are you|what are you",
        [
            "I'm a rule-based AI assistant built in Python — no external libraries needed!",
            "I'm ChatBot, your lightweight conversational Q&A assistant.",
        ]
    ),

    (
        r"who (made|built|created|wrote|coded) you|who'?s? your (creator|developer|author)",
        [
            "I was built in Python using only the standard library — regex-powered, zero dependencies!",
        ]
    ),

    (
        r"what can you do|what are your (skills|capabilities|features)|how can you help",
        [
            (
                "Here's what I can help with:\n"
                "  • General knowledge & Q&A\n"
                "  • Programming & coding concepts\n"
                "  • Science & technology topics\n"
                "  • Writing & editing guidance\n"
                "  • Definitions & explanations\n"
                "  • Casual conversation\n\n"
                "Just type your question!"
            ),
        ]
    ),

    (
        r"what(\'s| is) the (time|current time)|what time is it",
        [datetime.now().strftime("The current time is %I:%M %p.")]
    ),

    (
        r"what(\'s| is) (today'?s? date|the date|the day)|what day is it",
        [datetime.now().strftime("Today is %A, %B %d, %Y.")]
    ),

    # ──────────────────────────────────────────────────────────────────────────
    # PROGRAMMING LANGUAGES
    # ──────────────────────────────────────────────────────────────────────────

    (
        r'\bwhat is python\b|\btell me about python\b|\bexplain python\b',
        [
            (
                "Python is a high-level, interpreted programming language celebrated for its "
                "clean, readable syntax. Key facts:\n"
                "  • Created by Guido van Rossum (1991)\n"
                "  • Dynamically typed, garbage-collected\n"
                "  • Supports OOP, functional & procedural styles\n"
                "  • Hugely popular in data science, AI/ML, web dev, and automation\n"
                "  • Runs on Windows, macOS, and Linux"
            ),
        ]
    ),

    (
        r'\bwhat is javascript\b|\bwhat is js\b|\btell me about javascript\b',
        [
            (
                "JavaScript (JS) is the scripting language of the web:\n"
                "  • Runs natively in all modern browsers\n"
                "  • Also runs server-side via Node.js\n"
                "  • Dynamically typed and event-driven\n"
                "  • Powers interactive UIs, SPAs, and REST APIs\n"
                "  • Key ecosystem: React, Vue, Angular (frontend) / Express (backend)"
            ),
        ]
    ),

    (
        r'\bwhat is java\b|\btell me about java\b',
        [
            (
                "Java is a strongly-typed, object-oriented language:\n"
                "  • 'Write once, run anywhere' — compiles to bytecode for the JVM\n"
                "  • Statically typed with a rich type system\n"
                "  • Dominant in enterprise backends, Android apps, and big data\n"
                "  • Known for verbose but explicit syntax and strong tooling"
            ),
        ]
    ),

    (
        r'\bwhat is (c\+\+|cpp)\b|\btell me about c\+\+',
        [
            (
                "C++ is a general-purpose, compiled language built on top of C:\n"
                "  • Offers both low-level memory control and high-level OOP\n"
                "  • Used in game engines, OS kernels, embedded systems, and HPC\n"
                "  • Extremely fast — no garbage collector, manual memory management\n"
                "  • Foundation for engines like Unreal and systems like Windows"
            ),
        ]
    ),

    (
        r'\bwhat is (rust)\b|\btell me about rust\b',
        [
            (
                "Rust is a systems programming language focused on safety and speed:\n"
                "  • Guarantees memory safety without a garbage collector\n"
                "  • Ownership model prevents data races at compile time\n"
                "  • Used in WebAssembly, OS dev, game engines, and CLI tools\n"
                "  • Voted #1 most loved language on Stack Overflow for years running"
            ),
        ]
    ),

    (
        r'\bwhat is (go|golang)\b|\btell me about go\b',
        [
            (
                "Go (Golang) is a compiled language created by Google:\n"
                "  • Known for simplicity, fast compilation, and built-in concurrency\n"
                "  • Goroutines and channels make concurrent code straightforward\n"
                "  • Used widely in cloud infrastructure (Docker, Kubernetes are in Go)\n"
                "  • Statically typed with a garbage collector"
            ),
        ]
    ),

    # ──────────────────────────────────────────────────────────────────────────
    # DATA STRUCTURES & CS CONCEPTS
    # ──────────────────────────────────────────────────────────────────────────

    (
        r'\bwhat is an? (array|list)\b|\bexplain (array|list)\b',
        [
            (
                "An array (or list in Python) is an ordered collection of elements:\n"
                "  • Supports indexing: my_list[0] → first element\n"
                "  • Mutable — elements can be added, removed, or changed\n"
                "  • Python lists can hold mixed types: [1, 'hello', True]\n"
                "  • Key methods: .append(), .pop(), .sort(), .extend()"
            ),
        ]
    ),

    (
        r'\bwhat is a dictionary\b|\bwhat is a (hashmap|hash map|dict)\b',
        [
            (
                "A dictionary (dict) is a key-value data structure:\n"
                "  • Syntax: {'name': 'Alice', 'age': 30}\n"
                "  • O(1) average lookup time using hashing\n"
                "  • Keys must be hashable (strings, ints, tuples)\n"
                "  • Ordered by insertion since Python 3.7+"
            ),
        ]
    ),

    (
        r'\bwhat is a (stack)\b|\bexplain stack\b',
        [
            (
                "A stack is a Last-In-First-Out (LIFO) data structure:\n"
                "  • Push: add an item to the top\n"
                "  • Pop: remove the top item\n"
                "  • Used in: function call stacks, undo/redo, expression parsing\n"
                "  • Python implementation: use a list with .append() and .pop()"
            ),
        ]
    ),

    (
        r'\bwhat is a (queue)\b|\bexplain queue\b',
        [
            (
                "A queue is a First-In-First-Out (FIFO) data structure:\n"
                "  • Enqueue: add to the back\n"
                "  • Dequeue: remove from the front\n"
                "  • Used in: task scheduling, BFS, print queues\n"
                "  • Python: use collections.deque for efficient O(1) operations"
            ),
        ]
    ),

    (
        r'\bwhat is (recursion|recursive)\b|\bexplain recursion\b',
        [
            (
                "Recursion is when a function calls itself to solve a problem:\n"
                "  • Requires a base case to stop the recursion\n"
                "  • Each call uses its own stack frame\n"
                "  • Classic examples: factorial, Fibonacci, tree traversal\n"
                "  • Python default recursion limit: 1000 (sys.setrecursionlimit to change)"
            ),
        ]
    ),

    (
        r'\bwhat is big o\b|\bbig.o notation\b|\btime complexity\b',
        [
            (
                "Big O notation describes an algorithm's time or space growth:\n"
                "  • O(1)   — constant (dict lookup)\n"
                "  • O(log n) — logarithmic (binary search)\n"
                "  • O(n)   — linear (list scan)\n"
                "  • O(n²)  — quadratic (nested loops)\n"
                "  • O(2ⁿ)  — exponential (naive recursive fib)\n"
                "It describes worst-case performance as input size grows."
            ),
        ]
    ),

    # ──────────────────────────────────────────────────────────────────────────
    # AI / ML / DATA SCIENCE
    # ──────────────────────────────────────────────────────────────────────────

    (
        r'\bwhat is (ai|artificial intelligence)\b|\bexplain artificial intelligence\b',
        [
            (
                "Artificial Intelligence (AI) is the simulation of human intelligence in machines:\n"
                "  • Encompasses learning, reasoning, problem-solving, and perception\n"
                "  • Subfields: Machine Learning, Deep Learning, NLP, Computer Vision\n"
                "  • Narrow AI: excels at one task (chess, image recognition)\n"
                "  • General AI: hypothetical human-level reasoning — not yet achieved"
            ),
        ]
    ),

    (
        r'\bwhat is machine learning\b|\bexplain ml\b|\btell me about ml\b',
        [
            (
                "Machine Learning (ML) is a subset of AI that learns from data:\n"
                "  • Supervised learning — trained on labeled data (classification, regression)\n"
                "  • Unsupervised learning — finds patterns in unlabeled data (clustering)\n"
                "  • Reinforcement learning — learns via reward/penalty signals\n"
                "  • Key libraries: scikit-learn, TensorFlow, PyTorch, XGBoost"
            ),
        ]
    ),

    (
        r'\bwhat is (deep learning|neural network)\b',
        [
            (
                "Deep Learning uses multi-layer neural networks inspired by the brain:\n"
                "  • Layers of interconnected nodes (neurons) learn hierarchical features\n"
                "  • Powers image recognition, speech, language models, and more\n"
                "  • Requires large datasets and significant compute (GPUs)\n"
                "  • Popular frameworks: PyTorch, TensorFlow / Keras"
            ),
        ]
    ),

    (
        r'\bwhat is (nlp|natural language processing)\b',
        [
            (
                "NLP (Natural Language Processing) enables computers to understand text & speech:\n"
                "  • Core tasks: tokenization, sentiment analysis, translation, summarization\n"
                "  • Modern NLP is dominated by transformer models (BERT, GPT, T5)\n"
                "  • Python libraries: spaCy, NLTK, Hugging Face Transformers"
            ),
        ]
    ),

    # ──────────────────────────────────────────────────────────────────────────
    # WEB DEVELOPMENT
    # ──────────────────────────────────────────────────────────────────────────

    (
        r'\bwhat is (html)\b|\bexplain html\b',
        [
            (
                "HTML (HyperText Markup Language) structures web content:\n"
                "  • Uses tags like <h1>, <p>, <div>, <img>, <a>\n"
                "  • Defines the semantic structure of a webpage\n"
                "  • HTML5 introduced semantic elements: <article>, <section>, <nav>\n"
                "  • Works alongside CSS (styling) and JavaScript (behavior)"
            ),
        ]
    ),

    (
        r'\bwhat is (css)\b|\bexplain css\b',
        [
            (
                "CSS (Cascading Style Sheets) controls the visual presentation of HTML:\n"
                "  • Manages layout, colors, fonts, animations, and responsiveness\n"
                "  • Selectors target elements: .class, #id, element\n"
                "  • Key concepts: box model, flexbox, CSS Grid, media queries\n"
                "  • Preprocessors like SCSS add variables and nesting"
            ),
        ]
    ),

    (
        r'\bwhat is an? api\b|\bexplain api\b',
        [
            (
                "An API (Application Programming Interface) defines how software components interact:\n"
                "  • REST APIs use HTTP methods (GET, POST, PUT, DELETE) + JSON\n"
                "  • GraphQL APIs let clients request exactly the data they need\n"
                "  • APIs enable integration between apps, services, and platforms\n"
                "  • Python tools: requests (client), FastAPI / Flask (server)"
            ),
        ]
    ),

    # ──────────────────────────────────────────────────────────────────────────
    # SCIENCE
    # ──────────────────────────────────────────────────────────────────────────

    (
        r'\bwhat is (gravity|gravitation)\b|\bexplain gravity\b',
        [
            (
                "Gravity is the fundamental attractive force between masses:\n"
                "  • Newton: F = Gm₁m₂/r² (inverse-square law)\n"
                "  • Einstein (General Relativity): mass curves spacetime, gravity is that curvature\n"
                "  • Earth's surface gravity: ~9.81 m/s²\n"
                "  • Keeps planets in orbit, holds galaxies together, and shapes the universe"
            ),
        ]
    ),

    (
        r'\bwhat is (dna)\b|\bexplain dna\b',
        [
            (
                "DNA (Deoxyribonucleic Acid) is the molecule that stores genetic information:\n"
                "  • Double helix structure discovered by Watson & Crick (1953)\n"
                "  • Made of 4 nucleotide bases: A (Adenine), T (Thymine), C (Cytosine), G (Guanine)\n"
                "  • A pairs with T; C pairs with G\n"
                "  • Each human cell contains ~3 billion base pairs encoding ~20,000 genes"
            ),
        ]
    ),

    (
        r'\bwhat is (photosynthesis)\b|\bexplain photosynthesis\b',
        [
            (
                "Photosynthesis converts light energy into chemical energy:\n"
                "  • Equation: 6CO₂ + 6H₂O + light → C₆H₁₂O₆ (glucose) + 6O₂\n"
                "  • Occurs in chloroplasts using chlorophyll to capture sunlight\n"
                "  • Two stages: light-dependent reactions and the Calvin cycle\n"
                "  • Foundation of nearly all food chains on Earth"
            ),
        ]
    ),

    (
        r'\bwhat is (the speed of light)\b|\bhow fast is light\b',
        [
            (
                "The speed of light in a vacuum (c) is exactly 299,792,458 m/s (~3×10⁸ m/s):\n"
                "  • Light travels ~1 foot per nanosecond\n"
                "  • From the Sun to Earth takes ~8 minutes 20 seconds\n"
                "  • Einstein's Special Relativity: nothing with mass can reach c\n"
                "  • The cosmic speed limit — it's baked into the fabric of spacetime"
            ),
        ]
    ),

    # ──────────────────────────────────────────────────────────────────────────
    # CODING TIPS & BEST PRACTICES
    # ──────────────────────────────────────────────────────────────────────────

    (
        r'\bhow (do i|to) debug\b|\bdebugging tips\b',
        [
            (
                "Debugging tips that actually work:\n"
                "  1. Read the full error message — the type and line number are your first clue\n"
                "  2. Add print() / logging statements to trace variable values\n"
                "  3. Use a debugger: pdb (Python), browser DevTools (JS)\n"
                "  4. Isolate the problem — reproduce it in the smallest possible snippet\n"
                "  5. Rubber-duck debug: explain the code aloud line by line\n"
                "  6. Check recent changes — if it worked before, what changed?"
            ),
        ]
    ),

    (
        r'\bwhat is (git)\b|\bexplain git\b',
        [
            (
                "Git is a distributed version control system:\n"
                "  • Tracks changes to files over time\n"
                "  • Core concepts: repository, commit, branch, merge, pull request\n"
                "  • Key commands: git init, git clone, git add, git commit, git push\n"
                "  • Branching enables parallel development without conflicts\n"
                "  • Most code lives on GitHub, GitLab, or Bitbucket"
            ),
        ]
    ),

    (
        r'\bwhat is (oop|object.oriented)\b|\bexplain oop\b',
        [
            (
                "OOP (Object-Oriented Programming) organizes code around objects:\n"
                "  • Class: a blueprint defining attributes and methods\n"
                "  • Object: an instance of a class\n"
                "  • 4 pillars: Encapsulation, Abstraction, Inheritance, Polymorphism\n"
                "  • Makes large codebases more modular, reusable, and maintainable"
            ),
        ]
    ),

    # ──────────────────────────────────────────────────────────────────────────
    # GENERAL HELP
    # ──────────────────────────────────────────────────────────────────────────

    (
        r'\b(help|support|assist)\b',
        [
            (
                "I'm here to help! You can ask me about:\n"
                "  • Programming languages & coding concepts\n"
                "  • AI, ML, and data science\n"
                "  • Science (physics, biology, chemistry)\n"
                "  • Web development basics\n"
                "  • General knowledge Q&A\n\n"
                "What would you like to know?"
            ),
        ]
    ),
]

# ──────────────────────────────────────────────────────────────────────────────
# FALLBACK RESPONSES  (used when no pattern matches)
# ──────────────────────────────────────────────────────────────────────────────

FALLBACKS: list[str] = [
    "That's an interesting question! I don't have a specific answer for that — try rephrasing or checking a reliable source.",
    "I'm not sure about that one. Could you give me a bit more context?",
    "Hmm, that's outside my current knowledge base. Is there something else I can help with?",
    "I don't have enough information on that topic. Try asking in a different way?",
    "I'm not confident I can answer that accurately. Could you clarify what you're looking for?",
    "Good question — that one's beyond my pattern library. Try a search engine for the most up-to-date answer!",
]

# ──────────────────────────────────────────────────────────────────────────────
# CORE ENGINE
# ──────────────────────────────────────────────────────────────────────────────

def preprocess(text: str) -> str:
    """Normalize input: lowercase and strip whitespace."""
    return text.lower().strip()


def match_response(user_input: str) -> str:
    """
    Iterate through PATTERNS, return a random response from the first match.
    Falls back to a random FALLBACK response if nothing matches.
    """
    normalized = preprocess(user_input)

    for pattern, responses in PATTERNS:
        if re.search(pattern, normalized, re.IGNORECASE):
            return random.choice(responses)

    return random.choice(FALLBACKS)


# ──────────────────────────────────────────────────────────────────────────────
# CONVERSATION LOOP
# ──────────────────────────────────────────────────────────────────────────────

EXIT_COMMANDS: frozenset[str] = frozenset(
    {"quit", "exit", "bye", "goodbye", "farewell", "q", ":q", ".exit"}
)

BANNER = """
╔══════════════════════════════════════════════════════╗
║        AI Chatbot — Conversational Q&A System        ║
║  Rule-based · Python stdlib only · Zero dependencies ║
╚══════════════════════════════════════════════════════╝
  Type your question below.
  Type  quit / exit / bye  or press Ctrl+C to end.
──────────────────────────────────────────────────────
"""


def run_chatbot() -> None:
    """Main conversation loop."""
    print(BANNER)

    while True:
        try:
            user_input = input("You: ").strip()

            # Empty input
            if not user_input:
                print("Bot: Go ahead — ask me anything!\n")
                continue

            # Explicit exit
            if user_input.lower() in EXIT_COMMANDS:
                print("Bot: Goodbye! Have a wonderful day! 👋\n")
                break

            response = match_response(user_input)
            print(f"\nBot: {response}\n")
            print("─" * 54)

        except KeyboardInterrupt:
            print("\n\nBot: Session interrupted. Goodbye! 👋\n")
            break

        except EOFError:
            # Handles piped input / non-interactive mode
            break


# ──────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_chatbot()
