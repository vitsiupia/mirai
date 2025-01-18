from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QLabel, QLineEdit, QTextEdit, QComboBox, QWidget,
                           QScrollArea, QCheckBox, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from datetime import datetime

class SmartGoalsDialog(QDialog):
    def __init__(self, category_id, parent=None, goal_data=None):
        super().__init__(parent)
        self.category_id = category_id
        self.goal_data = goal_data
        self.setup_ui()
        if goal_data:
            self.load_goal_data(goal_data)
        
        # Połącz sygnał zmiany okresu z funkcją
        self.time_combo.currentTextChanged.connect(self.on_period_changed)
        
    def setup_ui(self):
        self.setWindowTitle("Cel SMART")
        self.setMinimumWidth(450)  # Zmniejszona szerokość
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
            }
            QLabel {
                color: #333333;
                font-size: 11px;
                font-weight: bold;
                margin-top: 5px;
            }
            QLineEdit, QTextEdit {
                padding: 5px;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                background-color: #f8f9fa;
                color: #333333;
                font-size: 11px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #4a90e2;
                background-color: #ffffff;
            }
            QPushButton {
                padding: 5px 10px;
                border-radius: 4px;
                font-weight: bold;
            }
            QComboBox {
                padding: 5px;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                background-color: #f8f9fa;
                color: #333333;
                font-size: 11px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(8)  # Zmniejszony spacing
        layout.setContentsMargins(15, 15, 15, 15)  # Zmniejszone marginesy

        # Title
        title_label = QLabel("Nazwa celu:")
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Wprowadź nazwę celu...")
        
        # S - Specific
        specific_label = QLabel("S - Co dokładnie chcesz osiągnąć?")
        self.specific_edit = QTextEdit()
        self.specific_edit.setPlaceholderText("Opisz szczegółowo swój cel...")
        self.specific_edit.setMaximumHeight(60)  # Zmniejszona wysokość
        
        # M - Measurable
        measurable_label = QLabel("M - Jak zmierzysz postęp?")
        self.measurable_edit = QTextEdit()
        self.measurable_edit.setPlaceholderText("Jakie konkretne miary zastosujesz...")
        self.measurable_edit.setMaximumHeight(60)
        
        # A - Achievable
        achievable_label = QLabel("A - Czy cel jest osiągalny?")
        self.achievable_edit = QTextEdit()
        self.achievable_edit.setPlaceholderText("Jakie zasoby są potrzebne...")
        self.achievable_edit.setMaximumHeight(60)
        
        # R - Relevant
        relevant_label = QLabel("R - Dlaczego ten cel jest istotny?")
        self.relevant_edit = QTextEdit()
        self.relevant_edit.setPlaceholderText("Jaki jest powód realizacji tego celu...")
        self.relevant_edit.setMaximumHeight(60)
        
        # T - Time-bound
        time_label = QLabel("T - Okres realizacji:")
        self.time_combo = QComboBox()
        self.time_combo.addItems(["5-10 lat", "1 rok", "6 miesięcy", "3 miesiące", "miesiąc"])
        
        # Dodaj kontener na wybór miesiąca
        self.month_container = QWidget()
        month_layout = QHBoxLayout(self.month_container)
        month_layout.setContentsMargins(0, 0, 0, 0)
        
        self.month_combo = QComboBox()
        months = ["Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec", 
                 "Lipiec", "Sierpień", "Wrzesień", "Październik", "Listopad", "Grudzień"]
        self.month_combo.addItems(months)
        
        # Ustaw bieżący miesiąc
        current_month = datetime.now().month
        self.month_combo.setCurrentIndex(current_month - 1)
        
        self.year_combo = QComboBox()
        current_year = datetime.now().year
        self.year_combo.addItems([str(year) for year in range(current_year, current_year + 5)])
        
        month_layout.addWidget(self.month_combo)
        month_layout.addWidget(self.year_combo)
        
        # Początkowo ukryj kontener wyboru miesiąca
        self.month_container.hide()
        
        # Subgoals button
        self.add_subgoal_button = QPushButton("+ Dodaj podcel")
        self.add_subgoal_button.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: none;
                color: #666;
                font-size: 11px;
                padding: 3px 8px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        self.add_subgoal_button.clicked.connect(self.add_subgoal)

        # Przyciski
        buttons_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Anuluj")
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #f8f9fa;
                border: 1px solid #e0e0e0;
                color: #666666;
                font-size: 11px;
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
                font-size: 11px;
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

        # Kontener na podcele (początkowo ukryty)
        self.subgoals_container = QWidget()
        self.subgoals_layout = QVBoxLayout(self.subgoals_container)
        self.subgoals_layout.setContentsMargins(0, 0, 0, 0)
        self.subgoals_layout.setSpacing(5)
        self.subgoals_container.hide()

        # Add all widgets to layout
       # Add all widgets to layout
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
        layout.addWidget(self.month_container)
        layout.addWidget(self.add_subgoal_button)
        layout.addWidget(self.subgoals_container)
        layout.addLayout(buttons_layout)  # Przeniesione na koniec

    def on_period_changed(self, text):
        """Obsługuje zmianę wybranego okresu."""
        if text == "miesiąc":
            self.month_container.show()
        else:
            self.month_container.hide()

    def add_subgoal(self):
        """Adds a new subgoal input field."""
        self.subgoals_container.show()  # Pokaż kontener gdy dodajemy pierwszy podcel
        
        subgoal_widget = QWidget()
        subgoal_layout = QHBoxLayout(subgoal_widget)
        subgoal_layout.setContentsMargins(0, 0, 0, 0)
        subgoal_layout.setSpacing(5)  # Dodane spacing między elementami
        
        checkbox = QCheckBox()
        checkbox.setStyleSheet("QCheckBox { spacing: 4px; }")
        
        subgoal_edit = QLineEdit()
        subgoal_edit.setPlaceholderText("Wpisz podcel...")
        subgoal_edit.setStyleSheet("""
            QLineEdit {
                padding: 4px;
                font-size: 11px;
            }
        """)
        
        delete_button = QPushButton("✖")  # Zmieniony symbol na ✖
        delete_button.setFixedSize(20, 20)
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #999;
                font-size: 14px;
                padding: 0px;
                margin: 0px;
            }
            QPushButton:hover {
                color: #ff4444;
                font-weight: bold;
            }
        """)
        delete_button.setCursor(Qt.PointingHandCursor)  # Dodany kursor wskazujący
        delete_button.clicked.connect(lambda: subgoal_widget.deleteLater())
        
        subgoal_layout.addWidget(checkbox)
        subgoal_layout.addWidget(subgoal_edit, stretch=1)
        subgoal_layout.addWidget(delete_button)
        
        self.subgoals_layout.addWidget(subgoal_widget)

    def get_subgoals(self):
        """Gets all subgoals data."""
        subgoals = []
        for i in range(self.subgoals_layout.count()):
            widget = self.subgoals_layout.itemAt(i).widget()
            if widget:
                checkbox = widget.findChild(QCheckBox)
                edit = widget.findChild(QLineEdit)
                if checkbox and edit and edit.text().strip():
                    subgoals.append({
                        'title': edit.text().strip(),
                        'completed': checkbox.isChecked()
                    })
        return subgoals

    def get_smart_goal_data(self):
        data = {
            'title': self.title_edit.text().strip(),
            'category_id': self.category_id,
            'specific': self.specific_edit.toPlainText().strip(),
            'measurable': self.measurable_edit.toPlainText().strip(),
            'achievable': self.achievable_edit.toPlainText().strip(),
            'relevant': self.relevant_edit.toPlainText().strip(),
            'time_bound': self.time_combo.currentText(),
            'subgoals': self.get_subgoals(),
            'target_month': None
        }
        
        if self.time_combo.currentText() == "miesiąc":
            month = self.month_combo.currentText()
            year = self.year_combo.currentText()
            data['target_month'] = f"{month} {year}"
            
        return data

    def load_goal_data(self, goal_data):
        """Loads existing goal data into the dialog."""
        self.setWindowTitle("Edytuj cel SMART")
        self.title_edit.setText(goal_data['title'])
        self.specific_edit.setPlainText(goal_data['specific'])
        self.measurable_edit.setPlainText(goal_data['measurable'])
        self.achievable_edit.setPlainText(goal_data['achievable'])
        self.relevant_edit.setPlainText(goal_data['relevant'])
        
        period_index = self.time_combo.findText(goal_data['time_bound'])
        if period_index >= 0:
            self.time_combo.setCurrentIndex(period_index)
            
        if goal_data['subgoals']:
            self.subgoals_container.show()
            for subgoal in goal_data['subgoals']:
                self.add_subgoal_with_data(subgoal)

        if goal_data.get('target_month'):
            self.time_combo.setCurrentText("miesiąc")
            self.month_container.show()
            month, year = goal_data['target_month'].split()
            month_index = self.month_combo.findText(month)
            year_index = self.year_combo.findText(year)
            if month_index >= 0:
                self.month_combo.setCurrentIndex(month_index)
            if year_index >= 0:
                self.year_combo.setCurrentIndex(year_index)

    def add_subgoal_with_data(self, subgoal_data):
        """Adds a new subgoal input field with existing data."""
        subgoal_widget = QWidget()
        subgoal_layout = QHBoxLayout(subgoal_widget)
        subgoal_layout.setContentsMargins(0, 0, 0, 0)
        
        checkbox = QCheckBox()
        checkbox.setChecked(subgoal_data.get('completed', False))
        
        subgoal_edit = QLineEdit()
        subgoal_edit.setText(subgoal_data['title'])
        
        delete_button = QPushButton("🗑")
        delete_button.setFixedSize(20, 20)
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #999;
                font-size: 12px;
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