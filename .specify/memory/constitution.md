<!--
Sync Impact Report:
Version change: 1.0.0 → 2.0.0
List of modified principles:
  - Accuracy → Comprehensive & Rigorous Content
  - Clarity → Course-Aligned Structure & Content
  - Reproducibility → Clarity & Accuracy
  - Rigor → Deliverable Format & Length
  - Added Principle 5: Instructional Content
  - Added Principle 6: Optional Advanced Steps
Added sections:
  - Key Standards and Constraints (Expanded)
  - Instructions and Success Criteria (Expanded)
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md: ⚠ pending (generic, needs adaptation for book context)
  - .specify/templates/spec-template.md: ⚠ pending (generic, needs adaptation for book context)
  - .specify/templates/tasks-template.md: ⚠ pending (generic, needs adaptation for book context)
  - .specify/templates/commands/sp.constitution.md: ⚠ pending (file not found)
  - README.md: ⚠ pending (file not found)
  - docs/quickstart.md: ⚠ pending (file not found)
Follow-up TODOs:
  - Adapt existing templates (.specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md) to align with the book context or create new templates if more appropriate.
  - Create .specify/templates/commands/sp.constitution.md if needed for specific constitution-related commands.
  - Create README.md and docs/quickstart.md if desired for the project, reflecting the new constitution's principles.
-->
# Physical AI & Humanoid Robotics Book Constitution

## Core Principles

### Comprehensive & Rigorous Content
Generate a comprehensive, academically rigorous, and structured book on Physical AI & Humanoid Robotics suitable for students in a technical course. Include simulation, ROS 2, NVIDIA Isaac, VLA, and humanoid robotics content, integrating real-world and simulated robotics concepts.

### Course-Aligned Structure & Content
Structured in chapters corresponding to modules and weekly topics. Emphasis on Physical AI principles, embodied intelligence, humanoid robot design, simulation, AI perception, and Vision-Language-Action integration. Input Reference: Course outline, modules, weekly breakdown, hardware requirements, lab options, and capstone project description (as provided).

### Clarity & Accuracy
Writing clarity: Flesch-Kincaid grade 10–12. All technical claims must be accurate and reproducible; cite sources where appropriate (APA style).

### Deliverable Format & Length
Book length: 50–80 pages (approx. 20,000–40,000 words). Output in Markdown or Docusaurus-compatible format, ready for GitHub Pages deployment.

### Instructional Content
Generate a table of contents with chapters for each module and week. For each chapter: Include theoretical explanation (Physical AI, robotics principles), practical implementation examples (ROS 2 code snippets, Gazebo simulation steps, Isaac Sim instructions, Unity visualization tips), hardware guidance (Jetson, RealSense, Edge Kits, and optional robot options). Add diagrams, flowcharts, or tables to explain complex systems. Add a capstone project chapter: Autonomous humanoid performing VLA tasks, voice-to-action, navigation, manipulation. Include FAQs, troubleshooting tips, and learning outcomes per chapter. Ensure RAG-readiness: Chunk text into retrievable sections for embedding in a chatbot. Provide a reference section with URLs or papers for all factual claims.

### Optional Advanced Steps
Use a “Code Snippet Generator” subagent to automatically produce ROS 2, Gazebo, Isaac, or VLA example code blocks. Use a “Diagram Generator” subagent to suggest diagrams for complex robotic systems. Use a “RAG Sectioner” subagent to split book into retrievable sections for chatbot integration.

## Key Standards and Constraints

**Key Standards:**
- Include diagrams, tables, and code snippets (ROS 2, Gazebo, Isaac, VLA).
- All technical claims must be accurate and reproducible; cite sources where appropriate (APA style).
- Writing clarity: Flesch-Kincaid grade 10–12.

**Constraints:**
- Book length: 50–80 pages (approx. 20,000–40,000 words).
- Structured in chapters corresponding to modules and weekly topics.

## Instructions and Success Criteria

**Instructions to Claude Code:**
- Generate a table of contents with chapters for each module and week.
- For each chapter:
    - Include theoretical explanation (Physical AI, robotics principles).
    - Provide practical implementation examples: ROS 2 code snippets, Gazebo simulation steps, Isaac Sim instructions, Unity visualization tips.
    - Include hardware guidance: Jetson, RealSense, Edge Kits, and optional robot options.
    - Add diagrams, flowcharts, or tables to explain complex systems.
    - Add a capstone project chapter: Autonomous humanoid performing VLA tasks, voice-to-action, navigation, manipulation.
    - Include FAQs, troubleshooting tips, and learning outcomes per chapter.
    - Ensure RAG-readiness: Chunk text into retrievable sections for embedding in a chatbot.
    - Provide a reference section with URLs or papers for all factual claims.

**Optional Advanced Step (Claude Code Subagents / Skills):**
- “Code Snippet Generator”: Automatically produce ROS 2, Gazebo, Isaac, or VLA example code blocks.
- “Diagram Generator”: Suggest diagrams for complex robotic systems.
- “RAG Sectioner”: Split book into retrievable sections for chatbot integration.

**Success Criteria:**
- Comprehensive coverage of Physical AI, humanoid robotics, simulation, ROS 2, NVIDIA Isaac, and VLA.
- Book content aligns with course outline, modules, and weekly breakdown.
- All technical claims are accurate, reproducible, and cited (APA style).
- Book is between 50-80 pages (20,000-40,000 words).
- Output is in Markdown or Docusaurus-compatible format, ready for GitHub Pages deployment.
- RAG-readiness is ensured for chatbot integration.

## Governance
The Constitution outlines the core principles, standards, and guidelines for generating the 'Physical AI & Humanoid Robotics' book. Amendments require documentation, approval, and a migration plan.

**Version**: 2.0.0 | **Ratified**: 2025-12-04 | **Last Amended**: 2025-12-04