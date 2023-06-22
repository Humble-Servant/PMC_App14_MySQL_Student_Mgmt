from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, \
    QComboBox, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QToolBar, QStatusBar
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        # self.setMinimumSize(800,600)

        # Add top level menu items
        file_menu_item = self.menuBar().addMenu("&File")
        edit_menu_item = self.menuBar().addMenu("&Edit")
        help_menu_item = self.menuBar().addMenu("&Help")
        
        # Add submenu items and actions, including icons for the toolbar actions
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)
        
        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)
        
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        
        # Add a table that shows the data
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)
        self.resize(800, 500)
        self.load_data()
        
        # Create toolbar and add elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)
        
        # Create status bar and add status bar elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        
        # hello = QLabel("Hello There!!")
        # statusbar.addWidget(hello)
        
        # Detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)
        
    def cell_clicked(self):
        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(self.edit)
        
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete)
        
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)
                
        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)
        
    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_num, row_data in enumerate(result):
            self.table.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.table.setItem(row_num, col_num, QTableWidgetItem(str(data)))
        connection.close()
        
    def insert(self):
        dialog = InsertDialog()
        dialog.exec()
        
    def search(self):
        dialog = SearchDialog()
        dialog.exec()
        
    def edit(self):
        dialog = EditDialog()
        dialog.exec()
    
    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()


class EditDialog(QDialog):
    pass


class DeleteDialog(QDialog):
    pass

        
class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Search")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        
        layout = QVBoxLayout()
        
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)
        
        add_student_button = QPushButton("Search")
        add_student_button.clicked.connect(self.search_name)
        layout.addWidget(add_student_button)
        
        self.setLayout(layout)
        
    def search_name(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        # rows = list(result)
        # print(rows)
        items = main.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            main.table.item(item.row(), 1).setSelected(True)
        cursor.close()
        connection.close()
        self.close()
        
        
class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        
        layout = QVBoxLayout()
        
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)
        
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)
        
        self.student_mobile = QLineEdit()
        self.student_mobile.setPlaceholderText("Phone")
        layout.addWidget(self.student_mobile)
        
        add_student_button = QPushButton("Add Student")
        add_student_button.clicked.connect(self.add_student)
        layout.addWidget(add_student_button)
        
        self.setLayout(layout)
        
    def add_student(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (self.student_name.text(), self.course_name.itemText(self.course_name.currentIndex()),
                        self.student_mobile.text()))
        connection.commit()
        cursor.close()
        connection.close()
        main.load_data()
        self.close()
        

app = QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec())
