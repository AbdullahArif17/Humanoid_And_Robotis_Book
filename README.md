# Humanoid & Robotics Book - Production Ready

A comprehensive, technical book on "Physical AI & Humanoid Robotics" with an integrated RAG (Retrieval-Augmented Generation) chatbot, fully configured for production deployment.

## 🚀 Features

- **Interactive Documentation**: Docusaurus-based book with comprehensive content on ROS 2, Gazebo/Unity, NVIDIA Isaac, and Vision-Language-Action (VLA)
- **AI-Powered Chatbot**: RAG-based chatbot that can answer questions about the entire book content
- **Production Ready**: Fully configured for deployment with Docker, Nginx, and SSL support
- **Scalable Architecture**: Microservices architecture with PostgreSQL and Qdrant vector database
- **Comprehensive Content**: 4 complete modules covering ROS 2, Digital Twins, NVIDIA Isaac, and Vision-Language-Action
- **Context-Aware**: Ask questions about selected text for targeted answers
- **Persistent Chat History**: Conversations saved across sessions

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

### Running the Book (Frontend)

1. Navigate to the book directory:
   ```bash
   cd book
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The book will be available at `http://localhost:3000`

### Running the RAG Chatbot (Backend)

1. Navigate to the rag-chatbot directory:
   ```bash
   cd rag-chatbot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your actual credentials
   ```

4. Set up Qdrant collection:
   ```bash
   python scripts/setup_qdrant.py
   ```

5. Ingest book content:
   ```bash
   python scripts/ingest_book_content.py
   ```

6. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

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

## 🏗️ Production Deployment

### Prerequisites for Production

- Docker and Docker Compose
- SSL certificates (optional but recommended)
- Production domain name
- Cloud hosting (AWS, GCP, Azure, or VPS)

### Environment Setup

Create a `.env` file in the `rag-chatbot` directory with production values:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_production_openai_api_key
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# Qdrant Configuration
QDRANT_URL=your_production_qdrant_url
QDRANT_API_KEY=your_production_qdrant_api_key
QDRANT_COLLECTION_NAME=humanoid_robotics_book

# Database Configuration
DATABASE_URL=postgresql://username:password@production-db-host:5432/database_name

# CORS Configuration
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

### Automated Deployment

1. Make the deployment script executable:
   ```bash
   chmod +x deploy.sh
   ```

2. Run the deployment script:
   ```bash
   ./deploy.sh
   ```

### Manual Deployment

1. Build the frontend:
   ```bash
   cd book
   npm install
   npm run build
   ```

2. Deploy with Docker Compose:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. Ingest content into vector database:
   ```bash
   docker-compose -f docker-compose.prod.yml exec backend python scripts/ingest_book_content.py
   ```

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
│   ├── Dockerfile               # Production-ready Docker configuration
│   └── README.md
│
├── ssl/                         # SSL certificates directory
├── nginx.conf                   # Production Nginx configuration
├── docker-compose.prod.yml      # Production Docker Compose
├── deploy.sh                    # Automated deployment script
├── DEPLOYMENT_GUIDE.md          # Comprehensive deployment documentation
├── plan.md                      # Architecture plan
├── tasks.md                     # Deployment tasks
├── .github/
│   └── workflows/
│       └── deploy.yml           # GitHub Actions CI/CD
│
└── README.md                    # This file
```

## 🌐 Production Architecture

The production setup includes:

- **Nginx**: Reverse proxy with SSL termination and static file serving
- **Docker**: Containerized services for consistency and scalability
- **PostgreSQL**: Production database with backup capabilities
- **Qdrant**: Vector database for semantic search
- **Health Checks**: Built-in monitoring endpoints
- **SSL Ready**: Configuration for HTTPS encryption

### SSL Configuration

1. Place your SSL certificate and key in the `ssl/` directory:
   ```
   ssl/
   ├── cert.pem (your SSL certificate)
   └── key.pem (your private key)
   ```

2. Update `nginx.conf` with your domain name

## 📊 Monitoring

### Health Checks

- Health endpoint: `https://yourdomain.com/health`
- Backend API: `https://yourdomain.com/api/`
- Frontend: `https://yourdomain.com/`

### Logs

View application logs:
```bash
docker-compose -f docker-compose.prod.yml logs -f
```

## 🔧 Troubleshooting

### Common Issues

1. **Environment Variables**: Ensure all required environment variables are set
2. **Database Connection**: Verify PostgreSQL connection details
3. **Qdrant Connection**: Check Qdrant URL and API key
4. **OpenAI API**: Verify API key and rate limits

### Debugging

1. Check container status:
   ```bash
   docker-compose -f docker-compose.prod.yml ps
   ```

2. Check logs for specific service:
   ```bash
   docker-compose -f docker-compose.prod.yml logs backend
   docker-compose -f docker-compose.prod.yml logs db
   docker-compose -f docker-compose.prod.yml logs nginx
   ```

3. Test API endpoints:
   ```bash
   curl https://yourdomain.com/health
   curl https://yourdomain.com/api/v1/chat -X POST -H "Content-Type: application/json" -d '{"message":"Hello","session_id":"test"}'
   ```

## 🛡️ Security

- API keys stored in environment variables
- Non-root user in Docker containers
- SSL/TLS encryption
- CORS policy enforcement
- Rate limiting (configure as needed)
- Secure database connections with SSL

## 📈 Scaling

- Multiple backend workers in Docker
- Database connection pooling
- CDN-ready static assets
- Horizontal scaling support
- Load balancing ready

## 🔄 Updates

To update the application:

1. Pull latest code:
   ```bash
   git pull origin main
   ```

2. Rebuild and restart:
   ```bash
   docker-compose -f docker-compose.prod.yml build
   docker-compose -f docker-compose.prod.yml up -d
   ```

## 📚 Content Management

Content is managed through the Docusaurus documentation system. To update book content:

1. Edit markdown files in `book/docs/`
2. Rebuild the frontend
3. Redeploy the static files

## 🤖 Chatbot Training

To retrain the RAG chatbot with new content:

```bash
docker-compose -f docker-compose.prod.yml exec backend python scripts/ingest_book_content.py
```

## 🚨 Emergency Procedures

- To stop all services: `docker-compose -f docker-compose.prod.yml down`
- To restart services: `docker-compose -f docker-compose.prod.yml restart`
- To access backend shell: `docker-compose -f docker-compose.prod.yml exec backend bash`

## 📝 Documentation

- [Backend README](rag-chatbot/README.md) - RAG chatbot setup and API docs
- [Deployment Guide](DEPLOYMENT_GUIDE.md) - Comprehensive production deployment instructions
- [Plan](plan.md) - Architecture and deployment planning
- [Tasks](tasks.md) - Deployment task checklist
- [Book Content](book/docs/) - All module documentation

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
