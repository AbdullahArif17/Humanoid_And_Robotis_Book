import os
import re

def parse_markdown_with_rag(file_path: str):
    """
    Parses a markdown file, splitting it into chunks based on headings and extracting
    RAG metadata embedded as HTML comments.

    Args:
        file_path (str): The path to the markdown file.

    Returns:
        list: A list of dictionaries, where each dictionary represents a chunk
              and contains 'content', 'metadata', and 'chunk_id'.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    chunks = []
    current_chunk_content = []
    current_metadata = {}
    current_chunk_id = None

    # Regex to find headings and RAG metadata comments
    # Matches:
    # 1. HTML comments like <!-- rag_chunk_id: ... -->
    # 2. Markdown headings like ## My Heading
    lines = content.split('\n')
    for line in lines:
        rag_match = re.match(r'<!--\s*rag_chunk_id:\s*([^ ]+)\s*-->', line)
        if rag_match:
            # If we encounter a new RAG metadata block, save the previous chunk
            if current_chunk_content and current_chunk_id:
                chunks.append({
                    'chunk_id': current_chunk_id,
                    'content': "\n".join(current_chunk_content).strip(),
                    'metadata': current_metadata.copy()
                })
            
            # Reset for new chunk
            current_chunk_content = []
            current_metadata = {}
            current_chunk_id = rag_match.group(1).strip()
            
            # Extract other metadata from the same comment block
            title_match = re.search(r'rag_chunk_title:\s*([^ ]+)', line)
            if title_match:
                current_metadata['title'] = title_match.group(1).strip()
            
            keywords_match = re.search(r'rag_keywords:\s*\[([^\]]+)\]', line)
            if keywords_match:
                current_metadata['keywords'] = [k.strip() for k in keywords_match.group(1).split(',')]
            
            # Add file_path to metadata
            current_metadata['file_path'] = file_path
            current_metadata['module'] = os.path.basename(os.path.dirname(file_path)) # Extract module name

        elif re.match(r'^#+\s', line) and current_chunk_content and current_chunk_id:
            # If we encounter a new heading and already have content for a chunk, save it
            chunks.append({
                'chunk_id': current_chunk_id,
                'content': "\n".join(current_chunk_content).strip(),
                'metadata': current_metadata.copy()
            })
            # Reset for new chunk (but keep previous metadata for now, might be refined later)
            current_chunk_content = []
            current_chunk_id = None # Reset chunk_id for auto-generated ones
            # For simplicity, we'll just continue with a new chunk,
            # in a real system, you might generate a new chunk_id based on heading

        current_chunk_content.append(line)

    # Add the last chunk if any content remains
    if current_chunk_content and current_chunk_id:
        chunks.append({
            'chunk_id': current_chunk_id,
            'content': "\n".join(current_chunk_content).strip(),
            'metadata': current_metadata.copy()
        })
    elif current_chunk_content and not current_chunk_id:
        # Handle case where there's content but no explicit RAG chunk ID for the first chunk
        # or chunks between explicit RAG IDs.
        # For now, we'll create a default ID for these.
        chunks.append({
            'chunk_id': f"auto_chunk_{len(chunks)}",
            'content': "\n".join(current_chunk_content).strip(),
            'metadata': current_metadata.copy()
        })


    return chunks

# Example usage (for testing)
if __name__ == '__main__':
    # Create a dummy markdown file for testing
    dummy_content = """
<!-- rag_chunk_id: intro_chunk -->
# Introduction

This is the introduction.

<!--
rag_chunk_id: section1_chunk
rag_chunk_title: Section One
rag_keywords: [key1, key2]
-->
## Section 1: First Part

Some content for the first section.

### Sub-section A

More content here.

<!-- rag_chunk_id: section2_chunk -->
## Section 2: Second Part

More content for the second section.
"""
    with open('dummy.md', 'w', encoding='utf-8') as f:
        f.write(dummy_content)

    parsed_chunks = parse_markdown_with_rag('dummy.md')
    for i, chunk in enumerate(parsed_chunks):
        print(f"--- Chunk {i+1} ---")
        print(f"Chunk ID: {chunk.get('chunk_id', 'N/A')}")
        print(f"Metadata: {chunk.get('metadata', {})}")
        print(f"Content (first 100 chars): {chunk['content'][:100]}...")
        print("-" * 20)

    os.remove('dummy.md')
