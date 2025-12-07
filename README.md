# Physical AI & Humanoid Robotics Book

A comprehensive technical book on Physical AI and Humanoid Robotics, built with Docusaurus and powered by an intelligent RAG chatbot.

## 🚀 Features

- 📚 **Comprehensive Content**: 4 complete modules covering ROS 2, Digital Twins, NVIDIA Isaac, and Vision-Language-Action
- 🤖 **RAG-Powered Chatbot**: Interactive Q&A using OpenAI, Qdrant, and Neon Postgres
- 🎯 **Context-Aware**: Ask questions about selected text for targeted answers
- 💬 **Persistent Chat History**: Conversations saved across sessions
- 🌐 **Production Ready**: Deployed to GitHub Pages with cloud backend

## 📖 Book Modules

### Module 1: The Robotic Nervous System (ROS 2)
Introduction to ROS 2 fundamentals, nodes, topics, services, and practical labs.

### Module 2: The Digital Twin (Gazebo & Unity)
Physics simulation, environment building, and sensor simulation for robotics.

### Module 3: The AI-Robot Brain (NVIDIA Isaac™)
Advanced AI perception, navigation, and learning with NVIDIA Isaac ecosystem.

### Module 4: Vision-Language-Action (VLA)
Integrating LLMs with robotics for voice-to-action and cognitive planning.

### Capstone Project
Autonomous humanoid performing complex VLA tasks integrating all modules.

## 🛠️ Tech Stack

### Frontend
- **Docusaurus 3.9.2**: Modern documentation framework
- **React 19**: UI components
- **TypeScript**: Type-safe development
- **GitHub Pages**: Hosting

### Backend (RAG Chatbot)
- **FastAPI**: High-performance Python web framework
- **OpenAI API**: GPT-4o-mini for responses, text-embedding-3-small for vectors
- **Qdrant Cloud**: Vector database for semantic search
- **Neon Serverless Postgres**: Chat history and session management
- **SQLAlchemy**: ORM for database operations

## 🚀 Quick Start

### Prerequisites

- Node.js 20+
- Python 3.11+
- OpenAI API key
- Qdrant Cloud account
- Neon Postgres account

### Local Development

#### 1. Clone the Repository

```bash
git clone https://github.com/AbdullahArif17/Humanoid_And_Robotis_Book.git
cd Humanoid_And_Robotis_Book
```

#### 2. Setup Frontend

```bash
cd book
npm install
npm start
```

The book will be available at `http://localhost:3000`

#### 3. Setup Backend

```bash
cd ../rag-chatbot
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
```

#### 4. Initialize Vector Database

```bash
python scripts/setup_qdrant.py
python scripts/ingest_book_content.py
```

#### 5. Run Backend

```bash
uvicorn app.main:app --reload
```

Backend API will be available at `http://localhost:8000`

## 📦 Project Structure

```
Humanoid_And_Robotis_Book/
├── book/                          # Docusaurus frontend
│   ├── docs/                      # Book content (markdown)
│   │   ├── 1-ros2-module/
│   │   ├── 2-digital-twin-module/
│   │   ├── 3-isaac-module/
│   │   ├── 4-vla-module/
│   │   └── capstone.md
│   ├── src/
│   │   ├── components/
│   │   │   └── Chatbot/          # React chatbot component
│   │   └── pages/
│   ├── docusaurus.config.ts
│   └── package.json
│
├── rag-chatbot/                   # FastAPI backend
│   ├── app/
│   │   ├── main.py               # FastAPI application
│   │   ├── config.py             # Configuration
│   │   ├── core/
│   │   │   ├── rag.py           # RAG engine
│   │   │   ├── embeddings.py    # OpenAI embeddings
│   │   │   └── chunking.py      # Markdown chunking
│   │   └── db/
│   │       ├── database.py      # Database connection
│   │       └── models.py        # SQLAlchemy models
│   ├── scripts/
│   │   ├── setup_qdrant.py      # Vector DB setup
│   │   └── ingest_book_content.py  # Content ingestion
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
│
├── .github/
│   └── workflows/
│       └── deploy.yml            # GitHub Actions CI/CD
│
├── DEPLOYMENT.md                 # Deployment guide
└── README.md                     # This file
```

## 🌐 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment instructions.

### Quick Deployment Steps

1. **Setup Cloud Services**: Qdrant, Neon, OpenAI
2. **Deploy Backend**: Render, Railway, or Docker
3. **Ingest Content**: Run ingestion scripts
4. **Deploy Frontend**: Push to GitHub (auto-deploys via Actions)

## 📚 Documentation

- [Backend README](rag-chatbot/README.md) - RAG chatbot setup and API docs
- [Deployment Guide](DEPLOYMENT.md) - Production deployment instructions
- [Book Content](book/docs/) - All module documentation

## 🧪 Testing

### Frontend

```bash
cd book
npm run build  # Test production build
```

### Backend

```bash
cd rag-chatbot
pytest tests/ -v  # Run tests (when implemented)
```

## 🤝 Contributing

This is a hackathon project for the GIAIC AI Hackathon. Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is part of the GIAIC AI Hackathon.

## 🙏 Acknowledgments

- **GIAIC** for organizing the hackathon
- **OpenAI** for GPT and embedding models
- **Qdrant** for vector database
- **Neon** for serverless Postgres
- **Docusaurus** for the documentation framework

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Live Demo**: [https://abdullaharif17.github.io/Humanoid_And_Robotis_Book/](https://abdullaharif17.github.io/Humanoid_And_Robotis_Book/)

**Built with** ❤️ **for the GIAIC AI Hackathon**
