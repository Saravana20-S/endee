# import streamlit as st
# from services.pipeline import process_repository
# from rag.retriever import retrieve_context
# from rag.generator import generate_answer

# st.title("AI GitHub Codebase Mentor")

# repo_url = st.text_input("Enter GitHub Repository URL")

# if st.button("Analyze Repository"):

#     process_repository(repo_url)

#     st.success("Repository processed successfully")


# question = st.text_input("Ask a question about the code")

# if question:

#     context = retrieve_context(question)

#     answer = generate_answer(question, context)

#     st.write(answer)



import streamlit as st
from services.pipeline import process_repository
from rag.retriever import retrieve_context
from rag.generator import generate_answer

# -------------------------------
# PAGE CONFIG
# -------------------------------

st.set_page_config(
    page_title="AI GitHub Codebase Mentor",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------
# TITLE
# -------------------------------

st.title("🤖 AI GitHub Codebase Mentor")
st.write("Analyze any GitHub repository and ask questions about the code.")

# -------------------------------
# SIDEBAR
# -------------------------------

with st.sidebar:
    st.header("Project Info")

    st.write("Pipeline")

    st.write("""
    1. Clone GitHub Repo
    2. Extract Code Files
    3. Chunk Code
    4. Generate Embeddings
    5. Store in Vector DB
    6. Semantic Search
    7. AI Answer
    """)

    st.write("---")
    st.write("Tech Stack")

    st.write("""
    - Python
    - Streamlit
    - Sentence Transformers
    - Endee Vector DB
    - Gemini API
    """)

# -------------------------------
# REPOSITORY INPUT
# -------------------------------

st.header("Step 1: Analyze Repository")

repo_url = st.text_input(
    "Enter GitHub Repository URL",
    placeholder="https://github.com/user/repository"
)

if st.button("Analyze Repository"):

    if repo_url == "":
        st.warning("Please enter a repository URL")

    else:

        with st.spinner("Cloning and processing repository..."):

            result = process_repository(repo_url)

        st.success("Repository processed successfully")

        if result:

            st.subheader("Repository Processing Stats")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Files Processed", result["files"])

            with col2:
                st.metric("Code Chunks", result["chunks"])

            with col3:
                st.metric("Embeddings Created", result["embeddings"])

# -------------------------------
# QUESTION SECTION
# -------------------------------

st.header("Step 2: Ask Questions About the Code")

question = st.text_input(
    "Ask a question",
    placeholder="What does this repository do?"
)

if question:

    with st.spinner("Searching vector database..."):

        results = retrieve_context(question)

    st.subheader("Relevant Code Chunks")

    if results:

        for r in results:

            st.code(r["text"], language="python")

    else:

        st.warning("No relevant code found")

    st.subheader("AI Explanation")

    with st.spinner("Generating answer..."):

        context = "\n".join([r["text"] for r in results])

        answer = generate_answer(question, context)

    st.success(answer)

# -------------------------------
# FOOTER
# -------------------------------

st.write("---")
st.write("Built with RAG + Vector Search")