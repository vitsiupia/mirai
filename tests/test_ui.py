import pytest
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.ui.smart_goals_dialog import SmartGoalsDialog

@pytest.fixture
def app():
    app = QApplication(sys.argv)
    yield app
    app.quit()

def test_smart_goals_dialog(app):
    dialog = SmartGoalsDialog(category_id=1)
    
    # Test wypełniania formularza
    dialog.title_edit.setText("Test Goal")
    dialog.specific_edit.setPlainText("Test Specific")
    dialog.measurable_edit.setPlainText("Test Measurable")
    
    # Sprawdź dane
    data = dialog.get_smart_goal_data()
    assert data['title'] == "Test Goal"
    assert data['specific'] == "Test Specific"