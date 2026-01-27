#!/usr/bin/env python
"""
Script pentru generarea a 100 de item-uri diverse în baza de date.
Item-uri din diferite domenii și cu diferite priorități.
"""
import os
import sys
import django
from datetime import datetime, timedelta
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crudapp.settings')
django.setup()

from api.models import Item
from django.utils import timezone

# Lista de item-uri diverse din diferite domenii
ITEMS_DATA = [
    # WORK - High Priority
    {"title": "Finalizează raportul trimestrial", "category": "work", "priority": "high", "description": "Pregătește prezentarea pentru board meeting"},
    {"title": "Code review pentru feature nou", "category": "work", "priority": "high", "description": "Review PR-ul pentru autentificare"},
    {"title": "Deploy în producție", "category": "work", "priority": "urgent", "description": "Deploy versiunea 2.0"},
    {"title": "Meeting cu echipa", "category": "work", "priority": "medium", "description": "Sprint planning pentru săptămâna viitoare"},
    {"title": "Actualizează documentația API", "category": "work", "priority": "medium", "description": "Adaugă exemple pentru noile endpoint-uri"},
    {"title": "Optimizează query-urile bazei de date", "category": "work", "priority": "high", "description": "Redu timpul de răspuns"},
    {"title": "Scrie teste pentru modul nou", "category": "work", "priority": "medium", "description": "Unit tests și integration tests"},
    {"title": "Configurare CI/CD pipeline", "category": "work", "priority": "high", "description": "Setup GitHub Actions"},
    {"title": "Refactor cod legacy", "category": "work", "priority": "low", "description": "Îmbunătățește cod vechi"},
    {"title": "Prezentare pentru client", "category": "work", "priority": "urgent", "description": "Demo pentru noul feature"},
    
    # PERSONAL - Mixed Priorities
    {"title": "Planifică vacanța de vară", "category": "personal", "priority": "medium", "description": "Caută destinații și rezervări"},
    {"title": "Organizează biblioteca", "category": "personal", "priority": "low", "description": "Sortează cărțile pe categorii"},
    {"title": "Învață un instrument nou", "category": "personal", "priority": "low", "description": "Începe lecții de chitară"},
    {"title": "Scrie în jurnal", "category": "personal", "priority": "low", "description": "Reflecții zilnice"},
    {"title": "Organizează fotografii", "category": "personal", "priority": "low", "description": "Backup și organizare"},
    {"title": "Pregătește cadou pentru ziua de naștere", "category": "personal", "priority": "high", "description": "Cadou pentru prieten"},
    {"title": "Înscrie-te la curs de limba străină", "category": "personal", "priority": "medium", "description": "Curs de spaniolă"},
    {"title": "Citește cartea recomandată", "category": "personal", "priority": "low", "description": "Clean Code - Robert Martin"},
    {"title": "Planifică petrecerea", "category": "personal", "priority": "medium", "description": "Organizează party-ul de aniversare"},
    {"title": "Actualizează CV-ul", "category": "personal", "priority": "medium", "description": "Adaugă proiecte recente"},
    
    # SHOPPING - Various
    {"title": "Cumpără ingrediente pentru rețetă", "category": "shopping", "priority": "medium", "description": "Pentru tortul de ciocolată"},
    {"title": "Cumpără cadouri de Crăciun", "category": "shopping", "priority": "high", "description": "Lista de cadouri pentru familie"},
    {"title": "Cumpără haine noi", "category": "shopping", "priority": "low", "description": "Pantaloni și tricouri"},
    {"title": "Cumpără echipament sportiv", "category": "shopping", "priority": "medium", "description": "Adidași și echipament pentru sală"},
    {"title": "Cumpără produse de curățenie", "category": "shopping", "priority": "medium", "description": "Detergent, hârtie igienică"},
    {"title": "Cumpără cadou de nuntă", "category": "shopping", "priority": "high", "description": "Cadou pentru prieteni"},
    {"title": "Cumpără electronice", "category": "shopping", "priority": "low", "description": "Mouse și tastatură wireless"},
    {"title": "Cumpără cărți", "category": "shopping", "priority": "low", "description": "Cărți tehnice și ficțiune"},
    {"title": "Cumpără plante pentru casă", "category": "shopping", "priority": "low", "description": "Plante decorative"},
    {"title": "Cumpără accesorii auto", "category": "shopping", "priority": "low", "description": "Covorașe și accesorii"},
    
    # HEALTH - Important
    {"title": "Programează consultație medicală", "category": "health", "priority": "high", "description": "Control de rutină"},
    {"title": "Ia medicamentele", "category": "health", "priority": "urgent", "description": "Nu uita tratamentul zilnic"},
    {"title": "Fă analize de sânge", "category": "health", "priority": "high", "description": "Programează la laborator"},
    {"title": "Merge la sală", "category": "health", "priority": "medium", "description": "Antrenament de 3 ori pe săptămână"},
    {"title": "Planifică mesele sănătoase", "category": "health", "priority": "medium", "description": "Meal prep pentru săptămână"},
    {"title": "Bea apă suficientă", "category": "health", "priority": "medium", "description": "2 litri pe zi"},
    {"title": "Meditație zilnică", "category": "health", "priority": "low", "description": "10 minute dimineața"},
    {"title": "Verifică tensiunea arterială", "category": "health", "priority": "medium", "description": "Măsurători săptămânale"},
    {"title": "Programează consultație dentist", "category": "health", "priority": "medium", "description": "Control și curățare"},
    {"title": "Cumpără vitamine", "category": "health", "priority": "low", "description": "Vitamina D și multivitamine"},
    
    # FINANCE - Important
    {"title": "Plătește facturile", "category": "finance", "priority": "urgent", "description": "Electricitate, apă, internet"},
    {"title": "Revizuiește bugetul lunar", "category": "finance", "priority": "high", "description": "Analiză cheltuieli"},
    {"title": "Investește în fonduri mutuale", "category": "finance", "priority": "medium", "description": "Diversifică portofoliul"},
    {"title": "Plătește taxele", "category": "finance", "priority": "urgent", "description": "Termen limită aproape"},
    {"title": "Revizuiește contractul de asigurare", "category": "finance", "priority": "medium", "description": "Verifică acoperirea"},
    {"title": "Creează fond de urgență", "category": "finance", "priority": "high", "description": "6 luni de cheltuieli"},
    {"title": "Plătește cardul de credit", "category": "finance", "priority": "high", "description": "Plată minimă sau integrală"},
    {"title": "Revizuiește investițiile", "category": "finance", "priority": "low", "description": "Analiză performanță"},
    {"title": "Plătește abonamente", "category": "finance", "priority": "medium", "description": "Netflix, Spotify, etc."},
    {"title": "Planifică economii pentru casă", "category": "finance", "priority": "medium", "description": "Fond pentru avans"},
    
    # OTHER - Various
    {"title": "Organizează garajul", "category": "other", "priority": "low", "description": "Curăță și sortează"},
    {"title": "Repară laptop-ul", "category": "other", "priority": "high", "description": "Ecran spart"},
    {"title": "Donează haine vechi", "category": "other", "priority": "low", "description": "Organizează și donează"},
    {"title": "Schimbă bateria la mașină", "category": "other", "priority": "medium", "description": "Programează service"},
    {"title": "Actualizează software-ul", "category": "other", "priority": "low", "description": "Update-uri de securitate"},
    {"title": "Backup date importante", "category": "other", "priority": "high", "description": "Backup în cloud"},
    {"title": "Organizează email-urile", "category": "other", "priority": "low", "description": "Arhivează vechile"},
    {"title": "Repară robinetul", "category": "other", "priority": "medium", "description": "Scurgeri de apă"},
    {"title": "Schimbă filtrele de aer", "category": "other", "priority": "low", "description": "Pentru AC"},
    {"title": "Organizează documentele", "category": "other", "priority": "low", "description": "Sortează și arhivează"},
]

