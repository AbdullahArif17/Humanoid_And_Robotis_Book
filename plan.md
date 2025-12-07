# Project Plan: Physical AI & Humanoid Robotics

## Project Goals

The primary goal of this project is to create a comprehensive, technical book on "Physical AI & Humanoid Robotics" using a Spec-Driven Development (SDD) approach with Docusaurus, deployable to GitHub Pages. Concurrently, an integrated RAG (Retrieval-Augmented Generation) chatbot will be embedded within the book to provide interactive Q&A capabilities, leveraging OpenAI agents, Qdrant Cloud, FastAPI, and Neon Serverless Postgres.

## Deliverables

1.  **Technical Book**:
    *   Authored with Docusaurus.
    *   Content covering ROS 2, Gazebo/Unity, NVIDIA Isaac, and Vision-Language-Action (VLA).
    *   Deployed to GitHub Pages.
    *   Structured with Spec-Kit Plus and Claude Code workflows.
    *   All content will be high quality, technically rigorous, beginner-friendly, and RAG-ready.

2.  **Integrated RAG Chatbot**:
    *   Embedded within the deployed Docusaurus book.
    *   Powered by OpenAI Agents/ChatKit SDKs.
    *   Vector search facilitated by Qdrant Cloud (Free Tier).
    *   Backend developed with FastAPI.
    *   State managed by Neon Serverless Postgres.
    *   Capable of answering questions about the entire book and user-selected text segments.

3.  **Planning & Specification Files**:
    *   `plan.md`: Overall project plan.
    *   `clarify.md`: List of clarifying questions.
    *   `specify.md` for each module: Detailed specifications for ROS 2, Gazebo & Unity, NVIDIA Isaac, and VLA.
    *   Book Folder Structure Outline: Docusaurus directory layout, navigation sidebar.

4.  **Bonus Deliverables (Optional, for extra points)**:
    *   Claude Code Subagents for specific tasks (e.g., writing, coding, debugging, RAG feeding).
    *   Agent Skills for reusable intelligence.

## Timeline & Milestones (Conceptual, without dates)

### Phase 1: Planning & Specification (Current Phase)
*   **Milestone**: All planning and specification files generated.
    *   Generate `plan.md`.
    *   Generate `clarify.md`.
    *   Generate `specify.md` for Module 1: ROS 2.
    *   Generate `specify.md` for Module 2: Gazebo & Unity.
    *   Generate `specify.md` for Module 3: NVIDIA Isaac.
    *   Generate `specify.md` for Module 4: VLA.
    *   Generate Book Folder Structure Outline.

### Phase 2: Book Infrastructure Setup
*   **Milestone**: Docusaurus book framework initialized and basic structure in place.
    *   Initialize Docusaurus project.
    *   Configure Docusaurus for documentation and blog posts.
    *   Implement initial book folder structure.
    *   Set up GitHub Pages deployment workflow (CI/CD).

### Phase 3: Book Content Authoring
*   **Milestone**: Core book content for all modules drafted and integrated.
    *   Author content for Module 1: ROS 2.
    *   Author content for Module 2: Gazebo & Unity.
    *   Author content for Module 3: NVIDIA Isaac.
    *   Author content for Module 4: VLA.
    *   Integrate hardware requirements documentation.
    *   Ensure all content is RAG-ready (chunkable sections).

### Phase 4: RAG Chatbot Development & Integration
*   **Milestone**: Chatbot backend and frontend implemented, integrated, and functional.
    *   Set up Qdrant Cloud instance and API.
    *   Develop FastAPI backend for RAG logic.
    *   Integrate Neon Serverless Postgres for state management.
    *   Implement OpenAI Agents/ChatKit SDKs for chatbot logic.
    *   Develop Docusaurus plugin/component for chatbot UI.
    *   Integrate chatbot into the deployed book.
    *   Implement "question about entire book" functionality.
    *   Implement "question about user-selected text" functionality.

### Phase 5: Testing, Refinement & Bonus Features
*   **Milestone**: Project thoroughly tested, refined, and bonus features implemented.
    *   Execute comprehensive testing plan.
    *   Address feedback and refine book content and chatbot functionality.
    *   Implement Claude Code Subagents (bonus).
    *   Implement Agent Skills (bonus).
    *   Final deployment and presentation.

## Tasks for Book Building

*   **Setup Docusaurus**: Initialize project, configure theme, navigation, and plugins.
*   **Content Authoring**: Write detailed, technical, and beginner-friendly content for each module.
*   **Markdown Formatting**: Ensure consistent use of headings, lists, code blocks, and RAG-ready chunking.
*   **Diagrams**: Create ASCII diagrams or placeholder for visual aids as per module specifications.
*   **Code Samples**: Embed relevant code samples within modules.
*   **Cross-referencing**: Link related sections and external references.
*   **Review & Edit**: Proofread for technical accuracy, clarity, and grammar.

## Tasks for RAG Chatbot Integration

*   **Qdrant Setup**: Provision Qdrant Cloud instance, create collections.
*   **Data Ingestion Pipeline**: Develop scripts to extract, chunk, embed book content, and upload to Qdrant.
*   **FastAPI Backend**:
    *   Design API endpoints for chat interaction, context retrieval.
    *   Implement RAG logic (retrieve relevant chunks from Qdrant, augment prompt).
    *   Integrate with OpenAI Agents/ChatKit SDKs.
    *   Connect to Neon Serverless Postgres for chat history/state.
