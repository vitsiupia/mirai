from database import DatabaseManager
from datetime import datetime, timedelta
import random

def generate_enhanced_data():
    db = DatabaseManager()
    
    # Goals for 5 years
    five_year_goals = [
        {
            'title': 'Międzynarodowa Franczyza Restauracji',
            'category_id': 2,  # Finanse
            'specific': 'Otworzyć sieć restauracji w trzech krajach europejskich',
            'measurable': '5 lokali, obrót roczny 5M EUR, zatrudnienie 50 osób',
            'achievable': 'Stopniowy rozwój, pozyskanie inwestorów, wykorzystanie doświadczenia',
            'relevant': 'Rozwój własnego biznesu i niezależność finansowa',
            'time_bound': '5-10 lat',
            'subgoals': [
                {'title': 'Otworzyć pierwszą restaurację w Polsce', 'completed': False},
                {'title': 'Stworzyć model franczyzowy', 'completed': False},
                {'title': 'Pozyskać inwestorów zagranicznych', 'completed': False},
                {'title': 'Rozwinąć markę w mediach społecznościowych', 'completed': False},
                {'title': 'Otworzyć pierwsze lokale za granicą', 'completed': False}
            ]
        },
        {
            'title': 'Osiągnąć harmonię duchową i fizyczną',
            'category_id': 8,  # Duchowość
            'specific': 'Stać się certyfikowanym nauczycielem jogi i medytacji',
            'measurable': '500h praktyki, certyfikacja międzynarodowa, własne studio',
            'achievable': 'Systematyczna praktyka i nauka',
            'relevant': 'Rozwój osobisty i dzielenie się wiedzą z innymi',
            'time_bound': '5-10 lat',
            'subgoals': [
                {'title': 'Ukończyć kurs nauczycielski jogi 200h', 'completed': False},
                {'title': 'Odbyć roczny retreat w Indiach', 'completed': False},
                {'title': 'Otworzyć własne studio jogi', 'completed': False},
                {'title': 'Napisać książkę o duchowości', 'completed': False},
                {'title': 'Zorganizować międzynarodowe warsztaty', 'completed': False}
            ]
        },
        {
            'title': 'Zostać Senior Software Architektem',
            'category_id': 1,  # Kariera
            'specific': 'Awansować na pozycję Senior Software Architekta w dużej firmie technologicznej',
            'measurable': 'Uzyskać 3 certyfikaty cloud, prowadzić 5 dużych projektów, mentorować 10 juniorów',
            'achievable': 'Systematyczny rozwój umiejętności i doświadczenia w architekturze systemów',
            'relevant': 'Rozwój kariery w kierunku architektury systemów',
            'time_bound': '5-10 lat',
            'subgoals': [
                {'title': 'Uzyskać certyfikat AWS Solutions Architect Professional', 'completed': False},
                {'title': 'Uzyskać certyfikat Google Cloud Architect', 'completed': False},
                {'title': 'Poprowadzić projekt mikrousług dla dużego klienta', 'completed': False},
                {'title': 'Stworzyć własny framework architektoniczny', 'completed': False},
                {'title': 'Zostać głównym architektem w projekcie międzynarodowym', 'completed': False}
            ]
        },
        {
            'title': 'Zbudować portfel inwestycyjny 1M PLN',
            'category_id': 2,  # Finanse
            'specific': 'Zbudować zdywersyfikowany portfel inwestycyjny o wartości 1 miliona złotych',
            'measurable': 'Regularne inwestycje, 20% roczny wzrost portfela',
            'achievable': 'Systematyczne oszczędzanie i mądre inwestowanie',
            'relevant': 'Zabezpieczenie finansowe i niezależność',
            'time_bound': '5-10 lat',
            'subgoals': [
                {'title': 'Utworzyć portfel akcji polskich', 'completed': False},
                {'title': 'Zainwestować w ETFy zagraniczne', 'completed': False},
                {'title': 'Kupić pierwszą nieruchomość inwestycyjną', 'completed': False},
                {'title': 'Założyć IKE i IKZE', 'completed': False},
                {'title': 'Stworzyć dodatkowe źródło dochodu pasywnego', 'completed': False}
            ]
        }
    ]
    
    # Yearly goals for 2025
    yearly_goals_2025 = [
        {
            'title': 'Napisać i wydać książkę programistyczną',
            'category_id': 1,  # Kariera
            'specific': 'Napisać i opublikować książkę o architekturze mikroserwisów',
            'measurable': '300 stron, 10 rozdziałów, praktyczne przykłady',
            'achievable': 'Systematyczne pisanie, współpraca z wydawnictwem',
            'relevant': 'Budowanie marki osobistej w branży IT',
            'time_bound': '1 rok',
            'target_month': 'Styczeń 2025',
            'subgoals': [
                {'title': 'Przygotować szczegółowy plan książki', 'completed': False},
                {'title': 'Napisać pierwsze 3 rozdziały', 'completed': False},
                {'title': 'Znaleźć wydawcę', 'completed': False},
                {'title': 'Zebrać recenzje od ekspertów', 'completed': False}
            ]
        },
        {
            'title': 'Osiągnąć poziom B2 w języku hiszpańskim',
            'category_id': 3,  # Rozwój osobisty
            'specific': 'Osiągnąć poziom B2 w języku hiszpańskim i zdać egzamin DELE',
            'measurable': 'Zdany egzamin DELE B2, 1000 słów w słowniczku',
            'achievable': 'Regularne lekcje i praktyka',
            'relevant': 'Rozwój osobisty i możliwości zawodowe',
            'time_bound': '1 rok',
            'target_month': 'Grudzień 2025',
            'subgoals': [
                {'title': 'Zapisać się na kurs hiszpańskiego', 'completed': False},
                {'title': 'Znaleźć partnera do konwersacji', 'completed': False},
                {'title': 'Oglądać seriale po hiszpańsku', 'completed': False}
            ]
        },
        {
            'title': 'Awans na pozycję Tech Leada',
            'category_id': 1,
            'specific': 'Uzyskać awans na stanowisko Tech Lead w obecnej firmie',
            'measurable': 'Prowadzenie 3 projektów, mentoring 5 juniorów, certyfikacja cloud',
            'achievable': 'Regularne poszerzanie kompetencji technicznych i miękkich',
            'relevant': 'Rozwój kariery w kierunku zarządzania zespołem',
            'time_bound': '1 rok',
            'target_month': 'Styczeń 2025',
            'subgoals': [
                {'title': 'Ukończyć kurs zarządzania zespołem IT', 'completed': False},
                {'title': 'Zdobyć certyfikat AWS Developer Associate', 'completed': False},
                {'title': 'Prowadzić cotygodniowe code review', 'completed': False}
            ]
        }
    ]
    
    # 6-month goals
    six_month_goals = [
        {
            'title': 'Remont i organizacja mieszkania',
            'category_id': 7,  # Odpoczynek
            'specific': 'Kompletny remont i reorganizacja mieszkania w stylu minimalistycznym',
            'measurable': 'Remont 3 pokoi, nowe meble, system organizacji',
            'achievable': 'Plan etapowy, budżet 30000 PLN',
            'relevant': 'Poprawa komfortu życia i organizacji',
            'time_bound': '6 miesięcy',
            'target_month': 'Czerwiec 2025',
            'subgoals': [
                {'title': 'Przygotować projekt wnętrz', 'completed': False},
                {'title': 'Znaleźć wykonawców', 'completed': False},
                {'title': 'Kupić nowe meble', 'completed': False},
                {'title': 'Wdrożyć system organizacji', 'completed': False}
            ]
        },
        {
            'title': 'Rozwinąć kanał YouTube o programowaniu',
            'category_id': 1,  # Kariera
            'specific': 'Stworzyć i rozwinąć kanał edukacyjny o programowaniu',
            'measurable': '20 filmów, 1000 subskrybentów',
            'achievable': 'Regularne publikacje, marketing',
            'relevant': 'Budowa marki osobistej i dodatkowy przychód',
            'time_bound': '6 miesięcy',
            'target_month': 'Lipiec 2025',
            'subgoals': [
                {'title': 'Przygotować plan contentu', 'completed': False},
                {'title': 'Nagrać pierwsze 5 filmów', 'completed': False},
                {'title': 'Nauczyć się montażu', 'completed': False}
            ]
        },
        {
            'title': 'Przygotowanie do maratonu',
            'category_id': 4,  # Zdrowie
            'specific': 'Przygotować się do udziału w maratonie warszawskim',
            'measurable': 'Przebiec 42km w czasie poniżej 4:30h',
            'achievable': 'Systematyczny trening według planu',
            'relevant': 'Poprawa kondycji i realizacja sportowego marzenia',
            'time_bound': '6 miesięcy',
            'target_month': 'Czerwiec 2025',
            'subgoals': [
                {'title': 'Ukończyć plan treningowy półmaratonu', 'completed': False},
                {'title': 'Przebiec 30km w treningu', 'completed': False},
                {'title': 'Skonsultować się z fizjoterapeutą', 'completed': False}
            ]
        }
    ]
    
    # 3-month goals
    three_month_goals = [
        {
            'title': 'Wdrożenie diety ketogenicznej',
            'category_id': 4,  # Zdrowie
            'specific': 'Przejść na dietę ketogeniczną i utrzymać ją',
            'measurable': 'Utrata 6 kg, poziom ketonów 1.5-3.0 mmol/L',
            'achievable': 'Stopniowe wprowadzanie zmian',
            'relevant': 'Poprawa zdrowia i energii',
            'time_bound': '3 miesiące',
            'target_month': 'Marzec 2025',
            'subgoals': [
                {'title': 'Konsultacja z dietetykiem', 'completed': False},
                {'title': 'Zakup niezbędnych suplementów', 'completed': False},
                {'title': 'Przygotować plan posiłków', 'completed': False}
            ]
        },
        {
            'title': 'Stworzenie portfela kryptowalut',
            'category_id': 2,  # Finanse
            'specific': 'Zbudować zdywersyfikowany portfel kryptowalut',
            'measurable': 'Inwestycja 10000 PLN w 5 różnych aktywów',
            'achievable': 'Systematyczne zakupy i analiza rynku',
            'relevant': 'Dywersyfikacja inwestycji',
            'time_bound': '3 miesiące',
            'target_month': 'Kwiecień 2025',
            'subgoals': [
                {'title': 'Przeanalizować top 20 kryptowalut', 'completed': False},
                {'title': 'Założyć bezpieczny portfel', 'completed': False},
                {'title': 'Zainwestować w wybrane aktywa', 'completed': False}
            ]
        },
        {
            'title': 'Kurs Full Stack Development',
            'category_id': 1,  # Kariera
            'specific': 'Ukończyć intensywny kurs Full Stack Development',
            'measurable': '12 projektów praktycznych, certyfikat ukończenia',
            'achievable': 'Dedykowane 2h dziennie na naukę',
            'relevant': 'Poszerzenie kompetencji programistycznych',
            'time_bound': '3 miesiące',
            'target_month': 'Marzec 2025',
            'subgoals': [
                {'title': 'Ukończyć moduł Frontend (React)', 'completed': False},
                {'title': 'Ukończyć moduł Backend (Node.js)', 'completed': False},
                {'title': 'Zbudować aplikację fullstack', 'completed': False}
            ]
        }
    ]
    
    # Monthly goals (January 2025)
    january_2025_goals = [
        {
            'title': 'Budżet i oszczędności - nowy rok',
            'category_id': 2,  # Finanse
            'specific': 'Stworzyć szczegółowy budżet na 2025 i zacząć oszczędzać',
            'measurable': 'Zaoszczędzić 2000 PLN, stworzyć arkusz wydatków',
            'achievable': 'Ograniczenie zbędnych wydatków, planowanie zakupów',
            'relevant': 'Poprawa sytuacji finansowej w nowym roku',
            'time_bound': '1 miesiąc',
            'target_month': 'Styczeń 2025',
            'subgoals': [
                {'title': 'Stworzyć szczegółowy arkusz budżetu', 'completed': False},
                {'title': 'Anulować niepotrzebne subskrypcje', 'completed': False},
                {'title': 'Założyć osobne konto oszczędnościowe', 'completed': False}
            ]
        },
        {
            'title': 'Plan rodzinnych aktywności',
            'category_id': 5,  # Rodzina
            'specific': 'Zaplanować i rozpocząć regularne aktywności rodzinne',
            'measurable': '4 wspólne weekendy, 2 wyjścia kulturalne',
            'achievable': 'Organizacja czasu w weekendy',
            'relevant': 'Wzmocnienie więzi rodzinnych',
            'time_bound': '1 miesiąc',
            'target_month': 'Styczeń 2025',
            'subgoals': [
                {'title': 'Stworzyć kalendarz rodzinny', 'completed': False},
                {'title': 'Zaplanować wspólne wyjścia', 'completed': False},
                {'title': 'Zorganizować rodzinny obiad', 'completed': False}
            ]
        },
        {
            'title': 'Zimowy program zdrowotny',
            'category_id': 4,  # Zdrowie
            'specific': 'Wdrożyć kompleksowy program zdrowotny na zimę',
            'measurable': 'Suplementacja witamin, 3 treningi tygodniowo, 8h snu',
            'achievable': 'Stopniowe wprowadzanie nawyków',
            'relevant': 'Wzmocnienie odporności i kondycji',
            'time_bound': '1 miesiąc',
            'target_month': 'Styczeń 2025',
            'subgoals': [
                {'title': 'Konsultacja z lekarzem', 'completed': False},
                {'title': 'Zakup witamin i suplementów', 'completed': False},
                {'title': 'Ustalić harmonogram treningów', 'completed': False}
            ]
        },
        {
            'title': 'Regularne spotkania z rodzicami',
            'category_id': 5,  # Rodzina
            'specific': 'Ustanowić tradycję regularnych spotkań z rodzicami',
            'measurable': 'Minimum 2 spotkania w tygodniu, wspólne obiady',
            'achievable': 'Organizacja czasu w weekendy i wieczory',
            'relevant': 'Wzmocnienie relacji z rodzicami',
            'time_bound': '1 miesiąc',
            'target_month': 'Styczeń 2025',
            'subgoals': [
                {'title': 'Ustalić stałe terminy spotkań', 'completed': False},
                {'title': 'Przygotować listę wspólnych aktywności', 'completed': False},
                {'title': 'Zorganizować wspólne gotowanie', 'completed': False}
            ]
        },
        {
            'title': 'Optymalizacja wydatków stałych',
            'category_id': 2,  # Finanse
            'specific': 'Przeanalizować i zoptymalizować wszystkie wydatki stałe',
            'measurable': 'Redukcja rachunków o 15%, negocjacja umów',
            'achievable': 'Analiza i renegocjacja umów',
            'relevant': 'Zmniejszenie kosztów życia',
            'time_bound': '1 miesiąc',
            'target_month': 'Styczeń 2025',
            'subgoals': [
                {'title': 'Audyt wszystkich rachunków', 'completed': False},
                {'title': 'Porównanie ofert dostawców', 'completed': False},
                {'title': 'Renegocjacja umów z dostawcami', 'completed': False}
            ]
        },
        {
            'title': 'Zdrowe nawyki żywieniowe',
            'category_id': 4,  # Zdrowie
            'specific': 'Wprowadzić zdrowe nawyki żywieniowe na nowy rok',
            'measurable': '5 posiłków dziennie, 2L wody, eliminacja cukru',
            'achievable': 'Stopniowa zmiana nawyków',
            'relevant': 'Poprawa zdrowia i energii',
            'time_bound': '1 miesiąc',
            'target_month': 'Styczeń 2025',
            'subgoals': [
                {'title': 'Przygotować plan posiłków', 'completed': False},
                {'title': 'Zrobić listę zdrowych przekąsek', 'completed': False},
                {'title': 'Kupić butelkę na wodę', 'completed': False}
            ]
        },
        {
            'title': 'Medytacja mindfulness',
            'category_id': 8,  # Duchowość
            'specific': 'Wprowadzić codzienną praktykę medytacji',
            'measurable': '20 minut dziennie, przez 30 dni',
            'achievable': 'Poranne sesje medytacyjne',
            'relevant': 'Redukcja stresu i poprawa koncentracji',
            'time_bound': '1 miesiąc',
            'target_month': 'Styczeń 2025',
            'subgoals': [
                {'title': 'Znaleźć odpowiednią aplikację', 'completed': False},
                {'title': 'Stworzyć kącik do medytacji', 'completed': False},
                {'title': 'Prowadzić dziennik praktyki', 'completed': False}
            ]
        },
        {
            'title': 'Organizacja domowego biura',
            'category_id': 7,  # Odpoczynek
            'specific': 'Stworzyć ergonomiczne i produktywne miejsce pracy',
            'measurable': 'Nowe biurko, krzesło, organizacja kabli',
            'achievable': 'Weekend na reorganizację',
            'relevant': 'Poprawa komfortu pracy zdalnej',
            'time_bound': '1 miesiąc',
            'target_month': 'Styczeń 2025',
            'subgoals': [
                {'title': 'Zakup ergonomicznego krzesła', 'completed': False},
                {'title': 'Organizacja przestrzeni roboczej', 'completed': False},
                {'title': 'Instalacja oświetlenia', 'completed': False}
            ]
        },
        {
            'title': 'Nauka TypeScript',
            'category_id': 1,  # Kariera
            'specific': 'Opanować podstawy TypeScript',
            'measurable': '5 małych projektów, przejście kursu online',
            'achievable': '1h dziennie nauki',
            'relevant': 'Rozwój umiejętności programistycznych',
            'time_bound': '1 miesiąc',
            'target_month': 'Styczeń 2025',
            'subgoals': [
                {'title': 'Ukończyć kurs online TypeScript', 'completed': False},
                {'title': 'Przepisać projekt React na TypeScript', 'completed': False},
                {'title': 'Zrobić własną bibliotekę komponentów', 'completed': False}
            ]
        }
    ]
    
    # Regular tasks (not SMART goals)
    regular_tasks = [
        {
            'title': 'Spotkanie zespołu projektowego',
            'category_id': 1,
            'description': 'Cotygodniowe spotkanie statusowe projektu',
            'deadline': '2025-01-22',
            'status': 'active',
            'priority': 1
        },
        {
            'title': 'Przygotowanie prezentacji',
            'category_id': 1,
            'description': 'Prezentacja kwartalna dla zarządu',
            'deadline': '2025-01-28',
            'status': 'active',
            'priority': 2
        },
        {
            'title': 'Wizyta u dentysty',
            'category_id': 4,
            'description': 'Regularna kontrola',
            'deadline': '2025-01-15',
            'status': 'active',
            'priority': 2
        },
        {
            'title': 'Spotkanie rodzinne',
            'category_id': 5,
            'description': 'Obiad z rodziną',
            'deadline': '2025-01-21',
            'status': 'active',
            'priority': 1
        },
        {
            'title': 'Codzienny code review',
            'category_id': 1,
            'description': 'Przegląd kodu zespołu',
            'deadline': '2025-01-31',
            'status': 'active',
            'priority': 1
        },
        {
            'title': 'Raport miesięczny',
            'category_id': 1,
            'description': 'Przygotowanie raportu z postępów zespołu',
            'deadline': '2025-01-25',
            'status': 'active',
            'priority': 2
        },
        {
            'title': 'Trening na siłowni',
            'category_id': 4,
            'description': 'Trening siłowy według planu',
            'deadline': '2025-01-20',
            'status': 'active',
            'priority': 1
        }
    ]
    
    with db:
        # Dodawanie celów 5-letnich
        for goal in five_year_goals:
            db.add_smart_goal(goal)
            
        # Dodawanie celów rocznych
        for goal in yearly_goals_2025:
            db.add_smart_goal(goal)
            
        # Dodawanie celów 6-miesięcznych
        for goal in six_month_goals:
            db.add_smart_goal(goal)
            
        # Dodawanie celów 3-miesięcznych
        for goal in three_month_goals:
            db.add_smart_goal(goal)
            
        # Dodawanie celów miesięcznych
        for goal in january_2025_goals:
            db.add_smart_goal(goal)
            
        # Dodawanie zwykłych zadań
        for task in regular_tasks:
            db.add_task(
                title=task['title'],
                category_id=task['category_id'],
                description=task['description'],
                deadline=task['deadline']
            )

if __name__ == "__main__":
    generate_enhanced_data()
    print("Przykładowe dane zostały wygenerowane!")