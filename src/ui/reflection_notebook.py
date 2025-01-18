import os
import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
                           QTextEdit, QPushButton, QComboBox, QStackedWidget,
                           QDialog, QScrollArea, QListWidget, QListWidgetItem)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from datetime import datetime

class ReflectionDialog(QDialog):
    def __init__(self, category_name: str, content: str, parent=None):
        super().__init__(parent)
        self.setup_ui(category_name, content)
        
    def setup_ui(self, category_name: str, content: str):
        self.setWindowTitle(f"Refleksja - {category_name}")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        
        layout = QVBoxLayout(self)
        
        # Treść refleksji
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setText(content)
        text_edit.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        
        layout.addWidget(text_edit)
        
        # Przycisk zamknięcia
        close_button = QPushButton("Zamknij")
        close_button.clicked.connect(self.accept)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        
        layout.addWidget(close_button)

class ReflectionListItem(QWidget):
    clicked = pyqtSignal(str, str)
    
    def __init__(self, category_name: str, content: str, parent=None):
        super().__init__(parent)
        self.category_name = category_name
        self.full_content = content
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 8, 10, 0)  # Zmniejszony górny i dolny margines
        
        # Pojedynczy blok
        self.frame = QFrame()
        self.frame.setFixedWidth(525)
        self.frame.setFixedHeight(100) 
        self.frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 8px;
            }
            QFrame:hover {
                background-color: #e9ecef;
            }
        """)
        
        # Layout dla zawartości
        frame_layout = QVBoxLayout()
        frame_layout.setContentsMargins(10, 8, 10, 8)  # Zmniejszone marginesy wewnętrzne
        frame_layout.setSpacing(2)  # Zmniejszony odstęp między elementami
        
        # Nazwa kategorii
        category_label = QLabel(self.category_name)
        category_label.setFont(QFont("Segoe UI", 11, QFont.DemiBold))  # Zmniejszona czcionka
        category_label.setStyleSheet("color: #2c3e50;")
        frame_layout.addWidget(category_label)
        
        # Tekst
        preview = self.full_content[:200] + "..." if len(self.full_content) > 200 else self.full_content
        content_label = QLabel(preview)
        content_label.setWordWrap(True)
        content_label.setStyleSheet("""
            color: #666;
            font-size: 11px;
            line-height: 1.4;
        """)
        content_label.setMinimumHeight(20)  # Zmniejszona minimalna wysokość
        content_label.setMaximumHeight(50)  # Zmniejszona maksymalna wysokość
        frame_layout.addWidget(content_label)
        
        self.frame.setLayout(frame_layout)
        layout.addWidget(self.frame)
        
    def mousePressEvent(self, event):
        self.clicked.emit(self.category_name, self.full_content)

class ReflectionNotebook(QWidget):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setup_ui()
        
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 15px;
            }
        """)
        
        # Kontener na zawartość
        self.stacked_widget = QStackedWidget()
        
        # Strona z listą
        self.list_page = QFrame()
        self.setup_list_page()
        self.stacked_widget.addWidget(self.list_page)
        
        # Strona formularza
        self.form_page = QFrame()
        self.setup_form_page()
        self.stacked_widget.addWidget(self.form_page)
        
        main_layout.addWidget(self.stacked_widget)
        
    def setup_list_page(self):
        main_container = QWidget()
        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(0, 0, 0, 10)
        
        # Kontener na listę z przewijaniem
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumHeight(400)  # Minimalna wysokość obszaru przewijania
        scroll_area.setMaximumHeight(600)  # Maksymalna wysokość obszaru przewijania
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #f1f1f1;
                width: 10px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background-color: #c1c1c1;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a1a1a1;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        
        scroll_content = QWidget()
        self.reflections_layout = QVBoxLayout(scroll_content)
        self.reflections_layout.setContentsMargins(0, 0, 0, 0)
        self.reflections_layout.setSpacing(-40)
        
        self.list_layout = self.reflections_layout
        
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        
        # Przycisk "Dodaj nową notatkę" na dole
        new_button = QPushButton("Dodaj nową notatkę")
        new_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        new_button.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: 500;
                margin: 10px 40px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        main_layout.addWidget(new_button)
        
        # Ładowanie refleksji
        self.load_reflections()
        
        layout = QVBoxLayout(self.list_page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(main_container)
        
    def setup_form_page(self):
        layout = QVBoxLayout(self.form_page)
        layout.setContentsMargins(40, 30, 40, 30)  # Większe marginesy
        layout.setSpacing(20)  # Większe odstępy między elementami
        
        # Container na nagłówek i opis
        header_container = QFrame()
        header_container.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 10px;
            }
        """)
        header_layout = QVBoxLayout(header_container)
        header_layout.setSpacing(12)
        
        # Nagłówek
        header = QLabel("Pomyśl o tym co musisz osiągać, żeby ocenić wybraną kategorię na 10")
        header.setFont(QFont("Segoe UI", 13, QFont.Bold))
        header.setWordWrap(True)
        header.setStyleSheet("color: #2c3e50;")
        header_layout.addWidget(header)
        
        # Opis
        description = QLabel("Wyobraź sobie idealny scenariusz. Przeanalizuj co z tego da się realizować, "
                           "a co jest nieosiągalne. Następnie napisz plan z pomocą celów SMART")
        description.setWordWrap(True)
        description.setStyleSheet("color: #666; font-size: 12px; line-height: 1.4;")
        header_layout.addWidget(description)
        
        layout.addWidget(header_container)
        
        # Label dla wyboru kategorii
        category_label = QLabel("Wybierz kategorię:")
        category_label.setStyleSheet("color: #2c3e50; font-weight: 500; font-size: 12px; margin-top: 10px;")
        layout.addWidget(category_label)
        
        # Wybór kategorii
        self.category_combo = QComboBox()
        self.category_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                padding: 8px 15px;
                background-color: white;
                font-size: 12px;
                min-height: 40px;
            }
            QComboBox:hover {
                border-color: #4a90e2;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
        """)
        self.load_categories()
        layout.addWidget(self.category_combo)
        
        # Label dla notatki
        note_label = QLabel("Twoja notatka:")
        note_label.setStyleSheet("color: #2c3e50; font-weight: 500; font-size: 12px; margin-top: 10px;")
        layout.addWidget(note_label)
        
        # Pole tekstowe
        self.text_edit = QTextEdit()
        self.text_edit.setMinimumHeight(200)  # Większa wysokość pola tekstowego
        self.text_edit.setStyleSheet("""
            QTextEdit {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 15px;
                font-size: 12px;
                line-height: 1.5;
            }
            QTextEdit:focus {
                border-color: #4a90e2;
            }
        """)
        layout.addWidget(self.text_edit)
        
        # Kontener na przyciski na dole
        button_container = QFrame()
        button_container.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-top: 1px solid #eaeaea;
                padding: 15px;
                margin-top: 20px;
            }
        """)
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(10, 0, 10, 0)
        
        # Przycisk zapisz
        save_button = QPushButton("Zapisz")
        save_button.clicked.connect(self.save_reflection)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: 500;
                min-width: 120px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        
        # Przycisk usuń
        cancel_button = QPushButton("Usuń")
        cancel_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #f8f9fa;
                color: #dc3545;
                border: 1px solid #dc3545;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: 500;
                min-width: 120px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #dc3545;
                color: white;
            }
        """)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        button_layout.addStretch()
        
        layout.addWidget(button_container)
        
    def get_button_style(self):
        return """
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """
        
    def load_categories(self):
        with self.db_manager as db:
            categories = db.get_all_categories()
            self.category_combo.clear()
            for category in categories:
                self.category_combo.addItem(category['name'], category['id'])
                
    def load_reflections(self):
        """Ładuje wszystkie refleksje do widoku listy."""
        with self.db_manager as db:
            reflections = db.get_all_reflections()

        # Wyczyść istniejące widgety
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not reflections:  # Dodana obsługa przypadku braku refleksji
            no_reflections_label = QLabel("Brak zapisanych refleksji")
            no_reflections_label.setStyleSheet("""
                QLabel {
                    color: #666;
                    font-style: italic;
                    padding: 20px;
                }
            """)
            no_reflections_label.setAlignment(Qt.AlignCenter)
            self.list_layout.addWidget(no_reflections_label)
            return
        
        # DODAJ TEN BRAKUJĄCY KOD:
        for reflection in reflections:
            reflection_item = ReflectionListItem(
                reflection['category_name'], 
                reflection['content']
            )
            reflection_item.clicked.connect(self.show_reflection_dialog)
            self.list_layout.addWidget(reflection_item)
            
    def show_reflection_dialog(self, category_name: str, content: str):
        dialog = ReflectionDialog(category_name, content, self)
        dialog.exec_()
        
    def save_reflection(self):
        category_id = self.category_combo.currentData()
        content = self.text_edit.toPlainText()
        
        if not content.strip():
            return
            
        with self.db_manager as db:
            # Sprawdź czy istnieje refleksja dla tej kategorii
            existing = db.get_reflection(category_id)
            if existing:
                db.update_reflection(category_id, content)
            else:
                db.add_reflection(category_id, content)
                
        # Wyczyść formularz i przełącz na listę
        self.text_edit.clear()
        self.stacked_widget.setCurrentIndex(0)
        self.load_reflections()  # Odśwież listę