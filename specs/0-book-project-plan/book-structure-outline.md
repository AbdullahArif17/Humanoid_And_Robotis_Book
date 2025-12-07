# Book Folder Structure Outline

This document outlines the proposed folder structure and sidebar navigation for the "Physical AI & Humanoid Robotics" Docusaurus book. The goal is to provide a clear, logical organization for content, facilitate easy navigation, and support the RAG chatbot's ability to retrieve information.

## Docusaurus Directory Layout

The `book/` directory will serve as the root for our Docusaurus project.

```
book/
├─── blog/                     # Blog posts (e.g., project updates, deeper dives)
│    └─── 2025-XX-XX-welcome-to-physical-ai.md
├─── docs/                     # Primary documentation content (the main book modules)
│    ├─── intro.md             # Introduction to the book and project
│    ├─── capstone.md          # Capstone project overview
│    │
│    ├─── 1-ros2-module/
│    │    ├─── index.md             # ROS 2 Module Overview
│    │    ├─── basics.md            # ROS 2 Core Concepts
│    │    ├─── packages.md          # Building ROS 2 Packages
│    │    └─── simulation.md        # ROS 2 and Simulation
│    │
│    ├─── 2-digital-twin-module/
│    │    ├─── index.md             # Digital Twin Module Overview
│    │    ├─── gazebo-setup.md      # Gazebo Environment Setup
│    │    ├─── unity-integration.md # Unity Integration
│    │    └─── sensor-sim.md        # Sensor Simulation
│    │
│    ├─── 3-isaac-module/
│    │    ├─── index.md             # NVIDIA Isaac Module Overview
│    │    ├─── isaac-sim.md         # Isaac Sim Deployment
│    │    ├─── perception.md        # Perception Pipelines (VSLAM)
│    │    └─── planning-rl.md       # Path Planning & Reinforcement Learning
│    │
│    └─── 4-vla-module/
│         ├─── index.md             # VLA Module Overview
│         ├─── whisper-ros2.md      # Voice-to-Action with Whisper & ROS 2
│         ├─── cognitive-planning.md# Cognitive Planning
│         └─── multi-modal.md       # Multi-modal Interaction
│
├─── src/                      # Components, pages, and custom CSS
│    ├─── components/
│    │    └─── HomepageFeatures/
│    │         ├─── index.tsx
│    │         └─── styles.module.css
│    ├─── css/
│    │    └─── custom.css
│    └─── pages/
│         ├─── index.module.css
│         └─── index.tsx
├─── static/                   # Static assets (images, favicon, etc.)
├─── docusaurus.config.ts      # Docusaurus configuration
├─── sidebars.ts               # Sidebar configuration for navigation
├─── package.json              # Project dependencies and scripts
├─── tsconfig.json             # TypeScript configuration
└─── README.md                 # Project README
```

## Docusaurus Sidebar Navigation (`sidebars.ts`)

The `sidebars.ts` file will define the structure of the left-hand navigation menu. This will mirror the `docs/` folder structure, providing a clear hierarchy for the book content.

```typescript
import type { SidebarsConfig } from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    'intro', // Introduction to the book
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      link: {
        type: 'doc',
        id: '1-ros2-module/index', // Link to the module overview
      },
      items: [
        '1-ros2-module/basics',
        '1-ros2-module/packages',
        '1-ros2-module/simulation',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      link: {
        type: 'doc',
        id: '2-digital-twin-module/index',
      },
      items: [
        '2-digital-twin-module/gazebo-setup',
        '2-digital-twin-module/unity-integration',
        '2-digital-twin-module/sensor-sim',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac)',
      link: {
        type: 'doc',
        id: '3-isaac-module/index',
      },
      items: [
        '3-isaac-module/isaac-sim',
        '3-isaac-module/perception',
        '3-isaac-module/planning-rl',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA)',
      link: {
        type: 'doc',
        id: '4-vla-module/index',
      },
      items: [
        '4-vla-module/whisper-ros2',
        '4-vla-module/cognitive-planning',
        '4-vla-module/multi-modal',
      ],
    },
    'capstone', // Capstone project overview
  ],
};

export default sidebars;
```

## RAG-Ready Considerations

The hierarchical structure of the `docs/` folder and the `sidebars.ts` configuration will naturally aid in creating RAG-ready content. Each markdown file within a module can be considered a distinct chunk for embedding. The `index.md` files for each module will provide a high-level overview, useful for broader queries, while the sub-documents will offer granular detail. This organization will help the RAG chatbot to retrieve relevant and focused information.