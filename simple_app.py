import streamlit as st
import os
from simple_chatbot import SimpleNoveChatbot

st.set_page_config(
    page_title="Nove - Nova's Enhanced Virtual Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        color: #000000;
    }
    .bot-message {
        background-color: #f8f9fa;
        border-left: 4px solid #4caf50;
        color: #000000;
    }
    .source-info {
        font-size: 0.8rem;
        color: #000000;
        margin-top: 0.5rem;
        padding: 0.5rem;
        background-color: #ffffff;
        border: 1px solid #ddd;
        border-radius: 0.25rem;
    }
    .welcome-message {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 1rem;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_chatbot():
    """Initialize the chatbot (cached for performance)"""
    document_paths = [
        "C:\\Users\\adars\\Desktop\\pograming\\Ragchatbot\\nova_faq_dataset.pdf",
        "C:\\Users\\adars\\Desktop\\pograming\\Ragchatbot\\solar_system_improved.json",
        "C:\\Users\\adars\\Desktop\\pograming\\Ragchatbot\\earth_geography_improved.json",
        "C:\\Users\\adars\\Desktop\\pograming\\Ragchatbot\\novaspark_clean.json",
        "C:\\Users\\adars\\Desktop\\pograming\\Ragchatbot\\product_launches_clean.json",
        "C:\\Users\\adars\\Desktop\\pograming\\Ragchatbot\\chatbot_dataset_clean.json"
    ]
    
    chatbot = SimpleNoveChatbot()
    
    if chatbot.initialize(document_paths):
        return chatbot
    else:
        st.error("❌ Failed to initialize chatbot. Please check the document paths.")
        return None

def main():
    """Main Streamlit app"""
    st.title("🤖 Nove - Nova's Enhanced Virtual Assistant")
    st.markdown("*Your intelligent assistant for NovaSpark AI, Earth Sciences, and Solar System information*")
    
    # Initialize chatbot
    if 'chatbot' not in st.session_state:
        with st.spinner("🚀 Initializing Nove... This may take a few moments on first run..."):
            st.session_state.chatbot = initialize_chatbot()
            st.session_state.messages = []
    
    chatbot = st.session_state.chatbot
    
    # Sidebar with information
    with st.sidebar:
        st.header("📚 About Nove")
        st.write("""
        **Nove** is Nova's Enhanced Virtual Assistant, powered by RAG (Retrieval-Augmented Generation) technology.
        
        **Knowledge Base:**
        - NovaSpark AI company info
        - Product documentation
        - Earth sciences data
        - Solar system information
        - FAQ and news articles
        
        **Capabilities:**
        - Semantic search
        - Context-aware responses
        - Source attribution
        """)
        
        if chatbot:
            stats = chatbot.vector_store.get_stats()
            st.subheader("📊 Knowledge Base Stats")
            st.write(f"- Documents: {stats.get('total_documents', 'N/A')}")
            st.write(f"- Model: {stats.get('model_name', 'N/A')}")
            st.write(f"- Index Type: {stats.get('index_type', 'N/A')}")
        
        st.subheader("💡 Sample Questions")
        sample_questions = [
            "What is NovaSpark AI?",
            "Tell me about SupportBot Pro",
            "What are Earth's climate zones?",
            "Which planet has the most moons?",
            "How does LeadSpark work?",
            "What is the Great Red Spot?"
        ]
        
        for question in sample_questions:
            if st.button(question, key=f"sample_{question}"):
                st.session_state.current_question = question
    
    # Main chat interface
    if not chatbot:
        st.error("Chatbot is not initialized. Please check your document paths.")
        return
    
    # Display welcome message or chat history
    if not st.session_state.messages:
        welcome_msg = chatbot.get_welcome_message()
        st.markdown(f'<div class="welcome-message">{welcome_msg}</div>', unsafe_allow_html=True)
    else:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'''
                <div class="chat-message user-message">
                    <strong>👤 You:</strong> {message["content"]}
                </div>
                ''', unsafe_allow_html=True)
            else:
                # Handle sources separately to avoid f-string nesting issues
                sources_html = ""
                if message.get("sources"):
                    source_list = ", ".join([f"{os.path.basename(s.get('source', 'Unknown'))} ({s.get('type', 'Unknown')})" for s in message["sources"]])
                    sources_html = f'<div class="source-info">📚 Sources: {source_list}</div>'
                
                st.markdown(f'''
                <div class="chat-message bot-message">
                    <strong>🤖 Nove:</strong> {message["content"]}
                    {sources_html}
                </div>
                ''', unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("Ask me anything about NovaSpark AI, Earth sciences, or the Solar System...")
    
    # Handle sample question buttons
    if 'current_question' in st.session_state:
        user_input = st.session_state.current_question
        del st.session_state.current_question
    
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Generate bot response
        with st.spinner("🤔 Thinking..."):
            result = chatbot.chat(user_input)
        
        # Add bot response to chat history
        st.session_state.messages.append({
            "role": "assistant", 
            "content": result["response"],
            "sources": result["sources"]
        })
        
        # Rerun to display the new messages
        st.rerun()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    main()
