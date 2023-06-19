from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QComboBox
import sys


class SpeedCalc(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Speed Calculator")
        grid = QGridLayout()
        
        # Create widgets
        dist_label = QLabel("Distance:")
        self.distance = QLineEdit()
        time_label = QLabel("Time (hours):")
        self.user_time = QLineEdit()
        self.units_combo = QComboBox()
        self.units_combo.addItems(['miles', 'kilometers'])
        calc_button = QPushButton("Calculate")
        calc_button.clicked.connect(self.calculate_speed)
        self.output = QLabel("")
        
        # Add widgets to layout
        grid.addWidget(dist_label, 0, 0)
        grid.addWidget(self.distance, 0, 1)
        grid.addWidget(self.units_combo, 0, 2)
        grid.addWidget(time_label, 1, 0)
        grid.addWidget(self.user_time, 1, 1)
        grid.addWidget(calc_button, 2, 0, 1, 3)
        grid.addWidget(self.output, 3, 0, 1, 3)
        
        # Build grid layout
        self.setLayout(grid)
        
    def calculate_speed(self):
        if self.user_time.text() == '':
            speed = 'error'
        else:
            speed = float(self.distance.text()) / float(self.user_time.text())
        if self.units_combo.currentText() == 'miles':
            units = 'mph'
        elif self.units_combo.currentText() == 'kilometers':
            units = 'kph'
        self.output.setText(f"{speed} {units}")


app = QApplication(sys.argv)
speed_calc = SpeedCalc()
speed_calc.show()
sys.exit(app.exec())
        