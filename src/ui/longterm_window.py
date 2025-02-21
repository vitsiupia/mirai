import os
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QLabel, QFrame, QScrollArea, 
                           QComboBox, QGridLayout, QDialog, QLineEdit, 
                           QCalendarWidget, QTextEdit, QMessageBox, QCheckBox, QSizePolicy, QProgressBar)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.ui.smart_goals_dialog import SmartGoalsDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from datetime import datetime



class LongTermTaskDialog(QDialog):
    def __init__(self, category_id, period, parent=None):
        super().__init__(parent)
        self.category_id = category_id
        self.period = period
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Dodaj nowy cel długoterminowy")
        self.setMinimumWidth(500)
        layout = QVBoxLayout(self)
        
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Nazwa celu")
        self.title_edit.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(self.title_edit)
        
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Opis celu")
        self.description_edit.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(self.description_edit)
        
        deadline_label = QLabel("Termin realizacji:")
        layout.addWidget(deadline_label)
        
        self.calendar = QCalendarWidget()
        self.calendar.setStyleSheet("""
            QCalendarWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QCalendarWidget QToolButton {
                color: #333;
            }
        """)
        layout.addWidget(self.calendar)
        
        buttons_layout = QHBoxLayout()
        
        save_button = QPushButton("Zapisz")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        save_button.clicked.connect(self.accept)
        
        cancel_button = QPushButton("Anuluj")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        cancel_button.clicked.connect(self.reject)
        
        smart_button = QPushButton("Dodaj jako cel SMART")
        smart_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        smart_button.clicked.connect(self.show_smart_dialog)
        
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(smart_button)
        buttons_layout.addWidget(cancel_button)
        layout.addLayout(buttons_layout)

    def show_smart_dialog(self):
        from smart_goals_dialog import SmartGoalsDialog  
        dialog = SmartGoalsDialog(self.category_id, self)
        if dialog.exec_() == QDialog.Accepted:
            self.accept()
    
    def get_task_data(self):
        return {
            'title': self.title_edit.text(),
            'description': self.description_edit.toPlainText(),
            'deadline': self.calendar.selectedDate().toString("yyyy-MM-dd"),
            'category_id': self.category_id,
            'period': self.period
        }


