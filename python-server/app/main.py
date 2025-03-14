from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from app.utils import process_document
from app.chroma_client import ChromaClient

app = FastAPI()

class DocumentRequest(BaseModel):
    file_path: str  # Path to the document
    metadata: dict  # Metadata (e.g., MongoDB ID, author, title)

class DeleteRequest(BaseModel):
    file_path: str  # Path to the document
    mongo_id: str  # MongoDB ID of the document to delete

class QueryRequest(BaseModel):
    mongo_id: str  # MongoDB ID of the document
    query: str  # Query string
    n_results: int = 5  # Number of results to return

@app.post("/saveDoc")
async def save_doc(request: DocumentRequest):

    print("Request recieved...")
    # Check if the file exists
    if not os.path.exists(request.file_path):
        print("File does not exist")
        raise HTTPException(status_code=404, detail="File not found")

    # Process the document (split into chunks and generate embeddings)
    chunks, embeddings = process_document(request.file_path)

    print("Document processed successfully")
    print("chunks: ", chunks)

    # Store embeddings in ChromaDB
    chroma_client = ChromaClient()
    chroma_client.add_document(chunks, embeddings, request.metadata)

    return {"message": "Document processed and stored successfully"}

@app.post("/deleteDoc")
async def delete_doc(request: DeleteRequest):
    # Delete the file from local drive (if it exists)
    if os.path.exists(request.file_path):
        try:
            os.remove(request.file_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete local file: {str(e)}")

    # Delete the document from ChromaDB
    chroma_client = ChromaClient()
    try:
        chroma_client.delete_document(request.mongo_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete from ChromaDB: {str(e)}")

    return {"message": "Document deleted successfully"}


@app.get("/getDocMeta/{mongo_id}")
async def get_doc_meta(mongo_id: str):
    """
    Retrieve metadata for a specific document by its MongoDB ID.
    """
    chroma_client = ChromaClient()
    
    try:
        # Query the collection for metadata
        metadata = chroma_client.get_metadata_by_mongo_id(mongo_id)
        if not metadata:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return {"metadata": metadata}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve metadata: {str(e)}")


@app.post("/queryDoc")
async def query_doc(request: QueryRequest):
    """
    Query a specific document by its MongoDB ID and a query string.
    """
    chroma_client = ChromaClient()
    
    try:
        # Query the document
        results = chroma_client.query_document(request.mongo_id, request.query, request.n_results)
        if not results:
            raise HTTPException(status_code=404, detail="No results found")
        
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to query document: {str(e)}")
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)