
# # app.py
# import streamlit as st
# import time
# from services.pipeline import GitHubMentorPipeline
# from vectordb.endee_client import endee_client
# from embeddings.embedding_model import embedder

# # 1. Page Configuration
# st.set_page_config(
#     page_title="AI GitHub Codebase Mentor",
#     page_icon="🤖",
#     layout="wide"
# )

# # 2. GitHub-Style Dark Theme CSS
# st.markdown("""
#     <style>
#     .stApp {
#         background-color: #0d1117;
#         color: #c9d1d9;
#     }
#     .stSidebar {
#         background-color: #161b22;
#         border-right: 1px solid #30363d;
#     }
#     .stButton>button {
#         border-radius: 6px;
#         font-weight: 600;
#         width: 100%;
#     }
#     /* Green Build Button */
#     div.stButton > button:first-child {
#         background-color: #238636;
#         color: white;
#         border: 1px solid rgba(27, 31, 35, 0.15);
#     }
#     /* Red Delete Button */
#     .delete-btn > div > button {
#         background-color: #da3633 !important;
#         color: white !important;
#     }
#     .stTextInput>div>div>input {
#         background-color: #0d1117;
#         color: #c9d1d9;
#         border: 1px solid #30363d;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # 3. Sidebar: Repository Ingestion
# with st.sidebar:
#     st.image("https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png", width=50)
#     st.title("Setup Workspace")
#     st.markdown("---")
    
#     repo_url = st.text_input("GitHub Repository URL", placeholder="https://github.com/user/repo")
#     project_id = st.text_input("Project Index Name", value="my-code-mentor")
    
#     if st.button("🚀 Build Knowledge Base"):
#         if not repo_url:
#             st.error("Please provide a repository URL.")
#         else:
#             try:
#                 pipeline = GitHubMentorPipeline(project_id)
#                 with st.status("🛠️ Processing Codebase...", expanded=True) as status:
#                     st.write("Cloning and embedding code...")
#                     pipeline.ingest_new_repo(repo_url)
#                     status.update(label="✅ Indexing Complete!", state="complete", expanded=False)
#                 st.success(f"Project '{project_id}' ready!")
#             except Exception as e:
#                 st.error(f"Ingestion failed: {str(e)}")

# # 4. Main Interface with Tabs
# st.title("🤖 AI GitHub Codebase Mentor")

# tab_chat, tab_manage = st.tabs(["💬 Chat Mentor", "⚙️ Manage Database"])

# with tab_chat:
#     st.caption("Ask questions about your code, logic, or project structure.")
    
#     # Initialize session state for chat history
#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     # Display chat history
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     # User Input
#     if prompt := st.chat_input("Ex: 'How is the area calculation implemented?'"):
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.markdown(prompt)

#         with st.chat_message("assistant"):
#             with st.spinner("Analyzing codebase..."):
#                 try:
#                     pipeline = GitHubMentorPipeline(project_id)
#                     response = pipeline.ask_question(prompt)
#                     st.markdown(response)
#                     st.session_state.messages.append({"role": "assistant", "content": response})
#                 except Exception as e:
#                     st.error(f"❌ Error: {str(e)}")

# with tab_manage:
#     st.header("Database Administration")
#     st.write(f"Current Active Index: `{project_id}`")
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.subheader("🔍 Vector Search")
#         search_query = st.text_input("Test Retrieval (Keyword search)", placeholder="e.g. 'encryption' or 'database'")
#         if st.button("Search Raw Vectors"):
#             if search_query:
#                 # Generate embedding for the search query
#                 q_vec = embedder.generate_embeddings([search_query])[0]
#                 # Search Endee directly
#                 results = endee_client.search_vectors(project_id, q_vec, k=3)
                
#                 if results and "data" in results:
#                     st.write("Top matches found in Endee:")
#                     st.json(results["data"])
#                 else:
#                     st.info("No matching vectors found or index is empty.")
#             else:
#                 st.warning("Please enter a search term.")

#     with col2:
#         st.subheader("🗑️ Danger Zone")
#         st.markdown("Deleting the index will remove all learned code. This cannot be undone.")
        
#         # Wrapping in a div to apply red styling
#         st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
#         if st.button("Clear Entire Index"):
#             confirm = st.checkbox("I understand this wipes the current knowledge base.")
#             if confirm:
#                 success = endee_client.delete_index(project_id)
#                 if success:
#                     st.success(f"Index '{project_id}' deleted successfully.")
#                     st.session_state.messages = [] # Clear chat history
#                 else:
#                     st.error("Failed to delete index. It may already be empty.")
#         st.markdown('</div>', unsafe_allow_html=True)

# # 5. Footer
# st.markdown("---")
# st.markdown("<p style='text-align: center; color: #8b949e;'>Built with Endee Vector DB & Gemini 2.5 Flash</p>", unsafe_allow_html=True)




