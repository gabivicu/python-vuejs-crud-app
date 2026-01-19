# Django Routing - Ghid pentru dezvoltatori Laravel

## Comparație Laravel vs Django

### Laravel (PHP)
```php
// routes/web.php
Route::get('/items', [ItemController::class, 'index']);
Route::post('/items', [ItemController::class, 'store']);
Route::get('/items/{id}', [ItemController::class, 'show']);
Route::put('/items/{id}', [ItemController::class, 'update']);
Route::delete('/items/{id}', [ItemController::class, 'destroy']);

// Sau cu Resource Controller
Route::resource('items', ItemController::class);
```

### Django (Python)
```python
# urls.py
from django.urls import path
from .views import ItemViewSet

# Opțiunea 1: ViewSet cu Router (similar cu Resource Controller)
router = DefaultRouter()
router.register(r'items', ItemViewSet)
urlpatterns = [
    path('', include(router.urls)),
]

# Opțiunea 2: Path-uri individuale (similar cu Route::get/post)
urlpatterns = [
    path('items/', ItemListView.as_view(), name='item-list'),
    path('items/<int:id>/', ItemDetailView.as_view(), name='item-detail'),
]
```

---

## Structura Routing în Django

### 1. **URL Configuration Principală** (`crudapp/urls.py`)

Aceasta este echivalentul `routes/web.php` sau `routes/api.php` din Laravel.

```python
# crudapp/urls.py
from django.urls import path, include

urlpatterns = [
    path('', api_root, name='api-root'),           # GET /
    path('admin/', admin.site.urls),                # GET /admin/
    path('api/', include('api.urls')),             # Include toate rutele din api.urls
]
```

**Comparație Laravel:**
```php
// Laravel
Route::get('/', [HomeController::class, 'index']);
Route::prefix('api')->group(function () {
    require __DIR__.'/api.php';
});
```

---

### 2. **URL Configuration pentru App** (`api/urls.py`)

Fiecare app Django poate avea propriul fișier `urls.py`, similar cu route groups în Laravel.

```python
# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet

router = DefaultRouter()
router.register(r'items', ItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

**Ce face `router.register()`?**

Când înregistrezi un ViewSet cu router, Django REST Framework generează automat următoarele rute:

| Metodă HTTP | URL Pattern | Action | Echivalent Laravel |
|------------|-------------|--------|-------------------|
| GET | `/api/items/` | list() | `Route::get('/items', 'index')` |
| POST | `/api/items/` | create() | `Route::post('/items', 'store')` |
| GET | `/api/items/{id}/` | retrieve() | `Route::get('/items/{id}', 'show')` |
| PUT | `/api/items/{id}/` | update() | `Route::put('/items/{id}', 'update')` |
| PATCH | `/api/items/{id}/` | partial_update() | `Route::patch('/items/{id}', 'update')` |
| DELETE | `/api/items/{id}/` | destroy() | `Route::delete('/items/{id}', 'destroy')` |

**Comparație Laravel:**
```php
// Laravel Resource Controller
Route::resource('items', ItemController::class);
// Generează aceleași rute automat
```

---

### 3. **ViewSet (Echivalent Controller în Laravel)**

```python
# api/views.py
from rest_framework import viewsets
from .models import Item
from .serializers import ItemSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    
    def get_queryset(self):
        # Logica de filtrare (similar cu query scopes în Laravel)
        queryset = Item.objects.all()
        completed = self.request.query_params.get('completed')
        if completed:
            queryset = queryset.filter(completed=completed.lower() == 'true')
        return queryset
```

**Comparație Laravel:**
```php
// Laravel Controller
class ItemController extends Controller {
    public function index(Request $request) {
        $query = Item::query();
        if ($request->has('completed')) {
            $query->where('completed', $request->completed);
        }
        return $query->get();
    }
}
```

---

## Tipuri de Routing în Django

### 1. **Function-Based Views** (Similar cu Closure Routes în Laravel)

```python
# urls.py
from django.urls import path
from .views import my_view

urlpatterns = [
    path('items/', my_view, name='item-list'),
]

# views.py
from django.http import JsonResponse

def my_view(request):
    return JsonResponse({'message': 'Hello'})
```

**Comparație Laravel:**
```php
Route::get('/items', function () {
    return response()->json(['message' => 'Hello']);
});
```

---

### 2. **Class-Based Views** (Similar cu Controller Methods)

```python
# urls.py
from django.urls import path
from .views import ItemListView

urlpatterns = [
    path('items/', ItemListView.as_view(), name='item-list'),
]

# views.py
from django.views.generic import ListView
from .models import Item

class ItemListView(ListView):
    model = Item
    template_name = 'items/list.html'
