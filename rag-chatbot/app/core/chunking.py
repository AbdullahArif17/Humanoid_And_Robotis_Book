import re
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class TextChunk:
    """Represents a chunk of text with metadata."""
    id: str
    content: str
    title: str
    source_file: str
    chunk_index: int
    metadata: Dict[str, Any] = None

class MarkdownChunker:
    """
    A class to chunk markdown content for RAG systems.
    """

    def __init__(self, max_chunk_size: int = 1000, overlap: int = 100):
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap

    def chunk_file(self, file_path: str, source_file: str) -> List[TextChunk]:
        """
        Chunk a markdown file into smaller pieces suitable for RAG.

        Args:
            file_path: Path to the markdown file
            source_file: Name of the source file for metadata

        Returns:
            List of TextChunk objects
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return self.chunk_content(content, source_file)

    def chunk_content(self, content: str, source_file: str) -> List[TextChunk]:
        """
        Chunk markdown content into smaller pieces.

        Args:
            content: Raw markdown content
            source_file: Name of the source file for metadata

        Returns:
            List of TextChunk objects
        """
        # Split content by headers to maintain context
        sections = self._split_by_headers(content)
        chunks = []

        for i, section in enumerate(sections):
            section_chunks = self._chunk_section(section, source_file, i)
            chunks.extend(section_chunks)

        return chunks

    def _split_by_headers(self, content: str) -> List[str]:
        """
        Split content by markdown headers to maintain context.
        """
        # Split by H1, H2, H3, H4 headers
        header_pattern = r'(\n|^)(#{1,4})\s+(.+?)\n'
        parts = re.split(header_pattern, content)

        sections = []
        current_section = ""

        # Reconstruct sections with headers
        for i in range(len(parts)):
            if i % 4 == 0:  # Content part
                current_section += parts[i]
            elif i % 4 == 1:  # Newline before header
                if current_section.strip():
                    sections.append(current_section.strip())
                current_section = parts[i] + parts[i+1] + " " + parts[i+2] + "\n"  # Header
            # Skip the header parts (i % 4 == 2, 3)

        if current_section.strip():
            sections.append(current_section.strip())

        return sections

    def _chunk_section(self, section: str, source_file: str, section_index: int) -> List[TextChunk]:
        """
        Chunk a single section into smaller pieces if needed.
        """
        if len(section) <= self.max_chunk_size:
            # Create a chunk with the section title
            title = self._extract_title(section)
            chunk_id = f"{source_file}_section_{section_index}_chunk_0"
            return [TextChunk(
                id=chunk_id,
                content=section,
                title=title,
                source_file=source_file,
                chunk_index=0
            )]

        # If section is too long, split into smaller chunks
        chunks = []
        section_lines = section.split('\n')
        title = self._extract_title(section)

        current_chunk = ""
        chunk_index = 0

        for line in section_lines:
            if len(current_chunk + line) > self.max_chunk_size:
                # Save current chunk
                if current_chunk.strip():
                    chunk_id = f"{source_file}_section_{section_index}_chunk_{chunk_index}"
                    chunks.append(TextChunk(
                        id=chunk_id,
                        content=current_chunk.strip(),
                        title=title,
                        source_file=source_file,
                        chunk_index=chunk_index
                    ))
                    chunk_index += 1

                # Start new chunk with overlap
                # Keep some overlap by including the last few lines of the previous chunk
                if len(line) > self.max_chunk_size:
                    # If the line itself is too long, split it
                    line_chunks = self._split_long_line(line)
                    for lc in line_chunks[:-1]:
                        chunk_id = f"{source_file}_section_{section_index}_chunk_{chunk_index}"
                        chunks.append(TextChunk(
                            id=chunk_id,
                            content=lc,
                            title=title,
                            source_file=source_file,
                            chunk_index=chunk_index
                        ))
                        chunk_index += 1
                    current_chunk = line_chunks[-1]
                else:
                    current_chunk = line + "\n"
            else:
                current_chunk += line + "\n"

        # Add the last chunk
        if current_chunk.strip():
            chunk_id = f"{source_file}_section_{section_index}_chunk_{chunk_index}"
            chunks.append(TextChunk(
                id=chunk_id,
                content=current_chunk.strip(),
                title=title,
                source_file=source_file,
                chunk_index=chunk_index
            ))

        return chunks

    def _extract_title(self, content: str) -> str:
        """
        Extract the title from the beginning of content (first H1 or H2).
        """
        lines = content.split('\n')
        for line in lines[:5]:  # Check first 5 lines
            h1_match = re.match(r'^#\s+(.+)', line)
            if h1_match:
                return h1_match.group(1).strip()

            h2_match = re.match(r'^##\s+(.+)', line)
            if h2_match:
                return h2_match.group(1).strip()

        # If no header found, use first 50 chars as title
        return content[:50].strip() + "..." if len(content) > 50 else content.strip()

    def _split_long_line(self, line: str) -> List[str]:
        """
        Split a line that is too long into smaller chunks.
        """
        chunks = []
        while len(line) > self.max_chunk_size:
            # Find a good breaking point (space)
            break_point = self.max_chunk_size
            for i in range(self.max_chunk_size, self.max_chunk_size - 100, -1):
                if i < len(line) and line[i] == ' ':
                    break_point = i
                    break

            chunks.append(line[:break_point])
            line = line[break_point:].lstrip()

        if line:
            chunks.append(line)

        return chunks


def chunk_markdown_files(file_paths: List[str]) -> List[TextChunk]:
    """
    Chunk multiple markdown files into TextChunk objects.

    Args:
        file_paths: List of paths to markdown files

    Returns:
        List of TextChunk objects
    """
    chunker = MarkdownChunker()
    all_chunks = []

    for file_path in file_paths:
        chunks = chunker.chunk_file(file_path, file_path)
        all_chunks.extend(chunks)

    return all_chunks