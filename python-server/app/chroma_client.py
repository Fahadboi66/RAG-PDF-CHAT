import chromadb
from sentence_transformers import SentenceTransformer

class ChromaClient:
    def __init__(self):
        """
        Initialize the ChromaDB client and connect to the server.
        """
        # Connect to ChromaDB server running on localhost:8000
        self.client = chromadb.HttpClient(host="chromadb", port=8000)
        
        # Create or get a collection named "documents"
        self.collection = self.client.get_or_create_collection(name="documents")

    def add_document(self, chunks, embeddings, metadata):
        """
        Add document chunks, embeddings, and metadata to ChromaDB.
        """
        # Generate unique IDs for each chunk (e.g., doc_0, doc_1, ...)
        ids = [f"{metadata['mongo_id']}_{i}" for i in range(len(chunks))]
        
        # Extract text from chunks
        documents = [chunk.page_content for chunk in chunks]
        
        # Add documents, embeddings, and metadata to ChromaDB
        self.collection.add(
            ids=ids,  # Unique IDs for each chunk
            embeddings=embeddings,  # Embeddings for each chunk
            documents=documents,  # Text content of each chunk
            metadatas=[metadata] * len(chunks)  # Metadata for each chunk
        )

    def delete_document(self, mongo_id: str):
        """
        Delete a document and its related chunks from ChromaDB.

        Args:
            mongo_id (str): The MongoDB ID of the document to delete.
        """
        # Delete all chunks with the given MongoDB ID
        self.collection.delete(where={"mongo_id": mongo_id})

    def get_metadata_by_mongo_id(self, mongo_id: str):
        """
        Retrieve metadata for a specific document by its MongoDB ID.

        Args:
            mongo_id (str): The MongoDB ID of the document.

        Returns:
            list: List of metadata for the document chunks.
        """
        # Query the collection for chunks with the given MongoDB ID
        results = self.collection.get(where={"mongo_id": mongo_id})
        
        # Extract metadata from the results
        metadata_list = results.get("metadatas", [])
        
        # Return the first metadata entry (all chunks share the same metadata)
        return metadata_list[0] if metadata_list else None

    def query_document(self, mongo_id: str, query: str, n_results: int = 5):
        """
        Query a specific document by its MongoDB ID and a query string.

        Args:
            mongo_id (str): The MongoDB ID of the document.
            query (str): The query string.
            n_results (int): Number of results to return.

        Returns:
            list: List of relevant document chunks.
        """
        # Generate embeddings for the query string
        model = SentenceTransformer("all-MiniLM-L6-v2")
        query_embedding = model.encode(query)

        # Query the collection for chunks with the given MongoDB ID
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where={"mongo_id": mongo_id}  # Filter by mongo_id
        )
        
        return results