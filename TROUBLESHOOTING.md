# Troubleshooting Guide

## Eroare 500 - Internal Server Error

### Cauze comune și soluții:

#### 1. Dependențe neinstalate
**Symptom:** `ModuleNotFoundError` sau `ImportError`

**Soluție:**
```bash
# Activează virtual environment
source venv/bin/activate  # Linux/Mac
# sau
venv\Scripts\activate  # Windows

# Instalează dependențele
pip install -r requirements.txt
```

#### 2. Migrații neaplicate
**Symptom:** `django.db.utils.OperationalError` sau erori legate de database

**Soluție:**
```bash
# Creează migrații pentru modificările din models
python manage.py makemigrations

# Aplică migrațiile
python manage.py migrate
```

#### 3. Redis Connection Error
**Symptom:** Erori legate de cache sau Redis

**Soluție:**
Aplicația folosește automat fallback la local memory cache dacă Redis nu este disponibil. Dacă vrei să folosești Redis:

```bash
# Instalează și pornește Redis
# macOS (cu Homebrew)
brew install redis
brew services start redis

# Linux
sudo apt-get install redis-server
sudo systemctl start redis

# Sau folosește Docker
docker run -d -p 6379:6379 redis:7-alpine
```

#### 4. drf-spectacular nu este instalat
**Symptom:** Erori legate de `drf_spectacular`

**Soluție:**
Aplicația funcționează și fără drf-spectacular (este opțional). Pentru API documentation:

```bash
pip install drf-spectacular
```

#### 5. Custom Manager Issues
**Symptom:** Erori legate de `ItemManager` sau `ItemQuerySet`

**Soluție:**
Verifică că `api/managers.py` există și este importat corect în `api/models.py`:

```python
# api/models.py
from .managers import ItemManager

class Item(models.Model):
    objects = ItemManager()
    # ...
```

#### 6. Port deja folosit
**Symptom:** `Address already in use`

**Soluție:**
```bash
# Găsește procesul care folosește portul 8000
lsof -ti:8000

# Oprește procesul
kill -9 $(lsof -ti:8000)

# Sau folosește alt port
python manage.py runserver 8001
```

## Verificări rapide

### 1. Verifică configurația Django
```bash
python manage.py check
```

### 2. Verifică migrațiile
```bash
python manage.py showmigrations
```

### 3. Verifică dacă serverul rulează
```bash
curl http://localhost:8000/api/items/
```

### 4. Verifică logs-urile
```bash
# În terminalul unde rulează serverul Django
# Vei vedea erorile detaliate în console
```

## Debug Mode

Pentru mai multe detalii despre erori, asigură-te că `DEBUG=True` în `settings.py`:

```python
DEBUG = True
```

**⚠️ ATENȚIE:** Nu folosi `DEBUG=True` în production!

## Logging

Aplicația are logging configurat. Verifică output-ul consolei pentru detalii despre erori.

Pentru logging mai detaliat, modifică nivelul în `settings.py`:

```python
LOGGING = {
    'loggers': {
        'django': {
            'level': 'DEBUG',  # Schimbă din 'INFO' în 'DEBUG'
        },
    },
}
```

## Contact

Dacă problema persistă, verifică:
1. Versiunea Python (trebuie să fie 3.11+)
2. Versiunea Django (trebuie să fie 4.2+)
3. Logs-urile serverului Django pentru eroarea exactă
