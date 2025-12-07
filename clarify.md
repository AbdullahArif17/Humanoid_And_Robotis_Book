# Clarifying Questions for Project Owner

To ensure the "Physical AI & Humanoid Robotics" project aligns perfectly with requirements and to make informed architectural decisions, please provide clarification on the following points:

## Book Structure & Content

1.  **Book Audience & Tone**: What is the primary target audience (e.g., beginners, intermediate developers, researchers)? This will influence the depth of technical detail and overall tone.
2.  **Chapter/Section Granularity**: For each module (ROS 2, Gazebo/Unity, NVIDIA Isaac, VLA), what level of chapter/section granularity is expected? Should it be a single long page per module, or broken down into multiple sub-sections?
3.  **Diagram Tooling**: Are there any preferred tools or formats for diagrams beyond ASCII (e.g., Mermaid.js, SVG, PNG)?
4.  **Code Sample Language Versions**: For code samples (e.g., Python for ROS 2, C# for Unity), are there specific language versions or frameworks to adhere to?
5.  **RAG-Ready Chunking Strategy**: Beyond general RAG-readiness, are there specific guidelines for how content should be chunked (e.g., by heading level, paragraph count, token limit)?

## RAG Chatbot Architecture & Data

6.  **Chatbot Integration Point**: Will the chatbot be a persistent element on all pages, or will it be accessible via a specific route/button?
7.  **API Security for FastAPI Backend**: What authentication and authorization mechanisms are required for the FastAPI backend (e.g., API keys, OAuth2)?
8.  **Data Chunking Unit**: For the RAG system, should the data be chunked by Docusaurus page, by heading, by paragraph, or by another metric? What is the preferred chunk size/overlap?
9.  **Vector Embedding Model**: What embedding model should be used for Qdrant? (e.g., OpenAI `text-embedding-ada-002`, `text-embedding-3-small`, or other open-source models).
10. **Chat History Persistence**: What is the desired retention policy for chat history in Neon Serverless Postgres (e.g., clear after session, retain for N days)?
11. **Chatbot Prompt Engineering**: Are there specific persona or instruction guidelines for the OpenAI Agents/ChatKit SDKs?
12. **Streaming Responses**: Is streaming (token-by-token output) desired for chatbot responses for a better user experience?

## Deployment & Environment Variables

13. **GitHub Pages Custom Domain**: Will the book be deployed to a custom domain, or the default `username.github.io/repo-name`?
14. **CI/CD Triggers**: Beyond pushes to `main`, are there other events that should trigger the GitHub Pages deployment (e.g., pull request merges)?
15. **Environment Variable Management**: How should sensitive credentials (e.g., OpenAI API key, Qdrant API key, Neon connection string) be managed in the deployment environment (e.g., GitHub Secrets, `.env` files)?

## Claude Code Subagents & Skills (Bonus)

16. **Prioritization of Subagents/Skills**: If we pursue bonus points, are there specific areas (writing, coding, debugging, RAG feeding) that would be most impactful for custom subagents/skills?
17. **Tool Access for Subagents**: What specific tools (e.g., file system access, web search, bash) should custom subagents have access to?

## General

18. **Definition of "Beginner-Friendly"**: What level of prior knowledge can be assumed for a "beginner-friendly" explanation in the context of advanced robotics and AI concepts?
