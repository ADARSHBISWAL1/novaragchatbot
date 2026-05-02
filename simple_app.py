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
    .creator-tag {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: rgba(255, 255, 255, 0.95);
        border: 1px solid #ddd;
        border-radius: 12px;
        padding: 8px 12px;
        display: flex;
        align-items: center;
        gap: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        z-index: 1000;
        font-size: 0.8rem;
        color: #333;
        backdrop-filter: blur(10px);
    }
    .creator-avatar {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        border: 1px solid #ddd;
    }
    .creator-info {
        display: flex;
        flex-direction: column;
        line-height: 1.2;
    }
    .creator-name {
        font-weight: 600;
        color: #2196f3;
    }
    .creator-badge {
        font-size: 0.7rem;
        color: #666;
        background: #f0f0f0;
        padding: 2px 6px;
        border-radius: 4px;
        margin-top: 2px;
    }
    .creator-link {
        text-decoration: none;
        color: inherit;
    }
    .creator-link:hover {
        text-decoration: none;
        color: #2196f3;
    }
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }
    .stat-card {
        background: white;
        border: 1px solid #ddd;
        border-radius: 0.5rem;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.5rem;
    }
    .category-section {
        background: white;
        border: 1px solid #ddd;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .category-header {
        font-weight: bold;
        color: #333;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .welcome-section {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 1rem;
        padding: 2rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    .welcome-title {
        font-size: 2rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 1rem;
    }
    .welcome-subtitle {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 1.5rem;
    }
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin-top: 1.5rem;
    }
    .feature-card {
        background: white;
        border: 1px solid #ddd;
        border-radius: 0.5rem;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    .feature-title {
        font-weight: bold;
        color: #333;
        margin-bottom: 0.5rem;
    }
    .feature-desc {
        font-size: 0.9rem;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_chatbot():
    """Initialize the chatbot (cached for performance)"""
    # Use relative paths that work both locally and on Streamlit Cloud
    document_paths = [
        "solar_system_improved.json",
        "earth_geography_improved.json", 
        "product_launches_clean.json",
        "chatbot_dataset_clean.json",
        "health_finance_clean.json"
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
        # Dashboard Header
        st.markdown("""
        <div class="dashboard-header">
            <h1>🤖 Nove Dashboard</h1>
            <p>Nova's Enhanced Virtual Assistant</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Knowledge Base Statistics
        if chatbot:
            stats = chatbot.vector_store.get_stats()
            st.markdown("""
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{}</div>
                    <div class="stat-label">Documents</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{}</div>
                    <div class="stat-label">Embedding Dim</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{}</div>
                    <div class="stat-label">Model</div>
                </div>
            </div>
            """.format(
                stats.get('total_documents', 'N/A'),
                stats.get('embedding_dimension', 'N/A'),
                stats.get('model_name', 'N/A').split('-')[0]
            ), unsafe_allow_html=True)
        
        # Knowledge Base Categories
        st.markdown("""
        <div class="category-section">
            <div class="category-header">
                <span>📚</span>
                <span>Knowledge Base Categories</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        categories = {
            "🌍 Earth Sciences": ["Geography", "Climate", "Environment", "Oceans"],
            "🪐 Solar System": ["Planets", "Moons", "Astronomy", "Space"],
            "🏢 Business": ["NovaSpark AI", "Products", "Launches", "Company Info"],
            "🏥 Health": ["Symptoms", "Conditions", "Treatments", "Prevention"],
            "💰 Finance": ["Investing", "Banking", "Markets", "Personal Finance"],
            "💬 Conversational": ["Greetings", "Jokes", "Help", "Emotions"]
        }
        
        for category, topics in categories.items():
            with st.expander(category):
                for topic in topics:
                    st.write(f"• {topic}")
        
        # Quick Actions
        st.markdown("""
        <div class="category-section">
            <div class="category-header">
                <span>⚡</span>
                <span>Quick Actions</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
        
        with col2:
            if st.button("📊 Refresh Stats", use_container_width=True):
                st.rerun()
        
        # Sample Questions by Category
        st.markdown("""
        <div class="category-section">
            <div class="category-header">
                <span>💡</span>
                <span>Sample Questions</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        question_categories = {
            "Business": [
                "What is NovaSpark AI?",
                "Tell me about SupportBot Pro",
                "How does LeadSpark work?"
            ],
            "Science": [
                "Which planet has the most moons?",
                "What are Earth's climate zones?",
                "What is the Great Red Spot?"
            ],
            "Health": [
                "What are diabetes symptoms?",
                "What is hypertension?",
                "What is a healthy diet?"
            ],
            "Finance": [
                "What is a stock?",
                "What is compound interest?",
                "What is diversification?"
            ],
            "General": [
                "Hi, how are you?",
                "Tell me a joke",
                "Thank you"
            ]
        }
        
        for category, questions in question_categories.items():
            with st.expander(category):
                for question in questions:
                    if st.button(question, key=f"sample_{question}", use_container_width=True):
                        st.session_state.current_question = question
    
    # Main chat interface
    if not chatbot:
        st.error("Chatbot is not initialized. Please check your document paths.")
        return
    
    # Display welcome message or chat history
    if not st.session_state.messages:
        # Welcome header
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 1rem; margin-bottom: 2rem;">
            <h1 style="font-size: 2rem; font-weight: bold; color: #333; margin-bottom: 1rem;">🤖 Welcome to Nove</h1>
            <p style="font-size: 1.1rem; color: #666; margin-bottom: 1.5rem;">Nova's Enhanced Virtual Assistant</p>
            <p style="color: #666; margin-bottom: 1.5rem;">
                I'm here to help you with information across multiple domains using advanced RAG technology.
                Ask me anything and I'll provide accurate, sourced responses!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: white; border: 1px solid #ddd; border-radius: 0.5rem; padding: 1rem; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🌍</div>
                <div style="font-weight: bold; color: #333; margin-bottom: 0.5rem;">Earth Sciences</div>
                <div style="font-size: 0.9rem; color: #666;">Geography, climate, environment, and more</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background: white; border: 1px solid #ddd; border-radius: 0.5rem; padding: 1rem; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🏥</div>
                <div style="font-weight: bold; color: #333; margin-bottom: 0.5rem;">Health</div>
                <div style="font-size: 0.9rem; color: #666;">Medical topics with educational focus</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: white; border: 1px solid #ddd; border-radius: 0.5rem; padding: 1rem; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🪐</div>
                <div style="font-weight: bold; color: #333; margin-bottom: 0.5rem;">Solar System</div>
                <div style="font-size: 0.9rem; color: #666;">Planets, moons, astronomy, and space</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background: white; border: 1px solid #ddd; border-radius: 0.5rem; padding: 1rem; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">💰</div>
                <div style="font-weight: bold; color: #333; margin-bottom: 0.5rem;">Finance</div>
                <div style="font-size: 0.9rem; color: #666;">Investing, banking, and personal finance</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: white; border: 1px solid #ddd; border-radius: 0.5rem; padding: 1rem; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🏢</div>
                <div style="font-weight: bold; color: #333; margin-bottom: 0.5rem;">Business</div>
                <div style="font-size: 0.9rem; color: #666;">NovaSpark AI, products, and company info</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background: white; border: 1px solid #ddd; border-radius: 0.5rem; padding: 1rem; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">💬</div>
                <div style="font-weight: bold; color: #333; margin-bottom: 0.5rem;">Conversational</div>
                <div style="font-size: 0.9rem; color: #666;">Chat, jokes, and friendly interactions</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Getting started section
        st.markdown("""
        <div style="margin-top: 2rem; padding: 1rem; background: rgba(255,255,255,0.8); border-radius: 0.5rem; border: 1px solid #ddd;">
            <p style="color: #333; font-weight: bold; margin-bottom: 0.5rem;">🚀 Getting Started:</p>
            <p style="color: #666; margin: 0;">
                Type your question below or explore sample questions in the sidebar. 
                I will provide accurate answers with source attribution!
            </p>
        </div>
        """, unsafe_allow_html=True)
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
    
    # Creator tag
    st.markdown("""
    <div class="creator-tag">
        <a href="https://github.com/ADARSHBISWAL1" target="_blank" class="creator-link">
            <img src="https://camo.githubusercontent.com/fe52f52856c225c1615f326817a0b200ca0d7b1f9c4781485601933da88668e6/68747470733a2f2f6d656469612e67697068792e636f6d2f6d656469612f6876524a434c4a7a366177566c496b4a375a2f67697068792e676966" alt="Adarsh Biswal" class="creator-avatar">
            <div class="creator-info">
                <span class="creator-name">Adarsh Biswal</span>
                <span class="creator-badge">Prototype</span>
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
