import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QFrame, QSlider, QSpinBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from datetime import datetime

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
        
        # Lewy panel z wykresem (powiększony)
        left_panel = QFrame()
        left_layout = QVBoxLayout(left_panel)
        left_panel.setMinimumWidth(500)  # Zwiększona minimalna szerokość
        
        # Tworzenie wykresu
        self.figure = Figure(figsize=(6, 6))  # Zwiększony rozmiar wykresu
        self.canvas = FigureCanvas(self.figure)
        left_layout.addWidget(self.canvas)
        
        main_layout.addWidget(left_panel)
        
        # Dodanie przycisku "Skala Ocen"
        scale_button = QPushButton("Skala Ocen")
        scale_button.clicked.connect(self.show_scale_description)
        left_layout.addWidget(scale_button)

        # Prawy panel z kontrolkami (zmniejszony)
        right_panel = QFrame()
        right_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
                margin: 10px;
                max-width: 350px;
            }
            QLabel {
                font-family: 'Segoe UI';
            }
            QSpinBox {
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                padding: 5px;
                min-width: 60px;
                min-height: 25px;
                font-size: 12px;
            }
            QSpinBox:hover {
                border-color: #4a90e2;
            }
        """)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(10)
        
        # Nagłówki (przesunięte w lewo, mniejsza czcionka)
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignLeft)
        
        title = QLabel("POZIOM ZADOWOLENIA Z ŻYCIA")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        header_layout.addWidget(title)
        
        description = QLabel("Na ile oceniasz swoje zadowolenie z życia w poszczególnych kategoriach od 1 do 10?")
        description.setFont(QFont("Segoe UI", 10))
        header_layout.addWidget(description)
        
        right_layout.addLayout(header_layout)
        
        # Kontener na kategorie
        self.categories_container = QVBoxLayout()
        self.categories_container.setSpacing(8)
        right_layout.addLayout(self.categories_container)
        
        right_layout.addStretch()
        main_layout.addWidget(right_panel)
        
    def show_scale_description(self):
        # Tworzenie okna dialogowego z opisem skali ocen
        dialog = QDialog(self)
        dialog.setWindowTitle("Skala Ocen")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        
        text_edit = QTextEdit(dialog)
        text_edit.setReadOnly(True)
        text_edit.setText("""
1 - Skrajne niezadowolenie: Absolutnie nie jesteś zadowolony z tego obszaru swojego życia. Czujesz, że nie działa on w ogóle, brak postępów i pozytywnych emocji. Możliwe jest uczucie frustracji, przygnębienia lub bezsilności.

2 - Bardzo duże niezadowolenie: Jest minimalna poprawa w stosunku do najniższego poziomu, ale nadal masz poważne trudności. Obszar ten wymaga natychmiastowej uwagi, a satysfakcja jest praktycznie zerowa.

3 - Duże niezadowolenie: Nadal odczuwasz duży brak satysfakcji, choć mogą pojawić się pewne drobne elementy, które działają. Wciąż jest jednak wiele do poprawienia.

4 - Zauważalne niezadowolenie: Czujesz się niezadowolony, ale widzisz pewne małe, choć nieregularne oznaki poprawy. Niektóre elementy działają, ale ogólny obraz nadal jest niezadowalający.

5 - Neutralność/średnie zadowolenie: Osiągnąłeś poziom przeciętny. Nie jesteś ani bardzo zadowolony, ani niezadowolony. Nie ma poważnych problemów, ale także brakuje istotnych sukcesów lub pozytywnych emocji.

6 - Umiarkowane zadowolenie: Zaczynasz odczuwać satysfakcję, choć nadal widzisz sporo miejsca na poprawę. Funkcjonujesz dobrze, ale jesteś świadomy, że mogłoby być znacznie lepiej.

7 - Dobre zadowolenie: Jest sporo pozytywnych emocji i satysfakcji w tym obszarze, choć nadal istnieją aspekty, które chciałbyś poprawić. Ogólny stan jest raczej pozytywny.

8 - Bardzo dobre zadowolenie: Czujesz dużą satysfakcję i radość z tego, jak funkcjonuje ten obszar twojego życia. Możliwe, że jest niewielkie miejsce na poprawę, ale ogólnie jesteś zadowolony.

