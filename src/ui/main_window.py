import os
import sys
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QLabel, QFrame, QScrollArea,
                           QGridLayout, QCheckBox, QSpacerItem, QSizePolicy,
                           QDialog, QLineEdit, QCalendarWidget, QTextEdit, QMessageBox, QPlainTextEdit, QProgressBar)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.database.database import DatabaseManager
from src.ui.balance_wheel import BalanceWheel
from src.ui.longterm_window import LongTermWindow  # Dodany import
from datetime import datetime
from src.ui.smart_goals_dialog import SmartGoalsDialog
from datetime import datetime, timedelta
from PyQt5.QtCore import pyqtSignal

class TaskDialog(QDialog):
    def __init__(self, category_id, parent=None):
        super().__init__(parent)
        self.category_id = category_id
        self.setup_ui()
    
    def open_smart_goal_dialog(self):
        """Otwiera okno formularza celu SMART z wstępnie wypełnionymi danymi z aktualnego formularza."""
        dialog = SmartGoalsDialog(self.category_id, self)
        dialog.title_edit.setText(self.title_edit.text())
        dialog.specific_edit.setPlainText(self.description_edit.toPlainText())
        
        if dialog.exec_() == QDialog.Accepted:
            smart_goal_data = dialog.get_smart_goal_data()
            parent_window = self.parent()
            if parent_window and hasattr(parent_window, 'db_manager'):
                with parent_window.db_manager as db:
                    db.add_smart_goal(smart_goal_data)
            self.reject()  # Zamknij okno zwykłego zadania

    def setup_ui(self):
        self.setWindowTitle("Nowe zadanie")
        self.setMinimumWidth(450)
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border-radius: 10px;
            }
            QLabel {
                color: #333333;
                font-size: 13px;
                font-weight: bold;
                margin-top: 10px;
            }
            QLineEdit, QTextEdit {
                padding: 8px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                background-color: #f8f9fa;
                color: #333333;
                font-size: 13px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #4a90e2;
                background-color: #ffffff;
            }
            QCalendarWidget {
                background-color: #ffffff;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
            }
            QCalendarWidget QToolButton {
                color: #333333;
                background-color: transparent;
                border: none;
                border-radius: 4px;
                padding: 8px;
                margin: 2px;
                font-weight: normal;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #f5f5f5;
            }
            QCalendarWidget QToolButton::menu-indicator {
                image: url(none);
                width: 12px;
                height: 12px;
                padding: 0px;
                margin: 0px;
            }
            QCalendarWidget QToolButton#qt_calendar_prevmonth {
                qproperty-icon: none;
                qproperty-text: "‹";
                font-size: 18px;
            }
            QCalendarWidget QToolButton#qt_calendar_nextmonth {
                qproperty-icon: none;
                qproperty-text: "›";
                font-size: 18px;
            }
            QCalendarWidget QMenu {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 4px;
                selection-background-color: #4a90e2;
                selection-color: white;
            }
            QCalendarWidget QSpinBox {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 4px;
                background: white;
            }
            QCalendarWidget QToolButton::menu-button {
                width: 16px;
                border: none;
                border-radius: 4px;
                padding: 0px;
            }
            QCalendarWidget QMenu::item {
                padding: 6px 16px;
                border-radius: 4px;
            }
            QCalendarWidget QMenu::item:selected {
                background-color: #4a90e2;
                color: white;
            }
            QCalendarWidget QSpinBox {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 2px;
            }
            QCalendarWidget QWidget { alternate-background-color: #f8f9fa; }
            QCalendarWidget QAbstractItemView:enabled {
                color: #333333;
                selection-background-color: #4a90e2;
                selection-color: #ffffff;
            }
            QCalendarWidget QAbstractItemView:disabled { color: #808080; }
        """)
        
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Kontener na formularze
        form_container = QWidget()
        form_container.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border-radius: 8px;
            }
        """)
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(10)
        
        # Tytuł zadania
        title_label = QLabel("Nazwa zadania")
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Wprowadź nazwę zadania...")
        self.title_edit.setMinimumHeight(40)
        
        # Opis zadania
        description_label = QLabel("Opis (opcjonalnie)")
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Dodaj szczegóły zadania...")
        self.description_edit.setMinimumHeight(100)
        self.description_edit.setMaximumHeight(120)
        
        # Deadline
        deadline_label = QLabel("Termin wykonania")
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar.setHorizontalHeaderFormat(QCalendarWidget.SingleLetterDayNames)
        
        # Dodawanie elementów do layoutu formularza
        form_layout.addWidget(title_label)
        form_layout.addWidget(self.title_edit)
        form_layout.addWidget(description_label)
        form_layout.addWidget(self.description_edit)
        form_layout.addWidget(deadline_label)
        form_layout.addWidget(self.calendar)
        
        # Przyciski
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        self.cancel_button = QPushButton("Anuluj")
        self.cancel_button.setMinimumHeight(40)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #f8f9fa;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                color: #666666;
                font-weight: bold;
                padding: 8px 16px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #e9ecef;
                border-color: #dee2e6;
            }
            QPushButton:pressed {
                background-color: #dee2e6;
            }
        """)
        self.cancel_button.clicked.connect(self.reject)
        
        self.save_button = QPushButton("Zapisz")
        self.save_button.setMinimumHeight(40)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                border: none;
                border-radius: 6px;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:pressed {
                background-color: #2d6da3;
            }
        """)
        self.save_button.clicked.connect(self.accept)
        
        # Przycisk SMART
        self.smart_button = QPushButton("Dodaj jako cel SMART")
        self.smart_button.setMinimumHeight(40)
        self.smart_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                border: none;
                border-radius: 6px;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        self.smart_button.clicked.connect(self.open_smart_goal_dialog)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.smart_button)
        
        # Dodawanie wszystkich elementów do głównego layoutu
        main_layout.addWidget(form_container)
        main_layout.addLayout(buttons_layout)
        
    def get_task_data(self):
        return {
            'title': self.title_edit.text(),
            'description': self.description_edit.toPlainText(),
            'deadline': self.calendar.selectedDate().toString("yyyy-MM-dd"),
            'category_id': self.category_id
        }
        
    def accept(self):
        if not self.title_edit.text().strip():
            QMessageBox.warning(
                self,
                "Błąd",
                "Nazwa zadania nie może być pusta!",
                QMessageBox.Ok
            )
            return
        super().accept()


