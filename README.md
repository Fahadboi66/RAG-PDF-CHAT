# 📄 RAG PDF Chat

An AI-powered application that allows users to upload PDF documents and ask questions about their content using **Retrieval-Augmented Generation (RAG)**. The application retrieves the most relevant information from the uploaded document using **ChromaDB** before generating context-aware responses with an LLM.

---

## ✨ Features

- 📂 Upload PDF documents
- 💬 Chat with your PDFs using natural language
- 🧠 Context-aware responses with RAG
- 🔍 Semantic search using vector embeddings
- 📚 Automatic document chunking
- ⚡ Fast similarity search with ChromaDB
- 🐳 Docker support

---

## 🏗️ Architecture

The project consists of two services:

### Node.js Server
- Handles client requests
- Manages PDF uploads
- Communicates with the Python AI service

### Python Server
- Processes uploaded PDFs
- Splits documents into chunks
- Generates embeddings
- Stores embeddings in ChromaDB
- Retrieves relevant document chunks
- Generates AI responses using the RAG pipeline

---

## 🔄 How It Works

1. Upload a PDF document.
2. The document is divided into smaller text chunks.
3. Embeddings are generated for each chunk.
4. The embeddings are stored in **ChromaDB**.
5. When a question is asked:
   - The question is converted into an embedding.
   - ChromaDB retrieves the most relevant document chunks.
   - The retrieved context and the user's question are sent to the LLM.
6. The model generates an answer based on the retrieved context.

---

## 🧠 RAG Pipeline

```text
           PDF Upload
                │
                ▼
      Document Processing
                │
                ▼
       Document Chunking
                │
                ▼
     Generate Embeddings
                │
                ▼
      Store in ChromaDB
                │
────────────────────────────────────
                │
         User Question
                │
                ▼
      Generate Embedding
                │
                ▼
   Similarity Search (ChromaDB)
                │
                ▼
 Retrieve Relevant Chunks
                │
                ▼
  LLM + Retrieved Context
                │
                ▼
         Final Response
```

---

## 🛠️ Technologies Used

- Python
- Node.js
- LangChain
- ChromaDB
- Docker
- Retrieval-Augmented Generation (RAG)
- Vector Embeddings

---

## 📂 Project Structure

```text
RAG-PDF-CHAT/
│
├── node-server/
│   └── Node.js application
│
├── python-server/
│   └── Python AI service
│
├── docker-compose.yml
│
└── README.md
```

---

## 🚀 Getting Started

### Clone the repository

```bash
git clone https://github.com/Fahadboi66/RAG-PDF-CHAT.git
cd RAG-PDF-CHAT
```

### Run with Docker

```bash
docker compose up --build
```

Or start the Node.js and Python servers separately according to their respective configurations.

---

## 📌 Future Improvements

- Multiple PDF support
- Chat history and conversation memory
- Streaming AI responses
- Authentication and user accounts
- Cloud deployment
- Support for additional document formats

---

## 👨‍💻 Author

**Fahad Zafar**

- LinkedIn: https://www.linkedin.com/in/fahadzafar66
- Email: fahadboi66@gmail.com

---

⭐ If you found this project useful, consider giving it a star!