```

**Comparație Laravel:**
```php
Route::get('/items', [ItemController::class, 'index']);
```

---

### 3. **ViewSets** (Specific Django REST Framework)

```python
# Cel mai similar cu Laravel Resource Controllers
router.register(r'items', ItemViewSet)
```

---

## Parametri în URL (Route Parameters)

### Django
```python
# urls.py
path('items/<int:id>/', ItemDetailView.as_view()),
path('items/<str:slug>/', ItemDetailView.as_view()),
path('items/<uuid:uuid>/', ItemDetailView.as_view()),

# views.py
def my_view(request, id):
    # id este automat convertit la int
    pass
```

### Laravel
```php
Route::get('/items/{id}', [ItemController::class, 'show']);
Route::get('/items/{slug}', [ItemController::class, 'show']);

public function show($id) {
    // $id este string, trebuie convertit manual dacă e nevoie
}
```

**Tipuri de parametri Django:**
- `<int:id>` - Integer
- `<str:slug>` - String (default)
- `<slug:slug>` - Slug format
- `<uuid:uuid>` - UUID
- `<path:path>` - Path (include /)

---

## Query Parameters

### Django
```python
# În ViewSet
def get_queryset(self):
    search = self.request.query_params.get('search')
    category = self.request.query_params.get('category')
    # sau
    search = self.request.GET.get('search')
```

### Laravel
```php
public function index(Request $request) {
    $search = $request->query('search');
    $category = $request->input('category');
}
```

---

## Custom Actions (Rute Personalizate)

### Django REST Framework
```python
# api/views.py
class ItemViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['get'])
    def stats(self, request):
        # Ruta generată: GET /api/items/stats/
        return Response({'total': 100})
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        # Ruta generată: POST /api/items/{id}/complete/
        item = self.get_object()
        item.completed = True
        item.save()
        return Response({'status': 'completed'})
```

**Comparație Laravel:**
```php
// Laravel
Route::get('/items/stats', [ItemController::class, 'stats']);
Route::post('/items/{id}/complete', [ItemController::class, 'complete']);
```

---

## Middleware vs Middleware

### Django
```python
# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'crudapp.middleware.RequestTimingMiddleware',
]

# middleware.py
class RequestTimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Before request
        start_time = time.time()
        response = self.get_response(request)
        # After request
        return response
```

### Laravel
```php
// Kernel.php
protected $middleware = [
    \App\Http\Middleware\TrustProxies::class,
];

// Middleware
public function handle($request, Closure $next) {
    // Before request
    $response = $next($request);
    // After request
    return $response;
}
```

---

## Naming Routes (Route Names)

### Django
```python
# urls.py
path('items/', ItemListView.as_view(), name='item-list'),

# În template sau cod
from django.urls import reverse
url = reverse('item-list')  # /items/
```

### Laravel
```php
Route::get('/items', [ItemController::class, 'index'])->name('items.index');

route('items.index'); // /items
```

---

## Redirects

### Django
```python
from django.shortcuts import redirect
from django.urls import reverse

def my_view(request):
    return redirect('item-list')
    # sau
    return redirect('/items/')
```

### Laravel
```php
return redirect()->route('items.index');
return redirect('/items');
```

---

## Exemple din Proiectul Tău

### Structura Actuală:

```
crudapp/
  ├── urls.py          # Root URL config (routes/web.php)
  └── api/
      ├── urls.py      # App URL config (route groups)
      └── views.py     # ViewSet (Controller)
```

### Rutele Generate Automat:

```
GET    /api/items/              → ItemViewSet.list()
POST   /api/items/              → ItemViewSet.create()
GET    /api/items/{id}/         → ItemViewSet.retrieve()
PUT    /api/items/{id}/         → ItemViewSet.update()
DELETE /api/items/{id}/         → ItemViewSet.destroy()
GET    /api/items/stats/        → ItemViewSet.stats()  (custom action)
```

---

## Sfaturi pentru Migrarea din Laravel

1. **ViewSet = Resource Controller** - Folosește ViewSet pentru CRUD operations
2. **Serializer = Form Request** - Serializers validează datele (similar cu Form Requests)
3. **Query Parameters** - Folosește `request.query_params` în loc de `$request->input()`
4. **Response** - Folosește `Response()` din DRF în loc de `response()->json()`
5. **Middleware** - Structură similară, dar sintaxă diferită

---

## Resurse Suplimentare

- [Django URL Dispatcher](https://docs.djangoproject.com/en/4.2/topics/http/urls/)
- [Django REST Framework Routers](https://www.django-rest-framework.org/api-guide/routers/)
- [Django REST Framework ViewSets](https://www.django-rest-framework.org/api-guide/viewsets/)

