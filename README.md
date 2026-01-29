# FullStack Todo Web Application

A comprehensive full-stack todo application featuring a Next.js frontend with TypeScript and Tailwind CSS, and a FastAPI backend with PostgreSQL database and JWT authentication. Built using spec-driven development methodology.

## 🚀 Features

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

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | Next.js 14, React, TypeScript | User Interface & Client-side Logic |
| **Styling** | Tailwind CSS | Responsive Styling & UI Components |
| **Backend** | FastAPI, Python 3.13+ | API Server & Business Logic |
| **Database** | PostgreSQL | Data Storage & Management |
| **ORM** | SQLAlchemy | Database Abstraction Layer |
| **Authentication** | JWT, bcrypt | User Authentication & Authorization |
| **Package Manager** | pnpm | Dependency Management |

## 📋 Prerequisites

- Node.js (v18 or higher)
- Python 3.13+
- PostgreSQL
- pnpm
- Git

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Muhammad-Umair13/Todo-FullStack-WebApp.git
cd Todo-FullStack-WebApp
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -e ".[dev]"
# Or using uv (recommended)
uv pip install -e ".[dev]"

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials and secret keys

# Initialize the database
alembic upgrade head

# Run the backend server
uvicorn src.main:app --reload --port 8000
```

### 3. Frontend Setup

```bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Install JavaScript dependencies
pnpm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your backend API URL

# Run the frontend development server
pnpm dev
```

### 4. Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 🏗️ Project Structure

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