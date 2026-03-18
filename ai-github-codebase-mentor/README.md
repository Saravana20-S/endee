# 🤖 AI GitHub Codebase Mentor
> **A Professional RAG-powered Engine for High-Scale Repository Intelligence**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![VectorDB](https://img.shields.io/badge/VectorDB-Endee-6f42c1.svg)](https://github.com/endee-database)
[![LLM](https://img.shields.io/badge/LLM-Gemini_3_Flash-4285F4.svg)](https://deepmind.google/technologies/gemini/)

---


## 🌟 The Vision
**AI GitHub Codebase Mentor** is a developer-centric **Knowledge Retrieval Engine**. It eliminates the "Onboarding Tax" by allowing engineers to instantly query deep architectural patterns in massive repositories using semantic search and Generative AI. 

Unlike standard chatbots, this tool understands the **contextual relationship** between files, providing answers grounded in the actual source code of the project.

---

## 🏗️ System Architecture



The Mentor operates through a sophisticated 4-stage pipeline:
1.  **Code Ingestion:** Clones GitHub repos and performs AST-aware chunking with context overlap.
2.  **Vectorization:** Local embedding generation using `all-MiniLM-L6-v2` (384-dimensions).
3.  **Endee Orchestration:** High-speed indexing with specialized metadata stringification to ensure database integrity.
4.  **Semantic Retrieval:** Hybrid search that fetches top-k relevant segments to ground the LLM response.

---

## 🚀 The Competitive Edge: Why Endee Vector DB?

I chose **Endee Vector DB** over cloud-based alternatives to provide a production-grade advantage:
* **Local-First Privacy:** Proprietary code never leaves the local environment during indexing, ensuring IP security.
* **Sub-Millisecond Retrieval:** Localized vector space minimizes latency, making the "Chat" experience feel instantaneous even with 5,000+ vectors.
* **Developer Diagnostics:** The UI includes a dedicated **"Vector Search"** tool, allowing developers to audit exactly what the AI "sees" before a response is generated.

---

## 🛠️ Technical Challenges & Solutions

| Challenge | Technical Solution |
| :--- | :--- |
| **"Value is not string" 500 Error** | Engineered a **Strict Sanitization Layer** in the client to force-stringify all metadata and IDs, ensuring compatibility with high-performance C++ backend engines. |
| **I/O Race Conditions** | Implemented an asynchronous "Settling Delay" after index creation to prevent file-lock errors during high-speed batching. |
| **Scalability (5k+ Chunks)** | Refactored ingestion into **Consolidated Payloads** (Batch Size: 30), optimizing memory overhead and preventing server timeouts. |
| **URL Path Collisions** | Built a normalization layer to handle special characters and spaces in project names (e.g., `Py Snippets` → `py_snippets`). |

---

## 💻 Tech Stack
* **Language:** Python 3.9+
* **Frontend:** Streamlit (Custom Obsidian-Midnight Theme)
* **Vector Database:** Endee (High-performance vector engine)
* **Embeddings:** Sentence-Transformers (`all-MiniLM-L6-v2`)
* **Orchestration:** RAG (Retrieval-Augmented Generation)
* **LLM API:** Google Gemini 3 Flash

---

## 🔧 Installation

1.  **Environment Setup**
    ```bash
    git clone [https://github.com/Saravana20-S/endee.git](https://github.com/Saravana20-S/endee.git)
    cd ai-github-codebase-mentor
    pip install -r requirements.txt
    ```

2.  **Configuration**
    Create a `.env` file:
    ```env
    GEMINI_API_KEY=your_api_key
    ENDEE_URL=http://localhost:8080
    ```

3.  **Launch**
    ```bash
    streamlit run app.py
    ```

---

## 👨‍💻 Author: Saravanan S
**Full Stack AI Engineer** Dedicated to building scalable, LLM-integrated developer tools.

🔗 [**Portfolio**](https://saravanan-s.vercel.app/)  
🔗 [**LinkedIn**](https://www.linkedin.com/in/saravanan-suresh/)  
🔗 [**GitHub**](https://github.com/Saravana20-S)

---
*Developed for evaluation and demonstration of advanced RAG pipeline orchestration.*