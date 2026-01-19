
import streamlit as st
import os
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory


# --- PAGE CONFIG ---
st.set_page_config(page_title="Chat with PDF", page_icon="📚", layout="wide")

# --- CSS STYLING ---
st.markdown("""
    <style>
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: CONFIGURATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=80)
    st.title("Settings")
    
    # API Key Handling (Secrets or Input)
    # if "GROQ_API_KEY" in st.secrets:
    #     st.success("✅ API Key loaded from Secrets")
    #     api_key = st.secrets["GROQ_API_KEY"]
    # else:
    #     api_key = st.text_input("Enter Groq API Key:", type="password")
    #     if not api_key:
    #         st.warning("⚠️ API Key required")
    api_key = None

# ✅ Try Streamlit secrets safely
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
      api_key = st.text_input("Enter Groq API Key:", type="password")
    if not api_key:
        st.warning("⚠️ API Key required")
    else:
      st.success("✅ API key loaded from environment")


    
    st.markdown("---")
    st.markdown("### 📂 Upload Document")
    uploaded_file = st.file_uploader("Upload your PDF", type="pdf")
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- HELPER FUNCTIONS ---

@st.cache_resource
def get_embeddings():
    """Load embeddings model once (cached)."""
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLm-L6-v2")

def process_pdf(pdf_docs):
    """Extract text -> Split -> Vectorize."""
    text = ""
    pdf_reader = PdfReader(pdf_docs)
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    
    # Create Vector Store (FAISS)
    embeddings = get_embeddings()
    vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore, api_key):
    """Create the Chat Chain."""
    llm = ChatGroq(temperature=0.2, model_name="llama-3.3-70b-versatile", groq_api_key=api_key)
    
    memory = ConversationBufferMemory(
        memory_key='chat_history', 
        return_messages=True
    )
    
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

# --- MAIN APP LOGIC ---

st.title("📚 Chat with your PDF (RAG)")
st.subheader("Upload a document and ask questions")

# Initialize Session State for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize Session State for Conversation Chain
if "conversation" not in st.session_state:
    st.session_state.conversation = None

# PROCESS UPLOAD
if uploaded_file and api_key:
    if "processed_file" not in st.session_state or st.session_state.processed_file != uploaded_file.name:
        with st.spinner("Processing PDF... (Creating Embeddings)"):
            vectorstore = process_pdf(uploaded_file)
            st.session_state.conversation = get_conversation_chain(vectorstore, api_key)
            st.session_state.processed_file = uploaded_file.name
            st.success("PDF Processed! You can now chat.")

# CHAT INTERFACE
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about your PDF..."):
    # 1. Display User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Get Bot Response
    if st.session_state.conversation:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.conversation({'question': prompt})
                answer = response['answer']
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
    else:

        st.error("Please upload a PDF first!")

