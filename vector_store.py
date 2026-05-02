import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Tuple
import pickle
import os

class VectorStore:
    """FAISS-based vector store for semantic search"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.documents = []
        self.dimension = 384  # Dimension for all-MiniLM-L6-v2
    
    def create_embeddings(self, texts: List[str]) -> np.ndarray:
        """Create embeddings for a list of texts"""
        print(f"Creating embeddings for {len(texts)} texts...")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return embeddings.astype('float32')
    
    def build_index(self, documents: List[Dict[str, Any]]):
        """Build FAISS index from documents"""
        self.documents = documents
        
        # Extract text content
        texts = [doc['content'] for doc in documents]
        
        # Create embeddings
        embeddings = self.create_embeddings(texts)
        
        # Create FAISS index
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(embeddings)
        
        print(f"Index built with {len(documents)} documents")
    
    def search(self, query: str, k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        """Search for similar documents"""
        if self.index is None:
            raise ValueError("Index not built. Call build_index first.")
        
        # Create query embedding
        query_embedding = self.model.encode([query])
        query_embedding = query_embedding.astype('float32')
        
        # Search
        distances, indices = self.index.search(query_embedding, k)
        
        # Return results with documents and distances
        results = []
        for i, (idx, dist) in enumerate(zip(indices[0], distances[0])):
            if idx < len(self.documents):
                doc = self.documents[idx]
                # Convert distance to similarity score (lower distance = higher similarity)
                similarity = 1 / (1 + dist)
                results.append((doc, similarity))
        
        return results
    
    def save_index(self, save_path: str):
        """Save index and documents to disk"""
        if self.index is None:
            raise ValueError("No index to save")
        
        # Save FAISS index
        faiss.write_index(self.index, f"{save_path}.faiss")
        
        # Save documents
        with open(f"{save_path}.pkl", 'wb') as f:
            pickle.dump(self.documents, f)
        
        print(f"Index saved to {save_path}")
    
    def load_index(self, load_path: str):
        """Load index and documents from disk"""
        # Load FAISS index
        self.index = faiss.read_index(f"{load_path}.faiss")
        
        # Load documents
        with open(f"{load_path}.pkl", 'rb') as f:
            self.documents = pickle.load(f)
        
        print(f"Index loaded from {load_path}")
        print(f"Loaded {len(self.documents)} documents")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store"""
        if self.index is None:
            return {"status": "No index built"}
        
        return {
            "total_documents": len(self.documents),
            "index_type": type(self.index).__name__,
            "embedding_dimension": self.dimension,
            "model_name": "all-MiniLM-L6-v2"
        }
