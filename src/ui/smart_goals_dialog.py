from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QLabel, QLineEdit, QTextEdit, QComboBox, QWidget,
                           QScrollArea, QCheckBox, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from datetime import datetime

class SmartGoalsDialog(QDialog):
    def __init__(self, category_id, parent=None):
        super().__init__(parent)
        self.category_id = category_id
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Cel SMART")
        self.setMinimumWidth(600)
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
            QComboBox {
                padding: 8px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                background-color: #f8f9fa;
                color: #333333;
                font-size: 13px;
            }
            QPushButton {
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
                min-width: 100px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title_label = QLabel("Nazwa celu:")
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Wprowadź nazwę celu...")
        
        # S - Specific
        specific_label = QLabel("S (Specific) - Co dokładnie chcesz osiągnąć?")
        self.specific_edit = QTextEdit()
        self.specific_edit.setPlaceholderText("Opisz szczegółowo swój cel...")
        self.specific_edit.setMaximumHeight(100)
        
        # M - Measurable
        measurable_label = QLabel("M (Measurable) - Jak zmierzysz postęp?")
        self.measurable_edit = QTextEdit()
        self.measurable_edit.setPlaceholderText("Jakie konkretne miary zastosujesz...")
        self.measurable_edit.setMaximumHeight(100)
        
        # A - Achievable
        achievable_label = QLabel("A (Achievable) - Czy cel jest osiągalny?")
        self.achievable_edit = QTextEdit()
        self.achievable_edit.setPlaceholderText("Jakie zasoby są potrzebne...")
        self.achievable_edit.setMaximumHeight(100)
        
        # R - Relevant
        relevant_label = QLabel("R (Relevant) - Dlaczego ten cel jest istotny?")
        self.relevant_edit = QTextEdit()
        self.relevant_edit.setPlaceholderText("Jaki jest powód realizacji tego celu...")
        self.relevant_edit.setMaximumHeight(100)
        
        # T - Time-bound
        time_label = QLabel("T (Time-bound) - Okres realizacji:")
        self.time_combo = QComboBox()
        self.time_combo.addItems(["5-10 lat", "1 rok", "6 miesięcy", "3 miesiące", "1 miesiąc"])

        # Sub-goals section
        subgoals_label = QLabel("Podcele:")
        self.subgoals_container = QWidget()
        self.subgoals_layout = QVBoxLayout(self.subgoals_container)
        
        # Add subgoal button
        self.add_subgoal_button = QPushButton("+ Dodaj podcel")
        self.add_subgoal_button.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: none;
                color: #666;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        self.add_subgoal_button.clicked.connect(self.add_subgoal)

        # Create scroll area for subgoals
        scroll = QScrollArea()
        scroll.setWidget(self.subgoals_container)
        scroll.setWidgetResizable(True)
        scroll.setMaximumHeight(150)

        # Buttons
        buttons_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Anuluj")
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #f8f9fa;
                border: 2px solid #e0e0e0;
                color: #666666;
            }
            QPushButton:hover {
                background-color: #e9ecef;
            }
        """)
        self.save_button = QPushButton("Zapisz")
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                border: none;
                color: white;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        
        self.cancel_button.clicked.connect(self.reject)
        self.save_button.clicked.connect(self.accept)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.save_button)

        # Add everything to main layout
        layout.addWidget(title_label)
        layout.addWidget(self.title_edit)
        layout.addWidget(specific_label)
        layout.addWidget(self.specific_edit)
        layout.addWidget(measurable_label)
        layout.addWidget(self.measurable_edit)
        layout.addWidget(achievable_label)
        layout.addWidget(self.achievable_edit)
        layout.addWidget(relevant_label)
        layout.addWidget(self.relevant_edit)
        layout.addWidget(time_label)
        layout.addWidget(self.time_combo)
        layout.addWidget(subgoals_label)
        layout.addWidget(scroll)
        layout.addWidget(self.add_subgoal_button)
        layout.addLayout(buttons_layout)

    def add_subgoal(self):
        subgoal_widget = QWidget()
        subgoal_layout = QHBoxLayout(subgoal_widget)
        
        checkbox = QCheckBox()
        subgoal_edit = QLineEdit()
        subgoal_edit.setPlaceholderText("Wpisz podcel...")
        
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
        delete_button.clicked.connect(lambda: subgoal_widget.deleteLater())
        
        subgoal_layout.addWidget(checkbox)
        subgoal_layout.addWidget(subgoal_edit, stretch=1)
        subgoal_layout.addWidget(delete_button)
        
        self.subgoals_layout.addWidget(subgoal_widget)

    def get_subgoals(self):
        subgoals = []
        for i in range(self.subgoals_layout.count()):
            widget = self.subgoals_layout.itemAt(i).widget()
            if widget:
                checkbox = widget.findChild(QCheckBox)
                edit = widget.findChild(QLineEdit)
                if checkbox and edit:
                    subgoals.append({
                        'title': edit.text(),
                        'completed': checkbox.isChecked()
                    })
        return subgoals

    def get_smart_goal_data(self):
    # Zbierz wszystkie podczęści
        subgoals = []
        for i in range(self.subgoals_layout.count()):
            widget = self.subgoals_layout.itemAt(i).widget()
            if widget:
                checkbox = widget.findChild(QCheckBox)
                edit = widget.findChild(QLineEdit)
                if checkbox and edit and edit.text().strip():  # Sprawdź czy tekst nie jest pusty
                    subgoals.append({
                        'title': edit.text().strip(),
                        'completed': checkbox.isChecked()
                    })

        # Zwróć kompletne dane celu SMART
        return {
            'title': self.title_edit.text().strip(),
            'category_id': self.category_id,
            'specific': self.specific_edit.toPlainText().strip(),
            'measurable': self.measurable_edit.toPlainText().strip(),
            'achievable': self.achievable_edit.toPlainText().strip(),
            'relevant': self.relevant_edit.toPlainText().strip(),
            'time_bound': self.time_combo.currentText(),
            'subgoals': subgoals
        }