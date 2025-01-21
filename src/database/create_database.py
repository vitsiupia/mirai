import sqlite3
import os
from datetime import datetime

def create_database():
    db_exists = os.path.exists("mirai.db")
    print(f"Czy baza danych istnieje: {db_exists}")
    
    if db_exists:
        os.remove("mirai.db")
        print("Usunięto istniejącą bazę danych")
    
    print("Tworzenie nowej bazy danych...")
    connection = sqlite3.connect("mirai.db")
    cursor = connection.cursor()
    
    print("Włączanie obsługi kluczy obcych...")
    cursor.execute("PRAGMA foreign_keys = ON")

    print("Tworzenie tabeli categories...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        color TEXT DEFAULT '#4a90e2',
        icon TEXT,
        sort_order INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    print("Tworzenie tabeli tasks...")
    cursor.execute("""
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
    )
    """)

    print("Tworzenie tabeli balance...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS balance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER NOT NULL,
        score INTEGER CHECK(score BETWEEN 1 AND 10) NOT NULL,
        notes TEXT,
        date DATE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
        UNIQUE(category_id, date)
    )
    """)

    print("Tworzenie tabeli smart_goals...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS smart_goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER NOT NULL,
        specific TEXT NOT NULL,
        measurable TEXT NOT NULL,
        achievable TEXT NOT NULL,
        relevant TEXT NOT NULL,
        time_bound TEXT NOT NULL,
        progress INTEGER DEFAULT 0 CHECK(progress BETWEEN 0 AND 100),
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
    )
    """)

    print("Tworzenie tabeli quotes...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        author TEXT,
        category TEXT,
        language TEXT DEFAULT 'pl',
        is_favorite BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    print("Tworzenie tabeli reflections...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reflections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
    )
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_reflections_category ON reflections(category_id)")

    print("Tworzenie indeksów...")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_category ON tasks(category_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_deadline ON tasks(deadline)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_period ON tasks(period)") 
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_balance_category_date ON balance(category_id, date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_smart_goals_task ON smart_goals(task_id)")

    print("Dodawanie domyślnych kategorii...")
    categories = [
        ('Kariera', 'Cele związane z pracą i rozwojem zawodowym', '#4a90e2', 'briefcase', 1),
        ('Finanse', 'Cele finansowe i budżetowe', '#2ecc71', 'dollar-sign', 2),
        ('Rozwój osobisty', 'Cele związane z samorozwojem', '#9b59b6', 'book', 3),
        ('Zdrowie', 'Cele związane ze zdrowiem i formą fizyczną', '#e74c3c', 'heart', 4),
        ('Rodzina', 'Cele związane z rodziną', '#f1c40f', 'users', 5),
        ('Związki', 'Cele związane z relacjami', '#e67e22', 'heart', 6),
        ('Odpoczynek', 'Cele związane z czasem wolnym', '#1abc9c', 'coffee', 7),
        ('Duchowość', 'Cele związane z rozwojem duchowym', '#95a5a6', 'feather', 8)
    ]
    
    cursor.executemany("""
    INSERT OR IGNORE INTO categories (name, description, color, icon, sort_order) 
    VALUES (?, ?, ?, ?, ?)
    """, categories)

    print("Dodawanie przykładowych cytatów...")
    quotes = [
        ('Rób, co możesz, z tym, co masz, tam, gdzie jesteś.', 'Theodore Roosevelt', 'motywacja', 'pl', 1),
        ('Sukces to suma małych wysiłków powtarzanych dzień po dniu.', 'Robert Collier', 'sukces', 'pl', 0),
        ('Droga do sukcesu jest zawsze w budowie.', 'Lily Tomlin', 'rozwój', 'pl', 0)
    ]
    
    cursor.executemany("""
    INSERT OR IGNORE INTO quotes (text, author, category, language, is_favorite) 
    VALUES (?, ?, ?, ?, ?)
    """, quotes)

    print("Zatwierdzanie zmian...")
    connection.commit()
    
    print("Sprawdzanie czy tabele zostały utworzone...")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"Utworzone tabele: {tables}")
    
    print("Zamykanie połączenia...")
    connection.close()
    
    print("Baza danych została utworzona pomyślnie!")

if __name__ == "__main__":
    create_database()