AI Chatbot — Conversational Q&A System
A rule-based conversational chatbot built in Python that handles general Q&A interactions. The bot processes user input, matches it against predefined patterns using regex, and returns contextually appropriate responses.
---
 Features
 Natural language input handling
 Pattern-based response matching using regex
 Continuous conversation loop with graceful exit handling
 Lightweight — runs with zero external dependencies
 30+ topic patterns across tech, science, coding, and general knowledge
---
 Project Structure
```
ai-chatbot/
└── chatbot.py   # Main chatbot script
```
---
 How to Run
Make sure you have Python 3.10+ installed.
```bash
python chatbot.py
```
That's it — no `pip install` needed!
---
 Sample Conversation
```
You: hello
Bot: Hello! How can I help you today?

You: what is python
Bot: Python is a high-level, interpreted programming language celebrated for its
     clean, readable syntax. Key facts:
       • Created by Guido van Rossum (1991)
       • Dynamically typed, garbage-collected
       ...

You: what is machine learning
Bot: Machine Learning (ML) is a subset of AI that learns from data:
       • Supervised learning — trained on labeled data
       • Unsupervised learning — finds patterns in unlabeled data
       ...

You: bye
Bot: Goodbye! Have a wonderful day! 👋
```
---
 Topics Covered
Category	Topics
Conversation	Greetings, farewells, thanks, acknowledgments
Identity / Meta	Bot name, capabilities, current time & date
Languages	Python, JavaScript, Java, C++, Rust, Go
CS Concepts	Arrays, dicts, stacks, queues, recursion, Big O
AI / ML	AI, Machine Learning, Deep Learning, NLP
Web Dev	HTML, CSS, REST APIs
Science	Gravity, DNA, Photosynthesis, Speed of light
Dev Tips	Debugging strategies, Git, OOP
---
 Extending the Bot
Adding a new topic is one tuple in `chatbot.py`:
```python
(r'\bwhat is docker\b', [
    "Docker is a containerization platform that packages apps into isolated containers..."
]),
```
---
 Tech Stack
Language: Python 3.10+
Libraries: `re`, `random`, `datetime` (all standard library)
---
 License
This project is open source and available under the MIT License.
