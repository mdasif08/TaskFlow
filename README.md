# TaskFlow - Microservices Task Management Platform

A complete, production-ready microservices-based task management platform built with FastAPI, React, PostgreSQL, Docker, and GitHub Actions CI/CD.

## 🏗️ Architecture Overview

TaskFlow demonstrates modern microservices architecture with:

- **Backend Service**: FastAPI + SQLAlchemy + JWT authentication
- **Frontend Service**: React + Vite + Tailwind CSS + Axios
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Deployment**: Docker Compose orchestration
- **CI/CD**: GitHub Actions for automated testing and deployment

## 📁 Project Structure

```
TaskFlow/
├── backend-service/          # FastAPI microservice
│   ├── app/
│   │   ├── main.py          # FastAPI application
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── routes.py        # API endpoints
│   │   ├── auth.py          # JWT authentication
│   │   └── database.py      # Database connection
│   ├── tests/               # Unit tests
│   ├── Dockerfile
│   └── requirements.txt
├── frontend-service/        # React application
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/          # Page components
│   │   ├── context/        # React Context
│   │   └── utils/          # Utility functions
│   ├── Dockerfile
│   └── package.json
├── .github/workflows/       # CI/CD pipeline
├── docker-compose.yml       # Service orchestration
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Git

### Running with Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd TaskFlow
   ```

2. **Start all services**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development

#### Option 1: Quick Setup Scripts
```bash
# Windows
setup-local.bat

# Linux/Mac
chmod +x setup-local.sh
./setup-local.sh
```

#### Option 2: Manual Setup

**Backend Service**
```bash
cd backend-service
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend Service**
```bash
cd frontend-service
npm install
npm run dev
```

**Note**: For local development, the backend uses SQLite by default. For PostgreSQL, use Docker Compose.

## 🔧 Troubleshooting

### Common Issues

#### 1. SQLAlchemy Import Error
**Error**: `ModuleNotFoundError: No module named 'sqlalchemy'`

**Solution**:
```bash
cd backend-service
pip install -r requirements.txt
```

#### 2. Pydantic Compatibility Issues
**Error**: Pydantic V1 functionality compatibility issues

**Solution**: The requirements.txt has been updated with flexible version constraints to resolve compatibility issues.

#### 3. Database Connection Issues
**Error**: Database connection failures

**Solutions**:
- **Local Development**: Uses SQLite by default (no setup required)
- **PostgreSQL**: Use Docker Compose for full stack
- **Custom Database**: Set `DATABASE_URL` environment variable

#### 4. Frontend Build Issues
**Error**: Node modules or build failures

**Solution**:
```bash
cd frontend-service
rm -rf node_modules package-lock.json
npm install
npm run dev
```

## 🔧 Configuration

### Environment Variables

#### Backend Service
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

#### Frontend Service
- `VITE_API_URL`: Backend API URL (default: http://localhost:8000/api)

## 📚 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/signup` | Register new user |
| POST | `/api/auth/login` | Login and get JWT token |

### Task Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | List tasks (with filters) |
| POST | `/api/tasks` | Create new task |
| GET | `/api/tasks/{id}` | Get task by ID |
| PUT | `/api/tasks/{id}` | Update task |
| DELETE | `/api/tasks/{id}` | Delete task |

### User Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/me` | Get current user profile |

### Query Parameters

#### GET /api/tasks
- `status`: Filter by status (pending, in_progress, completed)
- `priority`: Filter by priority (low, medium, high)
- `skip`: Pagination offset (default: 0)
- `limit`: Items per page (default: 10, max: 100)

## 🧪 Testing

### Backend Tests
```bash
cd backend-service
pytest tests/ -v --cov=app
```

### Frontend Tests
```bash
cd frontend-service
npm test
```

### Integration Tests
```bash
docker-compose up --build
# Run integration test suite
```

## 🐳 Docker Commands

### Build and Run
```bash
# Build all services
docker-compose build

# Start all services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Individual Services
```bash
# Backend only
docker-compose up backend-service

# Frontend only
docker-compose up frontend-service

# Database only
docker-compose up database
```

## 🔄 CI/CD Pipeline

The GitHub Actions workflow includes:

1. **Backend Testing**
   - Python linting (flake8, black)
   - Unit tests with pytest
   - Code coverage reporting

2. **Frontend Testing**
   - ESLint and Prettier
   - Jest unit tests
   - Code coverage reporting

3. **Security Scanning**
   - Trivy vulnerability scanning
   - Dependency security checks

4. **Docker Build & Push**
   - Multi-stage Docker builds
   - Image optimization
   - Registry push on main branch

5. **Integration Tests**
   - End-to-end service testing
   - API contract validation

## 🛠️ Development

### Adding New Features

1. **Backend**: Add new endpoints in `routes.py`, models in `models.py`
2. **Frontend**: Create components in `src/components/`, pages in `src/pages/`
3. **Database**: Update models and run migrations
4. **Tests**: Add corresponding unit tests

### Code Quality

- **Backend**: flake8, black, pytest
- **Frontend**: ESLint, Prettier, Jest
- **Git**: Conventional commits, branch protection
- **Security**: Dependabot, Trivy scanning

## 📊 Monitoring & Logging

### Application Metrics
- Request/response times
- Error rates
- Database query performance

### Logging
- Structured JSON logging
- Request correlation IDs
- Error tracking and alerting

## 🔒 Security Features

- JWT authentication with secure tokens
- Password hashing with bcrypt
- CORS configuration
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy
- XSS protection in React

## 🚀 Deployment

### Production Deployment

1. **Environment Setup**
   ```bash
   # Set production environment variables
   export DATABASE_URL=postgresql://user:pass@host:port/db
   export SECRET_KEY=your-production-secret-key
   ```

2. **Docker Compose Production**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Database Migrations**
   ```bash
   # Run database migrations
   docker-compose exec backend-service alembic upgrade head
   ```

### Scaling

- **Horizontal Scaling**: Multiple backend instances behind load balancer
- **Database**: Read replicas for query optimization
- **Caching**: Redis for session storage and API caching
- **CDN**: Static asset delivery optimization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Resume Highlights

This project demonstrates:

- **Microservices Architecture**: Service separation and communication
- **Full-Stack Development**: React frontend + FastAPI backend
- **Database Design**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT-based security implementation
- **Containerization**: Docker multi-stage builds
- **CI/CD**: GitHub Actions automation
- **Testing**: Unit, integration, and E2E testing
- **DevOps**: Infrastructure as code, monitoring, logging
- **Security**: Best practices and vulnerability scanning
- **Code Quality**: Linting, formatting, and coverage

## 🔮 Future Enhancements

- [ ] Real-time notifications with WebSockets
- [ ] File upload and attachment support
- [ ] Advanced task filtering and search
- [ ] Team collaboration features
- [ ] Mobile application
- [ ] Kubernetes deployment
- [ ] Monitoring with Prometheus/Grafana
- [ ] Message queue integration
- [ ] Multi-tenant architecture
- [ ] Advanced analytics and reporting

## 📞 Support

For questions or support, please open an issue in the GitHub repository.

---

**Built with ❤️ for modern microservices development**
