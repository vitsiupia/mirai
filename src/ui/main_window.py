import os
import sys
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QLabel, QFrame, QScrollArea,
                           QGridLayout, QCheckBox, QSpacerItem, QSizePolicy,
                           QDialog, QLineEdit, QCalendarWidget, QTextEdit, QMessageBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.database.database import DatabaseManager
from src.ui.balance_wheel import BalanceWheel
from src.ui.longterm_window import LongTermWindow  # Dodany import
from datetime import datetime

class TaskDialog(QDialog):
    def __init__(self, category_id, parent=None):
        super().__init__(parent)
        self.category_id = category_id
        self.setup_ui()
        
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
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.save_button)
        
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
    def __init__(self, category_id, category_name, db_manager, parent=None):
        super().__init__(parent)
        self.category_id = category_id
        self.category_name = category_name
        self.db_manager = db_manager
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
            add_button = QPushButton("+ Dodaj zadanie")
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
        with self.db_manager as db:  # Użycie context managera
            tasks = db.get_tasks_by_category(self.category_id)
            
        # Usuń istniejące zadania z layoutu
        for i in reversed(range(self.tasks_layout.count())): 
            widget = self.tasks_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        # Dodaj zadania
        for task in tasks:
            self.add_task_widget(task)

    def add_task_widget(self, task_data):
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
        task_content_layout.addWidget(task_label)
        
        # Dodaj datę, jeśli istnieje
        if task_data['deadline']:
            deadline = datetime.strptime(task_data['deadline'], '%Y-%m-%d').strftime('%d.%m.%Y')
            deadline_label = QLabel(f"Termin: {deadline}")
            deadline_label.setStyleSheet("color: #666; font-size: 11px;")
            task_content_layout.addWidget(deadline_label)
        
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

class TaskDetailsDialog(QDialog):
    def __init__(self, task_data, parent=None):
        super().__init__(parent)
        self.task_data = task_data
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Szczegóły zadania")
        self.setMinimumWidth(400)
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border-radius: 10px;
            }
            QLabel {
                color: #333333;
                font-size: 13px;
            }
            QLabel#titleLabel {
                font-size: 16px;
                font-weight: bold;
                color: #4a90e2;
                padding: 5px 0;
            }
            QLabel#deadlineLabel {
                color: #666666;
                font-style: italic;
            }
            QTextEdit {
                border: none;
                background-color: #f8f9fa;
                border-radius: 5px;
                padding: 10px;
                color: #333333;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Tytuł zadania
        title_label = QLabel(self.task_data['title'])
        title_label.setObjectName("titleLabel")
        layout.addWidget(title_label)
        
        # Termin wykonania
        if self.task_data['deadline']:
            deadline = datetime.strptime(self.task_data['deadline'], '%Y-%m-%d').strftime('%d.%m.%Y')
            deadline_label = QLabel(f"Termin wykonania: {deadline}")
        else:
            deadline_label = QLabel("Brak terminu wykonania")
        deadline_label.setObjectName("deadlineLabel")
        layout.addWidget(deadline_label)
        
        # Status
        status_text = "Zakończone" if self.task_data['status'] == 'completed' else "W trakcie"
        status_label = QLabel(f"Status: {status_text}")
        layout.addWidget(status_label)
        
        # Opis
        if self.task_data['description']:
            description_label = QLabel("Szczegóły:")
            layout.addWidget(description_label)
            
            description_text = QTextEdit()
            description_text.setPlainText(self.task_data['description'])
            description_text.setReadOnly(True)
            description_text.setMinimumHeight(100)
            layout.addWidget(description_text)
        
        # Przycisk zamknięcia
        close_button = QPushButton("Zamknij")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                border: none;
                border-radius: 5px;
                color: white;
                padding: 8px 16px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        close_button.clicked.connect(self.accept)
        
        layout.addWidget(close_button, alignment=Qt.AlignCenter)

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
        self.current_view = 'tasks'  # tasks, balance, longterm
        print("Inicjalizacja zakończona")
        
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
        top_bar_layout.setContentsMargins(10, 10, 10, 10)
        
        # Cytat (bez kontenera)
        quote_widget = QWidget()
        quote_layout = QVBoxLayout(quote_widget)
        quote_layout.setContentsMargins(0, 0, 100, 0)
        quote_layout.setSpacing(5)
        
        with self.db_manager as db:
            quote = db.get_random_quote()
            if quote:
                self.quote_text = QLabel(f'"{quote["text"]}"')
                self.quote_author = QLabel(f"- {quote['author']}")
                
                self.quote_text.setStyleSheet("""
                    QLabel {
                        color: #666;
                        font-style: italic;
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
                background-color: #2c3e50;
                border: 1px solid #1a2530;
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
        
        # Lokalizacja miesięcy
        months = {
            'January': 'Styczeń', 'February': 'Luty', 'March': 'Marzec',
            'April': 'Kwiecień', 'May': 'Maj', 'June': 'Czerwiec',
            'July': 'Lipiec', 'August': 'Sierpień', 'September': 'Wrzesień',
            'October': 'Październik', 'November': 'Listopad', 'December': 'Grudzień'
        }
        
        current_month = datetime.now().strftime("%B %Y")
        month_name = months[datetime.now().strftime("%B")]
        header = QLabel(f"Plan na {month_name} {datetime.now().year}")
        header.setFont(QFont("Segoe UI", 24, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("""
            QLabel {
                color: #333333;
                margin-bottom: 20px;
            }
        """)
        main_container_layout.addWidget(header)
        
        # Obszar przewijania dla bloków zadań
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet("background: transparent;")
        scroll_layout = QGridLayout(scroll_widget)
        scroll_layout.setSpacing(15)
        
        # Pobierz kategorie z bazy danych
        with self.db_manager as db:
            categories = db.get_all_categories()
            
        # Tworzenie bloków dla każdej kategorii
        for i, category in enumerate(categories):
            block = TaskBlock(category['id'], category['name'], self.db_manager)
            scroll_layout.addWidget(block, i // 2, i % 2)
        
        scroll_area.setWidget(scroll_widget)
        main_container_layout.addWidget(scroll_area)
        
        tasks_layout.addWidget(main_container)

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