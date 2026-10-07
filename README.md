
Mirai to desktopowa aplikacja napisana w Pythonie, wspierająca długoterminowe planowanie celów. Została stworzona w ramach pracy dyplomowej na Uniwersytecie Dolnośląskim DSW, aby przełożyć teoretyczne koncepcje planowania (metodologia SMART, Koło Balansu) na działające, lokalne narzędzie dla użytkownika.

## Główne funkcje

* **Implementacja metody SMART:** Aplikacja wymusza specyfikację celów (od miesięcznych po 10-letnie) zgodnie z kryteriami konkretności, mierzalności i terminowości.
* **Hierarchia zadań:** Możliwość rozbijania głównych celów na mniejsze kroki pośrednie o strukturze drzewiastej.
* **Koło Balansu:** Dynamicznie generowany wykres wizualizujący poziom satysfakcji użytkownika w różnych sferach życia.
* **Moduł refleksji:** Wbudowany system notatek przypisanych do konkretnych kategorii życia.

## Stack technologiczny

* **Język:** Python 3.8+
* **GUI:** PyQt5
* **Wizualizacja danych:** Matplotlib
* **Baza danych:** SQLite (lokalna)
* **Architektura:** W kodzie wykorzystano wzorce projektowe takie jak Singleton, Observer i Context Manager.

## Instalacja i uruchomienie

1. Sklonuj repozytorium:

```bash
git clone https://github.com/TwojaNazwaUzytkownika/mirai.git
cd mirai

```

2. Zainstaluj wymagane zależności:

```bash
pip install -r requirements.txt

```

3. Uruchom aplikację:

```bash
python main.py

```

## Struktura danych

Aplikacja przechowuje stan lokalnie w bazie SQLite. Główne tabele odpowiadają za:

* `categories` – słownik obszarów życia
* `tasks` / `smart_goals` – metryki i struktura zdefiniowanych celów
* `balance` – historia pomiarów dla Koła Balansu
* `reflections` / `quotes` – teksty użytkownika i wbudowana baza motywacyjna

## Plany rozwoju (Roadmap)

Obecna wersja to zamknięty projekt dyplomowy, jednak architektonicznie pozwala na rozbudowę o:

* Generowanie raportów i eksport do formatów PDF/CSV.
* Integrację z zewnętrznymi kalendarzami (np. Google Calendar API).
* Wdrożenie powiadomień systemowych.

## Autor i licencja

Projekt został zrealizowany przez **Viktoriię Tsiupiak**.

Kod udostępniony na licencji **MIT** – można go dowolnie modyfikować i używać.
