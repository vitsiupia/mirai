import os
import sys
import pytest
import sqlite3
import logging
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.database.database import DatabaseManager

# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)  # Wyświetla logi w konsoli
    ]
)

@pytest.fixture
def db():
    logging.info("Przygotowanie bazy danych w pamięci")
    # Używamy bazy w pamięci do testów
    db = DatabaseManager(":memory:")
    db.connect()
   
    logging.info("Tworzenie struktury tabel")
    # Jawne utworzenie tabel
    db.cursor.executescript("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        color TEXT DEFAULT '#4a90e2',
        icon TEXT,
        sort_order INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        deadline DATE,
        category_id INTEGER NOT NULL,
        status TEXT CHECK(status IN ('active', 'completed', 'deleted', 'in_progress')) DEFAULT 'active',
        priority INTEGER CHECK(priority BETWEEN 1 AND 5) DEFAULT 3,
        parent_id INTEGER DEFAULT NULL,
        period TEXT CHECK(period IN ('5-10 lat', '1 rok', '6 miesięcy', '3 miesiące', 'miesiąc', NULL)),
        reminder_date TIMESTAMP,
        tags TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP,
        target_month TEXT,
        FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
        FOREIGN KEY (parent_id) REFERENCES tasks(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS smart_goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER UNIQUE,
        specific TEXT,
        measurable TEXT,
        achievable TEXT,
        relevant TEXT,
        time_bound TEXT,
        progress INTEGER DEFAULT 0,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
    );
    """)
    db.connection.commit()
    logging.info("Struktura tabel utworzona pomyślnie")
   
    yield db
    
    logging.info("Zamykanie połączenia z bazą danych")
    db.disconnect()

def test_add_task(db):
    logging.info("Rozpoczęcie testu dodawania zadania")
    
    try:
        # Dodaj kategorię testową
        logging.info("Dodawanie kategorii testowej")
        db.cursor.execute(
            "INSERT INTO categories (name, description) VALUES (?, ?)",
            ("Test Category", "Test Description")
        )
        category_id = db.cursor.lastrowid
        logging.info(f"Utworzono kategorię o ID: {category_id}")
       
        # Test dodawania zadania
        logging.info("Dodawanie zadania testowego")
        task_id = db.add_task(
            title="Test Task",
            category_id=category_id,
            description="Test Description",
            deadline="2025-01-20"
        )
        logging.info(f"Dodano zadanie o ID: {task_id}")
       
        # Sprawdź czy zadanie zostało dodane
        db.cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        task = db.cursor.fetchone()
        
        logging.info(f"Szczegóły zadania: {task}")
        
        assert task is not None, "Zadanie nie zostało dodane do bazy"
        assert task[1] == "Test Task", "Tytuł zadania nie zgadza się"
        
        logging.info("Test dodawania zadania zakończony sukcesem")
    
    except Exception as e:
        logging.error(f"Błąd podczas testu dodawania zadania: {e}")
        raise

def test_get_tasks_by_category(db):
    logging.info("Rozpoczęcie testu pobierania zadań z kategorii")
    
    try:
        # Dodaj kategorię
        logging.info("Dodawanie kategorii testowej")
        db.cursor.execute(
            "INSERT INTO categories (name) VALUES (?)",
            ("Test Category",)
        )
        category_id = db.cursor.lastrowid
        logging.info(f"Utworzono kategorię o ID: {category_id}")
       
        # Dodaj zadania
        logging.info("Dodawanie zadań testowych")
        db.add_task(title="Task 1", category_id=category_id)
        db.add_task(title="Task 2", category_id=category_id)
        logging.info("Zadania dodane")
       
        # Pobierz i sprawdź zadania
        tasks = db.get_tasks_by_category(category_id)
        
        logging.info(f"Pobrano zadania: {tasks}")
        
        assert len(tasks) == 2, "Liczba zadań nie zgadza się"
        assert tasks[0]['title'] == "Task 1", "Pierwszy task ma nieprawidłowy tytuł"
        
        logging.info("Test pobierania zadań z kategorii zakończony sukcesem")
    
    except Exception as e:
        logging.error(f"Błąd podczas testu pobierania zadań z kategorii: {e}")
        raise