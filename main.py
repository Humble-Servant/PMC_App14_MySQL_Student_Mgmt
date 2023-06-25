from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QLineEdit, QPushButton, \
    QComboBox, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QToolBar, QStatusBar, QMessageBox
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3


class Database:
    def __init__(self, database_file="database.db"):
        self.database_file = database_file
        self.connection = sqlite3.connect(self.database_file)
        
    def __del__(self):
        print("Database connection closed!")
        self.connection.close()
        
    def get_all_data(self):
        result = self.connection.execute("SELECT * FROM students")
        return result
    
    def insert(self, name, course, mobile):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)", (name, course, mobile))
        self.connection.commit()
        cursor.close()
        
    def update(self, student_id, name, course, mobile):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE students SET name= ?, course = ?, mobile = ? WHERE id = ?",
                       (name, course, mobile, student_id))
        self.connection.commit()
        cursor.close()
        
    def delete(self, student_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE from students WHERE id = ?", (student_id, ))
        self.connection.commit()
        cursor.close()
        
    def search(self, name):
        cursor = self.connection.cursor()
        result = list(cursor.execute("SELECT * FROM students WHERE name = ?", (name,)))
        cursor.close()
        return result


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
        about_action.triggered.connect(self.about)
        
        # Create a database connection
        self.database = Database()
        
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
        
    def __del__(self):
        print("Closing Database connection!")
        del self.database
        
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
        result = self.database.get_all_data()
        self.table.setRowCount(0)
        for row_num, row_data in enumerate(result):
            self.table.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.table.setItem(row_num, col_num, QTableWidgetItem(str(data)))
        
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
        
    def about(self):
        dialog = AboutDialog()
        dialog.exec()
        
        
class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
        This app was created during the "Python Mega Course."
        Instructor: Ardit Sulce.
        """
        self.setText(content)


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        
        layout = QVBoxLayout()
        
        index = main.table.currentRow()
        self.student_id = main.table.item(index, 0).text()
        student_name = main.table.item(index, 1).text()
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)
        
        course = main.table.item(index, 2).text()
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course)
        layout.addWidget(self.course_name)
        
        mobile = main.table.item(index, 3).text()
        self.student_mobile = QLineEdit(mobile)
        self.student_mobile.setPlaceholderText("Phone")
        layout.addWidget(self.student_mobile)
        
        add_student_button = QPushButton("Update Student")
        add_student_button.clicked.connect(self.update_student)
        layout.addWidget(add_student_button)
        
        self.setLayout(layout)
        
    def update_student(self):
        main.database.update(self.student_id, self.student_name.text(),
                             self.course_name.itemText(self.course_name.currentIndex()), self.student_mobile.text())
        main.load_data()
        self.close()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")
        
        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete this record?")
        yes = QPushButton("Yes")
        no = QPushButton("No")
        
        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0, 1, 1)
        layout.addWidget(no, 1, 1, 1, 1)
        self.setLayout(layout)
        
        yes.clicked.connect(self.delete_student)
        no.clicked.connect(self.cancel)
        
    def delete_student(self):
        index = main.table.currentRow()
        student_id = main.table.item(index, 0).text()
        main.database.delete(student_id)
        main.load_data()
        self.close()
        
        confirmation = QMessageBox()
        confirmation.setWindowTitle("Success")
        confirmation.setText("Record deleted successfully!")
        confirmation.exec()
        
    def cancel(self):
        self.close()

        
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
        result = main.database.search(name)
        # print(list(result))
        items = main.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            main.table.item(item.row(), 1).setSelected(True)
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
        main.database.insert(self.student_name.text(), self.course_name.itemText(self.course_name.currentIndex()),
                             self.student_mobile.text())
        main.load_data()
        self.close()
        

app = QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec())

