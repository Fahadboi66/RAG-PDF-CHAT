from langchain_community.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader, UnstructuredPowerPointLoader, UnstructuredExcelLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

def process_document(file_path: str): 
    print("Processing Document....")
    # Load the document based on file type
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".docx"):
        print("Mime/Type: docx")
        loader = UnstructuredWordDocumentLoader(file_path)
    elif file_path.endswith(".pptx"):
        loader = UnstructuredPowerPointLoader(file_path)
    elif file_path.endswith(".xlsx"):
        loader = UnstructuredExcelLoader(file_path)
    else:
        raise ValueError("Unsupported file type")

    # Load the document
    documents = loader.load()

    # Split the document into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)

    # Generate embeddings for each chunk
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = [model.encode(chunk.page_content) for chunk in chunks]
    print("Embeddings created: ", embeddings)
    return chunks, embeddings