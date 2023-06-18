from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, QLineEdit
import sys


class AgeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        grid = QGridLayout()
        
        name_label = QLabel("Name:")
        name_line_edit = QLineEdit()
        
        dob_label = QLabel("Date of Birth mm/dd/yyyy:")
        dob_line_edit = QLineEdit()
        
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(name_line_edit, 0, 1)
        grid.addWidget(dob_label, 1, 0)
        grid.addWidget(dob_line_edit, 1, 1)
        
        self.setLayout(grid)
        

app = QApplication(sys.argv)
age_calc = AgeCalculator()
age_calc.show()
sys.exit(app.exec())
