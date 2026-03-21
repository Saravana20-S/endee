import streamlit as st
import time
import json
from services.pipeline import GitHubMentorPipeline
from vectordb.endee_client import endee_client
from embeddings.embedding_model import embedder
from config.settings import settings

# 1. Page Configuration
st.set_page_config(
    page_title="GitHub Code Mentor",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Professional Developer Theme (GitHub Dark)
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    section[data-testid="stSidebar"] { background-color: #161b22 !important; border-right: 1px solid #30363d; }
    [data-testid="stChatMessage"] { background-color: #161b22; border: 1px solid #30363d; border-radius: 12px; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { font-weight: 600; color: #8b949e; }
    .stTabs [aria-selected="true"] { color: #58a6ff !important; border-bottom: 2px solid #58a6ff !important; }
    .stButton>button { border-radius: 8px; transition: all 0.3s ease; }
    div[data-testid="stSidebar"] button { background-color: #238636 !important; color: white !important; width: 100%; }
    .stat-card { background-color: #161b22; padding: 20px; border-radius: 10px; border: 1px solid #30363d; text-align: center; }
    .delete-btn button { background-color: #da3633 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar: Workspace Control
with st.sidebar:
    st.image("https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png", width=40)
    st.title("Workspace")
    st.caption("v1.0.4 • Endee Mirror Active")
    st.markdown("---")
    
    repo_url = st.text_input("📦 Repository URL", placeholder="https://github.com/...")
    project_id = st.text_input("🔑 Index Name", value="my-code-mentor1")
    
    if st.button("🚀 Ingest & Sync Codebase"):
        if not repo_url:
            st.warning("Please enter a valid URL.")
        else:
            try:
                pipeline = GitHubMentorPipeline(project_id)
                with st.status("🛠️ Building Knowledge Base...", expanded=True) as status:
                    pipeline.ingest_new_repo(repo_url)
                    status.update(label="✅ Codebase Synced!", state="complete", expanded=False)
                st.success(f"Index '{project_id}' is live.")
                st.balloons()
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Sync Failed: {str(e)}")

# 4. Main View
st.title("⚡ AI Codebase Mentor")

# Tabs matching your Endee Dashboard requirements
tab_chat, tab_search, tab_insert, tab_manage = st.tabs([
    "💬 Chat Interface", "🔍 Vector Search", "➕ Manual Insert", "⚙️ Database Control"
])

# Fetch live stats for status indicators
stats = endee_client.get_index_stats(project_id)
total_vecs = stats.get('total_vectors', 0) if stats else 0

with tab_chat:
    chat_col, action_col = st.columns([6, 1])
    with action_col:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about the code..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Searching Vector Space..."):
                pipeline = GitHubMentorPipeline(project_id)
                response = pipeline.ask_question(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

with tab_search:
    st.subheader("🔍 Vector Search (Endee Search Mirror)")
    col_q, col_k = st.columns([3, 1])
    query_text = col_q.text_input("Semantic Query", placeholder="e.g. video processing logic")
    k_val = col_k.number_input("Top K Results", min_value=1, max_value=20, value=5)
    
    if st.button("Execute Search"):
        with st.spinner("Retrieving similar vectors..."):
            q_vec = embedder.generate_embeddings([query_text])[0]
            results = endee_client.search_vectors(q_vec, project_id, k=k_val)
            st.json(results)

with tab_insert:
    st.subheader("➕ Manual Vector Injection")
    st.info("Directly insert a custom vector/metadata pair into the Endee index.")
    
    v_text = st.text_area("Content to Embed", placeholder="Paste a code snippet or note here...")
    v_meta_json = st.text_area("Metadata JSON", value='{"file": "manual_entry.py", "type": "snippet"}')
    
    if st.button("Commit to Endee"):
        try:
            vector = embedder.generate_embeddings([v_text])[0]
            metadata = json.loads(v_meta_json)
            metadata["title"] = v_text[:1000] # Ensure content is in 'title' for Chat retrieval
            
            if endee_client.insert_vectors(project_id, [vector], [metadata]):
                st.success("✅ Vector successfully inserted! Refresh the Dashboard to see updated count.")
                time.sleep(1)
                st.rerun()
        except Exception as e:
            st.error(f"Insertion failed: {e}")

with tab_manage:
    st.subheader("⚙️ Database Administration")
    
    # Live Stats Row
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown(f'<div class="stat-card"><h3>{total_vecs}</h3><p>Total Vectors</p></div>', unsafe_allow_html=True)
    with s2:
        st.markdown(f'<div class="stat-card"><h3>384</h3><p>Dimensions</p></div>', unsafe_allow_html=True)
    with s3:
        status_color = "🟢" if stats and not stats.get('error') else "🔴"
        st.markdown(f'<div class="stat-card"><h3>{status_color}</h3><p>API Status</p></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🗑️ Danger Zone")
    st.write(f"Deleting the index **{project_id}** is irreversible.")
    
    if st.button("⚠️ Wipe Index & Local Backup"):
        pipeline = GitHubMentorPipeline(project_id)
        if pipeline.delete_project():
            st.success("Index and local files deleted.")
            time.sleep(1)
            st.rerun()

# 5. Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #8b949e;'>Synced with Endee Dashboard • v1.0.4</p>", unsafe_allow_html=True)

