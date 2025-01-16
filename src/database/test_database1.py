import sys
sys.path.append('src')  # dodaj ścieżkę do src jeśli potrzebne
from database import DatabaseManager
from datetime import datetime

def test_database():
    print("Rozpoczynam testy DatabaseManager...")
    
    # Inicjalizacja managera
    db = DatabaseManager("mirai.db")
    
    try:
        with db:
            print("\n1. Test pobierania kategorii:")
            categories = db.get_all_categories()
            print(f"Znaleziono {len(categories)} kategorii:")
            for category in categories:
                print(f"- {category['name']} (ID: {category['id']})")

            if len(categories) > 0:
                test_category_id = categories[0]['id']
                
                print("\n2. Test dodawania zadania:")
                task_title = "Testowe zadanie"
                task_id = db.add_task(
                    title=task_title,
                    category_id=test_category_id,
                    description="Opis testowego zadania",
                    deadline="2024-12-31"
                )
                print(f"Dodano zadanie z ID: {task_id}")

                print("\n3. Test pobierania zadań dla kategorii:")
                tasks = db.get_tasks_by_category(test_category_id)
                print(f"Zadania w kategorii {categories[0]['name']}:")
                for task in tasks:
                    print(f"- {task['title']} (Status: {task['status']})")

                print("\n4. Test dodawania celu SMART:")
                smart_id = db.add_smart_goal(
                    task_id=task_id,
                    specific="Test specific",
                    measurable="Test measurable",
                    achievable="Test achievable",
                    relevant="Test relevant",
                    time_bound="Test time bound"
                )
                print(f"Dodano cel SMART z ID: {smart_id}")

                print("\n5. Test pobierania celu SMART:")
                smart_goal = db.get_smart_goal(task_id)
                if smart_goal:
                    print("Szczegóły celu SMART:")
                    for key, value in smart_goal.items():
                        print(f"- {key}: {value}")

                print("\n6. Test aktualizacji statusu zadania:")
                success = db.update_task_status(task_id, "completed")
                print(f"Aktualizacja statusu: {'udana' if success else 'nieudana'}")

                print("\n7. Test koła balansu:")
                for category in categories[:3]:  # Test dla pierwszych trzech kategorii
                    db.update_balance_score(category['id'], score=8)
                
                scores = db.get_balance_scores()
                print("Wyniki koła balansu:")
                for score in scores:
                    print(f"- {score['category']}: {score['score']}")

                print("\n8. Test pobierania losowego cytatu:")
                quote = db.get_random_quote()
                if quote:
                    print(f"Cytat: {quote['text']}")
                    print(f"Autor: {quote['author']}")

                print("\n9. Test usuwania zadania:")
                success = db.delete_task(task_id)
                print(f"Usunięcie zadania: {'udane' if success else 'nieudane'}")

            else:
                print("Błąd: Brak kategorii w bazie danych!")

    except Exception as e:
        print(f"\nBŁĄD: {str(e)}")
    
    print("\nTesty zakończone!")

if __name__ == "__main__":
    test_database()