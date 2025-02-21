import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple  
import threading


class DatabaseManager:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, db_path: str = "mirai.db"):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.db_path = db_path
                cls._instance.connection = None
                cls._instance.cursor = None
                cls._instance._initialize()
            return cls._instance
    
    def _initialize(self):
        """Inicjalizacja instancji (wywoływana tylko raz)"""
        self.db_path = "mirai.db"
        self.connection = None
        self.cursor = None

    def connect(self):
        """Nawiązuje połączenie z bazą danych."""
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            self.cursor.execute("PRAGMA foreign_keys = ON")

    def disconnect(self):
        """Zamyka połączenie z bazą danych."""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    @classmethod
    def get_instance(cls, db_path: str = "mirai.db") -> 'DatabaseManager':
        """Metoda dostępowa do instancji Singletona"""
        return cls(db_path)
    

    def add_task(self, title: str, category_id: int, description: str = None, 
                deadline: str = None, parent_id: int = None) -> int:
        """Dodaje nowe zadanie i zwraca jego ID."""
        query = """
        INSERT INTO tasks (title, category_id, description, deadline, parent_id, status)
        VALUES (?, ?, ?, ?, ?, 'in_progress')
        """
        self.cursor.execute(query, (title, category_id, description, deadline, parent_id))
        self.connection.commit()
        return self.cursor.lastrowid

    def get_tasks_by_category(self, category_id: int) -> List[Dict]:
        """Pobiera wszystkie aktywne zadania dla danej kategorii."""
        query = """
        SELECT id, title, description, deadline, status
        FROM tasks
        WHERE category_id = ? AND status != 'deleted'
        ORDER BY deadline
        """
        self.cursor.execute(query, (category_id,))
        tasks = []
        for row in self.cursor.fetchall():
            tasks.append({
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'deadline': row[3],
                'status': row[3],
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
    
    def update_balance_score(self, category_id: int, score: int) -> bool:
        """Aktualizuje wynik w kole balansu."""
        query = """
        INSERT OR REPLACE INTO balance (category_id, score)
        VALUES (?, ?)
        """
        self.cursor.execute(query, (category_id, score))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def get_balance_scores(self) -> List[Dict]:
        """Pobiera aktualne wyniki koła balansu."""
        query = """
        SELECT c.name, b.score
        FROM categories c
        LEFT JOIN balance b ON c.id = b.category_id
        ORDER BY c.sort_order
        """
        self.cursor.execute(query)
        return [{
            'category': row[0],
            'score': row[1] if row[1] is not None else 0
        } for row in self.cursor.fetchall()]

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
        try:
            task_query = """
            INSERT INTO tasks (title, category_id, period, target_month, status)
            VALUES (?, ?, ?, ?, 'in_progress')
            """
            self.cursor.execute(task_query, (
                goal_data['title'],
                goal_data['category_id'],
                goal_data['time_bound'],
                goal_data.get('target_month')
            ))
            task_id = self.cursor.lastrowid

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

            if goal_data.get('subgoals'):
                subgoal_query = """
                INSERT INTO tasks (
                    title, category_id, parent_id, status, period, target_month
                ) VALUES (?, ?, ?, ?, ?, ?)
                """
                for subgoal in goal_data['subgoals']:
                    status = 'completed' if subgoal.get('completed', False) else 'in_progress'
                    self.cursor.execute(subgoal_query, (
                        subgoal['title'],
                        goal_data['category_id'],
                        task_id,
                        status,
                        goal_data['time_bound'],
                        goal_data.get('target_month')
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
            s.progress,
            t.target_month  -- Dodane na końcu listy
        FROM tasks t
        JOIN smart_goals s ON t.id = s.task_id
        WHERE t.category_id = ? 
        AND t.period = ?
        AND t.status != 'deleted'
        """
        self.cursor.execute(query, (category_id, period))
        goals = []
        for row in self.cursor.fetchall():

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
                'target_month': row[9],  
                'subgoals': subgoals
            })
        return goals

    def update_subgoal_status(self, subgoal_id, completed):
        """Updates the status of a subgoal."""
        status = 'completed' if completed else 'in_progress'
        query = "UPDATE tasks SET status = ? WHERE id = ?"
        self.cursor.execute(query, (status, subgoal_id))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def delete_smart_goal(self, goal_id):
        """Deletes a SMART goal and all its subgoals."""
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
        SET progress = ?
        WHERE task_id = ?
        """
        self.cursor.execute(query, (progress, goal_id))
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    def update_smart_goal(self, goal_id: int, goal_data: dict) -> bool:
        """Updates an existing SMART goal and its subgoals."""
        try:
            task_query = """
            UPDATE tasks 
            SET title = ?,
                period = ?
            WHERE id = ?
            """
            self.cursor.execute(task_query, (
                goal_data['title'],
                goal_data['time_bound'],
                goal_id
            ))

            smart_query = """
            UPDATE smart_goals 
            SET specific = ?,
                measurable = ?,
                achievable = ?,
                relevant = ?,
                time_bound = ?
            WHERE task_id = ?
            """
            self.cursor.execute(smart_query, (
                goal_data['specific'],
                goal_data['measurable'],
                goal_data['achievable'],
                goal_data['relevant'],
                goal_data['time_bound'],
                goal_id
            ))

            self.cursor.execute("DELETE FROM tasks WHERE parent_id = ?", (goal_id,))

            if goal_data.get('subgoals'):
                subgoal_query = """
                INSERT INTO tasks (
                    title, category_id, parent_id, status, period
                ) VALUES (?, ?, ?, ?, ?)
                """
                for subgoal in goal_data['subgoals']:
                    status = 'completed' if subgoal.get('completed', False) else 'in_progress'
                    self.cursor.execute(subgoal_query, (
                        subgoal['title'],
                        goal_data['category_id'],
                        goal_id,
                        status,
                        goal_data['time_bound']
                    ))

            self.connection.commit()
            return True

        except Exception as e:
            print(f"Error updating SMART goal: {e}")
            self.connection.rollback()
            return False

    def get_smart_goal_details(self, goal_id: int) -> Dict:
        """Gets full details of a SMART goal including subgoals."""
        query = """
        SELECT 
            t.title,
            t.category_id,
            s.specific,
            s.measurable,
            s.achievable,
            s.relevant,
            s.time_bound,
            t.period
        FROM tasks t
        JOIN smart_goals s ON t.id = s.task_id
        WHERE t.id = ? AND t.status != 'deleted'
        """
        self.cursor.execute(query, (goal_id,))
        row = self.cursor.fetchone()
        
        if not row:
            return None
            
        subgoal_query = """
        SELECT id, title, status
        FROM tasks
        WHERE parent_id = ? AND status != 'deleted'
        """
        self.cursor.execute(subgoal_query, (goal_id,))
        subgoals = [{
            'title': sub[1],
            'completed': sub[2] == 'completed'
        } for sub in self.cursor.fetchall()]
        
        return {
            'id': goal_id,
            'title': row[0],
            'category_id': row[1],
            'specific': row[2],
            'measurable': row[3],
            'achievable': row[4],
            'relevant': row[5],
            'time_bound': row[6],
            'period': row[7],
            'subgoals': subgoals
        }
    
    def add_reflection(self, category_id: int, content: str) -> int:
        """Dodaje nową refleksję dla kategorii."""
        query = """
        INSERT INTO reflections (category_id, content)
        VALUES (?, ?)
        """
        self.cursor.execute(query, (category_id, content))
        self.connection.commit()
        return self.cursor.lastrowid

    def update_reflection(self, category_id: int, content: str) -> bool:
        """Aktualizuje istniejącą refleksję dla kategorii."""
        query = """
        UPDATE reflections 
        SET content = ?
        WHERE category_id = ?
        """
        self.cursor.execute(query, (content, category_id))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def get_reflection(self, category_id: int) -> Optional[Dict]:
        """Pobiera refleksję dla danej kategorii."""
        query = """
        SELECT id, content, created_at
        FROM reflections
        WHERE category_id = ?
        """
        self.cursor.execute(query, (category_id,))
        row = self.cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'content': row[1],
                'created_at': row[2]
            }
        return None

    def get_all_reflections(self) -> List[Dict]:
        """Pobiera wszystkie refleksje wraz z nazwami kategorii."""
        query = """
        SELECT r.id, r.category_id, c.name, r.content, r.created_at
        FROM reflections r
        JOIN categories c ON r.category_id = c.id
        ORDER BY c.sort_order
        """
        self.cursor.execute(query)
        reflections = []
        for row in self.cursor.fetchall():
            reflections.append({
                'id': row[0],
                'category_id': row[1],
                'category_name': row[2],
                'content': row[3],
                'created_at': row[4]
            })
        return reflections
        
    def delete_reflection(self, category_id: int) -> bool:
        """Usuwa refleksję dla danej kategorii."""
        query = "DELETE FROM reflections WHERE category_id = ?"
        self.cursor.execute(query, (category_id,))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def get_tasks_by_category_and_date_range(self, category_id: int, start_date: str, end_date: str) -> List[Dict]:
        """Pobiera zadania dla danej kategorii w określonym zakresie dat."""
        month_mapping = {
            1: 'Styczeń', 2: 'Luty', 3: 'Marzec', 4: 'Kwiecień',
            5: 'Maj', 6: 'Czerwiec', 7: 'Lipiec', 8: 'Sierpień',
            9: 'Wrzesień', 10: 'Październik', 11: 'Listopad', 12: 'Grudzień'
        }
        
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        target_month = f"{month_mapping[start_date_obj.month]} {start_date_obj.year}"
        
        query = """
        SELECT id, title, description, deadline, status
        FROM tasks
        WHERE category_id = ? 
        AND status != 'deleted'
        AND (
            (deadline BETWEEN ? AND ?)  -- Zwykłe zadania z deadline
            OR  -- Cele SMART z target_month
            (EXISTS (
                SELECT 1 
                FROM smart_goals sg 
                WHERE sg.task_id = tasks.id
            ) AND target_month = ?)
        )
        ORDER BY deadline
        """
        
        self.cursor.execute(query, (category_id, start_date, end_date, target_month))
        tasks = []
        for row in self.cursor.fetchall():
            is_smart_goal = False
            self.cursor.execute("SELECT 1 FROM smart_goals WHERE task_id = ?", (row[0],))
            if self.cursor.fetchone():
                is_smart_goal = True
                
            tasks.append({
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'deadline': row[3],
                'status': row[4],
                'is_smart_goal': is_smart_goal
            })
        return tasks
    
    def add_subgoal(self, goal_id: int, title: str, completed: bool = False) -> int:
        """Dodaje nowy podcel do istniejącego celu SMART.
        
        Args:
            goal_id (int): ID głównego celu SMART
            title (str): Nazwa podcelu
            completed (bool): Czy podcel jest już wykonany
            
        Returns:
            int: ID nowego podcelu
        """
        status = 'completed' if completed else 'in_progress'
        
        query = """
        SELECT category_id, period
        FROM tasks
        WHERE id = ?
        """
        self.cursor.execute(query, (goal_id,))
        parent_info = self.cursor.fetchone()
        
        if not parent_info:
            raise ValueError("Nie znaleziono głównego celu")
            
        category_id, period = parent_info
        
        query = """
        INSERT INTO tasks (
            title, category_id, parent_id, status, period
        ) VALUES (?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (
            title,
            category_id,
            goal_id,
            status,
            period
        ))
        
        subgoal_id = self.cursor.lastrowid
        self.connection.commit()
        
        subgoals = self.get_subgoals_by_goal(goal_id)
        total = len(subgoals)
        completed_count = len([sg for sg in subgoals if sg['completed']])
        progress = int((completed_count / total) * 100) if total > 0 else 0
        self.update_goal_progress(goal_id, progress)
        
        return subgoal_id