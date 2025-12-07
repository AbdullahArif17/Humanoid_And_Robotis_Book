import re
from typing import List, Dict, Optional
from pathlib import Path
import markdown
from bs4 import BeautifulSoup


class MarkdownChunker:
    """Parse and chunk markdown content for RAG."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def extract_rag_metadata(self, content: str) -> Dict[str, any]:
        """
        Extract RAG metadata from HTML comments in markdown.
        
        Example:
        <!--
        rag_chunk_id: module1_overview
        rag_chunk_title: Module 1 Overview
        rag_keywords: [ROS 2, introduction]
        -->
        """
        metadata = {}
        
        # Find HTML comment blocks
        comment_pattern = r'<!--\s*(.*?)\s*-->'
        comments = re.findall(comment_pattern, content, re.DOTALL)
        
        for comment in comments:
            # Parse key-value pairs
            if 'rag_chunk_id' in comment:
                lines = comment.strip().split('\n')
                for line in lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # Parse keywords as list
                        if key == 'rag_keywords' and value.startswith('['):
                            value = [k.strip() for k in value.strip('[]').split(',')]
                        
                        metadata[key] = value
        
        return metadata
    
    def chunk_by_headers(self, content: str, file_path: str) -> List[Dict[str, any]]:
        """
        Chunk markdown content by headers while preserving context.
        
        Args:
            content: Markdown content
            file_path: Path to the source file
            
        Returns:
            List of chunks with metadata
        """
        chunks = []
        
        # Split by major headers (## or ###)
        sections = re.split(r'\n(#{2,3}\s+.*?)\n', content)
        
        current_chunk = ""
        current_metadata = {}
        chunk_id = 0
        
        for i, section in enumerate(sections):
            # Check if this is a header
            if section.startswith('##'):
                # Save previous chunk if it exists
                if current_chunk.strip():
                    chunks.append({
                        'content': current_chunk.strip(),
                        'metadata': {
                            **current_metadata,
                            'source_file': file_path,
                            'chunk_id': chunk_id
                        }
                    })
                    chunk_id += 1
                
                # Start new chunk with header
                current_chunk = section + "\n"
                current_metadata = {}
            else:
                # Extract metadata if present
                metadata = self.extract_rag_metadata(section)
                if metadata:
                    current_metadata.update(metadata)
                
                # Add content to current chunk
                current_chunk += section
                
                # If chunk is too large, split it
                if len(current_chunk) > self.chunk_size:
                    # Find a good split point (paragraph break)
                    split_chunks = self._split_large_chunk(current_chunk)
                    
                    for split_chunk in split_chunks[:-1]:
                        chunks.append({
                            'content': split_chunk.strip(),
                            'metadata': {
                                **current_metadata,
                                'source_file': file_path,
                                'chunk_id': chunk_id
                            }
                        })
                        chunk_id += 1
                    
                    # Keep the last part for the next iteration
                    current_chunk = split_chunks[-1]
        
        # Add the last chunk
        if current_chunk.strip():
            chunks.append({
                'content': current_chunk.strip(),
                'metadata': {
                    **current_metadata,
                    'source_file': file_path,
                    'chunk_id': chunk_id
                }
            })
        
        return chunks
    
    def _split_large_chunk(self, text: str) -> List[str]:
        """Split a large chunk into smaller pieces at paragraph boundaries."""
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            if len(current_chunk) + len(para) > self.chunk_size and current_chunk:
                chunks.append(current_chunk)
                current_chunk = para
            else:
                current_chunk += "\n\n" + para if current_chunk else para
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks if chunks else [text]
    
    def clean_markdown(self, content: str) -> str:
        """Remove HTML comments and convert markdown to plain text."""
        # Remove HTML comments
        content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
        
        # Convert markdown to HTML then to text for cleaner output
        html = markdown.markdown(content)
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text(separator='\n')
        
        # Clean up extra whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()


# Global instance
chunker = MarkdownChunker()
