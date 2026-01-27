# Pre-commit Hooks Setup

Acest proiect folosește **pre-commit hooks** pentru a asigura calitatea codului înainte de commit.

## Instalare

### 1. Instalează pre-commit

```bash
pip install pre-commit
```

Sau folosește scriptul automatizat:

```bash
chmod +x .pre-commit-install.sh
./.pre-commit-install.sh
```

### 2. Instalează dependențele frontend

```bash
cd frontend
npm install
```

### 3. Instalează hooks-urile Git

```bash
pre-commit install
```

## Verificări Configurate

### Backend (Python)

- **Black** - Formatare automată a codului Python
- **isort** - Sortare automată a import-urilor
- **flake8** - Linting Python cu verificări de stil
- **Trailing whitespace** - Elimină spații la sfârșitul liniilor
- **End of file fixer** - Adaugă newline la sfârșitul fișierelor

### Frontend (JavaScript/Vue)

- **ESLint** - Linting JavaScript/Vue cu fixare automată
- **Prettier** - Formatare automată pentru JS, Vue, CSS, JSON, Markdown

## Utilizare

### Rulare automată

Hooks-urile rulează automat la fiecare `git commit`. Dacă găsesc probleme, commit-ul va fi blocat până când sunt rezolvate.

### Rulare manuală

Pentru a rula toate verificările manual:

```bash
# Toate fișierele
pre-commit run --all-files

# Doar fișierele staged
pre-commit run

# Hook specific
pre-commit run black --all-files
pre-commit run eslint --all-files
```

### Rulare manuală pentru frontend

```bash
cd frontend

# Linting
npm run lint

# Formatare
npm run format

# Verificare formatare (fără modificare)
npm run format:check
```

### Rulare manuală pentru backend

```bash
# Formatare cu Black
black .

# Sortare import-uri cu isort
isort .

# Linting cu flake8
flake8 .

# Verificare tipuri cu mypy (opțional)
mypy .
```

## Bypass (Nu recomandat!)

Dacă trebuie să faci un commit urgent fără verificări (NU recomandat):

```bash
git commit --no-verify -m "your message"
```

## Actualizare Hooks

Pentru a actualiza hooks-urile la versiunile cele mai noi:

```bash
pre-commit autoupdate
```

## Configurare

- `.pre-commit-config.yaml` - Configurația principală pentru pre-commit
- `.flake8` - Configurație flake8 pentru Python
- `pyproject.toml` - Configurație Black, isort, mypy
- `frontend/.eslintrc.cjs` - Configurație ESLint
- `frontend/.prettierrc` - Configurație Prettier

## Troubleshooting

### Eroare: "pre-commit: command not found"

Instalează pre-commit:
```bash
pip install pre-commit
```

### Eroare: "ESLint not found"

Instalează dependențele frontend:
```bash
cd frontend && npm install
```

### Hooks nu rulează

Verifică dacă sunt instalate:
```bash
pre-commit install
```

### Vrei să skip un hook specific

Editează `.pre-commit-config.yaml` și comentează hook-ul respectiv.

## Best Practices

1. **Nu bypass hooks-urile** - Ele există pentru a menține calitatea codului
2. **Rezolvă problemele înainte de commit** - Folosește `pre-commit run --all-files`
3. **Actualizează hooks-urile periodic** - `pre-commit autoupdate`
4. **Comunică cu echipa** - Dacă un hook cauzează probleme, discută soluții
