# Migration Guide - New Features

## Step 1: Create and Run Migrations

After adding the new fields to the Item model, you need to create and run migrations:

```bash
# Activate your virtual environment first
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

## Step 2: Restart Django Server

After running migrations, restart your Django development server:

```bash
python manage.py runserver
```

## New Features Added

### Backend Features:
1. **New Model Fields:**
   - `category` - Work, Personal, Shopping, Health, Finance, Other
   - `priority` - Low, Medium, High, Urgent
   - `due_date` - DateTime field for deadlines
   - `tags` - Comma-separated tags

2. **Enhanced API:**
   - Search functionality (title, description, tags)
   - Filter by category, priority, completion status, due date
   - Sorting options
   - Statistics endpoint (`/api/items/stats/`)

### Frontend Features:
1. **Dashboard** - View statistics and charts
2. **Search & Filters** - Search and filter items by multiple criteria
3. **Categories & Priority** - Visual badges and filtering
4. **Due Dates** - Set deadlines with overdue highlighting
5. **Tags** - Add tags to items
6. **Bulk Operations** - Select multiple items and perform actions
7. **Dark Mode** - Toggle between light and dark themes
8. **Export** - Export items as JSON or CSV
9. **Sorting** - Sort by date, priority, title, etc.

## Troubleshooting

If you encounter errors:

1. **Migration errors:** Make sure you've run `makemigrations` and `migrate`
2. **Field errors:** Old items will have default values for new fields
3. **API errors:** Check that Django server is running on port 8000
4. **Frontend errors:** Make sure Vue dev server is running on port 5173

## Testing the New Features

1. Create a new item with category, priority, and due date
2. Use the search bar to find items
3. Filter by category or priority
4. View the dashboard for statistics
5. Select multiple items and use bulk operations
6. Toggle dark mode
7. Export your items

