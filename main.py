import sys
import pyodbc
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel, QLineEdit

def connect_to_db():
    conn = pyodbc.connect('DSN=a3')
    print(f"connection established: {conn}")
    return conn

def get_data(ordernr):
    conn = connect_to_db()
    cursor = conn.cursor()
    sql_query = f"""
    SELECT 
        art_proto.p1_bezeichnung
    FROM 
        org.art_proto art_proto
    WHERE 
        (art_proto.p1_ordernummer={ordernr})
    """
    cursor.execute(sql_query)
    results = cursor.fetchall()
    print(f"cursor fetched: {results}")
    return results

class GUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Occasion Preis Füller"
        self.left = 100
        self.top = 100
        self.height = 600
        self.width = 200
        self.initUI()

    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.main_layout = QVBoxLayout()
        self.input_layout = QVBoxLayout()
        self.input_label = QLabel("Aufragsnummer:")
        self.input_text = QLineEdit()
        self.input_layout.addWidget(self.input_label)
        self.input_layout.addWidget(self.input_text)
        self.submit_button = QtWidgets.QPushButton("Bestätigen")
        self.submit_button.clicked.connect(self.submit)
        self.input_layout.addWidget(self.submit_button)
        self.output_layout = QVBoxLayout()
        self.main_layout.addLayout(self.input_layout)
        self.main_layout.addLayout(self.output_layout)
        self.setLayout(self.main_layout)
        self.show()

    def submit(self):
        ordernr = self.input_text.text()
        print(f"submit clicked, Auftragsnummer: {ordernr}")
        data = get_data(ordernr)
        for item in data:
            label = QLabel(str(item[0]), self)
            self.output_layout.addWidget(label)
        # Ensure new widgets are visible and layout is adjusted
        self.output_layout.update()
        self.adjustSize()  # This forces the window to resize and layout to reflow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec())
