import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class DatabaseManager:
    def __init__(self, db_path: str = "mirai.db"):
        self.db_path = db_path
        self.connection = None
        self.cursor = None

    def connect(self):
        """Nawiązuje połączenie z bazą danych."""
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")

    def disconnect(self):
        """Zamyka połączenie z bazą danych."""
        if self.connection:
            self.connection.close()

    def __enter__(self):
        """Umożliwia używanie with."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Zamyka połączenie po wyjściu z with."""
        self.disconnect()

    # Operacje na zadaniach
    def add_task(self, title: str, category_id: int, description: str = None, 
                 deadline: str = None, parent_id: int = None) -> int:
        """Dodaje nowe zadanie i zwraca jego ID."""
        query = """
        INSERT INTO tasks (title, category_id, description, deadline, parent_id)
        VALUES (?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (title, category_id, description, deadline, parent_id))
        self.connection.commit()
        return self.cursor.lastrowid

    def get_tasks_by_category(self, category_id: int) -> List[Dict]:
        """Pobiera wszystkie aktywne zadania dla danej kategorii."""
        query = """
        SELECT id, title, description, deadline, status, priority
        FROM tasks
        WHERE category_id = ? AND status != 'deleted'
        ORDER BY priority DESC, deadline
        """
        self.cursor.execute(query, (category_id,))
        tasks = []
        for row in self.cursor.fetchall():
            tasks.append({
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'deadline': row[3],
                'status': row[4],
                'priority': row[5]
            })
        return tasks

    def update_task_status(self, task_id: int, status: str) -> bool:
        """Aktualizuje status zadania."""
        query = """
        UPDATE tasks 
        SET status = ?,
            completed_at = CASE WHEN ? = 'completed' THEN CURRENT_TIMESTAMP ELSE NULL END
        WHERE id = ?
        """
        self.cursor.execute(query, (status, status, task_id))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def delete_task(self, task_id: int) -> bool:
        """Usuwa zadanie (soft delete)."""
        query = "UPDATE tasks SET status = 'deleted' WHERE id = ?"
        self.cursor.execute(query, (task_id,))
        self.connection.commit()
        return self.cursor.rowcount > 0

   

    def get_smart_goal(self, task_id: int) -> Optional[Dict]:
        """Pobiera cel SMART dla zadania."""
        query = """
        SELECT id, specific, measurable, achievable, relevant, time_bound, progress
        FROM smart_goals
        WHERE task_id = ?
        """
        self.cursor.execute(query, (task_id,))
        row = self.cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'specific': row[1],
                'measurable': row[2],
                'achievable': row[3],
                'relevant': row[4],
                'time_bound': row[5],
                'progress': row[6]
            }
        return None
    
    # Operacje na kole balansu
    def update_balance_score(self, category_id: int, score: int, 
                           date: str = None) -> bool:
        """Aktualizuje wynik w kole balansu."""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        query = """
        INSERT OR REPLACE INTO balance (category_id, score, date)
        VALUES (?, ?, ?)
        """
        self.cursor.execute(query, (category_id, score, date))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def get_balance_scores(self, date: str = None) -> List[Dict]:
        """Pobiera wyniki koła balansu dla danej daty."""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
            
        query = """
        SELECT c.name, b.score
        FROM categories c
        LEFT JOIN balance b ON c.id = b.category_id AND b.date = ?
        ORDER BY c.sort_order
        """
        self.cursor.execute(query, (date,))
        scores = []
        for row in self.cursor.fetchall():
            scores.append({
                'category': row[0],
                'score': row[1] if row[1] is not None else 0
            })
        return scores

    # Operacje na cytatach
    def get_random_quote(self) -> Optional[Dict]:
        """Pobiera losowy cytat."""
        query = "SELECT text, author FROM quotes ORDER BY RANDOM() LIMIT 1"
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        if row:
            return {
                'text': row[0],
                'author': row[1]
            }
        return None

    # Operacje na kategoriach
    def get_all_categories(self) -> List[Dict]:
        """Pobiera wszystkie kategorie."""
        query = """
        SELECT id, name, description, color, icon, sort_order
        FROM categories
        ORDER BY sort_order
        """
        self.cursor.execute(query)
        categories = []
        for row in self.cursor.fetchall():
            categories.append({
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'color': row[3],
                'icon': row[4],
                'sort_order': row[5]
            })
        return categories
    
    def add_smart_goal(self, goal_data: dict) -> int:
        """Adds a new SMART goal and its subgoals.
        
        Args:
            goal_data: Dictionary containing:
                - title: str
                - category_id: int
                - specific: str
                - measurable: str
                - achievable: str
                - relevant: str
                - time_bound: str
                - subgoals: list[dict] (optional)
        """
        try:
            # First, create the main task
            task_query = """
            INSERT INTO tasks (title, category_id, period)
            VALUES (?, ?, ?)
            """
            self.cursor.execute(task_query, (
                goal_data['title'],
                goal_data['category_id'],
                goal_data['time_bound']
            ))
            task_id = self.cursor.lastrowid

            # Then create the SMART goal details
            smart_query = """
            INSERT INTO smart_goals (
                task_id, specific, measurable, achievable, 
                relevant, time_bound
            ) VALUES (?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(smart_query, (
                task_id,
                goal_data['specific'],
                goal_data['measurable'],
                goal_data['achievable'],
                goal_data['relevant'],
                goal_data['time_bound']
            ))

            # Finally, add any subgoals as child tasks
            if goal_data.get('subgoals'):
                subgoal_query = """
                INSERT INTO tasks (
                    title, category_id, parent_id, status, period
                ) VALUES (?, ?, ?, ?, ?)
                """
                for subgoal in goal_data['subgoals']:
                    status = 'completed' if subgoal.get('completed', False) else 'active'
                    self.cursor.execute(subgoal_query, (
                        subgoal['title'],
                        goal_data['category_id'],
                        task_id,
                        status,
                        goal_data['time_bound']
                    ))

            self.connection.commit()
            return task_id
            
        except Exception as e:
            print(f"Error adding SMART goal: {e}")
            self.connection.rollback()
            raise

    def get_smart_goals_by_period(self, category_id, period):
        """Gets all SMART goals for a category and period."""
        query = """
        SELECT 
            t.id,
            t.title,
            t.status,
            s.specific,
            s.measurable,
            s.achievable,
            s.relevant,
            s.time_bound,
            s.progress
        FROM tasks t
        JOIN smart_goals s ON t.id = s.task_id
        WHERE t.category_id = ? 
        AND t.period = ?
        AND t.status != 'deleted'
        """
        self.cursor.execute(query, (category_id, period))
        goals = []
        for row in self.cursor.fetchall():
            # Get subgoals for this goal
            subgoal_query = """
            SELECT id, title, status
            FROM tasks
            WHERE parent_id = ?
            AND status != 'deleted'
            """
            self.cursor.execute(subgoal_query, (row[0],))
            subgoals = [{
                'id': sub[0],
                'title': sub[1],
                'completed': sub[2] == 'completed'
            } for sub in self.cursor.fetchall()]
            
            goals.append({
                'id': row[0],
                'title': row[1],
                'status': row[2],
                'specific': row[3],
                'measurable': row[4],
                'achievable': row[5],
                'relevant': row[6],
                'time_bound': row[7],
                'progress': row[8],
                'subgoals': subgoals
            })
        return goals

    def update_subgoal_status(self, subgoal_id, completed):
        """Updates the status of a subgoal."""
        status = 'completed' if completed else 'active'
        query = "UPDATE tasks SET status = ? WHERE id = ?"
        self.cursor.execute(query, (status, subgoal_id))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def delete_smart_goal(self, goal_id):
        """Deletes a SMART goal and all its subgoals."""
        # This will cascade delete the smart_goals entry and all subgoals
        query = "UPDATE tasks SET status = 'deleted' WHERE id = ?"
        self.cursor.execute(query, (goal_id,))
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    def get_goal_id_by_subgoal(self, subgoal_id: int) -> int:
        """Pobiera ID głównego celu na podstawie ID podzadania."""
        query = "SELECT parent_id FROM tasks WHERE id = ?"
        self.cursor.execute(query, (subgoal_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_subgoals_by_goal(self, goal_id: int) -> List[Dict]:
        """Pobiera wszystkie podzadania dla danego celu."""
        query = """
        SELECT id, title, status
        FROM tasks
        WHERE parent_id = ? AND status != 'deleted'
        """
        self.cursor.execute(query, (goal_id,))
        return [{'id': row[0], 
                'title': row[1], 
                'completed': row[2] == 'completed'} 
                for row in self.cursor.fetchall()]

    def update_goal_progress(self, goal_id: int, progress: int) -> bool:
        """Aktualizuje postęp głównego celu."""
        query = """
        UPDATE smart_goals
        SET progress = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE task_id = ?
        """
        self.cursor.execute(query, (progress, goal_id))
        self.connection.commit()
        return self.cursor.rowcount > 0