# Django Middleware Documentation

Această aplicație demonstrează utilizarea middleware-urilor Django, inclusiv middleware-uri built-in și custom, folosind toate metodele standard: `process_request`, `process_view`, `process_response` și `process_exception`.

## Middleware-uri Implementate

### 1. Built-in Django Middleware (Folosite)

Aplicația folosește următoarele middleware-uri built-in Django:

- **SecurityMiddleware** - Adaugă headere de securitate
- **SessionMiddleware** - Gestionează sesiunile
- **CorsMiddleware** (django-cors-headers) - Gestionează CORS pentru API
- **CommonMiddleware** - Funcționalități comune (redirect-uri, etc.)
- **CsrfViewMiddleware** - Protecție CSRF
- **AuthenticationMiddleware** - Autentificare utilizatori
- **MessageMiddleware** - Mesaje pentru utilizatori
- **XFrameOptionsMiddleware** - Protecție clickjacking

### 2. Custom Middleware (Create)

#### 2.1. RequestTimingMiddleware
**Metode folosite:** `process_request`, `process_response`

**Funcționalitate:**
- Măsoară timpul de procesare al fiecărui request
- Adaugă header `X-Process-Time` în response
- Loghează durata fiecărui request

**Exemplu:**
```python
def process_request(self, request):
    request.start_time = time.time()
    return None  # Continuă procesarea

def process_response(self, request, response):
    duration = time.time() - request.start_time
    response['X-Process-Time'] = f"{duration:.3f}"
    return response
```

#### 2.2. RateLimitingMiddleware
**Metode folosite:** `process_request`

**Funcționalitate:**
- Implementează rate limiting simplu (100 request-uri/minut per IP)
- Blochează request-urile care depășesc limita
- Returnează răspuns 429 (Too Many Requests) pentru request-uri blocate

**Exemplu:**
```python
def process_request(self, request):
    if request_count >= 100:
        return JsonResponse({'error': 'Rate limit exceeded'}, status=429)
    return None  # Continuă procesarea
```

#### 2.3. RequestLoggingMiddleware
**Metode folosite:** `process_view`, `process_response`

**Funcționalitate:**
- Loghează informații despre view-ul apelat
- Adaugă numele view-ului în header-ul response-ului
- Demonstrează utilizarea `process_view` pentru interceptarea apelurilor de view

**Exemplu:**
```python
def process_view(self, request, view_func, view_args, view_kwargs):
    view_name = view_func.__name__
    logger.info(f"View called: {view_name}")
    request.view_name = view_name
    return None

def process_response(self, request, response):
    response['X-View-Name'] = request.view_name
    return response
```

#### 2.4. SecurityHeadersMiddleware
**Metode folosite:** `process_response`

**Funcționalitate:**
- Adaugă headere de securitate la toate response-urile
- Include headere CORS pentru request-uri API
- Demonstrează modificarea response-urilor

**Exemplu:**
```python
def process_response(self, request, response):
    response['X-Content-Type-Options'] = 'nosniff'
    response['X-Frame-Options'] = 'DENY'
    response['X-XSS-Protection'] = '1; mode=block'
    return response
```

#### 2.5. APIErrorHandlingMiddleware
**Metode folosite:** `process_exception`

**Funcționalitate:**
- Interceptează excepțiile pentru request-uri API
- Returnează răspunsuri JSON pentru erori API
- Loghează erorile pentru debugging

**Exemplu:**
```python
def process_exception(self, request, exception):
    if request.path.startswith('/api/'):
        return JsonResponse({
            'error': 'An internal server error occurred.'
        }, status=500)
    return None  # Lasă Django să gestioneze eroarea normal
```

## Ordinea Middleware-urilor

Ordinea middleware-urilor în `settings.py` este importantă:

1. **SecurityMiddleware** - Primul, pentru headere de securitate
2. **SessionMiddleware** - Gestionează sesiunile
3. **CorsMiddleware** - Gestionează CORS
4. **CommonMiddleware** - Funcționalități comune
5. **RequestTimingMiddleware** - Măsoară timpul (custom)
6. **RateLimitingMiddleware** - Rate limiting (custom)
7. **CsrfViewMiddleware** - Protecție CSRF
8. **AuthenticationMiddleware** - Autentificare
9. **RequestLoggingMiddleware** - Logging view-uri (custom)
10. **MessageMiddleware** - Mesaje
11. **XFrameOptionsMiddleware** - Protecție clickjacking
12. **SecurityHeadersMiddleware** - Headere securitate (custom)
13. **APIErrorHandlingMiddleware** - Ultimul, pentru a intercepta toate excepțiile

## Metode Middleware Standard

### process_request(request)
- Apelat înainte ca Django să determine view-ul
- Poate returna `None` (continuă) sau `HttpResponse` (oprește procesarea)
- Folosit pentru: autentificare, rate limiting, logging

### process_view(request, view_func, view_args, view_kwargs)
- Apelat înainte ca Django să apeleze view-ul
- Primește funcția view și argumentele sale
- Poate returna `None` (continuă) sau `HttpResponse` (oprește)
- Folosit pentru: logging detaliat, modificare argumente view

### process_response(request, response)
- Apelat după ce view-ul returnează un response
- Primește request-ul și response-ul
- Trebuie să returneze un `HttpResponse`
- Folosit pentru: modificare headere, logging, timing

### process_exception(request, exception)
- Apelat doar dacă view-ul aruncă o excepție
- Poate returna `None` (lasă Django să gestioneze) sau `HttpResponse`
- Folosit pentru: error handling personalizat, logging erori

## Testare Middleware-uri

### Testare RequestTimingMiddleware
```bash
curl -I http://localhost:8000/api/items/
# Verifică header-ul X-Process-Time în response
```

### Testare RateLimitingMiddleware
```bash
# Fă 101 request-uri rapide
for i in {1..101}; do curl http://localhost:8000/api/items/; done
# Al 101-lea request ar trebui să returneze 429
```

### Testare RequestLoggingMiddleware
```bash
# Verifică log-urile în consolă pentru informații despre view-uri
# Verifică header-ul X-View-Name în response
```

### Testare SecurityHeadersMiddleware
```bash
curl -I http://localhost:8000/api/items/
# Verifică headerele de securitate în response
```

### Testare APIErrorHandlingMiddleware
```bash
# Generează o eroare în API (de exemplu, accesează un endpoint inexistent)
curl http://localhost:8000/api/items/999999/
# Ar trebui să returneze un JSON cu eroare în loc de HTML
```

## Configurare Logging

Logging-ul este configurat în `settings.py` pentru a afișa informații despre middleware-uri în consolă.

## Note Importante

1. **Ordinea middleware-urilor contează** - Middleware-urile sunt procesate în ordinea din `MIDDLEWARE`
2. **Return None** - Pentru a continua procesarea normală
3. **Return HttpResponse** - Pentru a opri procesarea și a returna un răspuns
4. **process_exception** - Este apelat doar pentru excepții neprinse
5. **Performance** - Middleware-urile rulează la fiecare request, deci trebuie să fie eficiente

## Referințe

- [Django Middleware Documentation](https://docs.djangoproject.com/en/4.2/topics/http/middleware/)
- [Writing Custom Middleware](https://docs.djangoproject.com/en/4.2/topics/http/middleware/#writing-your-own-middleware)


