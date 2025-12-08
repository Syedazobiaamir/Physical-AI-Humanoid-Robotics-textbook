# Physical AI & Humanoid Robotics Textbook

[![Frontend CI](https://github.com/Syedazobiaamir/Physical-AI-Humanoid-Robotics-textbook/actions/workflows/frontend.yml/badge.svg)](https://github.com/Syedazobiaamir/Physical-AI-Humanoid-Robotics-textbook/actions/workflows/frontend.yml)
[![Backend CI](https://github.com/Syedazobiaamir/Physical-AI-Humanoid-Robotics-textbook/actions/workflows/backend.yml/badge.svg)](https://github.com/Syedazobiaamir/Physical-AI-Humanoid-Robotics-textbook/actions/workflows/backend.yml)

An **AI-native, interactive textbook platform** for learning Physical AI and Humanoid Robotics. Built with modern web technologies and powered by AI for personalized learning experiences.

![Platform Preview](frontend/static/img/logo.svg)

## Key Features

| Feature | Description |
|---------|-------------|
| **Interactive MDX Content** | 13-week curriculum with hands-on labs and code examples |
| **AI Chat Assistant** | RAG-powered Q&A - select text to ask questions |
| **Content Personalization** | Adapt difficulty to beginner/intermediate/advanced |
| **Urdu Translation** | On-demand translation preserving code blocks |
| **Chapter Quizzes** | Auto-generated MCQs with instant feedback |
| **OAuth Authentication** | Sign in with Google or GitHub |
| **Progress Tracking** | Monitor your learning journey |

## Curriculum Overview

### Module 1: ROS2 Fundamentals (Weeks 1-3)
- Introduction to ROS2 architecture and DDS
- Nodes, Topics, Services, and Actions
- Building your first ROS2 packages

### Module 2: Robot Perception (Weeks 4-6)
- Sensor integration (IMU, LiDAR, Depth cameras)
- Computer vision with OpenCV and ROS2
- SLAM and localization

### Module 3: Motion & Control (Weeks 7-9)
- Robot kinematics and dynamics
- Motion planning algorithms
- Control systems implementation

### Module 4: Integration & AI (Weeks 10-13)
- Reinforcement learning for robotics
- System integration patterns
- Advanced topics and final project

## Tech Stack

### Frontend
- **Framework**: [Docusaurus](https://docusaurus.io/) with TypeScript
- **Components**: React with custom MDX components
- **Styling**: CSS Modules + CSS-in-JS
- **Deployment**: Vercel / GitHub Pages

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.11+)
- **Database**: SQLite (dev) / Neon Postgres (prod)
- **Vector Store**: [Qdrant](https://qdrant.tech/) for RAG
- **AI Providers**: Google Gemini, OpenAI, Anthropic Claude
- **Auth**: Custom OAuth with JWT

## Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/Syedazobiaamir/Physical-AI-Humanoid-Robotics-textbook.git
cd Physical-AI-Humanoid-Robotics-textbook
```

### 2. Start the Frontend
```bash
cd frontend
npm install
npm start
```
Frontend runs at http://localhost:3000

### 3. Start the Backend (Optional - for AI features)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Add your API keys to .env
uvicorn src.main:app --reload
```
Backend API at http://localhost:8000 | Docs at http://localhost:8000/docs

### Environment Variables

Create `backend/.env` with:
```env
# Required: At least one AI provider
GEMINI_API_KEY=your_key_here     # Recommended - free tier available

# Optional: Additional providers
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Optional: Vector database for RAG
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your_key_here

# Optional: Production database
NEON_DB_URL=postgresql://user:pass@host/db

# Auth (generate with: python -c "import secrets; print(secrets.token_hex(32))")
JWT_SECRET_KEY=your_secret_key
```

## Project Structure

```
physical-ai-textbook/
├── frontend/                    # Docusaurus frontend
│   ├── docs/                   # MDX chapter content
│   │   ├── module-1/          # Weeks 1-3: ROS2 Fundamentals
│   │   ├── module-2/          # Weeks 4-6: Perception
│   │   ├── module-3/          # Weeks 7-9: Motion & Control
│   │   └── module-4/          # Weeks 10-13: Integration & AI
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── Auth/         # Authentication (SignIn, SignUp, UserMenu)
│   │   │   ├── ChatBot/      # AI chat widget
│   │   │   ├── Hero/         # Landing page hero
│   │   │   └── ModuleCard/   # Course module cards
│   │   ├── pages/            # Custom pages
│   │   └── css/              # Global styles
│   └── static/               # Images, fonts
│
├── backend/                    # FastAPI backend
│   ├── src/
│   │   ├── api/              # REST endpoints
│   │   ├── auth/             # OAuth & JWT
│   │   ├── models/           # SQLAlchemy models
│   │   ├── services/         # Business logic
│   │   ├── agents/           # AI subagents
│   │   └── llm/              # AI provider integrations
│   ├── Dockerfile            # Container build
│   ├── railway.json          # Railway deployment
│   ├── render.yaml           # Render deployment
│   └── fly.toml              # Fly.io deployment
│
├── specs/                      # Feature specifications
│   └── 1-ai-textbook-platform/
│       ├── spec.md           # Requirements
│       ├── plan.md           # Architecture
│       └── tasks.md          # Implementation tasks
│
├── .specify/                   # Spec-Kit Plus
│   ├── skills/               # Claude Code skills
│   │   ├── chapter-writer/   # MDX generation
│   │   ├── summary/          # Key points extraction
│   │   ├── quiz-generator/   # MCQ generation
│   │   └── validator/        # Content validation
│   ├── templates/            # Document templates
│   └── memory/               # Project constitution
│
└── .github/workflows/          # CI/CD pipelines
    ├── frontend.yml          # Frontend build & deploy
    └── backend.yml           # Backend test & Docker
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/login/oauth` | POST | Initiate OAuth login |
| `/api/v1/auth/login/callback` | POST | Handle OAuth callback |
| `/api/v1/rag/query` | POST | Semantic search |
| `/api/v1/rag/chat` | POST | RAG-powered chat |
| `/api/v1/personalization/adapt-content` | POST | Adapt content to skill level |
| `/api/v1/translation/urdu` | POST | Translate to Urdu |
| `/api/v1/quizzes/{chapter_id}` | GET | Get chapter quiz |

Full API documentation: http://localhost:8000/docs

## Deployment

### Frontend (Vercel)
1. Connect your GitHub repo to Vercel
2. Set root directory to `frontend`
3. Build command: `npm run build`
4. Output directory: `build`

### Backend (Railway/Render/Fly.io)
1. Connect your GitHub repo
2. Set root directory to `backend`
3. Add environment variables
4. Deploy using included config files

### Environment Variables for Production
```env
ENVIRONMENT=production
DEBUG=false
BACKEND_CORS_ORIGINS=https://your-frontend-domain.vercel.app
DATABASE_URL=postgresql://...
JWT_SECRET_KEY=generate_secure_key
```

## Development

### Frontend Commands
```bash
npm start           # Development server
npm run build       # Production build
npm run serve       # Preview production build
npm run lint        # ESLint
npm run format      # Prettier
```

### Backend Commands
```bash
uvicorn src.main:app --reload   # Development server
pytest                           # Run tests
black src/                       # Format code
flake8 src/                      # Lint code
mypy src/                        # Type check
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Docusaurus](https://docusaurus.io/) - Documentation framework
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Qdrant](https://qdrant.tech/) - Vector similarity search
- [Google Gemini](https://ai.google.dev/) - AI model provider
- [OpenAI](https://openai.com/) - AI model provider
- [Anthropic Claude](https://anthropic.com/) - AI model provider

---

Built with AI assistance using [Claude Code](https://claude.ai/code)
