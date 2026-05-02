import json
import PyPDF2
from typing import List, Dict, Any
import re

class DocumentProcessor:
    """Process and chunk documents for RAG system"""
    
    def __init__(self):
        self.chunk_size = 1000
        self.chunk_overlap = 200
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            print(f"Error reading PDF {pdf_path}: {e}")
            return ""
    
    def process_json_file(self, json_path: str) -> List[Dict[str, Any]]:
        """Process JSON file and extract content"""
        try:
            with open(json_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
            documents = []
            
            # Handle improved Q&A format
            if isinstance(data, list) and len(data) > 0 and 'question' in data[0]:
                # New Q&A format
                for item in data:
                    if isinstance(item, dict) and 'question' in item and 'answer' in item:
                        # Combine question and answer for better context
                        content = f"Question: {item['question']}\nAnswer: {item['answer']}"
                        documents.append({
                            'id': item.get('id', f'doc_{len(documents)}'),
                            'content': content,
                            'metadata': {
                                'source': json_path,
                                'type': 'qa',
                                'category': item.get('category', 'general'),
                                'keywords': item.get('keywords', [])
                            }
                        })
            
            # Handle original array format (like earth_geography_climate.json, solar_system.json)
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    if isinstance(item, dict):
                        content = self._extract_content_from_dict(item)
                        if content:
                            documents.append({
                                'id': item.get('id', f'doc_{i}'),
                                'content': content,
                                'metadata': {'source': json_path, 'type': 'json'}
                            })
            
            # Handle object format (like rag_dataset.json)
            elif isinstance(data, dict):
                if 'documents' in data:
                    for doc in data['documents']:
                        documents.append({
                            'id': doc['id'],
                            'content': doc['content'],
                            'metadata': {
                                'source': json_path,
                                'type': doc.get('type', 'unknown'),
                                'category': doc.get('metadata', {}).get('category', 'general')
                            }
                        })
                
                # Handle company section if exists
                if 'company' in data:
                    company = data['company']
                    documents.append({
                        'id': company['id'],
                        'content': company['content'],
                        'metadata': {
                            'source': json_path,
                            'type': company.get('type', 'company'),
                            'category': 'company'
                        }
                    })
            
            return documents
            
        except Exception as e:
            print(f"Error processing JSON {json_path}: {e}")
            return []
    
    def _extract_content_from_dict(self, item: Dict) -> str:
        """Extract meaningful content from a dictionary item"""
        content_parts = []
        
        # Add title if exists
        if 'title' in item:
            content_parts.append(f"Title: {item['title']}")
        
        # Add main content
        if 'content' in item:
            content_parts.append(item['content'])
        
        # Add description if exists
        elif 'description' in item:
            content_parts.append(item['description'])
        
        # Add notable features for solar system data
        if 'notable_features' in item:
            content_parts.append(f"Notable Features: {item['notable_features']}")
        
        # For solar system objects, add key properties
        if 'physical_properties' in item:
            props = item['physical_properties']
            content_parts.append(f"Mass: {props.get('mass_kg', 'N/A')} kg")
            content_parts.append(f"Diameter: {props.get('diameter_km', 'N/A')} km")
            content_parts.append(f"Gravity: {props.get('gravity_m_s2', 'N/A')} m/s²")
        
        if 'orbital_data' in item:
            orbital = item['orbital_data']
            if 'distance_from_sun_au' in orbital:
                content_parts.append(f"Distance from Sun: {orbital['distance_from_sun_au']} AU")
            if 'orbital_period_years' in orbital:
                content_parts.append(f"Orbital Period: {orbital['orbital_period_years']} years")
        
        if 'atmosphere' in item:
            atm = item['atmosphere']
            if 'composition' in atm:
                content_parts.append(f"Atmosphere Composition: {atm['composition']}")
            if 'notable_features' in atm:
                content_parts.append(f"Atmospheric Features: {atm['notable_features']}")
        
        return "\n".join(content_parts)
    
    def chunk_text(self, text: str, doc_id: str, metadata: Dict) -> List[Dict[str, Any]]:
        """Split text into chunks"""
        chunks = []
        
        # Simple sentence-based chunking
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        current_chunk = ""
        chunk_index = 0
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= self.chunk_size:
                current_chunk += sentence + " "
            else:
                if current_chunk.strip():
                    chunks.append({
                        'id': f"{doc_id}_chunk_{chunk_index}",
                        'content': current_chunk.strip(),
                        'metadata': {**metadata, 'chunk_index': chunk_index}
                    })
                    chunk_index += 1
                
                current_chunk = sentence + " "
        
        # Add the last chunk
        if current_chunk.strip():
            chunks.append({
                'id': f"{doc_id}_chunk_{chunk_index}",
                'content': current_chunk.strip(),
                'metadata': {**metadata, 'chunk_index': chunk_index}
            })
        
        return chunks
    
    def process_all_documents(self, file_paths: List[str]) -> List[Dict[str, Any]]:
        """Process all document files"""
        all_chunks = []
        
        for file_path in file_paths:
            print(f"Processing: {file_path}")
            
            if file_path.endswith('.pdf'):
                text = self.extract_text_from_pdf(file_path)
                if text:
                    chunks = self.chunk_text(
                        text, 
                        f"pdf_{len(all_chunks)}", 
                        {'source': file_path, 'type': 'pdf'}
                    )
                    all_chunks.extend(chunks)
            
            elif file_path.endswith('.json'):
                documents = self.process_json_file(file_path)
                for doc in documents:
                    chunks = self.chunk_text(
                        doc['content'], 
                        doc['id'], 
                        doc['metadata']
                    )
                    all_chunks.extend(chunks)
        
        print(f"Total chunks created: {len(all_chunks)}")
        return all_chunks