class LongTermTaskBlock(QFrame):
    def __init__(self, category_id, category_name, period, db_manager, parent=None):
        super().__init__(parent)
        self.category_id = category_id
        self.category_name = category_name
        self.period = period
        self.db_manager = db_manager
        self.setup_ui()
        self.load_smart_goals()

    def setup_ui(self):
        self.setObjectName("taskBlock")
        self.setMinimumWidth(450)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)  
        self.setStyleSheet("""
            #taskBlock {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #e0e0e0;
                padding: 15px;
            }
        """)
        
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(8)
        self.layout.setContentsMargins(15, 15, 15, 15)
        
        header_container = QWidget()
        header_layout = QVBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(3)
        
        self.category_label = QLabel(self.category_name)
        self.category_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.category_label.setStyleSheet("color: #333333;")
        header_layout.addWidget(self.category_label)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #e0e0e0; margin: 3px 0;")
        header_layout.addWidget(separator)
        
        self.layout.addWidget(header_container)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
        """)
        
        self.tasks_container = QWidget()
        self.tasks_layout = QVBoxLayout(self.tasks_container)
        self.tasks_layout.setContentsMargins(0, 0, 0, 0)
        self.tasks_layout.setSpacing(4)
        self.tasks_layout.setAlignment(Qt.AlignTop)
        
        scroll_area.setWidget(self.tasks_container)
        self.layout.addWidget(scroll_area)
        
        add_button = QPushButton("+ Dodaj cel SMART")
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: none;
                border-radius: 4px;
                padding: 8px;
                color: #69a6f1;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        add_button.clicked.connect(self.show_add_smart_goal_dialog)
        self.layout.addWidget(add_button)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'tasks_layout'):
            content_height = self.tasks_layout.sizeHint().height()
            min_height = max(300, content_height + 150)  
            self.setMinimumHeight(min_height)

    def show_goal_details(self, goal_data):
        dialog = GoalDetailsDialog(goal_data, self)
        dialog.exec_()

    def add_goal_widget(self, goal_data):
        goal_widget = QFrame()
        goal_widget.setCursor(Qt.PointingHandCursor)  
        goal_widget.mousePressEvent = lambda e: self.show_goal_details(goal_data)
        goal_widget.setStyleSheet("""
            QFrame {
                border: 1px solid #f0f0f0;
                border-radius: 4px;
                background-color: #ffffff;
                padding: 8px;
                margin: 2px 0;
            }
            QFrame:hover {
                background-color: #f8f9fa;
                border-color: #e0e0e0;
            }
        """)
        
        goal_layout = QVBoxLayout(goal_widget)
        goal_layout.setSpacing(4)
        goal_layout.setContentsMargins(8, 8, 8, 8)
        
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QLabel(goal_data['title'])
        title_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        if goal_data['status'] == 'completed':
            title_label.setStyleSheet("text-decoration: line-through; color: #888;")
        
        progress_bar = QProgressBar()
        progress_bar.setValue(goal_data['progress'])
        progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #ddd;
                border-radius: 4px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 4px;
            }
        """)
        
        edit_button = QPushButton("🖊️")
        edit_button.setFixedSize(22, 22)
        edit_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #999;
                font-size: 14px;
            }
            QPushButton:hover {
                color: #4a90e2;
            }
        """)
        edit_button.clicked.connect(lambda: self.edit_smart_goal(goal_data['id']))
        
        delete_button = QPushButton("🗑")
        delete_button.setFixedSize(22, 22)
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #999;
                font-size: 14px;
            }
            QPushButton:hover {
                color: #ff4444;
            }
        """)
        delete_button.clicked.connect(lambda: self.delete_smart_goal(goal_data['id']))
        
        header_layout.addWidget(title_label, stretch=1)
        header_layout.addWidget(progress_bar, stretch=2)
        header_layout.addWidget(edit_button)
        header_layout.addWidget(delete_button)
        
        goal_layout.addWidget(header_widget)
        
        if goal_data['subgoals']:
            subgoals_widget = QWidget()
            subgoals_layout = QVBoxLayout(subgoals_widget)
            subgoals_layout.setContentsMargins(10, 2, 0, 0)
            subgoals_layout.setSpacing(3)
            
            for subgoal in goal_data['subgoals']:
                subgoal_widget = QWidget()
                subgoal_layout = QHBoxLayout(subgoal_widget)
                subgoal_layout.setContentsMargins(0, 0, 0, 0)
                
                checkbox = QCheckBox()
                checkbox.setChecked(subgoal['completed'])
                checkbox.setStyleSheet("QCheckBox { spacing: 5px; }")
                checkbox.stateChanged.connect(
                    lambda state, sid=subgoal['id']: 
                    self.update_subgoal_status(sid, state == Qt.Checked)
                )
                
                subgoal_label = QLabel(subgoal['title'])
                subgoal_label.setStyleSheet("font-size: 11px;")
                if subgoal['completed']:
                    subgoal_label.setStyleSheet("text-decoration: line-through; color: #888; font-size: 11px;")
                
                subgoal_layout.addWidget(checkbox)
                subgoal_layout.addWidget(subgoal_label, stretch=1)
                
                subgoals_layout.addWidget(subgoal_widget)
            
            goal_layout.addWidget(subgoals_widget)
        
        self.tasks_layout.addWidget(goal_widget)

    def edit_smart_goal(self, goal_id):
        try:
            with self.db_manager as db:
                goal_data = db.get_smart_goal_details(goal_id)
                
            if goal_data:
                dialog = SmartGoalsDialog(self.category_id, self, goal_data)
                if dialog.exec_() == QDialog.Accepted:
                    updated_data = dialog.get_smart_goal_data()
                    with self.db_manager as db:
                        if db.update_smart_goal(goal_id, updated_data):
                            self.load_smart_goals()  # Odśwież widok
                        else:
                            QMessageBox.critical(self, "Błąd", "Nie udało się zaktualizować celu SMART")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas edycji celu: {str(e)}")


    def show_add_smart_goal_dialog(self):
        try:
            dialog = SmartGoalsDialog(self.category_id, self)
            if dialog.exec_() == QDialog.Accepted:
                goal_data = dialog.get_smart_goal_data()
                print("Otrzymane dane celu SMART:", goal_data)  

                with self.db_manager as db:
                    task_id = db.add_smart_goal(goal_data)
                    print(f"Utworzono cel SMART z ID: {task_id}")  
                
                print("Odświeżanie widoku celów...")  
                self.load_smart_goals()
                print("Zakończono odświeżanie widoku.")  
        except Exception as e:
            print(f"Błąd podczas dodawania celu SMART: {e}")
            QMessageBox.critical(self, "Błąd", f"Nie udało się dodać celu SMART: {str(e)}")

    def delete_smart_goal(self, goal_id):
        with self.db_manager as db:
            db.delete_smart_goal(goal_id)
        self.load_smart_goals()

    def update_subgoal_status(self, subgoal_id, completed):
        with self.db_manager as db:
            db.update_subgoal_status(subgoal_id, completed)
            
            goal_id = db.get_goal_id_by_subgoal(subgoal_id)
            
            subgoals = db.get_subgoals_by_goal(goal_id)
            completed_count = sum(1 for s in subgoals if s['completed'])
            progress = int((completed_count / len(subgoals)) * 100) if subgoals else 0
            
            db.update_goal_progress(goal_id, progress)
            
        self.load_smart_goals()

    def load_smart_goals(self):
        while self.tasks_layout.count():
            child = self.tasks_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        with self.db_manager as db:
            goals = db.get_smart_goals_by_period(self.category_id, self.period)
            
        for goal in goals:
            self.add_goal_widget(goal)