9 - Prawie pełne zadowolenie: Ten obszar życia działa bardzo dobrze, a poziom satysfakcji jest bliski maksymalnego. Czujesz się spełniony, ale widzisz jeszcze niewielki potencjał na drobne ulepszenia.

10 - Pełne zadowolenie: Absolutna satysfakcja. Wszystko działa tak, jak sobie wymarzyłeś. Nie czujesz potrzeby wprowadzania jakichkolwiek zmian w tym obszarze, ponieważ jesteś w pełni spełniony i zadowolony.
        """)
        
        layout.addWidget(text_edit)
        
        # Przycisk zamykający okno
        close_button = QPushButton("Zamknij", dialog)
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)
        
        dialog.exec_()
    
    def create_category_widget(self, category, score):
        frame = QFrame()
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(5, 5, 5, 5)  # Dodanie marginesów
        layout.setSpacing(10)  # Odstępy między elementami
        
        # Nazwa kategorii
        name_label = QLabel(category['name'])
        name_label.setFont(QFont("Segoe UI", 11))
        name_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)  # Wyrównanie tekstu
        name_label.setMinimumHeight(25)  # Minimalna wysokość etykiety
        layout.addWidget(name_label)
        
        # SpinBox dla oceny
        spinbox = QSpinBox()
        spinbox.setMinimum(1)
        spinbox.setMaximum(10)
        spinbox.setValue(score)
        spinbox.setAlignment(Qt.AlignCenter)
        spinbox.setFixedWidth(80)  # Ograniczenie szerokości SpinBox
        layout.addWidget(spinbox)
        
        # Automatyczne zapisywanie i aktualizacja przy zmianie wartości
        spinbox.valueChanged.connect(lambda value: self.save_and_update(category['id'], value))
    
        return frame

    def load_data(self):
        with self.db_manager as db:
            self.categories = db.get_all_categories()
            scores = db.get_balance_scores()
        
        # Czyszczenie kontenera kategorii
        for i in reversed(range(self.categories_container.count())):
            widget = self.categories_container.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        # Tworzenie słownika ocen
        scores_dict = {score['category']: score['score'] for score in scores}
        
        # Tworzenie widgetów dla każdej kategorii
        self.category_widgets = []
        for category in self.categories:
            score = scores_dict.get(category['name'], 5)  # Domyślna wartość 5
            widget = self.create_category_widget(category, score)
            self.categories_container.addWidget(widget)
            self.category_widgets.append((category['id'], widget))
        
        self.update_chart()
        
    def save_and_update(self, category_id, value):
        current_date = datetime.now().strftime('%Y-%m-%d')
        with self.db_manager as db:
            db.update_balance_score(category_id, value, current_date)
        self.update_chart()
        
    def update_chart(self):
        self.figure.clear()
        
        # Pobieranie aktualnych wartości
        values = []
        labels = []
        for category in self.categories:
            with self.db_manager as db:
                scores = db.get_balance_scores()
                scores_dict = {score['category']: score['score'] for score in scores}
                values.append(scores_dict.get(category['name'], 1))
                labels.append(category['name'])
        
        # Konwersja na radiany
        angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
        
        # Zamknięcie wykresu
        values.append(values[0])
        angles = np.concatenate((angles, [angles[0]]))
        
        # Tworzenie wykresu
        ax = self.figure.add_subplot(111, projection='polar')
        
        # Rysowanie wykresu
        ax.plot(angles, values, 'o-', linewidth=2, color='#4a90e2')
        ax.fill(angles, values, alpha=0.3, color='#4a90e2')
        
        # Dodanie okręgów pomocniczych
        for i in range(2, 11, 2):
            circle = plt.Circle((0, 0), i, transform=ax.transData._b,
                              fill=False, color='gray', alpha=0.1)
            ax.add_artist(circle)
        
        # Ustawienia wykresu
        ax.set_thetagrids(angles[:-1] * 180/np.pi, labels)
        ax.set_ylim(0, 10)
        ax.grid(True)
        ax.set_facecolor('#f8f9fa')
        self.figure.patch.set_facecolor('#ffffff')
        
        self.canvas.draw()
