📅 Mirai – Aplikacja do planowania celów długoterminowych

Mirai to desktopowa aplikacja stworzona w języku Python z wykorzystaniem bibliotek PyQt5 i Matplotlib. Jej celem jest wspieranie użytkowników w skutecznym planowaniu i realizacji długoterminowych celów życiowych, zgodnie z metodologią SMART oraz z wykorzystaniem narzędzia Koło Balansu (Wheel of Life).
📌 Funkcjonalności
- Tworzenie i zarządzanie celami zgodnymi z metodą SMART
- Planowanie celów krótko-, średnio- i długoterminowych (od miesiąca do 10 lat)
- Tworzenie celów pośrednich z hierarchiczną strukturą
- Analiza postępów za pomocą Koła Balansu (interaktywna wizualizacja)
- Prowadzenie refleksyjnych notatek z podziałem na kategorie życia
- Cytaty motywacyjne do codziennej inspiracji
- Intuicyjny, przejrzysty interfejs użytkownika (GUI)
- System obsługi błędów oraz zapisu danych w bazie SQLite

🧠 Metodologie i narzędzia
SMART – cele muszą być konkretne, mierzalne, osiągalne, istotne i określone w czasie
Koło Balansu (Wheel of Life) – wizualne narzędzie do oceny satysfakcji w różnych dziedzinach życia
Metody zarządzania czasem: Pomodoro, Getting Things Done (GTD), Macierz Eisenhowera (priorytetyzacja)
Gamifikacja – śledzenie postępów i utrzymywanie motywacji

🛠️ Technologie
- Python
- PyQt5 – budowa interfejsu graficznego
- Matplotlib – wizualizacja danych (Koło Balansu)
- SQLite – lokalna baza danych
- Wzorce projektowe: Singleton, Observer, Context Manager

💻 Instalacja
Wymagania:
- Python 3.8+
- 
Instalacja zależności:
pip install -r requirements.txt

Uruchomienie aplikacji:
python main.py

📂 Struktura bazy danych
Aplikacja wykorzystuje bazę danych SQLite z tabelami:
- categories – obszary życia
- tasks – cele i zadania
- smart_goals – szczegóły metodologii SMART
- balance – oceny w Kołu Balansu
- reflections – notatki użytkownika
- quotes – motywujące cytaty

🧪 Testowanie
Aplikacja została przetestowana ręcznie, ze szczególnym uwzględnieniem:
- Dodawania, edycji i usuwania zadań
- Obsługi błędów w połączeniach z bazą danych
- Integralności danych między celami SMART a celami pośrednimi
- Responsywności GUI

🧭 Przyszły rozwój
- Eksport danych do pliku PDF/CSV
- Synchronizacja z chmurą i wersja mobilna
- Integracja z kalendarzami (Google, Outlook)
- Personalizowane przypomnienia i system nagród

👩‍💻 Autor
Projekt wykonany przez Viktoriia Tsiupiak w ramach pracy dyplomowej na Uniwersytecie Dolnośląskim DSW we Wrocławiu

📄 Licencja

Projekt dostępny na licencji MIT. Możesz go dowolnie modyfikować i rozpowszechniać.
