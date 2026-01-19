# Informații despre Baza de Date

## Tipul Bazei de Date

Aplicația folosește **SQLite** - o bază de date relațională ușoară, perfectă pentru dezvoltare și aplicații mici-medii.

## Locația Bazei de Date

Baza de date este stocată în fișierul:
```
/Users/gvicu/Documents/python-crud-app/db.sqlite3
```

Acest fișier conține toate datele aplicației:
- Toate itemurile create (Item model)
- Tabelele Django (utilizatori, sesiuni, etc.)

## Structura Bazei de Date

### Tabelul `api_item`
Conține toate itemurile create în aplicație cu următoarele coloane:

| Coloană | Tip | Descriere |
|---------|-----|-----------|
| `id` | Integer | ID unic al itemului |
| `title` | String (200) | Titlul itemului |
| `description` | Text | Descrierea itemului |
| `completed` | Boolean | Status completat/pending |
| `category` | String (20) | Categoria (work, personal, etc.) |
| `priority` | String (10) | Prioritatea (low, medium, high, urgent) |
| `due_date` | DateTime | Data limită (poate fi null) |
| `tags` | String (500) | Tag-uri separate prin virgulă |
| `created_at` | DateTime | Data creării |
| `updated_at` | DateTime | Data ultimei actualizări |

## Cum să Vezi Datele

### 1. Django Admin Panel
Cel mai simplu mod de a vedea și gestiona datele:

```bash
# Creează un superuser (dacă nu există)
python manage.py createsuperuser

# Pornește serverul
python manage.py runserver

# Accesează http://localhost:8000/admin/
```

### 2. SQLite Browser (DB Browser for SQLite)
Poți deschide fișierul `db.sqlite3` cu un tool grafic:

1. Descarcă [DB Browser for SQLite](https://sqlitebrowser.org/)
2. Deschide fișierul `db.sqlite3`
3. Vezi și editează datele direct

### 3. Linia de comandă SQLite
```bash
# Deschide baza de date
sqlite3 db.sqlite3

# Vezi toate tabelele
.tables

# Vezi structura tabelului api_item
.schema api_item

# Selectează toate itemurile
SELECT * FROM api_item;

# Ieșire
.quit
```

### 4. Python Shell (Django)
```bash
python manage.py shell
```

```python
from api.models import Item

# Vezi toate itemurile
items = Item.objects.all()
for item in items:
    print(item.title, item.category, item.priority)

# Numără itemurile
Item.objects.count()

# Filtrează după categorie
Item.objects.filter(category='work')

# Filtrează itemurile completate
Item.objects.filter(completed=True)
```

## Backup și Restaurare

### Backup
```bash
# Copiază fișierul bazei de date
cp db.sqlite3 db.sqlite3.backup
```

### Restaurare
```bash
# Restaurează dintr-un backup
cp db.sqlite3.backup db.sqlite3
```

## Migrații

Când schimbi modelele (cum am făcut adăugând câmpuri noi), trebuie să creezi migrații:

```bash
# Creează migrații pentru schimbări
python manage.py makemigrations

# Aplică migrațiile la baza de date
python manage.py migrate
```

Migrațiile existente:
- `0001_initial.py` - Crearea tabelului Item inițial
- `0002_add_new_fields.py` - Adăugarea câmpurilor: category, priority, due_date, tags

## Caracteristici SQLite

✅ **Avantaje:**
- Nu necesită server separat
- Fișier unic, ușor de backup
- Perfect pentru dezvoltare
- Suport complet SQL
- Rapid pentru aplicații mici-medii

⚠️ **Limitări:**
- Nu este ideal pentru aplicații cu mulți utilizatori simultani
- Nu suportă operații concurente complexe
- Pentru producție, consideră PostgreSQL sau MySQL

## Schimbarea Bazei de Date (pentru producție)

Pentru producție, poți schimba la PostgreSQL sau MySQL:

### PostgreSQL
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### MySQL
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydb',
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

## Verificare Stare Baza de Date

```bash
# Verifică migrațiile
python manage.py showmigrations

# Verifică conexiunea la baza de date
python manage.py dbshell
```

## Date de Test

Poți crea date de test folosind Django shell sau admin panel. Datele vor fi persistate în `db.sqlite3` până când le ștergi manual sau resetezi baza de date.

