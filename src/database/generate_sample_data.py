import sqlite3
import random
from datetime import datetime, timedelta
from database import DatabaseManager

def generate_sample_data():
    print("Generowanie przykładowych danych...")
    db = DatabaseManager()

    # Przykładowe zadania dla każdej kategorii
    sample_tasks = [
        # Kariera
        ["Zaktualizować CV", "Napisać list motywacyjny", "Przygotować się do rozmowy kwalifikacyjnej",
         "Ukończyć kurs Python", "Wziąć udział w konferencji IT"],
        # Finanse
        ["Stworzyć budżet miesięczny", "Założyć konto oszczędnościowe", "Przeanalizować wydatki",
         "Zaplanować inwestycje", "Odłożyć 10% wypłaty"],
        # Rozwój osobisty
        ["Przeczytać książkę o produktywności", "Nauczyć się nowego języka", "Medytować codziennie",
         "Zapisać się na warsztaty", "Prowadzić dziennik"],
        # Zdrowie
        ["Ćwiczyć 3 razy w tygodniu", "Pić 2L wody dziennie", "Jeść więcej warzyw",
         "Chodzić na basen", "Regularnie się wysypiać"],
        # Rodzina
        ["Zorganizować rodzinny obiad", "Zaplanować weekend z dziećmi", "Zadzwonić do rodziców",
         "Pomóc bratu w przeprowadzce", "Spotkanie rodzinne"],
        # Związki
        ["Zaplanować randkę", "Kupić prezent dla partnera", "Wspólny wyjazd weekendowy",
         "Zapisać się na taniec", "Wspólne gotowanie"],
        # Odpoczynek
        ["Przeczytać nową książkę", "Obejrzeć film", "Spacer w parku",
         "Spotkanie z przyjaciółmi", "Relaksująca kąpiel"],
        # Duchowość
        ["Medytacja poranna", "Zapisać się na yogę", "Czytanie o filozofii",
         "Praktyka wdzięczności", "Spacer kontemplacyjny"]
    ]

    # Przykładowe cele SMART
    smart_goals = [
        {
            'title': 'Awans na stanowisko senior developera',
            'category_id': 1,  # Kariera
            'specific': 'Uzyskać awans na stanowisko senior developera poprzez rozwój umiejętności technicznych',
            'measurable': 'Ukończenie 3 certyfikacji i prowadzenie 2 projektów',
            'achievable': 'Posiadam już 3 lata doświadczenia i wsparcie przełożonego',
            'relevant': 'Awans pozwoli mi rozwijać się zawodowo i zwiększyć zarobki',
            'time_bound': '1 rok',
            'subgoals': [
                {'title': 'Uzyskać certyfikat AWS', 'completed': False},
                {'title': 'Prowadzić mentoring juniorów', 'completed': False},
                {'title': 'Ukończyć kurs architektury', 'completed': False}
            ]
        },
        {
            'title': 'Zgromadzenie funduszu awaryjnego',
            'category_id': 2,  # Finanse
            'specific': 'Utworzenie funduszu awaryjnego w wysokości 6-miesięcznych wydatków',
            'measurable': 'Zgromadzić 30,000 PLN na koncie oszczędnościowym',
            'achievable': 'Możliwość odkładania 20% miesięcznych dochodów',
            'relevant': 'Zabezpieczenie finansowe jest kluczowe dla stabilności',
            'time_bound': '6 miesięcy',
            'subgoals': [
                {'title': 'Utworzyć osobne konto', 'completed': True},
                {'title': 'Ustawić automatyczne przelewy', 'completed': False},
                {'title': 'Przeanalizować możliwości oszczędzania', 'completed': False}
            ]
        },
        {
            'title': 'Maraton za rok',
            'category_id': 4,  # Zdrowie
            'specific': 'Przebiec maraton w czasie poniżej 4 godzin',
            'measurable': 'Treningi 4 razy w tygodniu, stopniowe zwiększanie dystansu',
            'achievable': 'Już biegam półmaratony, mam doświadczenie',
            'relevant': 'Poprawa kondycji i spełnienie sportowego marzenia',
            'time_bound': '1 rok',
            'subgoals': [
                {'title': 'Ukończenie planu treningowego', 'completed': False},
                {'title': 'Udział w zawodach przygotowawczych', 'completed': False},
                {'title': 'Konsultacja z trenerem', 'completed': True}
            ]
        }
    ]

    # Statusy zadań
    statuses = ['active', 'completed', 'in_progress']
    periods = ['5-10 lat', '1 rok', '6 miesięcy', '3 miesiące', '1 miesiąc']

    with db:
        # Pobierz wszystkie kategorie
        categories = db.get_all_categories()
        
        # Dodaj przykładowe cele SMART
        for goal in smart_goals:
            db.add_smart_goal(goal)
        
        # Dla każdej kategorii
        for idx, category in enumerate(categories):
            # Dodaj 3-5 losowych zadań
            num_tasks = random.randint(3, 5)
            category_tasks = sample_tasks[idx]
            
            for _ in range(num_tasks):
                # Losowe dane dla zadania
                task_name = random.choice(category_tasks)
                status = random.choice(statuses)
                days_offset = random.randint(1, 30)
                deadline = (datetime.now() + timedelta(days=days_offset)).strftime('%Y-%m-%d')
                period = random.choice(periods)
                
                # Dodaj zadanie
                task_data = {
                    'title': task_name,
                    'category_id': category['id'],
                    'specific': f'Konkretny cel: {task_name}',
                    'measurable': 'Postęp mierzony w procentach wykonania',
                    'achievable': 'Cel jest realny do osiągnięcia',
                    'relevant': 'Zadanie wspiera moje cele długoterminowe',
                    'time_bound': period,
                    'subgoals': [
                        {'title': f'Podcel 1 dla {task_name}', 'completed': False},
                        {'title': f'Podcel 2 dla {task_name}', 'completed': False}
                    ]
                }
                
                # 30% szans na dodanie jako cel SMART
                if random.random() < 0.3:
                    db.add_smart_goal(task_data)

                # Dla niektórych zadań dodaj ocenę w kole balansu
                if random.random() < 0.5:  # 50% szans na dodanie oceny
                    score = random.randint(1, 10)
                    db.update_balance_score(
                        category_id=category['id'],
                        score=score,
                        date=datetime.now().strftime('%Y-%m-%d')
                    )

    print("Przykładowe dane zostały wygenerowane!")

if __name__ == "__main__":
    generate_sample_data()