class TaskBlock(QFrame):
    def __init__(self, category_id, category_name, db_manager, selected_date, parent=None):
        super().__init__(parent)
        self.category_id = category_id
        self.category_name = category_name
        self.db_manager = db_manager
        self.selected_date = selected_date  # DateTime object
        self.setup_ui()
        self.load_tasks()

    def setup_ui(self):
            self.setObjectName("taskBlock")
            self.setStyleSheet("""
                #taskBlock {
                    background-color: white;
                    border-radius: 10px;
                    border: 1px solid #e0e0e0;
                    margin: 5px;
                    padding: 10px;
                }
            """)
            
            self.layout = QVBoxLayout(self)
            self.layout.setSpacing(10)
            
            # Kontener na nagłówek kategorii
            header_container = QWidget()
            header_layout = QVBoxLayout(header_container)
            header_layout.setContentsMargins(0, 0, 0, 0)
            header_layout.setSpacing(0)
            
            self.category_label = QLabel(self.category_name)
            self.category_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
            header_layout.addWidget(self.category_label)
            
            # Dodaj separator
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setFrameShadow(QFrame.Sunken)
            separator.setStyleSheet("background-color: #e0e0e0; margin: 5px 0;")
            header_layout.addWidget(separator)
            
            self.layout.addWidget(header_container)
            
            # Kontener na zadania
            tasks_container = QWidget()
            tasks_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.tasks_layout = QVBoxLayout(tasks_container)
            self.tasks_layout.setContentsMargins(0, 0, 0, 0)
            self.tasks_layout.setAlignment(Qt.AlignTop)
            self.layout.addWidget(tasks_container)
            
            # Przycisk dodawania na dole
            add_button = QPushButton("+ Dodaj nowy cel")
            add_button.setStyleSheet("""
                QPushButton {
                    background-color: #f0f0f0;
                    border: none;
                    border-radius: 5px;
                    padding: 8px;
                    color: #666;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
            """)
            add_button.clicked.connect(self.show_add_task_dialog)
            self.layout.addWidget(add_button)

    def load_tasks(self):
        # Oblicz pierwszy i ostatni dzień wybranego miesiąca
        first_day = self.selected_date.replace(day=1)
        if self.selected_date.month == 12:
            last_day = self.selected_date.replace(year=self.selected_date.year + 1, month=1, day=1)
        else:
            last_day = self.selected_date.replace(month=self.selected_date.month + 1, day=1)
        last_day = last_day - timedelta(days=1)

        with self.db_manager as db:
            tasks = db.get_tasks_by_category_and_date_range(
                self.category_id,
                first_day.strftime('%Y-%m-%d'),
                last_day.strftime('%Y-%m-%d')
            )
            
        # Usuń istniejące zadania z layoutu
        for i in reversed(range(self.tasks_layout.count())): 
            widget = self.tasks_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        # Dodaj zadania
        for task in tasks:
            self.add_task_widget(task)


    def add_task_widget(self, task_data):
        task_data['category_id'] = self.category_id
        task_widget = QWidget()
        task_layout = QHBoxLayout(task_widget)
        task_layout.setContentsMargins(0, 0, 0, 0)
        task_layout.setSpacing(5)
        
        checkbox = QCheckBox()
        checkbox.setChecked(task_data['status'] == 'completed')
        checkbox.stateChanged.connect(lambda state: self.update_task_status(task_data['id'], state))
        
        
        task_content = QWidget()
        task_content_layout = QVBoxLayout(task_content)
        task_content_layout.setSpacing(2)
        task_content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Dodaj ikonę lub oznaczenie dla celu SMART
        title_text = task_data['title']
        

        task_label = QLabel(title_text)
        if task_data['status'] == 'completed':
            task_label.setStyleSheet("text-decoration: line-through; color: #888;")
        else:
            task_label.setStyleSheet("font-weight: normal;" if task_data.get('is_smart_goal') else "")
            
        task_content_layout.addWidget(task_label)
        
        # Dodaj datę, jeśli istnieje
        if task_data['deadline']:
            deadline = datetime.strptime(task_data['deadline'], '%Y-%m-%d').strftime('%d.%m.%Y')
            deadline_label = QLabel(f"Termin: {deadline}")
            deadline_label.setStyleSheet("color: #666; font-size: 11px;")
            task_content_layout.addWidget(deadline_label)
        
        # Dodaj obsługę kliknięcia
        task_content.mousePressEvent = lambda e: self.show_task_details(task_data)
        
        task_layout.addWidget(checkbox)
        task_layout.addWidget(task_content, stretch=1)
        
        # Dodaj przycisk usuwania
        delete_button = QPushButton("🗑")
        delete_button.setFixedSize(24, 24)
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #999;
            }
            QPushButton:hover {
                color: #ff4444;
            }
        """)
        delete_button.clicked.connect(lambda: self.delete_task(task_data['id']))
        
        task_layout.addWidget(delete_button)
        
        self.tasks_layout.addWidget(task_widget)

    def show_add_task_dialog(self):
        dialog = TaskDialog(self.category_id, self)
        if dialog.exec_() == QDialog.Accepted:
            task_data = dialog.get_task_data()
            with self.db_manager as db:  # Użycie context managera
                task_id = db.add_task(
                    title=task_data['title'],
                    category_id=task_data['category_id'],
                    description=task_data['description'],
                    deadline=task_data['deadline']
                )
            self.load_tasks()

    def show_task_details(self, task_data):
        dialog = TaskDetailsDialog(task_data, self)
        dialog.exec_()

    def update_task_status(self, task_id, state):
        status = 'completed' if state == Qt.Checked else 'active'
        with self.db_manager as db:  # Użycie context managera
            db.update_task_status(task_id, status)
        self.load_tasks()

    def delete_task(self, task_id):
        with self.db_manager as db:  # Użycie context managera
            db.delete_task(task_id)
        self.load_tasks()

    def set_task_data(self, task_data):
        """Wypełnia formularz danymi istniejącego zadania."""
        self.title_edit.setText(task_data['title'])
        if task_data.get('description'):
            self.description_edit.setPlainText(task_data['description'])
        if task_data.get('deadline'):
            date = datetime.strptime(task_data['deadline'], '%Y-%m-%d')
            self.calendar.setSelectedDate(date)


class MonthYearSelector(QWidget):
    month_changed = pyqtSignal(datetime)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_date = datetime.now()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 10)
        layout.setSpacing(10)
        
        # Przycisk poprzedniego miesiąca
        self.prev_button = QPushButton("←")
        self.prev_button.setFixedSize(40, 40)
        self.prev_button.clicked.connect(self.previous_month)
        self.prev_button.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: none;
                border-radius: 20px;
                font-size: 16px;
                color: #666;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        
        # Przycisk następnego miesiąca
        self.next_button = QPushButton("→")
        self.next_button.setFixedSize(40, 40)
        self.next_button.clicked.connect(self.next_month)
        self.next_button.setStyleSheet(self.prev_button.styleSheet())
        
        # Label z aktualnym miesiącem i rokiem
        self.date_label = QLabel()
        self.date_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        self.date_label.setStyleSheet("color: #333333;")
        
        layout.addStretch(1)
        layout.addWidget(self.prev_button)
        layout.addWidget(self.date_label)
        layout.addWidget(self.next_button)
        layout.addStretch(1)
        
        self.update_label()
        
    def update_label(self):
        months = {
            1: 'Styczeń', 2: 'Luty', 3: 'Marzec', 4: 'Kwiecień',
            5: 'Maj', 6: 'Czerwiec', 7: 'Lipiec', 8: 'Sierpień',
            9: 'Wrzesień', 10: 'Październik', 11: 'Listopad', 12: 'Grudzień'
        }
        month_name = months[self.current_date.month]
        self.date_label.setText(f"Plan na {month_name} {self.current_date.year}")
        self.month_changed.emit(self.current_date)
        
    def previous_month(self):
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        self.update_label()
        
    def next_month(self):
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        self.update_label()

        
class TaskDetailsDialog(QDialog):
    def __init__(self, task_data, parent=None):
        super().__init__(parent)
        self.task_data = task_data
        self.db_manager = parent.db_manager if parent else None
        self.parent = parent
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Szczegóły zadania")
        self.setMinimumWidth(400)
        self.setMaximumHeight(600)
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border-radius: 8px;
            }
            QLabel {
                color: #333333;
                font-size: 12px;
            }
            QLabel#titleLabel {
                font-size: 14px;
                font-weight: bold;
                color: #4a90e2;
            }
            QLabel#headerLabel {
                font-weight: bold;
                color: #2c3e50;
                font-size: 12px;
                padding-top: 5px;
            }
            QTextEdit, QPlainTextEdit {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 4px;
                font-size: 12px;
                max-height: 60px;
                min-height: 40px;
            }
            QProgressBar {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                text-align: center;
                max-height: 15px;
            }
            QProgressBar::chunk {
                background-color: #4a90e2;
            }
            QPushButton#editButton {
                background-color: transparent;
                border: none;
                color: #4a90e2;
                padding: 2px;
            }
            QPushButton#editButton:hover {
                color: #357abd;
            }
            QCheckBox {
                font-size: 12px;
                padding-left: 20px;  /* Added padding for indentation */
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(15, 15, 15, 15)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_widget)
        self.scroll_layout.setSpacing(5)
        
        # Header section with title and basic info
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setSpacing(2)
        header_layout.setContentsMargins(0, 0, 0, 5)
        
        # Title container with edit button
        title_container = QWidget()
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)

        title_label = QLabel(self.task_data['title'])
        title_label.setObjectName("titleLabel")
        title_layout.addWidget(title_label)

        # Dodaj przycisk edycji dla wszystkich zadań (usuwamy warunek is_smart_goal)
        edit_button = QPushButton("Edytuj 🖊️")
        edit_button.setObjectName("editButton")
        edit_button.clicked.connect(self.edit_task)
        title_layout.addWidget(edit_button)
                
        header_layout.addWidget(title_container)
        
        # Status and deadline info
        info_widget = QWidget()
        info_layout = QHBoxLayout(info_widget)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(10)
        
        status_text = "✅ Zakończone" if self.task_data['status'] == 'completed' else "⏳ W trakcie"
        status_label = QLabel(status_text)
        status_label.setStyleSheet("color: " + ("#2ecc71" if self.task_data['status'] == 'completed' else "#666"))
        info_layout.addWidget(status_label)
        
        if self.task_data['deadline']:
            deadline = datetime.strptime(self.task_data['deadline'], '%Y-%m-%d').strftime('%d.%m.%Y')
            deadline_label = QLabel(f"📅 {deadline}")
            info_layout.addWidget(deadline_label)
        
        info_layout.addStretch()
        header_layout.addWidget(info_widget)
        self.scroll_layout.addWidget(header_widget)
        
        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #e0e0e0;")
        self.scroll_layout.addWidget(separator)
        
        # SMART goal specific content
        if self.task_data.get('is_smart_goal') and self.db_manager:
            with self.db_manager as db:
                smart_data = db.get_smart_goal(self.task_data['id'])
                if smart_data:
                    # Progress bar
                    if 'progress' in smart_data:
                        progress_widget = QWidget()
                        progress_layout = QHBoxLayout(progress_widget)
                        progress_layout.setContentsMargins(0, 5, 0, 5)

                        progress_bar = QProgressBar()
                        progress_bar.setMaximum(100)
                        progress_bar.setValue(smart_data['progress'])

                        # Usunięcie tekstu z paska
                        progress_bar.setStyleSheet("""
                            QProgressBar {
                                text-align: left;  /* Opcjonalnie zmienia pozycję tekstu */
                                color: transparent;  /* Ukrywa tekst wewnątrz paska */
                            }
                            QProgressBar::chunk {
                                background-color: #8bd88e;
                            }
                        """)

                        progress_label = QLabel(f"{smart_data['progress']}%")
                        progress_label.setStyleSheet("min-width: 45px;")  # Opcjonalne wyrównanie zewnętrzne

                        progress_layout.addWidget(QLabel("Postęp:"))
                        progress_layout.addWidget(progress_bar)
                        progress_layout.addWidget(progress_label)

                        self.scroll_layout.addWidget(progress_widget)
                    
                    # Subgoals section
                    subgoals = db.get_subgoals_by_goal(self.task_data['id'])
                    if subgoals:
                        subgoals_widget = QWidget()
                        subgoals_layout = QVBoxLayout(subgoals_widget)
                        subgoals_layout.setSpacing(2)

                        # Dodaj etykietę "Podcele:" z odpowiednim stylem
                        subgoals_label = QLabel("Podcele:")
                        subgoals_label.setObjectName("headerLabel")
                        subgoals_label.setStyleSheet("""
                            QLabel#headerLabel {
                                font-weight: bold;
                                color: #2c3e50;
                                font-size: 12px;
                                padding-top: 5px;
                                margin-bottom: 5px;  /* Dodane */
                                text-align: left;    /* Dodane */
                            }
                        """)
                        subgoals_layout.addWidget(subgoals_label)
                        subgoals_layout.addSpacing(5)  # Dodaje trochę przestrzeni po etykiecie

                        # Kontener na checkboxy podcelów
                        checkboxes_container = QWidget()
                        checkboxes_layout = QVBoxLayout(checkboxes_container)
                        checkboxes_layout.setContentsMargins(0, 0, 0, 0)
                        checkboxes_layout.setSpacing(2)

                        for subgoal in subgoals:
                            subgoal_container = QWidget()
                            subgoal_layout = QHBoxLayout(subgoal_container)
                            subgoal_layout.setContentsMargins(0, 0, 0, 0)

                            checkbox = QCheckBox(subgoal['title'])
                            checkbox.setChecked(subgoal['completed'])
                            checkbox.setStyleSheet("""
                                QCheckBox {
                                    padding: 5px;
                                    border-radius: 4px;
                                }
                                QCheckBox:hover {
                                    background-color: #f5f5f5;
                                }
                            """)
                            checkbox.stateChanged.connect(
                                lambda state, sg_id=subgoal['id']:
                                self.update_subgoal_status(sg_id, state == Qt.Checked)
                            )
                            
                            subgoal_layout.addWidget(checkbox)
                            checkboxes_layout.addWidget(subgoal_container)

                        # Dodaj kontener z checkboxami do głównego layoutu podcelów
                        subgoals_layout.addWidget(checkboxes_container)
                        
                        # Dodaj całość do głównego layoutu
                        self.scroll_layout.addWidget(subgoals_widget)
                    
                    # SMART criteria grid
                    smart_grid = QWidget()
                    grid_layout = QGridLayout(smart_grid)
                    grid_layout.setSpacing(5)
                    
                    criteria = [
                        ("S", "Specific", smart_data['specific']),
                        ("M", "Measurable", smart_data['measurable']),
                        ("A", "Achievable", smart_data['achievable']),
                        ("R", "Relevant", smart_data['relevant']),
                        ("T", "Time-bound", smart_data['time_bound'])
                    ]
                    
                    for row, (letter, name, value) in enumerate(criteria):
                        letter_label = QLabel(letter)
                        letter_label.setStyleSheet("font-weight: bold; color: #4a90e2; min-width: 15px;")
                        name_label = QLabel(name)
                        name_label.setStyleSheet("color: #666;")
                        
                        text = QPlainTextEdit()
                        text.setPlainText(value)
                        text.setReadOnly(True)
                        
                        grid_layout.addWidget(letter_label, row, 0)
                        grid_layout.addWidget(name_label, row, 1)
                        grid_layout.addWidget(text, row, 2)
                    
                    self.scroll_layout.addWidget(smart_grid)
        
        # Description section
        if self.task_data['description']:
            description_label = QLabel("Opis:")
            description_label.setObjectName("headerLabel")
            self.scroll_layout.addWidget(description_label)
            
            description_text = QTextEdit()
            description_text.setPlainText(self.task_data['description'])
            description_text.setReadOnly(True)
            self.scroll_layout.addWidget(description_text)
        
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        # Close button
        close_button = QPushButton("Zamknij")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                border: none;
                border-radius: 4px;
                color: white;
                padding: 5px 15px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button, alignment=Qt.AlignCenter)

    def update_subgoal_status(self, subgoal_id: int, completed: bool):
        """Updates the subgoal status and recalculates the main goal's progress."""
        with self.db_manager as db:
            db.update_subgoal_status(subgoal_id, completed)
            # Update main goal progress
            goal_id = db.get_goal_id_by_subgoal(subgoal_id)
            if goal_id:
                subgoals = db.get_subgoals_by_goal(goal_id)
                total = len(subgoals)
                completed_count = len([sg for sg in subgoals if sg['completed']])
                progress = int((completed_count / total) * 100) if total > 0 else 0
                db.update_goal_progress(goal_id, progress)
                
                # Refresh UI
                for widget in self.findChildren(QProgressBar):
                    widget.setValue(progress)
                for widget in self.findChildren(QLabel):
                    if widget.text().endswith('%'):
                        widget.setText(f"{progress}%")
                
        # Refresh parent view
        if self.parent and hasattr(self.parent, 'load_tasks'):
            self.parent.load_tasks()

    def edit_task(self):
        """Opens the task edit dialog."""
        if self.task_data.get('is_smart_goal'):
            # Istniejąca logika dla celów SMART
            ...
        else:
            # Logika dla zwykłych zadań
            dialog = TaskDialog(self.task_data.get('category_id'), self)
            # Wypełnij dane istniejącego zadania
            dialog.title_edit.setText(self.task_data['title'])
            if self.task_data.get('description'):
                dialog.description_edit.setPlainText(self.task_data['description'])
            if self.task_data.get('deadline'):
                date = datetime.strptime(self.task_data['deadline'], '%Y-%m-%d')
                dialog.calendar.setSelectedDate(date)
            
            if dialog.exec_() == QDialog.Accepted:
                updated_data = dialog.get_task_data()
                if self.db_manager:
                    with self.db_manager as db:
                        success = db.update_task(
                            task_id=self.task_data['id'],
                            title=updated_data['title'],
                            description=updated_data['description'],
                            deadline=updated_data['deadline']
                        )
                        if success:
                            # Aktualizuj dane w pamięci
                            self.task_data.update({
                                'title': updated_data['title'],
                                'description': updated_data['description'],
                                'deadline': updated_data['deadline']
                            })
                            
                            # Odśwież widok rodzica
                            if self.parent and hasattr(self.parent, 'load_tasks'):
                                self.parent.load_tasks()
                                
                            # Zamknij okno szczegółów
                            self.accept()
                            
                            # Pokaż zaktualizowane szczegóły
                            if self.parent:
                                self.parent.show_task_details(self.task_data)

