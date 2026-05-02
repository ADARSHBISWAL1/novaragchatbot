import os
from typing import List, Dict, Any
from document_processor import DocumentProcessor
from vector_store import VectorStore

class SimpleNoveChatbot:
    """Simplified RAG Chatbot named 'Nove' - Nova's Enhanced Virtual Assistant"""
    
    def __init__(self):
        self.name = "Nove"
        self.description = "Nova's Enhanced Virtual Assistant - I'm here to help you with information about NovaSpark AI, Earth sciences, and the Solar System!"
        
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
    
    def generate_simple_response(self, query: str, context_docs: List[Dict[str, Any]]) -> str:
        """Generate a simple response without OpenAI"""
        if not context_docs:
            return f"I couldn't find specific information about '{query}' in my knowledge base. Could you try rephrasing your question or ask about something else?"
        
        # Look for exact question matches in Q&A format
        for doc in context_docs:
            content = doc['content']
            metadata = doc.get('metadata', {})
            
            # Check if this is Q&A format content
            if metadata.get('type') == 'qa' and 'Question:' in content and 'Answer:' in content:
                # Extract the question and answer
                parts = content.split('\nAnswer: ')
                if len(parts) >= 2:
                    question_part = parts[0].replace('Question: ', '').strip()
                    answer_part = parts[1].strip()
                    
                    # Check if the query matches or is similar to the question
                    if self._is_similar_query(query.lower(), question_part.lower()):
                        return answer_part
        
        # If no exact match, try to find relevant answers
        best_answers = []
        for doc in context_docs[:3]:
            content = doc['content']
            metadata = doc.get('metadata', {})
            
            # For Q&A format, extract just the answer part
            if metadata.get('type') == 'qa' and 'Answer:' in content:
                answer_part = content.split('Answer: ')[1].strip()
                best_answers.append(answer_part)
            else:
                # For other formats, extract key information
                if len(content) > 300:
                    content = content[:300] + "..."
                best_answers.append(content)
        
        # Remove duplicates and format naturally
        unique_answers = []
        seen = set()
        for answer in best_answers:
            if answer not in seen:
                unique_answers.append(answer)
                seen.add(answer)
        
        if unique_answers:
            return "\n\n".join(unique_answers[:2])  # Return top 2 answers
        else:
            return f"I found some information about {query}, but I need to process it better. Could you try asking more specifically?"
    
    def _is_similar_query(self, query1: str, query2: str) -> bool:
        """Check if two queries are similar"""
        # Simple similarity check - can be improved
        query1_words = set(query1.split())
        query2_words = set(query2.split())
        
        # Check if at least 60% of words match
        intersection = query1_words.intersection(query2_words)
        union = query1_words.union(query2_words)
        
        if not union:
            return False
        
        similarity = len(intersection) / len(union)
        return similarity > 0.6
    
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
        response = self.generate_simple_response(query, relevant_docs)
        
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
    from typing import List, Dict, Any
    
    # Document paths
    document_paths = [
        "C:\\Users\\adars\\Desktop\\pograming\\Ragchatbot\\nova_faq_dataset.pdf",
        "C:\\Users\\adars\\Desktop\\pograming\\Ragchatbot\\earth_geography_climate.json",
        "C:\\Users\\adars\\Desktop\\pograming\\Ragchatbot\\rag_dataset.json",
        "C:\\Users\\adars\\Desktop\\pograming\\Ragchatbot\\rag_dataset_product_launches.json",
        "C:\\Users\\adars\\Desktop\\pograming\\Ragchatbot\\solar_system.json"
    ]
    
    # Initialize chatbot
    nove = SimpleNoveChatbot()
    
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
