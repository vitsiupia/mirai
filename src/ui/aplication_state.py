# application_state.py
from typing import Dict, List, Set, Any
import threading

class Observer:
    def update(self, state_changes: Dict[str, Any]) -> None:
        """Metoda wywoływana gdy stan się zmienia"""
        pass

class ApplicationStateManager:
    def __init__(self, db_manager):
        self._observers: Dict[str, Set[Observer]] = {
            'tasks': set(),
            'balance': set(),
            'goals': set(),
            'reflections': set()
        }
        self._state = {
            'tasks': [],
            'balance': [],
            'goals': [],
            'reflections': []
        }
        self._lock = threading.Lock()
        self.db_manager = db_manager

    def attach(self, observer: Observer, state_type: str) -> None:
        """Dodaje obserwatora dla konkretnego typu stanu"""
        with self._lock:
            self._observers[state_type].add(observer)

    def detach(self, observer: Observer, state_type: str) -> None:
        """Usuwa obserwatora dla konkretnego typu stanu"""
        with self._lock:
            self._observers[state_type].discard(observer)

    def notify(self, state_type: str) -> None:
        """Powiadamia obserwatorów o zmianie stanu"""
        with self._lock:
            state_changes = {state_type: self._state[state_type]}
            for observer in self._observers[state_type]:
                observer.update(state_changes)

    def update_tasks(self) -> None:
        """Aktualizuje stan zadań"""
        with self.db_manager as db:
            self._state['tasks'] = db.get_all_tasks()
        self.notify('tasks')

    def update_balance(self) -> None:
        """Aktualizuje stan koła balansu"""
        with self.db_manager as db:
            self._state['balance'] = db.get_balance_scores()
        self.notify('balance')

    def update_goals(self) -> None:
        """Aktualizuje stan celów"""
        with self.db_manager as db:
            self._state['goals'] = db.get_all_smart_goals()
        self.notify('goals')

    def update_reflections(self) -> None:
        """Aktualizuje stan notatek"""
        with self.db_manager as db:
            self._state['reflections'] = db.get_all_reflections()
        self.notify('reflections')