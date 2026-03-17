



import streamlit as st
from services.pipeline import process_repository
from rag.retriever import retrieve_context
from rag.generator import generate_answer
from vectordb.endee_client import vector_store

st.set_page_config(page_title="AI GitHub Codebase Mentor", page_icon="🤖", layout="wide")

if "processed" not in st.session_state:
    st.session_state.processed = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🤖 AI GitHub Codebase Mentor")
st.write("Analyze any GitHub repository and ask questions about the code.")

with st.sidebar:
    st.header("📊 Project Info")
    st.write("### Pipeline")
    st.write("1. Clone GitHub Repo\n2. Extract Code Files\n3. Chunk Code\n4. Generate Embeddings\n5. Store in Vector DB (Endee / Local)\n6. Semantic Search\n7. AI Answer")
    st.write("---")
    st.write("### Tech Stack")
    st.write("- Python\n- Streamlit\n- Sentence Transformers\n- Endee Vector DB (with fallback)\n- Gemini API")
    st.write("---")
    if st.checkbox("🔍 Show stored embeddings"):
        st.write(f"Total embeddings: {len(vector_store)}")
        for i, item in enumerate(vector_store[:5]):
            meta = item.get("metadata", {}) if isinstance(item, dict) else {}
            st.code(meta.get("code", "")[:300])

st.header("🚀 Step 1: Analyze Repository")
repo_url = st.text_input("Enter GitHub Repository URL", placeholder="https://github.com/user/repository")

if st.button("Analyze Repository"):
    if not repo_url:
        st.warning("Please enter a repository URL")
    elif st.session_state.processed:
        st.warning("Repository already processed ✅")
    else:
        with st.spinner("Cloning and processing repository..."):
            result = process_repository(repo_url)
        st.session_state.processed = True
        st.success("Repository processed successfully 🎉")
        if result:
            col1, col2, col3 = st.columns(3)
            col1.metric("Files", result["files"])
            col2.metric("Chunks", result["chunks"])
            col3.metric("Embeddings", result["embeddings"])

st.header("💬 Step 2: Ask Questions About the Code")
question = st.text_input("Ask a question", placeholder="What does serializer.py do?")

if question:
    with st.spinner("🔍 Searching vector database..."):
        results = retrieve_context(question)

    if not results:
        st.warning("No relevant code found")
    else:
        st.subheader("📄 Relevant Code Chunks")
        for r in results:
            st.write(f"**File:** {r['file']}")
            st.code(r['code'], language="python")

        context = "\n\n".join(r['code'] for r in results)
        with st.spinner("🤖 Generating answer..."):
            answer = generate_answer(question, context)
        st.session_state.chat_history.append((question, answer))
        st.subheader("🧠 AI Explanation")
        st.success(answer)

if st.session_state.chat_history:
    st.header("🗂️ Chat History")
    for q, a in reversed(st.session_state.chat_history):
        st.markdown(f"**🧑 You:** {q}")
        st.markdown(f"**🤖 AI:** {a}")
        st.write("---")

st.write("---")
st.caption("Built with ❤️ using RAG + Vector Search + Gemini")