# Django CRUD App with Vue.js Frontend

A comprehensive CRUD application demonstrating modern development practices, patterns, and best practices.

## 🚀 Features

### Backend (Django)
- ✅ **Custom Managers & Querysets** - Advanced query patterns and reusable database logic
- ✅ **Database Indexing** - Optimized queries with strategic indexes
- ✅ **Caching** - Redis integration for performance optimization
- ✅ **API Documentation** - OpenAPI/Swagger documentation with drf-spectacular
- ✅ **Comprehensive Testing** - Unit tests, integration tests with pytest
- ✅ **Service Layer** - Separation of concerns with service-oriented architecture
- ✅ **Custom Middleware** - Request timing, rate limiting, logging, security headers
- ✅ **Advanced Filtering** - Complex query building with custom manager methods
- ✅ **Structured Logging** - Professional logging configuration

### Frontend (Vue.js)
- ✅ **State Management** - Pinia store for centralized state
- ✅ **Composables** - Reusable composition API patterns
- ✅ **Error Handling** - Centralized error handling with composables
- ✅ **Loading States** - Professional loading state management
- ✅ **Vue Router** - Multi-page navigation
- ✅ **Responsive Design** - Mobile-first approach
- ✅ **Dark Mode** - Theme switching capability

### DevOps & Quality
- ✅ **Docker** - Multi-stage Dockerfiles for production
- ✅ **Docker Compose** - Complete development environment
- ✅ **CI/CD** - GitHub Actions pipeline
- ✅ **Pre-commit Hooks** - Code quality automation
- ✅ **Code Formatting** - Black, isort, ESLint
- ✅ **Type Checking** - mypy support

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- Redis (optional, for caching)
- Docker & Docker Compose (optional)

## 🛠️ Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/gabivicu/python-vuejs-crud-app.git
   cd python-vuejs-crud-app
   ```

2. **Backend Setup**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

   # Run migrations
   python manage.py migrate

   # Create superuser (optional)
   python manage.py createsuperuser

   # Run server
   python manage.py runserver
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access the application**
   - Frontend: http://localhost:5173/app
   - Backend API: http://localhost:8000/api/items/
   - API Documentation: http://localhost:8000/api/schema/swagger-ui/
   - Admin Panel: http://localhost:8000/admin

### Docker Setup (Recommended for Development)

The project uses Docker Compose with separate development and production configurations.

**For Development (with Hot Reload):**

```bash
# Build and run development services (backend + frontend-dev + redis)
docker compose up -d backend frontend-dev redis

# Or build and run all at once
docker compose up -d

# View logs
docker compose logs -f

# View logs for specific service
docker compose logs -f frontend-dev
docker compose logs -f backend

# Stop services
docker compose down

# Restart a specific service
docker compose restart backend
docker compose restart frontend-dev
```

**Access the application:**
- **Frontend (Development)**: http://localhost:5173/app
- **Backend API**: http://localhost:8000/api/items/
- **API Documentation**: http://localhost:8000/api/schema/swagger-ui/
- **Admin Panel**: http://localhost:8000/admin

**Important Notes:**
- The `frontend-dev` container uses Vite dev server with **hot-reload** enabled
- Changes to frontend files (`frontend/src/`) are automatically detected and reloaded
- Backend uses Django's `runserver` with **auto-reload** - Python file changes are detected automatically
- No need to restart containers for code changes - only for dependency changes or Docker config changes
- The production `frontend` container (port 80) is commented out by default - uncomment in `docker-compose.yml` if needed

**For Production Build:**

If you need to test the production build:

1. Uncomment the `frontend` service in `docker-compose.yml`
2. Build and run:
   ```bash
   docker compose up -d frontend
   ```
3. Access at: http://localhost/app

## 🧪 Testing

### Backend Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=api --cov-report=html

# Run specific test file
pytest api/tests/test_models.py
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## 📚 API Documentation

Interactive API documentation is available at:
- Swagger UI: http://localhost:8000/api/schema/swagger-ui/
- ReDoc: http://localhost:8000/api/schema/redoc/
- OpenAPI Schema: http://localhost:8000/api/schema/

## 🏗️ Architecture

### Backend Structure
```
api/
├── models.py          # Database models with custom managers
├── managers.py        # Custom querysets and managers
├── serializers.py     # DRF serializers
├── views.py           # ViewSets with advanced patterns
├── services.py        # Business logic layer
├── urls.py            # URL routing
└── tests/             # Comprehensive test suite
    ├── test_models.py
    ├── test_managers.py
    └── test_views.py
```

### Frontend Structure
```
frontend/src/
├── stores/            # Pinia stores
│   └── items.js
├── composables/       # Reusable composition functions
│   ├── useDebounce.js
│   ├── useErrorHandler.js
│   └── useLoading.js
├── components/        # Vue components
├── pages/             # Route pages
├── router/            # Vue Router configuration
└── api.js             # API service layer
```

## 🔥 Hot Reload & Development Workflow

### How Hot Reload Works

**Frontend (Vite Dev Server):**
- Files in `frontend/src/` are watched automatically
- Changes are detected via polling (configured for Docker)
- Browser automatically refreshes when files change
- No container restart needed for code changes

**Backend (Django runserver):**
- Python files are watched automatically
- Django auto-reloads when `.py` files change
- No container restart needed for code changes

### When to Restart Containers

You only need to restart containers for:
- ✅ Installing new Python packages (`requirements.txt`)
- ✅ Installing new npm packages (`package.json`)
- ✅ Changes to Docker configuration (`Dockerfile`, `docker-compose.yml`)
- ✅ Changes to environment variables in `docker-compose.yml`

You **don't need** to restart for:
- ❌ Changes to Vue components (`frontend/src/**/*.vue`)
- ❌ Changes to Python code (`api/**/*.py`, `crudapp/**/*.py`)
- ❌ Changes to CSS/JavaScript files
- ❌ Changes to templates or static files

### Quick Commands

```bash
# Start development environment
docker compose up -d backend frontend-dev redis

# Check status
docker compose ps

# View logs (follow mode)
docker compose logs -f frontend-dev
docker compose logs -f backend

# Restart a service (if needed)
docker compose restart backend
docker compose restart frontend-dev

# Stop everything
docker compose down
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
REDIS_HOST=localhost
REDIS_PORT=6379
```

### Caching
The application uses Redis for caching. If Redis is not available, it falls back to local memory cache.

## 📝 Code Quality

### Pre-commit Hooks
```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### Code Formatting
```bash
# Format Python code
black .
isort .

# Format frontend code
cd frontend
npm run format
```

## 🚢 Deployment

### Production Checklist
- [ ] Set `DEBUG=False` in production
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Use environment variables for secrets
- [ ] Set up proper database (PostgreSQL recommended)
- [ ] Configure Redis for caching
- [ ] Set up static file serving
- [ ] Configure SSL/TLS
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Gabriel Vicu**
- GitHub: [@gabivicu](https://github.com/gabivicu)

## 🙏 Acknowledgments

- Django REST Framework
- Vue.js
- Pinia
- drf-spectacular
- All contributors and open-source libraries used
