import os
import openai
from typing import List, Dict, Any
from dotenv import load_dotenv
from document_processor import DocumentProcessor
from vector_store import VectorStore

load_dotenv()

class NoveChatbot:
    """RAG Chatbot named 'Nove' - Nova's Enhanced Virtual Assistant"""
    
    def __init__(self, api_key: str = None):
        self.name = "Nove"
        self.description = "Nova's Enhanced Virtual Assistant - I'm here to help you with information about NovaSpark AI, Earth sciences, and the Solar System!"
        
        # Set up OpenAI
        if api_key:
            openai.api_key = api_key
        elif os.getenv('OPENAI_API_KEY'):
            openai.api_key = os.getenv('OPENAI_API_KEY')
        else:
            print("Warning: No OpenAI API key found. Please set OPENAI_API_KEY environment variable.")
        
        # Initialize components
        self.document_processor = DocumentProcessor()
        self.vector_store = VectorStore()
        self.is_initialized = False
    
    def initialize(self, document_paths: List[str], index_path: str = "nove_index"):
        """Initialize the chatbot with documents"""
        print(f"🚀 Initializing {self.name}...")
        
        # Try to load existing index
        if os.path.exists(f"{index_path}.faiss") and os.path.exists(f"{index_path}.pkl"):
            print("📚 Loading existing index...")
            self.vector_store.load_index(index_path)
        else:
            print("📄 Processing documents...")
            # Process documents
            chunks = self.document_processor.process_all_documents(document_paths)
            
            if not chunks:
                print("❌ No documents processed successfully!")
                return False
            
            # Build vector index
            print("🔍 Building vector index...")
            self.vector_store.build_index(chunks)
            
            # Save index for future use
            self.vector_store.save_index(index_path)
        
        self.is_initialized = True
        print(f"✅ {self.name} is ready to assist!")
        print(f"📊 Knowledge Base Stats: {self.vector_store.get_stats()}")
        return True
    
    def search_relevant_docs(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Search for relevant documents"""
        if not self.is_initialized:
            raise ValueError("Chatbot not initialized. Call initialize() first.")
        
        results = self.vector_store.search(query, k)
        return [doc for doc, score in results if score > 0.3]  # Filter low relevance
    
    def generate_response(self, query: str, context_docs: List[Dict[str, Any]]) -> str:
        """Generate response using OpenAI with context"""
        if not context_docs:
            return "I apologize, but I couldn't find relevant information in my knowledge base to answer your question. Could you please rephrase it or ask something else?"
        
        # Prepare context
        context = "\n\n".join([
            f"Document {i+1}: {doc['content'][:500]}..." 
            for i, doc in enumerate(context_docs[:3])
        ])
        
        # Create prompt
        prompt = f"""You are Nove, Nova's Enhanced Virtual Assistant. You're helpful, friendly, and knowledgeable about NovaSpark AI products, Earth sciences, and the Solar System.

Based on the following context information, please answer the user's question. If the context doesn't contain the answer, say so politely and suggest what information you do have available.

Context:
{context}

User Question: {query}

Please provide a helpful and accurate response:"""

        try:
            from openai import OpenAI
            client = OpenAI()
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Nove, a helpful AI assistant specialized in NovaSpark AI, Earth sciences, and Solar System information."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            return f"I apologize, but I encountered an error while generating my response: {str(e)}"
    
    def chat(self, query: str) -> Dict[str, Any]:
        """Main chat interface"""
        if not self.is_initialized:
            return {
                "response": "I'm not initialized yet. Please call initialize() with your document paths first.",
                "sources": []
            }
        
        # Search for relevant documents
        relevant_docs = self.search_relevant_docs(query)
        
        # Generate response
        response = self.generate_response(query, relevant_docs)
        
        # Prepare sources
        sources = []
        for doc in relevant_docs[:3]:
            metadata = doc.get('metadata', {})
            sources.append({
                "source": metadata.get('source', 'Unknown'),
                "type": metadata.get('type', 'Unknown'),
                "category": metadata.get('category', 'General')
            })
        
        return {
            "response": response,
            "sources": sources,
            "query": query
        }
    
    def get_welcome_message(self) -> str:
        """Get welcome message"""
        return f"""👋 Hello! I'm {self.name}, {self.description}

I can help you with:
• NovaSpark AI company information and products
• Earth geography, climate, and environmental topics
• Solar system and astronomy information
• General questions based on my knowledge base

What would you like to know today?"""

def main():
    """Test the chatbot"""
    # Document paths
    document_paths = [
        "C:\\Users\\adars\\Desktop\\pograming\\Ragchatbot\\nova_faq_dataset.pdf",
        "C:\\Users\\adars\\Desktop\\pograming\\Ragchatbot\\earth_geography_climate.json",
        "C:\\Users\\adars\\Desktop\\pograming\\Ragchatbot\\rag_dataset.json",
        "C:\\Users\\adars\\Desktop\\pograming\\Ragchatbot\\rag_dataset_product_launches.json",
        "C:\\Users\\adars\\Desktop\\pograming\\Ragchatbot\\solar_system.json"
    ]
    
    # Initialize chatbot
    nove = NoveChatbot()
    
    if nove.initialize(document_paths):
        print("\n" + "="*50)
        print(nove.get_welcome_message())
        print("="*50)
        
        # Test queries
        test_queries = [
            "What is NovaSpark AI?",
            "Tell me about Earth's atmosphere",
            "What are the planets in the solar system?",
            "What products does NovaSpark AI offer?",
            "How does SupportBot Pro work?"
        ]
        
        for query in test_queries:
            print(f"\n🤔 User: {query}")
            result = nove.chat(query)
            print(f"🤖 {nove.name}: {result['response']}")
            if result['sources']:
                print(f"📚 Sources: {[s['source'] for s in result['sources']]}")
            print("-" * 30)

if __name__ == "__main__":
    main()
