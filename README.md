# 🤖 Nove - Nova's Enhanced Virtual Assistant


active link - https://novaragchatbot-cde.streamlit.app

A sophisticated RAG (Retrieval-Augmented Generation) chatbot that provides intelligent responses based on a comprehensive knowledge base.

## 🌟 Features

- **Multi-Source Knowledge**: Integrates information from NovaSpark AI company data, Earth sciences, and Solar system data
- **Semantic Search**: Uses advanced embedding models for accurate document retrieval
- **Context-Aware Responses**: Generates relevant answers using retrieved context
- **Web Interface**: Beautiful Streamlit-based chat interface
- **Source Attribution**: Shows the sources used for each response
- **Fast Performance**: FAISS-based vector storage for efficient similarity search

## 📚 Knowledge Base

Nove is trained on the following documents:

1. **NovaSpark AI Data**
   - Company profile and team information
   - Product details (SupportBot Pro, LeadSpark, FlowDesk)
   - News articles and press releases
   - Customer stories and case studies
   - FAQ and support information

2. **Earth Sciences**
   - Geography and climate information
   - Atmospheric data
   - Ocean and weather patterns
   - Environmental topics

3. **Solar System**
   - Detailed information about all planets
   - Physical properties and orbital data
   - Atmospheric composition
   - Moon information

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. **Clone or download the project files**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**:
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your OpenAI API key
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the web interface**:
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** and navigate to `http://localhost:8501`

### Command Line Usage

You can also test Nove directly from the command line:

```bash
python rag_chatbot.py
```

## 🏗️ Architecture

### Components

1. **Document Processor** (`document_processor.py`)
   - Handles PDF text extraction
   - Processes JSON files with different structures
   - Intelligent text chunking for optimal retrieval

2. **Vector Store** (`vector_store.py`)
   - Uses Sentence Transformers for embeddings
   - FAISS index for fast similarity search
   - Persistent storage capabilities

3. **RAG Chatbot** (`rag_chatbot.py`)
   - Main chatbot logic
   - OpenAI integration for response generation
   - Context retrieval and formatting

4. **Web Interface** (`app.py`)
   - Streamlit-based chat interface
   - Real-time conversation
   - Source attribution display

### Technology Stack

- **Embedding Model**: Sentence Transformers (all-MiniLM-L6-v2)
- **Vector Database**: FAISS
- **LLM**: OpenAI GPT-3.5-turbo
- **Web Framework**: Streamlit
- **Document Processing**: PyPDF2, JSON

## 📊 Usage Examples

### Sample Questions

Try asking Nove questions like:

- "What is NovaSpark AI and what products do they offer?"
- "Tell me about Earth's atmosphere and climate zones"
- "Which planet in the solar system has the most moons?"
- "How does SupportBot Pro help businesses?"
- "What are the main layers of Earth's structure?"
- "Explain the Great Red Spot on Jupiter"

### Response Features

Each response includes:
- **Contextual Answer**: Based on retrieved relevant documents
- **Source Attribution**: Shows which documents were used
- **Confidence Scoring**: Filters out low-relevance results

## 🔧 Configuration

### Customization Options

You can customize various aspects of Nove:

1. **Embedding Model**: Change the Sentence Transformer model in `vector_store.py`
2. **Chunk Size**: Adjust text chunking parameters in `document_processor.py`
3. **Search Parameters**: Modify the number of retrieved documents and similarity thresholds
4. **LLM Model**: Switch to different OpenAI models in `rag_chatbot.py`

### Adding New Documents

To add new documents to the knowledge base:

1. Place your files in the project directory
2. Update the `document_paths` list in `rag_chatbot.py` and `app.py`
3. Delete the existing index files (`nove_index.faiss` and `nove_index.pkl`)
4. Restart the application to reindex

## 📝 File Structure

```
Ragchatbot/
├── app.py                     # Streamlit web interface
├── rag_chatbot.py            # Main chatbot implementation
├── document_processor.py      # Document processing and chunking
├── vector_store.py           # Vector storage and search
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── README.md                 # This file
├── nova_faq_dataset.pdf      # NovaSpark FAQ document
├── earth_geography_climate.json    # Earth sciences data
├── rag_dataset.json          # Company and product information
├── rag_dataset_product_launches.json  # Product launch data
├── solar_system.json         # Solar system data
├── nove_index.faiss          # Generated FAISS index
└── nove_index.pkl            # Generated document store
```

## 🛠️ Development

### Testing

Run the test script to verify everything works:

```bash
python rag_chatbot.py
```

### Performance Optimization

- The vector index is automatically saved after first run
- Subsequent runs load the pre-built index for faster startup
- FAISS provides efficient similarity search even with large document sets

### Troubleshooting

**Common Issues:**

1. **OpenAI API Key Error**: Make sure your `.env` file contains a valid API key
2. **Document Processing Errors**: Check that all document paths are correct
3. **Memory Issues**: For very large document sets, consider reducing chunk size
4. **Slow Performance**: The first run will be slow as it builds the index; subsequent runs are much faster

## 📄 License

This project is for educational and demonstration purposes.

## 🤝 Contributing

Feel free to enhance Nove with:
- Additional document types support
- Better chunking strategies
- Advanced retrieval techniques
- UI/UX improvements

## 🚀 Future Enhancements

- Support for more document formats (Word, Excel, etc.)
- Multi-language support
- Conversation memory
- Advanced filtering options
- API endpoints for integration