# Tag-uri diverse
TAGS_POOL = [
    "urgent", "important", "personal", "work", "shopping", "health", "finance",
    "weekend", "monthly", "yearly", "recurring", "one-time", "project",
    "family", "friends", "self-care", "maintenance", "upgrade", "review",
    "planning", "execution", "follow-up", "reminder", "deadline"
]

def generate_items(count=100):
    """Generează item-uri diverse în baza de date."""
    
    print(f"🚀 Generare {count} item-uri...")
    print("=" * 60)
    
    created_count = 0
    
    # Generează item-uri din lista predefinită și variante
    for i in range(count):
        # Folosește item-uri din listă sau generează variante
        if i < len(ITEMS_DATA):
            item_data = ITEMS_DATA[i].copy()
        else:
            # Generează variante pentru item-urile rămase
            base_item = random.choice(ITEMS_DATA)
            item_data = base_item.copy()
            item_data["title"] = f"{base_item['title']} #{i+1}"
        
        # Adaugă variabilitate
        # Due date aleatoriu (unele în trecut, unele în viitor)
        days_offset = random.randint(-30, 60)
        due_date = timezone.now() + timedelta(days=days_offset) if random.random() > 0.3 else None
        
        # Completed status (30% completed)
        completed = random.random() < 0.3
        
        # Tags aleatorii (1-3 tag-uri)
        num_tags = random.randint(1, 3)
        tags = random.sample(TAGS_POOL, num_tags)
        
        # Creează item-ul
        item = Item.objects.create(
            title=item_data["title"],
            description=item_data.get("description", ""),
            category=item_data["category"],
            priority=item_data["priority"],
            completed=completed,
            due_date=due_date,
            tags=", ".join(tags)
        )
        
        created_count += 1
        
        if created_count % 10 == 0:
            print(f"✅ Creat {created_count}/{count} item-uri...")
    
    print("=" * 60)
    print(f"✅ Gata! {created_count} item-uri create cu succes!")
    print()
    
    # Statistici
    total = Item.objects.count()
    completed = Item.objects.filter(completed=True).count()
    pending = Item.objects.filter(completed=False).count()
    
    print("📊 Statistici:")
    print(f"   Total item-uri: {total}")
    print(f"   ✅ Completed: {completed}")
    print(f"   ⏳ Pending: {pending}")
    print()
    
    # Statistici pe categorii
    print("📁 Pe categorii:")
    for cat_code, cat_name in Item.CATEGORY_CHOICES:
        count = Item.objects.filter(category=cat_code).count()
        if count > 0:
            print(f"   {cat_name}: {count}")
    print()
    
    # Statistici pe priorități
    print("⚡ Pe priorități:")
    for prio_code, prio_name in Item.PRIORITY_CHOICES:
        count = Item.objects.filter(priority=prio_code).count()
        if count > 0:
            print(f"   {prio_name}: {count}")
    print()

if __name__ == '__main__':
    try:
        # Verifică dacă există deja item-uri
        existing_count = Item.objects.count()
        if existing_count > 0:
            response = input(f"⚠️  Există deja {existing_count} item-uri. Vrei să continui? (y/n): ")
            if response.lower() != 'y':
                print("❌ Anulat.")
                sys.exit(0)
        
        generate_items(100)
        
    except KeyboardInterrupt:
        print("\n❌ Anulat de utilizator.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Eroare: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
