# Django Vue.js CRUD Application

A full-stack CRUD (Create, Read, Update, Delete) application built with Django REST Framework backend and Vue.js frontend.

## Features

### Core CRUD Operations
- ✅ Create new items
- 📖 Read/List all items
- ✏️ Update existing items
- 🗑️ Delete items
- ✅ Toggle item completion status

### Advanced Features
- 🔍 **Search & Filter** - Search by title/description/tags, filter by category, priority, status, due date
- 📊 **Dashboard** - View statistics, completion rates, and charts
- 🏷️ **Categories & Tags** - Organize items with categories (Work, Personal, Shopping, etc.) and tags
- ⚡ **Priority Levels** - Set priority (Low, Medium, High, Urgent) with visual indicators
- 📅 **Due Dates** - Set deadlines with overdue highlighting
- 📈 **Sorting** - Sort by date, priority, title, etc.
- ☑️ **Bulk Operations** - Select multiple items and perform batch actions
- 🌙 **Dark Mode** - Toggle between light and dark themes
- 📤 **Export** - Export items as JSON or CSV
- 🎨 Modern, responsive UI with smooth animations

## Project Structure

```
python-crud-app/
├── crudapp/          # Django project settings
├── api/              # Django app with models, views, serializers
├── frontend/         # Vue.js frontend application
│   ├── src/
│   │   ├── App.vue   # Main Vue component
│   │   ├── api.js    # API service for backend communication
│   │   ├── main.js   # Vue app entry point
│   │   └── style.css # Styles
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── manage.py
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.8+
- Node.js 16+ and npm
- pip (Python package manager)

## Setup Instructions

### Backend Setup (Django)

1. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run database migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
   
   **Important:** After pulling the latest changes with new features, you must run migrations to add the new database fields (category, priority, due_date, tags).

4. **Create a superuser** (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

5. **Start the Django development server**:
   ```bash
   python manage.py runserver
   ```

   The backend API will be available at `http://localhost:8000`
   - API endpoints: `http://localhost:8000/api/items/`
   - Admin panel: `http://localhost:8000/admin/`

### Frontend Setup (Vue.js)

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Start the Vue.js development server**:
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`

## Usage

1. Make sure both servers are running:
   - Django backend on `http://localhost:8000`
   - Vue.js frontend on `http://localhost:5173`

2. Open your browser and navigate to `http://localhost:5173`

3. You can now:
   - **Create items** with category, priority, due date, and tags
   - **Search** items using the search bar
   - **Filter** by category, priority, status, or due date
   - **Sort** items by various criteria
   - **View Dashboard** for statistics and charts
   - **Select multiple items** for bulk operations
   - **Toggle Dark Mode** for comfortable viewing
   - **Export** your data as JSON or CSV
   - **Edit/Delete** individual items

## API Endpoints

The Django REST Framework provides the following endpoints:

### Basic CRUD
- `GET /api/items/` - List all items (with optional filters)
- `POST /api/items/` - Create a new item
- `GET /api/items/{id}/` - Get a specific item
- `PUT /api/items/{id}/` - Update an item
- `DELETE /api/items/{id}/` - Delete an item

### Advanced Endpoints
- `GET /api/items/stats/` - Get statistics and analytics

### Query Parameters for Filtering

- `?search=keyword` - Search in title, description, or tags
- `?category=work` - Filter by category (work, personal, shopping, health, finance, other)
- `?priority=high` - Filter by priority (low, medium, high, urgent)
- `?completed=true` - Filter by completion status
- `?due_filter=overdue` - Filter by due date (overdue, today, upcoming)
- `?ordering=-created_at` - Sort results (created_at, updated_at, due_date, priority, title)

### Example API Requests

```bash
# Create a new item with all fields
curl -X POST http://localhost:8000/api/items/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Task",
    "description": "Task description",
    "category": "work",
    "priority": "high",
    "due_date": "2024-12-31T23:59:59Z",
    "tags": "urgent, important",
    "completed": false
  }'

# Search items
curl "http://localhost:8000/api/items/?search=meeting"

# Filter by category and priority
curl "http://localhost:8000/api/items/?category=work&priority=high"

# Get statistics
curl "http://localhost:8000/api/items/stats/"
```

## Technologies Used

### Backend
- Django 4.2.7
- Django REST Framework 3.14.0
- django-cors-headers 4.3.1

### Frontend
- Vue.js 3.3.4
- Vite 5.0.0
- Axios 1.6.0

## Development

### Running Tests

Currently, no tests are included. You can add tests using:
- Django's test framework for backend
- Vue Test Utils for frontend

### Building for Production

**Frontend:**
```bash
cd frontend
npm run build
```

The built files will be in `frontend/dist/`

**Backend:**
Follow Django deployment best practices for production deployment.

## Troubleshooting

- **CORS errors**: Make sure `django-cors-headers` is installed and configured in `settings.py`
- **API connection errors**: Verify Django server is running on port 8000
- **Frontend not loading**: Check that Node.js dependencies are installed and Vite dev server is running

## License

This project is open source and available for educational purposes.

