Check out live project here - https://falyfktf3qyiruuzosbtfm.streamlit.app/

# 📚 Chat with PDF using RAG & Llama 3

This is a **Retrieval-Augmented Generation (RAG)** application built with **Streamlit** and **LangChain**. It allows users to upload a PDF document and chat with it using the **Groq API (Llama 3)** for extremely fast inference.

## 🚀 Features

* **RAG Pipeline**: accurately retrieves context from uploaded documents.
* **Groq API Integration**: Uses `llama-3.3-70b` for high-speed, free/low-cost responses.
* **Vector Search**: Uses **FAISS** and **HuggingFace Embeddings** for semantic search.
* **Memory**: Maintains conversation history so you can ask follow-up questions.
* **Secure**: API Keys are managed via Streamlit Secrets (no hardcoding).

## 🛠️ Tech Stack

* **Frontend**: Streamlit
* **LLM**: Groq (Llama 3.3)
* **Embeddings**: `sentence-transformers/all-MiniLm-L6-v2`
* **Vector Store**: FAISS
* **Orchestration**: LangChain

## 📦 Installation & Local Run

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
    cd YOUR_REPO_NAME
    ```

2.  **Install dependencies**
    It is crucial to install the specific versions to avoid conflicts:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the App**
    ```bash
    streamlit run app.py
    ```
4. Screenshots
<img width="1363" height="680" alt="image" src="https://github.com/user-attachments/assets/8c98f94a-bf1f-4b80-8aa1-adec91e492cd" />

## 🔑 Configuration

To run this app, you need a **Groq API Key**.
1.  Get your free key from [console.groq.com](https://console.groq.com/).
2.  **Local Run**: The app will ask for the key in the sidebar if not found in environment variables.
3.  **Deployment**: Set the key in Streamlit "Secrets" settings as `GROQ_API_KEY`.

## 📂 Project Structure
├── app.py # Main application logic ├── requirements.txt # Dependencies with specific versions └── README.md # Documentation
---
*Built by Sutharsan N.*
