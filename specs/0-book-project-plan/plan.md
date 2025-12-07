# Implementation Plan: Hackathon Book Project

**Branch**: `0-book-project-plan` | **Date**: 2025-12-05 | **Spec**: [Link to the overall project spec, which isn't explicitly created yet, but would be `specs/0-book-project-plan/spec.md`]
**Input**: Comprehensive project requirements for "Physical AI & Humanoid Robotics" book and integrated RAG chatbot.

## Summary

This plan outlines the development of a comprehensive technical book on Physical AI & Humanoid Robotics using Docusaurus, deployed to GitHub Pages, with content generated and structured via Claude Code and Spec-Kit Plus. It also details the integration of a RAG chatbot for interactive learning, leveraging OpenAI Agents/ChatKit SDKs, FastAPI, Neon Serverless Postgres, and Qdrant Cloud Free Tier. An optional bonus includes creating reusable intelligence through Claude Code Subagents and Agent Skills.

## Technical Context

**Language/Version**: Python 3.9+, JavaScript (Node.js for Docusaurus), C++ (for ROS 2 components if low-level control is needed)
**Primary Dependencies**: Docusaurus, ROS 2, Gazebo/Ignition, NVIDIA Isaac Sim, Unity 3D, OpenAI Whisper, FastAPI, Neon Serverless Postgres, Qdrant Cloud Free Tier, OpenAI Agents/ChatKit SDKs.
**Storage**: Git (for Docusaurus content), Neon Serverless Postgres (for chatbot metadata/state), Qdrant Cloud Free Tier (for vector embeddings).
**Testing**: Unit tests for RAG chatbot components (FastAPI endpoints, embedding generation), Docusaurus build validation, end-to-end testing for RAG chatbot interaction and content retrieval.
**Target Platform**: GitHub Pages (for Docusaurus), Cloud (for FastAPI/Neon/Qdrant).
**Project Type**: Multi-faceted: Documentation (Docusaurus), Backend API (FastAPI), AI/Robotics Simulation (ROS 2, Gazebo, Isaac Sim, Unity).
**Performance Goals**: RAG chatbot response time < 2 seconds for most queries. Docusaurus site load time < 3 seconds. Real-time simulation for robotics modules.
**Constraints**: Book length 50-80 pages (20,000-40,000 words). Minimum 15 sources for academic rigor. Markdown/Docusaurus-compatible output. Flesch-Kincaid grade 10-12. Chatbot responses based *only* on selected text. Qdrant Cloud Free Tier limitations.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Comprehensive & Rigorous Content**: The plan ensures comprehensive coverage of Physical AI, humanoid robotics, simulation, ROS 2, NVIDIA Isaac, and VLA, aligning with the project's core objective.
- [x] **Course-Aligned Structure & Content**: The plan is structured into modules corresponding to weekly topics, emphasizing core Physical AI principles.
- [x] **Clarity & Accuracy**: The plan aims for clear, actionable, and reproducible steps, maintaining technical rigor and citing relevant resources.
- [x] **Deliverable Format & Length**: The plan targets the specified book length and Markdown/Docusaurus format, with deployment to GitHub Pages.
- [x] **Instructional Content**: The plan explicitly includes tasks for theoretical explanations, practical examples (code, diagrams), hardware guidance, a capstone project, FAQs, troubleshooting, and RAG-ready chunking.
- [x] **Optional Advanced Steps**: The plan incorporates considerations for optional Subagents and Agent Skills, aligning with the bonus objective.

## Project Structure

### Documentation (this feature)

```text
specs/0-book-project-plan/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (to be generated)
├── data-model.md        # Phase 1 output (to be generated, if applicable for RAG)
├── quickstart.md        # Phase 1 output (to be generated for Docusaurus/Chatbot)
├── contracts/           # Phase 1 output (API contracts for RAG chatbot)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Docusaurus Book Structure
book/
├── docs/                # Markdown files for book modules (Module 1-4, Capstone)
│   ├── module1.md
│   ├── module2.md
│   ├── module3.md
│   └── module4.md
├── src/                 # Docusaurus components, styles, etc.
├── static/              # Images, diagrams, static assets
├── docusaurus.config.js # Docusaurus configuration
└── sidebar.js           # Book navigation structure

# RAG Chatbot Backend
rag-chatbot/
├── app/                 # FastAPI application
│   ├── main.py          # FastAPI entry point
│   ├── api/             # API endpoints for chatbot interaction
│   ├── core/            # Core logic (embedding, retrieval)
│   └── db/              # Database interaction (Neon Postgres)
├── vectors/             # Qdrant client and vector operations
├── agents/              # OpenAI Agents/ChatKit SDK integration
├── requirements.txt     # Python dependencies
└── Dockerfile           # Dockerize FastAPI app

# Reusable Intelligence (Optional Bonus)
.claude/
├── subagents/           # Custom Claude Code Subagents
└── skills/              # Custom Agent Skills
```

**Structure Decision**: The project will adopt a hybrid structure: a `book/` directory for the Docusaurus-based technical book and a `rag-chatbot/` directory for the integrated RAG chatbot backend. This separation allows independent development and deployment while maintaining clear integration points. Optional Claude Code Subagents and Agent Skills will reside in `.claude/` for dynamic loading.

## Module-Based Task Breakdown

### Module 1: The Robotic Nervous System (ROS 2)

**Goal**: Introduce ROS 2 fundamentals, its architecture, and practical application in Physical AI and humanoid robotics.

**Tasks**:
- [x] T001 [US1] Write Module 1 overview and key concepts (ROS 2 Nodes, Topics, Services, URDF, rclpy) in `book/docs/module1.md`
- [x] T002 [US1] Explain connection to Physical AI and humanoid robotics in `book/docs/module1.md`
- [x] T003 [US1] Define learning objectives for Module 1 in `book/docs/module1.md`
- [x] T004 [US1] List software, hardware, and knowledge prerequisites for Module 1 in `book/docs/module1.md`
- [x] T005 [US2] Develop step-by-step lab: build basic ROS 2 packages with Python (rclpy) in `book/docs/module1.md`
- [x] T006 [US2] Provide runnable ROS 2 code snippets (publisher, subscriber, service) in `book/docs/module1.md`
- [x] T007 [US2] Detail simulation steps for ROS 2 nodes and services in `book/docs/module1.md`
- [x] T008 [US3] Create RAG-ready chunks for Module 1 content in `book/docs/module1.md`
- [x] T009 [US1] Suggest diagrams for ROS 2 communication flow in `book/docs/module1.md`
- [x] T010 [US1] Include FAQs and troubleshooting tips for ROS 2 in `book/docs/module1.md`
- [x] T011 [US1] Add references and resources for Module 1 in `book/docs/module1.md`

**Tools Used**: Claude Code (content generation), Spec-Kit Plus (structuring), ROS 2 (concepts, code), Python (rclpy examples).

### Module 2: The Digital Twin (Gazebo & Unity)

**Goal**: Explore physics simulation, environment building, and sensor simulation using Gazebo and Unity for humanoid robotics.

**Tasks**:
- [x] T012 [US1] Write Module 2 overview and key concepts (physics sim, environment building, Gazebo, Unity, sensor sim) in `book/docs/module2.md`
- [x] T013 [US1] Explain connection to Physical AI and humanoid robotics in `book/docs/module2.md`
- [x] T014 [US1] Define learning objectives for Module 2 in `book/docs/module2.md`
- [x] T015 [US1] List software, hardware, and knowledge prerequisites for Module 2 in `book/docs/module2.md`
- [x] T016 [US2] Develop step-by-step lab: setup Gazebo simulation environments in `book/docs/module2.md`
- [x] T017 [US2] Provide code/config examples for Gazebo worlds and robot models in `book/docs/module2.md`
- [x] T018 [US3] Develop step-by-step lab: Unity integration for high-fidelity rendering/human-robot interaction in `book/docs/module2.md`
- [x] T019 [US3] Develop step-by-step lab: sensor simulation (LiDAR, Depth Cameras, IMUs) in `book/docs/module2.md`
- [x] T020 [US3] Create RAG-ready chunks for Module 2 content in `book/docs/module2.md`
- [x] T021 [US1] Suggest diagrams for Gazebo/Unity integration architecture in `book/docs/module2.md`
- [x] T022 [US1] Include FAQs and troubleshooting tips for Gazebo/Unity in `book/docs/module2.md`
- [x] T023 [US1] Add references and resources for Module 2 in `book/docs/module2.md`

**Tools Used**: Claude Code, Spec-Kit Plus, Gazebo/Ignition (simulation), Unity (rendering, interaction).

### Module 3: The AI-Robot Brain (NVIDIA Isaac™)

**Goal**: Introduce NVIDIA Isaac ecosystem for advanced AI perception, navigation, and learning in robotics.

**Tasks**:
- [x] T024 [US1] Write Module 3 overview and key concepts (Isaac Sim, Isaac ROS, VSLAM, Nav2, RL) in `book/docs/module3.md`
- [x] T025 [US1] Explain connection to Physical AI and humanoid robotics in `book/docs/module3.md`
- [x] T026 [US1] Define learning objectives for Module 3 in `book/docs/module3.md`
- [x] T027 [US1] List software, hardware, and knowledge prerequisites for Module 3 in `book/docs/module3.md`
- [x] T028 [US2] Develop step-by-step lab: deploy Isaac Sim environments in `book/docs/module3.md`
- [x] T029 [US2] Develop step-by-step lab: integrate sensors and perform VSLAM in `book/docs/module3.md`
- [x] T030 [US3] Develop step-by-step lab: path planning with Nav2 in `book/docs/module3.md`
- [x] T031 [US3] Develop step-by-step lab: reinforcement learning examples in `book/docs/module3.md`
- [x] T032 [US3] Create RAG-ready chunks for Module 3 content in `book/docs/module3.md`
- [x] T033 [US1] Suggest diagrams for Isaac Sim/ROS architecture in `book/docs/module3.md`
- [x] T034 [US1] Include FAQs and troubleshooting tips for Isaac in `book/docs/module3.md`
- [x] T035 [US1] Add references and resources for Module 3 in `book/docs/module3.md`

**Tools Used**: Claude Code, Spec-Kit Plus, NVIDIA Isaac Sim, Isaac ROS, Nav2 (path planning).

### Module 4: Vision-Language-Action (VLA)

**Goal**: Integrate LLMs with robotics for voice-to-action, cognitive planning, and multi-modal interaction.

**Tasks**:
- [x] T036 [US1] Write Module 4 overview and key concepts (LLM integration, Voice-to-Action, cognitive planning, multi-modal interaction) in `book/docs/module4.md`
- [x] T037 [US1] Explain connection to Physical AI and humanoid robotics in `book/docs/module4.md`
- [x] T038 [US1] Define learning objectives for Module 4 in `book/docs/module4.md`
- [x] T039 [US1] List software, hardware, and knowledge prerequisites for Module 4 in `book/docs/module4.md`
- [x] T040 [US2] Develop step-by-step lab: integrate Whisper with ROS 2 for Voice-to-Action in `book/docs/module4.md`
- [x] T041 [US3] Develop step-by-step lab: cognitive planning examples (high-level commands to robot actions) in `book/docs/module4.md`
- [x] T042 [US3] Develop step-by-step lab: multi-modal perception and action integration in `book/docs/module4.md`
- [x] T043 [US3] Provide code snippets for ROS 2 action execution, object manipulation, LLM integration in `book/docs/module4.md`
- [x] T044 [US3] Create RAG-ready chunks for Module 4 content in `book/docs/module4.md`
- [x] T045 [US1] Suggest diagrams for VLA pipeline architecture in `book/docs/module4.md`
- [x] T046 [US1] Include FAQs and troubleshooting tips for VLA in `book/docs/module4.md`
- [x] T047 [US1] Add references and resources for Module 4 in `book/docs/module4.md`

**Tools Used**: Claude Code, Spec-Kit Plus, OpenAI Whisper (voice-to-action), GPT/LLM integration (cognitive planning), ROS 2 (action execution).

### Capstone Project: Autonomous Humanoid VLA

**Goal**: Integrate concepts from all modules to create an autonomous humanoid performing complex VLA tasks.

**Tasks**:
- [ ] T048 [CAP] Define capstone project objectives and scope in `book/docs/capstone.md`
- [ ] T049 [CAP] Outline system architecture for integrated VLA humanoid in `book/docs/capstone.md`
- [ ] T050 [CAP] Develop step-by-step guide for voice-to-action, navigation, manipulation tasks in `book/docs/capstone.md`
- [ ] T051 [CAP] Provide integration examples for ROS 2, Isaac Sim, VLA components in `book/docs/capstone.md`
- [ ] T052 [CAP] Suggest assessment criteria for capstone project in `book/docs/capstone.md`
- [ ] T053 [CAP] Create RAG-ready chunks for capstone project content in `book/docs/capstone.md`

## Timeline & Milestones

This timeline is indicative and can be adjusted based on team capacity and progress.

| Milestone                       | Modules/Tasks Involved                         | Suggested Duration |
|---------------------------------|------------------------------------------------|--------------------|
| **Phase 1: Book Setup & Module 1** | Docusaurus setup, Module 1 content generation | 1-2 Days           |
| **Phase 2: Modules 2 & 3**      | Module 2 & 3 content generation                 | 2-3 Days           |
| **Phase 3: Module 4 & Capstone**| Module 4 content, Capstone project outline    | 2-3 Days           |
| **Phase 4: RAG Chatbot Core**   | Qdrant, FastAPI, Neon setup, embedding         | 3-4 Days           |
| **Phase 5: RAG Chatbot Integration & Testing** | Chatbot UI, interaction, testing            | 2-3 Days           |
| **Phase 6: Deployment & Polish**| GitHub Pages deployment, final review, RAG tuning | 1-2 Days           |
| **Phase 7: Optional Bonus**     | Subagents/Skills development                    | 1-2 Days           |

## RAG Chatbot Integration Plan

### Steps to prepare retrievable text chunks

1.  **Define Chunking Strategy**:
    -   Chunk by Docusaurus markdown headings (e.g., H1, H2, H3) for semantic relevance.
    -   Ensure chunks are self-contained and provide sufficient context.
    -   Consider overlapping chunks to maintain context across boundaries.
2.  **Extraction and Preprocessing**:
    -   Develop a script (e.g., Python) to read Docusaurus markdown files (`book/docs/*.md`).
    -   Parse markdown to extract text content, preserving metadata (e.g., module, heading path).
    -   Clean text (remove markdown syntax, extra whitespace).
3.  **Embedding Generation**:
    -   Use a chosen embedding model (e.g., OpenAI `text-embedding-ada-002` or a local model) to generate vector embeddings for each text chunk.
    -   Store chunks and their embeddings.

### API setup for Qdrant + FastAPI + ChatKit integration

1.  **Qdrant Cloud Free Tier Setup**:
    -   Create a Qdrant Cloud account and set up a new collection for vector storage.
    -   Configure API key and endpoint.
2.  **FastAPI Backend (`rag-chatbot/app/`)**:
    -   Develop FastAPI endpoints for:
        -   Receiving user queries.
        -   Performing vector search in Qdrant (retrieval).
        -   Integrating with an LLM (e.g., OpenAI API) for response generation.
        -   Handling chat history and context with Neon Serverless Postgres.
    -   Implement `rag-chatbot/app/core/` for embedding logic, Qdrant client, and LLM orchestration.
    -   Implement `rag-chatbot/app/db/` for Neon Postgres client and chat history management.
3.  **Neon Serverless Postgres Setup**:
    -   Set up a Neon project and create a database for storing chatbot session data, user preferences, and potentially curated Q&A pairs.
    -   Configure connection string and integrate with FastAPI.
4.  **OpenAI Agents/ChatKit SDKs Integration**:
    -   Integrate ChatKit SDK within the Docusaurus frontend or as part of the FastAPI backend to manage chat UI and user interaction.
    -   If using OpenAI Agents, configure their interaction with the FastAPI backend for advanced conversational flows.

### Testing scenarios

1.  **Unit Tests**:
    -   Test individual FastAPI endpoints (`rag-chatbot/app/api/`).
    -   Test embedding generation and Qdrant interaction (`rag-chatbot/app/core/`, `rag-chatbot/vectors/`).
    -   Test Neon Postgres client functionality (`rag-chatbot/app/db/`).
2.  **Integration Tests**:
    -   End-to-end test: user query -> FastAPI -> Qdrant (retrieval) -> LLM (generation) -> response.
    -   Test chat history persistence and retrieval via Neon Postgres.
3.  **User Acceptance Testing (UAT)**:
    -   Verify chatbot accurately answers questions based *only* on book content.
    -   Test chatbot responses to questions about text selected by the user.
    -   Evaluate response relevance, coherence, and adherence to constraints.

## Reusable Intelligence (Bonus)

### Suggested Subagents and Agent Skills to implement

-   **"Book Sectioner" Subagent**: (Type: general-purpose, model: haiku)
    -   **Prompt**: "Given a Docusaurus markdown file, analyze its content and suggest optimal text chunks for RAG embedding, including unique identifiers and metadata (e.g., module, heading path)."
    -   **Purpose**: Automate the manual chunking process, ensuring consistency and RAG-readiness.
-   **"Code Example Generator" Agent Skill**: (Type: general-purpose, model: sonnet)
    -   **Prompt**: "Given a technical concept from the book (e.g., 'ROS 2 publisher node'), generate a runnable code snippet in Python (rclpy) that illustrates this concept, suitable for inclusion in a Docusaurus markdown file."
    -   **Purpose**: Expedite code example creation and ensure correctness.
-   **"Diagram Suggester" Agent Skill**: (Type: general-purpose, model: sonnet)
    -   **Prompt**: "Given a description of a complex robotic system or process (e.g., 'ROS 2 communication flow between a publisher and subscriber'), suggest a suitable diagram type (flowchart, block diagram) and key elements to include, outputting in Mermaid or PlantUML syntax."
    -   **Purpose**: Assist in visualizing complex technical concepts.

### How they can be loaded dynamically like “Matrix Trinity” example

-   **Configuration via `.claude/settings.json`**: Define custom subagents and skills in `.claude/settings.json` or a similar configuration file. This allows Claude Code to discover and load them dynamically at runtime.
    ```json
    {
      "subagents": [
        {
          "name": "book-sectioner",
          "type": "general-purpose",
          "prompt_file": ".claude/subagents/book-sectioner.md",
          "model": "haiku"
        }
      ],
      "skills": [
        {
          "name": "code-example-generator",
          "prompt_file": ".claude/skills/code-example-generator.md",
          "model": "sonnet"
        }
      ]
    }
    ```
-   **Dynamic Invocation**: Claude Code's internal mechanism can detect these definitions and make them available via the `Task` tool (for subagents) or `Skill` tool (for skills), similar to how it handles built-in capabilities or external MCP servers.

### Tasks to maximize bonus points

-   [ ] T054 [BONUS] Implement the "Book Sectioner" Subagent in `.claude/subagents/book-sectioner.md`
-   [ ] T055 [BONUS] Implement the "Code Example Generator" Agent Skill in `.claude/skills/code-example-generator.md`
-   [ ] T056 [BONUS] Implement the "Diagram Suggester" Agent Skill in `.claude/skills/diagram-suggester.md`
-   [ ] T057 [BONUS] Demonstrate dynamic loading and usage of all implemented Subagents/Skills.

## Hardware & Cloud Requirements

### Local Workstations & Edge Kits

-   **Primary Development Workstation**:
    -   **CPU**: Multi-core (Intel i7/i9 or AMD Ryzen 7/9 equivalent)
    -   **RAM**: 32 GB minimum, 64 GB recommended
    -   **GPU**: NVIDIA RTX 3070/4070 or higher (for Isaac Sim, local LLM inference) with at least 8 GB VRAM
    -   **Storage**: 1 TB SSD (NVMe recommended)
    -   **OS**: Ubuntu 20.04/22.04 LTS (for ROS 2, Gazebo, Isaac Sim compatibility)
-   **Edge Kits (Optional for real-world deployment/testing)**:
    -   NVIDIA Jetson Nano/Xavier NX/Orin Nano (for running ROS 2 nodes, basic AI inference on hardware)
    -   Intel RealSense Depth Cameras (D435/D455) for perception labs
    -   Optional: Small humanoid robot platform (e.g., Robotis OP3, Unitree Go1) for capstone project.

### Optional Cloud Resources

-   **Neon Serverless Postgres**: Free Tier for RAG chatbot database.
-   **Qdrant Cloud**: Free Tier for vector database.
-   **GitHub Pages**: Free for Docusaurus book hosting.
-   **Optional LLM APIs**: OpenAI API, Anthropic Claude API (for RAG chatbot generation if local inference is insufficient or for cost optimization).
-   **Optional GPU Cloud Instances**: For heavy Isaac Sim RL training or large LLM inference if local workstation is insufficient (e.g., AWS EC2, Google Cloud, Azure).

## Assessment & Evaluation Criteria

### Base Points (Out of 100)

-   **Book Content (40 points)**:
    -   Completeness of Module 1-4 and Capstone content.
    -   Accuracy and technical rigor.
    -   Clarity and readability (Flesch-Kincaid 10-12).
    -   Inclusion of code examples, diagrams, labs, FAQs, troubleshooting.
    -   Adherence to Markdown/Docusaurus format.
-   **RAG Chatbot Functionality (40 points)**:
    -   Successful deployment of FastAPI, Neon, Qdrant stack.
    -   Accurate retrieval of information from book content.
    -   LLM generates coherent and relevant answers based *only* on retrieved text.
    -   Chatbot responds to user-selected text queries.
    -   Robust error handling.
-   **Deployment (20 points)**:
    -   Docusaurus book successfully deployed to GitHub Pages.
    -   RAG chatbot backend accessible and functional.
    -   All necessary configurations and dependencies clearly documented.

### Bonus Points (Up to 50)

-   **Reusable Intelligence (25 points)**:
    -   Implementation of at least two suggested Claude Code Subagents/Agent Skills.
    -   Demonstration of dynamic loading and effective use within Claude Code.
    -   Quality and reusability of the implemented intelligence.
-   **Advanced RAG Features (15 points)**:
    -   Contextual chat history management beyond basic turn-taking.
    -   Multi-hop reasoning for complex queries.
    -   Integration of advanced ranking or re-ranking for retrieval.
-   **Enhanced Humanoid Control (10 points)**:
    -   Demonstration of advanced humanoid control (e.g., dynamic balancing, advanced manipulation) in simulation.
    -   Novel multi-modal interaction techniques beyond basic VLA.

## References & Resources

-   **Claude Code Documentation**: [https://code.claude.com/docs](https://code.claude.com/docs)
-   **Spec-Kit Plus Documentation**: [Link to Spec-Kit Plus official documentation/GitHub] (NEEDS CLARIFICATION: exact link)
-   **Docusaurus Documentation**: [https://docusaurus.io/docs](https://docusaurus.io/docs)
-   **NVIDIA Isaac Sim Documentation**: [https://docs.omniverse.nvidia.com/app_isaacsim/app_isaacsim/overview.html](https://docs.omniverse.nvidia.com/app_isaacsim/app_isaacsim/overview.html)
-   **OpenAI ChatKit SDKs/Agents**: [https://platform.openai.com/docs/assistants/overview](https://platform.openai.com/docs/assistants/overview) (or specific ChatKit docs if available)
-   **ROS 2 Documentation**: [https://docs.ros.org/en/foxy/index.html](https://docs.ros.org/en/foxy/index.html) (adjust version as needed)
-   **Gazebo/Ignition Documentation**: [https://gazebosim.org/docs](https://gazebosim.org/docs)
-   **Unity 3D Robotics**: [https://docs.unity3d.com/Packages/com.unity.robotics.ros-tcp-connector@latest/index.html](https://docs.unity3d.com/Packages/com.unity.robotics.ros-tcp-connector@latest/index.html)
-   **OpenAI Whisper Documentation**: [https://openai.com/research/whisper](https://openai.com/research/whisper) (for model details)
-   **FastAPI Documentation**: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
-   **Neon Serverless Postgres Documentation**: [https://neon.tech/docs/](https://neon.tech/docs/)
-   **Qdrant Cloud Documentation**: [https://qdrant.tech/documentation/cloud/](https://qdrant.tech/documentation/cloud/)
-   **Relevant Research Papers/Lectures**: (To be added as specific modules are developed)