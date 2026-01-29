# Todo FullStack Web Application (Phase III: AI Chatbot)

A monorepo with a Next.js frontend, FastAPI backend, and Phase III AI Chatbot integration (Google Gemini, optional Claude/OpenAI fallbacks). Spec‑Driven Development, pnpm/turbo tooling.

## 🚀 Highlights

### Frontend (Next.js)
- **Modern UI**: Clean, responsive interface built with Next.js 14 and TypeScript
- **Authentication**: Secure login/signup functionality with protected routes
- **Dashboard**: Personalized dashboard showing user's tasks and statistics
- **Task Management**: Create, read, update, and delete tasks with rich filtering options
- **Responsive Design**: Works seamlessly across desktop, tablet, and mobile devices

### Backend (FastAPI)
- **RESTful API**: Comprehensive API endpoints for all CRUD operations
- **Authentication**: JWT-based authentication with secure token management
- **Database**: PostgreSQL with SQLAlchemy ORM for robust data management
- **Security**: Password hashing, input validation, and protection against common vulnerabilities
- **Documentation**: Interactive API documentation with Swagger UI

### Additional Features
- **User Management**: Separate user accounts with individual task ownership
- **Task Organization**: Sort, filter, and prioritize tasks efficiently
- **Data Persistence**: Reliable database storage with backup capabilities
- **Type Safety**: Full TypeScript support across frontend and backend

## 🧰 Tech Stack & Key Versions

| Layer | Technology | Version (approx) |
|-------|------------|------------------|
| Frontend | Next.js, React, TypeScript | next ^14.2.0, react 18.2, typescript 5.9 |
| Styling | Tailwind CSS | ^3.x |
| Backend | FastAPI, Uvicorn, SQLModel | fastapi ^0.115, uvicorn ^0.32, sqlmodel ^0.0.31 |
| AI / Chatbot | Google Gemini (google-genai), fallbacks | google-genai >= 1.0.0 |
| DB | PostgreSQL (psycopg2) | postgres-compatible |
| Monorepo | pnpm, turbo | pnpm@9+, turbo ^2.x |

> Note: Specific pinned versions are in `package.json` and `backend/pyproject.toml`.

## 📋 Prerequisites

- Node.js (v18 or higher)
- Python 3.13+
- PostgreSQL
- pnpm
- Git

## Quickstart (Development)

1. Clone the repo

```bash
git clone <your-repo-url>
cd <repo-folder>
```

2. Install root tooling (optional)

```bash
pnpm install
```

3. Backend (FastAPI)

```bash
cd backend
# Install Python deps (poetry or pip)
# If using pipenv or venv, prefer: pip install -e ".[dev]"
# Or: poetry install
cp .env.example .env
# Edit .env and set DATABASE_URL, JWT_SECRET, and GEMINI_API_KEY (if using Gemini)
alembic upgrade head
uvicorn src.main:app --reload --port 8000
```

4. Frontend (Next.js)

```bash
cd frontend
pnpm install
cp .env.example .env.local
# Edit .env.local to point to backend API (e.g., NEXT_PUBLIC_API_URL=http://localhost:8000)
pnpm dev
```

5. Open the app

- Frontend: http://localhost:3000
- Backend docs: http://localhost:8000/api/docs

## AI Chatbot (Phase III)

- Configuration: set `GEMINI_API_KEY` in `backend/.env`. The app expects `GEMINI_MODEL` (default: `gemini-2.0-flash`).
- Troubleshooting: see `GEMINI_API_FIX.md` for quota and error fixes; `CLAUDE.md` contains Claude guidance.
- Fallbacks: The codebase contains notes and guides for switching to Claude or OpenAI if needed.

---

## Project Structure (high-level)

```
Todo-FullStack-WebApp/
├── backend/                  # FastAPI backend application
│   ├── alembic/             # Database migration scripts
│   ├── src/
│   │   ├── auth/           # Authentication modules
│   │   ├── core/           # Core configurations
│   │   ├── models/         # Database models
│   │   ├── routers/        # API route definitions
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── main.py         # Application entry point
│   ├── tests/              # Backend test suite
│   ├── requirements.txt    # Python dependencies
│   └── pyproject.toml      # Python project configuration
├── frontend/               # Next.js frontend application
│   ├── src/
│   │   ├── app/           # Next.js 14 App Router pages
│   │   ├── components/    # Reusable UI components
│   │   └── lib/           # Utility functions
│   ├── public/            # Static assets
│   ├── package.json       # Node.js dependencies
│   └── tailwind.config.ts # Tailwind CSS configuration
├── specs/                 # Specification-driven development artifacts
├── tests/                 # Cross-platform tests
├── .env.example          # Environment variables template
├── pnpm-workspace.yaml   # Monorepo workspace configuration
└── README.md            # This file
```

## 🔐 Authentication Flow

1. **Registration**: Users create an account with email and password
2. **Login**: Credentials are verified and JWT token is issued
3. **Authorization**: JWT token is included in requests to protected endpoints
4. **Token Refresh**: Automatic token refresh for seamless user experience

## 🧪 Testing

### Backend Tests
```bash
# Run all backend tests
pytest

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Run specific test module
pytest tests/unit/test_task.py
```

### Frontend Tests
```bash
# Run frontend tests
pnpm test
```

## 🚀 Production Deployment

### Backend
- Use a WSGI/ASGI server like Gunicorn or Uvicorn in production
- Configure environment variables for production settings
- Set up a production-grade database (PostgreSQL)
- Implement proper logging and monitoring

### Frontend
- Build for production: `pnpm build`
- Serve static files through a CDN or web server
- Configure environment variables for production API endpoints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/) for the backend API
- Frontend powered by [Next.js](https://nextjs.org/)
- Styled with [Tailwind CSS](https://tailwindcss.com/)
- Database management with [PostgreSQL](https://www.postgresql.org/)
- Spec-driven development methodology with [SpecKit Plus](https://github.com/anthropics/spec-kit-plus)

## 📞 Support

If you encounter any issues or have questions about the application, please open an issue in the GitHub repository.

---

**Updated:** This README was updated to reflect Phase III (AI Chatbot integration). For detailed AI troubleshooting, see `GEMINI_API_FIX.md` and `CLAUDE.md`.