class LongTermWindow(QMainWindow):
    def __init__(self, db_manager=None, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.parent = parent
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Mirai - Planowanie Długoterminowe")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet("QMainWindow { background-color: #f5f5f5; }")
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        self.main_container = QFrame()
        self.main_container.setObjectName("mainTaskContainer")
        self.main_container.setStyleSheet("""
            #mainTaskContainer {
                background-color: white;
                border-radius: 50px;
                padding: 20px;
                margin: 0px;
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
        """)
        
        self.main_container_layout = QVBoxLayout(self.main_container)
        self.main_container_layout.setSpacing(20)
        
        self.header_container = QWidget()
        self.header_layout = QHBoxLayout(self.header_container)
        self.header_layout.setSpacing(15)
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        self.header_layout.setAlignment(Qt.AlignCenter)

        self.period_header = QLabel("Plan na:")
        self.period_header.setFont(QFont("Segoe UI", 24, QFont.Bold))
        self.period_header.setStyleSheet("""
            color: #2c3e50;
        """)

        self.period_combo = QComboBox()
        self.period_combo.addItems(["5-10 lat", "1 rok", "6 miesięcy", "3 miesiące"])
        
        self.period_combo.setStyleSheet("""
        QComboBox {
            background-color: white;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 8px;
            min-width: 180px;
            font-size: 20px;
            color: #2c3e50;
        }
    
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 40px;
            
            border-top-right-radius: 8px;
            border-bottom-right-radius: 8px;
        }
        
        QComboBox::down-arrow {
            width: 20px;
            height: 20px;
            color: #2c3e50;
        }
    """)


        self.period_combo.setEditable(True)
        self.period_combo.lineEdit().setAlignment(Qt.AlignCenter)
        self.period_combo.setEditable(False)

        self.period_combo.setFixedWidth(200)
        self.period_combo.setEditable(False)

        self.header_layout.addWidget(self.period_header)
        self.header_layout.addWidget(self.period_combo)

        self.main_container_layout.addWidget(self.header_container)
        self.main_container_layout.setAlignment(self.header_container, Qt.AlignCenter)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        self.scroll_widget = QWidget()
        self.scroll_layout = QGridLayout(self.scroll_widget)
        self.scroll_layout.setSpacing(20)
        self.scroll_layout.setContentsMargins(20, 20, 20, 20)
        self.scroll_layout.setColumnMinimumWidth(0, 480)
        self.scroll_layout.setColumnMinimumWidth(1, 480)
        self.scroll_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        
        scroll_area.setWidget(self.scroll_widget)
        self.main_container_layout.addWidget(scroll_area)
        
        main_layout.addWidget(self.main_container)
        
        self.period_combo.currentTextChanged.connect(self.load_period_tasks)
        
        self.load_period_tasks(self.period_combo.currentText())

    def load_period_tasks(self, period):
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        with self.db_manager as db:
            categories = db.get_all_categories()
        
        if len(categories) % 2 == 1:
            categories.append(None)
            
        for i, category in enumerate(categories):
            if category:
                block = LongTermTaskBlock(
                    category['id'],
                    category['name'],
                    period,
                    self.db_manager
                )
            else:
                block = QWidget()
                block.setFixedSize(520, 380)
            
            self.scroll_layout.addWidget(block, i // 2, i % 2)

class GoalDetailsDialog(QDialog):
    def __init__(self, goal_data, parent=None):
        super().__init__(parent)
        self.goal_data = goal_data
        self.db_manager = parent.db_manager if parent else None
        self.parent = parent
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Szczegóły Celu")
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        header = QHBoxLayout()
        title = QLabel(self.goal_data['title'])
        title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        title.setStyleSheet("color: #69a6f1;")
        header.addWidget(title)
        
        edit_button = QPushButton("🖊️")
        edit_button.setFixedSize(30, 30)
        edit_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover { color: #4a90e2; }
        """)
        edit_button.clicked.connect(lambda: self.parent.edit_smart_goal(self.goal_data['id']))
        header.addWidget(edit_button)
        layout.addLayout(header)

        info_layout = QHBoxLayout()
        status_text = "✅ Zakończone" if self.goal_data['status'] == 'completed' else "⏳ W trakcie"
        status_label = QLabel(status_text)
        status_label.setStyleSheet(f"color: {'#2ecc71' if self.goal_data['status'] == 'completed' else '#666'};")
        info_layout.addWidget(status_label)
        info_layout.addStretch()
        layout.addLayout(info_layout)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #e0e0e0; margin: 5px 0;")
        layout.addWidget(separator)
        
        progress_layout = QHBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(self.goal_data['progress'])
        self.progress_bar.setFormat("%p%")  
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #ddd;
                border-radius: 4px;
                text-align: center;
                height: 15px;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
            }
        """)
        progress_layout.addWidget(self.progress_bar)
        layout.addLayout(progress_layout)

        smart_frame = QFrame()
        smart_frame.setStyleSheet("""
            QFrame { 
                background-color: #f8f9fa; 
                border-radius: 4px; 
                padding: 10px; 
            }
        """)
        smart_layout = QVBoxLayout(smart_frame)
        smart_layout.setSpacing(8)  
        
        criteria = [
            ("S", "Specific", "Konkretny", self.goal_data['specific']),
            ("M", "Measurable", "Mierzalny", self.goal_data['measurable']),
            ("A", "Achievable", "Osiągalny", self.goal_data['achievable']),
            ("R", "Relevant", "Istotny", self.goal_data['relevant']),
            ("T", "Time-bound", "Określony w czasie", self.goal_data['time_bound'])
        ]
        
        for letter, eng_name, pl_name, content in criteria:
            criterion_layout = QHBoxLayout()
            criterion_layout.setSpacing(10)  
            
            labels_widget = QWidget()
            labels_widget.setFixedWidth(230)  
            labels_layout = QHBoxLayout(labels_widget)
            labels_layout.setContentsMargins(0, 0, 0, 0)
            
            letter_label = QLabel(letter)
            letter_label.setFixedWidth(15)
            letter_label.setStyleSheet("""
                font-weight: bold; 
                color: #4a90e2;
            """)
            
            name_label = QLabel(f"{eng_name} - {pl_name}")
            name_label.setStyleSheet("color: #666;")
            
            labels_layout.addWidget(letter_label)
            labels_layout.addWidget(name_label)
            labels_layout.addStretch()
            
            content_label = QLabel(content)
            content_label.setWordWrap(True)
            content_label.setMinimumWidth(200)  
            content_label.setStyleSheet("""
                QLabel {
                    background-color: white;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    padding: 8px;
                    min-height: 20px;
                }
            """)
            
            criterion_layout.addWidget(labels_widget)
            criterion_layout.addWidget(content_label, 1) 
            smart_layout.addLayout(criterion_layout)
            
        layout.addWidget(smart_frame)
        
        if self.goal_data.get('subgoals'):
            subgoals_frame = QFrame()
            subgoals_frame.setStyleSheet("QFrame { background-color: #f8f9fa; border-radius: 4px; padding: 10px; }")
            subgoals_layout = QVBoxLayout(subgoals_frame)
            
            subgoals_label = QLabel("Podcele:")
            subgoals_label.setStyleSheet("font-weight: bold;")
            subgoals_layout.addWidget(subgoals_label)
            
            for subgoal in self.goal_data['subgoals']:
                checkbox = QCheckBox(subgoal['title'])
                checkbox.setChecked(subgoal['completed'])
                checkbox.setEnabled(False)
                checkbox.setStyleSheet("padding: 2px;")
                subgoals_layout.addWidget(checkbox)
            
            layout.addWidget(subgoals_frame)
        
        close_button = QPushButton("Zamknij")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button, alignment=Qt.AlignRight)

def main():
    app = QApplication(sys.argv)
    from database import DatabaseManager
    db_manager = DatabaseManager()
    window = LongTermWindow(db_manager=db_manager)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()