def modify_task_widget(self, task_data):
    task_widget = QWidget()
    task_layout = QHBoxLayout(task_widget)
    task_widget.setStyleSheet("""
        QWidget {
            border-radius: 5px;
        }
        QWidget:hover {
            background-color: #f0f0f0;
        }
    """)
    
    checkbox = QCheckBox()
    checkbox.setChecked(task_data['status'] == 'completed')
    checkbox.stateChanged.connect(lambda state: self.update_task_status(task_data['id'], state))
    
    task_content = QWidget()
    task_content_layout = QVBoxLayout(task_content)
    task_content_layout.setSpacing(2)
    task_content_layout.setContentsMargins(0, 0, 0, 0)
    
    task_label = QLabel(task_data['title'])
    if task_data['status'] == 'completed':
        task_label.setStyleSheet("text-decoration: line-through; color: #888;")
    
    # Dodaj datę, jeśli istnieje
    if task_data['deadline']:
        deadline = datetime.strptime(task_data['deadline'], '%Y-%m-%d').strftime('%d.%m.%Y')
        deadline_label = QLabel(f"Termin: {deadline}")
        deadline_label.setStyleSheet("color: #666; font-size: 11px;")
        task_content_layout.addWidget(deadline_label)
    
    task_content_layout.addWidget(task_label)
    
    # Dodaj obsługę kliknięcia dla widgetu zadania
    task_content.mousePressEvent = lambda e: self.show_task_details(task_data)
    
    delete_button = QPushButton("🗑")
    delete_button.setFixedSize(24, 24)
    delete_button.setStyleSheet("""
        QPushButton {
            background-color: transparent;
            border: none;
            color: #999;
        }
        QPushButton:hover {
            color: #ff4444;
        }
    """)
    delete_button.clicked.connect(lambda: self.delete_task(task_data['id']))
    
    task_layout.addWidget(checkbox)
    task_layout.addWidget(task_content, stretch=1)
    task_layout.addWidget(delete_button)
    
    return task_widget