import streamlit as st
import time
from services.pipeline import GitHubMentorPipeline
from vectordb.endee_client import endee_client
from embeddings.embedding_model import embedder

# 1. Page Configuration
st.set_page_config(
    page_title="GitHub Code Mentor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Professional Developer Theme (GitHub/Vercel Hybrid)
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d;
    }
    
    /* Chat Bubble Styling */
    [data-testid="stChatMessage"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        font-weight: 600;
        color: #8b949e;
    }
    .stTabs [aria-selected="true"] {
        color: #58a6ff !important;
        border-bottom: 2px solid #58a6ff !important;
    }

    /* Buttons */
    .stButton>button {
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    /* Build Button (Green) */
    div[data-testid="stSidebar"] button {
        background-color: #238636 !important;
        color: white !important;
        border: none;
    }
    
    /* Search Result Cards */
    .search-card {
        background-color: #161b22;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #30363d;
        margin-bottom: 10px;
    }
    
    /* Delete Button (Red) */
    .delete-container button {
        background-color: #da3633 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar: Workspace Control
with st.sidebar:
    st.image("https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png", width=40)
    st.title("Workspace")
    st.caption("v1.0.2 • Stable Build")
    st.markdown("---")
    
    repo_url = st.text_input("📦 Repository URL", placeholder="https://github.com/...")
    project_id = st.text_input("🔑 Index Name", value="my-code-mentor1")
    
    st.markdown("### Process Strategy")
    st.info("Uses local embedding (384-dim) + Batch Processing (30 chunks).")
    
    if st.button("🚀 Ingest & Sync Codebase"):
        if not repo_url:
            st.warning("Please enter a valid URL.")
        else:
            try:
                pipeline = GitHubMentorPipeline(project_id)
                with st.status("🛠️ Building Knowledge Base...", expanded=True) as status:
                    st.write("Cloning repository structure...")
                    # The actual ingestion logic
                    pipeline.ingest_new_repo(repo_url)
                    status.update(label="✅ Codebase Synced!", state="complete", expanded=False)
                st.success(f"Index '{project_id}' is now live.")
                st.balloons()
            except Exception as e:
                st.error(f"Sync Failed: {str(e)}")

# 4. Main View
st.title("⚡ AI Codebase Mentor")

tab_chat, tab_manage = st.tabs(["💬 Chat Interface", "⚙️ Database Control"])

with tab_chat:
    # Header for Chat
    chat_col, action_col = st.columns([6, 1])
    with chat_col:
        st.caption("Ask anything about your code's architecture, logic, or potential bugs.")
    with action_col:
        if st.button("🗑️ Clear"):
            st.session_state.messages = []
            st.rerun()

    # Chat Memory Init
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Interaction
    if prompt := st.chat_input("Ex: 'Where is the user authentication logic?'"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing Index..."):
                try:
                    pipeline = GitHubMentorPipeline(project_id)
                    response = pipeline.ask_question(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Neural Error: {str(e)}")

with tab_manage:
    st.subheader("Database Administration")
    st.write(f"Connected Index: `{project_id}`")
    
    col_search, col_danger = st.columns(2)
    
    with col_search:
        st.markdown("### 🔍 Vector Lookup")
        st.markdown("Check if code segments exist in the vector space.")
        search_query = st.text_input("Test Query", placeholder="Enter code keyword...")
        
        if st.button("Verify Retrieval"):
            if search_query:
                with st.spinner("Querying Endee DB..."):
                    q_vec = embedder.generate_embeddings([search_query])[0]
                    results = endee_client.search_vectors(project_id, q_vec, k=3)
                    
                    if results and (isinstance(results, list) or "data" in results):
                        st.success("Data points retrieved successfully!")
                        st.json(results)
                    else:
                        st.error("No vectors found. Index might be empty.")
            else:
                st.info("Input a keyword to test search.")

    with col_danger:
        st.markdown("### 🗑️ Wipe Knowledge")
        st.markdown("This permanently deletes the vector data for this project.")
        
        st.markdown('<div class="delete-container">', unsafe_allow_html=True)
        if st.button("⚠️ Delete Entire Index"):
            # Use session state to handle confirmation so it doesn't vanish on rerun
            st.warning("Are you absolutely sure?")
            if st.checkbox("Confirm permanent deletion"):
                success = endee_client.delete_index(project_id)
                if success:
                    st.session_state.messages = []
                    st.success("Index deleted. Workspace reset.")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Deletion failed. Check connection.")
        st.markdown('</div>', unsafe_allow_html=True)

# 5. Footer
st.markdown("---")
footer_col1, footer_col2 = st.columns(2)
with footer_col1:
    st.markdown("Built with **Endee Vector DB** & **all-MiniLM-L6-v2**")
with footer_col2:
    st.markdown("<p style='text-align: right;'>© 2026 AI Code Mentor</p>", unsafe_allow_html=True)