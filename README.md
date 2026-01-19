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
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/api/schema/swagger-ui/
   - Admin Panel: http://localhost:8000/admin

### Docker Setup

```bash
# Build and run all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

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
