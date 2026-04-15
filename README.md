# 🐍 PyBot — RAG-Powered Python Tutor Agent

> An intelligent Python tutor agent that answers from **your own documents**, runs code live, explains errors, and generates practice exercises — built with Google ADK + Gemini.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Google ADK](https://img.shields.io/badge/Google%20ADK-latest-orange?logo=google&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash%20Lite-purple?logo=google&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-vector%20store-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## ✨ Features

- 🔍 **RAG Retrieval** — Searches your own `.txt` documents before answering, grounded in real context
- ▶️ **Live Code Execution** — Runs Python snippets via subprocess and returns output or errors
- 🐛 **Error Explainer** — Diagnoses common Python errors and suggests fixes
- 📝 **Exercise Generator** — Creates beginner/intermediate practice problems by topic
- 💬 **Conversational Memory** — Maintains session history within a run via ADK's InMemorySessionService

---

## 🏗️ Architecture

```
pybot-rag-agent/
│
├── main.py          # Entry point — CLI chat loop, session management
├── agent.py         # ADK LlmAgent definition with tools and instructions
├── tools.py         # 4 callable tools: search, run, explain, exercise
├── rag.py           # RAG pipeline — chunking, embedding, indexing, retrieval
│
├── data/            # 📂 Your .txt knowledge base files go here
│   └── python_basics.txt
│
├── vector_store/    # Auto-created ChromaDB persistent storage
├── .env             # API key config (not committed)
└── requirements.txt
```

### How it works

```
User Query
    │
    ▼
search_python_docs (RAG)
    │
    ├── Embed query with SentenceTransformer (all-MiniLM-L6-v2)
    ├── Cosine similarity search in ChromaDB
    ├── Filter by relevance threshold (≥ 62%)
    └── Return ranked context with source attribution
    │
    ▼
Gemini 2.5 Flash Lite (via Google ADK)
    │
    ├── run_python_code   → subprocess execution
    ├── explain_error     → error pattern matching
    └── generate_exercise → topic-based exercise lookup
    │
    ▼
PyBot Response (with source + follow-up question)
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/pybot-rag-agent.git
cd pybot-rag-agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your API key

Create a `.env` file in the root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Get your key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 4. Add your documents

Place `.txt` files inside the `data/` folder. These are the documents PyBot will search when answering questions.

```
data/
├── python_basics.txt
├── oop_concepts.txt
└── error_handling.txt
```

### 5. Run PyBot

```bash
python main.py
```

---

## 💬 Example Usage

```
You: What is a list comprehension?

  [Tool] search_python_docs(What is a list comprehension?)

PyBot: Based on your knowledge base...
[Source: python_basics.txt | Relevance: 87.3%]
A list comprehension is a concise way to create lists...

What would you like to practice next — writing your own list comprehension?
```

```
You: Run this code: print([x**2 for x in range(5)])

  [Tool] run_python_code(print([x**2 for x in range(5)]))

PyBot: Code ran successfully!
Output: [0, 1, 4, 9, 16]

Would you like to try modifying this to filter only even squares?
```

---

## 🧰 Tech Stack

| Component | Technology |
|---|---|
| Agent Framework | [Google ADK](https://google.github.io/adk-docs/) |
| LLM | Gemini 2.5 Flash Lite |
| Vector Database | [ChromaDB](https://www.trychroma.com/) |
| Embeddings | [SentenceTransformers](https://www.sbert.net/) — `all-MiniLM-L6-v2` |
| Code Execution | Python `subprocess` |
| Session Management | ADK `InMemorySessionService` |

---

## ⚙️ Configuration

Key constants in `rag.py` you can tune:

| Variable | Default | Description |
|---|---|---|
| `CHUNK_SIZE` | `400` | Characters per document chunk |
| `CHUNK_OVERLAP` | `50` | Overlap between chunks |
| `TOP_K` | `3` | Number of chunks retrieved per query |
| `min_relevance` | `62.0` | Minimum similarity score (%) to use a chunk |

---

## 📋 Requirements

```txt
google-adk
google-genai
chromadb
sentence-transformers
python-dotenv
```

---

## 🔮 Roadmap

- [ ] Support PDF and Markdown documents in RAG pipeline
- [ ] Persistent session storage across restarts
- [ ] Dynamic exercise generation via LLM (instead of hardcoded)
- [ ] Web UI with Streamlit or Gradio
- [ ] Multi-agent setup with a separate "code reviewer" agent

---

## 🤝 Contributing

Pull requests are welcome! For major changes, open an issue first to discuss what you'd like to change.

---

## 📄 License

MIT License — feel free to use, modify, and distribute.

---

<p align="center">Built with ❤️ using Google ADK + Gemini</p>
