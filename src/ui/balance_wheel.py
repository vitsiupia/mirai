import os
import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QFrame, QSlider, QSpinBox, QScrollArea,QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from datetime import datetime
import matplotlib
matplotlib.rcParams['font.family'] = ['Segoe UI Emoji', 'Arial', 'DejaVu Sans']
matplotlib.rcParams['font.sans-serif'] = ['Segoe UI Emoji', 'Arial', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False
from .reflection_notebook import ReflectionNotebook
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton

class BalanceWheel(QWidget):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.categories = []
        self.scores = []
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(20)  
        
        left_panel = QFrame()
        left_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 25px;
                padding: 15px;
                margin: 10px;
                border: 1px solid #e0e0e0;
            }
        """)
        left_layout = QVBoxLayout(left_panel)
        left_panel.setMinimumWidth(800)  
        left_panel.setMaximumWidth(850)  
        
        self.figure = Figure(figsize=(4, 4)) 
        self.canvas = FigureCanvas(self.figure)
        left_layout.addWidget(self.canvas)
        
        scale_button = QPushButton("Skala Ocen")
        scale_button.setStyleSheet("""
            QPushButton {
                background-color: #f8f9fa;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                color: #4a90e2;
                font-weight: 500;
                font-family: 'Segoe UI';
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #e9ecef;
            }
        """)
        scale_button.setCursor(Qt.PointingHandCursor)
        scale_button.clicked.connect(self.show_scale_description)
        left_layout.addWidget(scale_button)
        
        main_layout.addWidget(left_panel)

        middle_panel = QFrame()
        middle_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 25px;
                padding: 20px;
                margin: 10px;
                border: 1px solid #e0e0e0;
            }
            QLabel {
                font-family: 'Segoe UI';
                color: #333;
            }
        """)
        middle_panel.setMinimumWidth(200)  
        middle_panel.setMaximumWidth(500)  
        middle_layout = QVBoxLayout(middle_panel)
        middle_layout.setSpacing(10)
        middle_layout.setContentsMargins(-35, -20, 20, 20)

        header_container = QFrame()
        header_container.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                margin-left: 0px; 
                margin-bottom: 20px;
                padding: 5px;
                border: 1px solid #e0e0e0;
            }
        """)

        header_container.setMinimumWidth(350)  
        header_container.setMaximumWidth(550)

        # Inicjalizacja układu
        header_layout = QVBoxLayout(header_container)
        header_layout.setContentsMargins(0, -50, -60, 0) 
        header_layout.setSpacing(4)

        title = QLabel("POZIOM ZADOWOLENIA Z ŻYCIA")
        title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        title.setWordWrap(True)
        title.setStyleSheet("color: #333; border: none;")
        header_layout.addWidget(title)
        
        description = QLabel("Na ile oceniasz swoje zadowolenie z życia w poszczególnych kategoriach od 1 do 10?")
        description.setFont(QFont("Segoe UI", 10))
        description.setWordWrap(True)
        description.setStyleSheet("color: #666; border: none;")
        header_layout.addWidget(description)
        
        middle_layout.addWidget(header_container)
        
        # Kontener na kategorie z przewijaniem
        self.categories_container = QVBoxLayout()
        self.categories_container.setSpacing(12)
        middle_layout.addLayout(self.categories_container)
    
        middle_layout.addStretch()
        
        main_layout.addWidget(middle_panel)
        
        main_layout.addStretch(1)

        right_panel = ReflectionNotebook(self.db_manager)
        right_panel.setMinimumWidth(600)  # Minimalna szerokość
        right_panel.setMaximumWidth(650)  # Maksymalna szerokość
        main_layout.addWidget(right_panel)

    def create_category_widget(self, category, score):
        container = QWidget()
        container.setFixedHeight(50)
        container.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
        """)
        
        layout = QHBoxLayout(container)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(10)
        
        name_container = QWidget()
        name_container.setFixedWidth(250)  
        name_container.setStyleSheet("border: none;")
        name_layout = QHBoxLayout(name_container)
        name_layout.setContentsMargins(0, 0, 0, 0)
        
        name_label = QLabel(category['name'])
        name_label.setFont(QFont("Segoe UI", 11))
        name_label.setStyleSheet("""
            QLabel {
                color: #333333;
                background-color: transparent;
                border: none;
            }
        """)
        name_layout.addWidget(name_label)
        name_layout.addStretch() 
        
        layout.addWidget(name_container)
        
        spinbox = QSpinBox()
        spinbox.setStyleSheet("""
            QSpinBox {
                background-color: white;
                border: 1px solid #dddddd;
                border-radius: 4px;
                padding: 5px;
                min-width: 60px;
                max-width: 60px;
                min-height: 20px;
            }
            QSpinBox:hover {
                border: 1px solid #4a90e2;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                border: none;
                background: transparent;
                width: 15px;
            }
        """)
        spinbox.setMinimum(1)
        spinbox.setMaximum(10)
        spinbox.setValue(score)
        spinbox.setAlignment(Qt.AlignCenter)
        layout.addWidget(spinbox)
        
        spinbox.valueChanged.connect(lambda value: self.save_and_update(category['id'], value))
        
        layout.addStretch()
        
        return container
        
    def show_scale_description(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Skala Ocen")
        dialog.setMinimumWidth(600)  
        dialog.setMinimumHeight(400)  
        
        dialog.resize(800, 600)
        
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QScrollArea {
                border: none;
            }
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        

        main_layout = QVBoxLayout(dialog)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: white;")
        
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(10)
        container_layout.setContentsMargins(0, 0, 0, 0)
        
        grid_layout = QGridLayout()
        grid_layout.setSpacing(8)
        
        scale_descriptions = [
            (10, "Pełne zadowolenie", 
            "Absolutna satysfakcja. Wszystko działa tak, jak sobie wymarzyłeś. Nie czujesz potrzeby wprowadzania jakichkolwiek zmian w tym obszarze, ponieważ jesteś w pełni spełniony i zadowolony."),
            (9, "Prawie pełne zadowolenie", 
            "Ten obszar życia działa bardzo dobrze, a poziom satysfakcji jest bliski maksymalnego. Czujesz się spełniony, ale widzisz jeszcze niewielki potencjał na drobne ulepszenia."),
            (8, "Bardzo dobre zadowolenie", 
            "Czujesz dużą satysfakcję i radość z tego, jak funkcjonuje ten obszar twojego życia. Możliwe, że jest niewielkie miejsce na poprawę, ale ogólnie jesteś zadowolony."),
            (7, "Dobre zadowolenie", 
            "Jest sporo pozytywnych emocji i satysfakcji w tym obszarze, choć nadal istnieją aspekty, które chciałbyś poprawić. Ogólny stan jest raczej pozytywny."),
            (6, "Umiarkowane zadowolenie", 
            "Zaczynasz odczuwać satysfakcję, choć nadal widzisz sporo miejsca na poprawę. Funkcjonujesz dobrze, ale jesteś świadomy, że mogłoby być znacznie lepiej."),
            (5, "Neutralność/średnie zadowolenie", 
            "Osiągnąłeś poziom przeciętny. Nie jesteś ani bardzo zadowolony, ani niezadowolony. Nie ma poważnych problemów, ale także brakuje istotnych sukcesów lub pozytywnych emocji."),
            (4, "Zauważalne niezadowolenie", 
            "Czujesz się niezadowolony, ale widzisz pewne małe, choć nieregularne oznaki poprawy. Niektóre elementy działają, ale ogólny obraz nadal jest niezadowalający."),
            (3, "Duże niezadowolenie", 
            "Nadal odczuwasz duży brak satysfakcji, choć mogą pojawić się pewne drobne elementy, które działają. Wciąż jest jednak wiele do poprawienia."),
            (2, "Bardzo duże niezadowolenie", 
            "Jest minimalna poprawa w stosunku do najniższego poziomu, ale nadal masz poważne trudności. Obszar ten wymaga natychmiastowej uwagi, a satysfakcja jest praktycznie zerowa."),
            (1, "Skrajne niezadowolenie", 
            "Absolutnie nie jesteś zadowolony z tego obszaru swojego życia. Czujesz, że nie działa on w ogóle, brak postępów i pozytywnych emocji. Możliwe jest uczucie frustracji, przygnębienia lub bezsilności.")
        ]
        
        for i, (score, title, description) in enumerate(scale_descriptions):
            score_widget = QFrame()
            score_widget.setStyleSheet(f"""
                QFrame {{
                    background-color: {self._get_score_color(score)};
                    border-radius: 6px;
                    padding: 8px;
                }}
            """)
            
            score_layout = QHBoxLayout(score_widget)
            score_layout.setSpacing(8)
            score_layout.setContentsMargins(10, 8, 10, 8)
            
            number_label = QLabel(f"{score}")
            number_label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    font-weight: bold;
                    color: #333;
                    min-width: 20px;
                }
            """)
            score_layout.addWidget(number_label)
            
            text_container = QVBoxLayout()
            text_container.setSpacing(2)
            
            title_label = QLabel(title)
            title_label.setStyleSheet("""
                QLabel {
                    font-size: 13px;
                    font-weight: bold;
                    color: #333;
                }
            """)
            text_container.addWidget(title_label)
            
            desc_label = QLabel(description)
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("""
                QLabel {
                    color: #444;
                    font-size: 12px;
                    line-height: 1.3;
                }
            """)
            text_container.addWidget(desc_label)
            
            score_layout.addLayout(text_container)
            score_layout.setStretch(1, 1)  
            
            row = i % 5
            col = i // 5
            grid_layout.addWidget(score_widget, row, col)
        
        container_layout.addLayout(grid_layout)
        scroll.setWidget(container)
        main_layout.addWidget(scroll)
        
        button_panel = QWidget()
        button_layout = QHBoxLayout(button_panel)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.addStretch()  
        
        close_button = QPushButton("Zamknij")
        close_button.setCursor(Qt.PointingHandCursor)
        button_layout.addWidget(close_button)
        main_layout.addWidget(button_panel)
        
        close_button.clicked.connect(dialog.accept)
        dialog.exec_()

    def _get_score_color(self, score):
        if score >= 9:
            return "#e3f2fd"
        elif score >= 7:
            return "#e8f5e9"
        elif score >= 5:
            return "#fff3e0"
        elif score >= 3:
            return "#fce4ec"
        else:
            return "#ffebee"
    

    def load_data(self):
        with self.db_manager as db:
            self.categories = db.get_all_categories()
            scores = db.get_balance_scores()
        
        scores_dict = {score['category']: score['score'] for score in scores}
        self.scores = scores  # Zachowaj scores do wykorzystania w update_chart
        
        # Wyczyść istniejące widgety
        for i in reversed(range(self.categories_container.count())):
            widget = self.categories_container.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        self.category_widgets = []
        for category in self.categories:
            score = scores_dict.get(category['name'], 5)  
            widget = self.create_category_widget(category, score)
            self.categories_container.addWidget(widget)
            self.category_widgets.append((category['id'], widget))
        
        self.update_chart()
        
    def save_and_update(self, category_id, value):
        with self.db_manager as db:
            db.update_balance_score(category_id, value)
        self.update_chart()
        
    def update_chart(self):
        self.figure.clear()
    
        with self.db_manager as db:
            scores = db.get_balance_scores()
            scores_dict = {score['category']: score['score'] for score in scores}

        values = []
        labels = []
        for category in self.categories:
            values.append(scores_dict.get(category['name'], 1))
            labels.append(category['name'])
    
        if not values:  # Jeśli lista jest pusta
            return  # Przerywamy aktualizację wykresu
        
        angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
        values.append(values[0])
        angles = np.concatenate((angles, [angles[0]]))
       
        ax = self.figure.add_subplot(111, projection='polar')
        colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC', '#99CCFF', 
                 '#FFB366', '#99FF99', '#FF99FF', '#66FFCC']
        
        for i in range(len(values)-1):
            sector_angles = [angles[i], angles[i+1], 0]  
            sector_values = [values[i], values[i+1], 0] 
            
            ax.fill(sector_angles, sector_values, alpha=0.3, color=colors[i % len(colors)])
            
            ax.plot([angles[i], angles[i+1]], [values[i], values[i+1]], 
                   'o-', linewidth=2, color=colors[i % len(colors)])
       
        for i in range(2, 11, 2):
            circle = plt.Circle((0, 0), i, transform=ax.transData._b,
                              fill=False, color='gray', alpha=0.1)
            ax.add_artist(circle)
       
        ax.set_thetagrids(angles[:-1] * 180/np.pi, labels)
        ax.set_ylim(0, 10)  
        ax.grid(True)
       
        ax.tick_params(pad=20)  
       
        self.figure.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
       
        ax.set_facecolor('#f8f9fa')
        self.figure.patch.set_facecolor('#ffffff')
       
        self.canvas.draw()