*   **Docusaurus Frontend Integration**:
    *   Develop React component for chatbot UI.
    *   Integrate chatbot component into Docusaurus pages.
    *   Implement text selection event listeners for context-aware Q&A.
*   **Deployment**: Deploy FastAPI backend and ensure secure communication with Docusaurus frontend.

## Tasks for Deployment to GitHub Pages

*   **Docusaurus Build**: Configure Docusaurus build process.
*   **GitHub Repository**: Create a new GitHub repository for the project.
*   **GitHub Pages Setup**: Configure GitHub Pages branch and settings.
*   **CI/CD Workflow**: Set up GitHub Actions for automated build and deployment to GitHub Pages on pushes to `main`.

## Tasks for Creating Subagents & Skills (Bonus)

*   **Identify Opportunities**: Analyze common tasks in writing, coding, debugging, RAG feeding that could be automated.
*   **Subagent Design**: Define purpose, inputs, outputs, and tools for each subagent.
*   **Agent Skill Development**: Create new skills for Claude Code, defining their functionality and integration points.
*   **Testing**: Validate subagent and skill functionality with test cases.

## Testing Plan

*   **Book Content Testing**:
    *   **Accuracy**: Verify technical correctness of all information.
    *   **Clarity**: Assess readability and beginner-friendliness.
    *   **RAG Readiness**: Ensure content is properly structured for chunking and retrieval by the chatbot.
    *   **Broken Links**: Check all internal and external links.
    *   **Code Sample Verification**: Ensure all code samples are runnable and produce expected output.
*   **Chatbot Functionality Testing**:
    *   **End-to-end Chat Flow**: Test conversational turns, response quality.
    *   **Full Book Q&A**: Test chatbot's ability to answer questions across the entire book.
    *   **Contextual Q&A**: Test chatbot's ability to answer questions based on user-selected text.
    *   **Performance**: Measure response latency and throughput.
    *   **Reliability**: Test under various loads and edge cases.
    *   **Security**: Basic vulnerability scanning for FastAPI backend.
*   **Deployment Testing**:
    *   Verify successful deployment to GitHub Pages.
    *   Test accessibility and functionality of the deployed book and chatbot.
    *   Ensure CI/CD pipeline functions correctly.

## Evaluation Criteria

*   **Book Quality (40%)**: Technical accuracy, clarity, completeness, adherence to Docusaurus best practices, RAG readiness.
*   **Chatbot Functionality (40%)**: Accuracy of responses, contextual understanding, robustness, integration seamlessness, use of specified tools (OpenAI Agents/ChatKit, Qdrant, FastAPI, Neon).
*   **Spec-Driven Development Adherence (10%)**: Proper use of Spec-Kit Plus, Claude Code workflows, PHR/ADR generation.
*   **Deployment & Usability (10%)**: Successful GitHub Pages deployment, book navigability, chatbot user experience.
*   **Bonus Features (up to 50 points)**: Implementation and utility of Claude Code Subagents and Agent Skills.

## Hardware Notes

*   **Digital Twin Workstation**:
    *   **GPU**: NVIDIA RTX series (e.g., RTX 3080/4080 or better) for Gazebo, Unity, and NVIDIA Isaac simulation.
    *   **OS**: Ubuntu 22.04 LTS.
    *   **RAM**: 32GB+ recommended for large simulations.
    *   **CPU**: Multi-core Intel i7/i9 or AMD Ryzen 7/9.
*   **Jetson Orin Edge Kit**: Required for deploying and testing AI models at the edge.
*   **RealSense D435i**: Depth camera for perception tasks.
*   **IMUs, microphones, etc.**: Various sensors for robot interaction and data collection.
*   **Robot options**: Unitree Go2, Unitree G1, Hiwonder humanoid, Robotis OP3 (at least one for practical application/demonstration).

## Cloud vs Local Development Modes

*   **Local Development**:
    *   **Book**: Docusaurus can be developed and served locally.
    *   **FastAPI Backend**: Local development and testing are feasible.
    *   **RAG**: Qdrant (local instance or Docker), Neon (local Postgres or mock DB).
    *   **Simulations**: Gazebo, Unity, NVIDIA Isaac (requires powerful local workstation).
    *   **Edge AI**: Jetson Orin requires local physical access.
*   **Cloud Development**:
    *   **Book Deployment**: GitHub Pages (cloud-hosted).
    *   **Qdrant**: Qdrant Cloud (primary).
    *   **Neon Postgres**: Neon Serverless Postgres (primary).
    *   **FastAPI Backend**: Can be deployed to cloud platforms (e.g., Render, Vercel, AWS Lambda, Google Cloud Run) for easy integration with the deployed book.
    *   **Simulation**: Cloud-based simulation environments (e.g., AWS RoboMaker, NVIDIA Omniverse Cloud) could be explored for larger-scale or collaborative work, but local workstation is sufficient for hackathon.
    *   **Code Editor**: Cloud-based IDEs (e.g., GitHub Codespaces) can provide a consistent development environment.

**Decision**: A hybrid approach is recommended. Local for Docusaurus content authoring and initial chatbot development/testing, with cloud services for Qdrant, Neon, and the deployed FastAPI backend. GitHub Pages for book hosting.