def show_task_details(self, task_data):
    dialog = TaskDetailsDialog(task_data, self)
    dialog.exec_()
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        print("Inicjalizacja MainWindow...")
        self.db_manager = DatabaseManager()
        print("DatabaseManager utworzony")
        self.setup_ui()
        self.refresh_quote()  # Dodana metoda do odświeżania cytatu
        self.current_view = 'tasks'
        print("Inicjalizacja zakończona")
        
    def refresh_quote(self):
        """Odświeża cytat w interfejsie."""
        with self.db_manager as db:
            quote = db.get_random_quote()
            if quote:
                self.quote_text.setText(f'"{quote["text"]}"')
                self.quote_author.setText(f"- {quote['author']}")
        
    def setup_ui(self):
        self.setWindowTitle("Mirai - Planer Celów")
        self.setMinimumSize(1000, 700)
        self.setStyleSheet('''
            QMainWindow {
                background-color: #f5f5f5;
                border-radius: 50px;
            }
            QScrollBar:vertical {
                width: 8px;
                background: transparent;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #c1c1c1;
                min-height: 30px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a8a8a8;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            QScrollBar:horizontal {
                height: 8px;
                background: transparent;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background-color: #c1c1c1;
                min-width: 30px;
                border-radius: 4px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #a8a8a8;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }
        ''')
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        # Górny pasek (tylko z cytatem)
        top_bar = QWidget()
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(5, 5, 5, 5)
        
        # Cytat (bez kontenera)
        quote_widget = QWidget()
        quote_layout = QVBoxLayout(quote_widget)
        quote_layout.setContentsMargins(0, 10, 100, 0)
        quote_layout.setSpacing(5)
        
        # Inicjalizuj puste etykiety dla cytatu
        self.quote_text = QLabel()
        self.quote_author = QLabel()
        
        self.quote_text.setStyleSheet("""
            QLabel {
                color: #666;
                font-size: 16px;
            }
        """)
        self.quote_author.setStyleSheet("""
            QLabel {
                color: #888;
            }
        """)
        self.quote_author.setAlignment(Qt.AlignRight)
        
        quote_layout.addWidget(self.quote_text)
        quote_layout.addWidget(self.quote_author)
        
        top_bar_layout.addStretch(1)
        top_bar_layout.addWidget(quote_widget)
        main_layout.addWidget(top_bar)
        
        # Kontener na widoki
        self.views_container = QWidget()
        self.views_layout = QVBoxLayout(self.views_container)
        main_layout.addWidget(self.views_container)
        
        # Widok zadań miesięcznych
        self.tasks_view = QWidget()
        self.setup_tasks_view()
        
        # Widok koła balansu
        self.balance_wheel = BalanceWheel(self.db_manager)
        
        # Widok planowania długoterminowego
        self.longterm_view = LongTermWindow(self.db_manager, self)
        
        # Dodaj widoki do kontenera
        self.views_layout.addWidget(self.tasks_view)
        self.views_layout.addWidget(self.balance_wheel)
        self.views_layout.addWidget(self.longterm_view)
        
        # Początkowo pokaż tylko widok zadań
        self.balance_wheel.hide()
        self.longterm_view.hide()
        
        # Dolny pasek z przyciskami
        bottom_bar = QWidget()
        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setContentsMargins(50, 10, 0, 10)
        
        # Panel przycisków
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)
        
        # Tworzenie przycisków
        self.switch_to_tasks_button = QPushButton("Plan na miesiąc")
        self.switch_to_balance_button = QPushButton("Koło Balansu")
        self.switch_to_longterm_button = QPushButton("Planowanie Długoterminowe")
        
        # Style dla przycisków
        # Style dla przycisków
        button_style = """
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton[active="true"] {
                background-color: #3b75ad;
                
            }
        """
        self.switch_to_tasks_button.setStyleSheet(button_style)
        self.switch_to_balance_button.setStyleSheet(button_style)
        self.switch_to_longterm_button.setStyleSheet(button_style)
        
        # Połączenie przycisków z funkcjami
        self.switch_to_tasks_button.clicked.connect(lambda: self.switch_view('tasks'))
        self.switch_to_balance_button.clicked.connect(lambda: self.switch_view('balance'))
        self.switch_to_longterm_button.clicked.connect(lambda: self.switch_view('longterm'))
        
        # Dodawanie przycisków do layoutu
        buttons_layout.addWidget(self.switch_to_tasks_button)
        buttons_layout.addWidget(self.switch_to_balance_button)
        buttons_layout.addWidget(self.switch_to_longterm_button)
        buttons_layout.addStretch(1)
        
        bottom_layout.addLayout(buttons_layout)
        main_layout.addWidget(bottom_bar)
        
        # Ustawienie początkowego aktywnego widoku
        self.update_active_button('tasks')
        
    def setup_tasks_view(self):
        tasks_layout = QVBoxLayout(self.tasks_view)
        
        # Główny kontener dla wszystkich elementów
        main_container = QFrame()
        main_container.setObjectName("mainTaskContainer")
        main_container.setStyleSheet("""
            #mainTaskContainer {
                background-color: white;
                border-radius: 55px;
                padding: 20px;
                margin: 5px;
            }
        """)
        main_container_layout = QVBoxLayout(main_container)
        
        # Dodaj selektor miesiąca i roku
        self.month_selector = MonthYearSelector()
        self.month_selector.month_changed.connect(self.refresh_tasks)
        main_container_layout.addWidget(self.month_selector)
        
        # Obszar przewijania dla bloków zadań
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_widget = QWidget()
        self.scroll_widget.setStyleSheet("background: transparent;")
        self.scroll_layout = QGridLayout(self.scroll_widget)
        self.scroll_layout.setSpacing(15)
        
        self.refresh_tasks(datetime.now())
        
        scroll_area.setWidget(self.scroll_widget)
        main_container_layout.addWidget(scroll_area)
        
        tasks_layout.addWidget(main_container)
    
    def refresh_tasks(self, selected_date):
        # Usuń istniejące bloki zadań
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Pobierz kategorie z bazy danych
        with self.db_manager as db:
            categories = db.get_all_categories()
            
        # Tworzenie bloków dla każdej kategorii
        for i, category in enumerate(categories):
            block = TaskBlock(category['id'], category['name'], 
                            self.db_manager, selected_date)
            self.scroll_layout.addWidget(block, i // 2, i % 2)

    def switch_view(self, view_name):
        """Przełącza widok aplikacji między zadaniami, kołem balansu i planowaniem długoterminowym."""
        # Ukryj wszystkie widoki
        self.tasks_view.hide()
        self.balance_wheel.hide()
        self.longterm_view.hide()
        
        # Pokaż wybrany widok
        if view_name == 'tasks':
            self.tasks_view.show()
            self.setWindowTitle("Mirai - Planer Celów")
        elif view_name == 'balance':
            self.balance_wheel.show()
            self.setWindowTitle("Mirai - Koło Balansu")
        elif view_name == 'longterm':
            self.longterm_view.show()
            self.setWindowTitle("Mirai - Planowanie Długoterminowe")
        
        self.current_view = view_name
        self.update_active_button(view_name)
    
    def update_active_button(self, active_view):
        """Aktualizuje style przycisków na podstawie aktywnego widoku."""
        self.switch_to_tasks_button.setProperty('active', active_view == 'tasks')
        self.switch_to_balance_button.setProperty('active', active_view == 'balance')
        self.switch_to_longterm_button.setProperty('active', active_view == 'longterm')
        
        # Wymuszenie odświeżenia stylów
        self.switch_to_tasks_button.style().unpolish(self.switch_to_tasks_button)
        self.switch_to_tasks_button.style().polish(self.switch_to_tasks_button)
        self.switch_to_balance_button.style().unpolish(self.switch_to_balance_button)
        self.switch_to_balance_button.style().polish(self.switch_to_balance_button)
        self.switch_to_longterm_button.style().unpolish(self.switch_to_longterm_button)
        self.switch_to_longterm_button.style().polish(self.switch_to_longterm_button)

    def set_tasks_container_color(self, color: str):
        """Zmienia kolor tła głównego kontenera zadań."""
        self.tasks_view.findChild(QFrame, "mainTaskContainer").setStyleSheet(f"""
            #mainTaskContainer {{
                background-color: {color};
                border-radius: 15px;
                padding: 20px;
                margin: 10px;
            }}
        """)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())