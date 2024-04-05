import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from connection import connect_to_db
from PyQt5 import uic

class EmployeeForm(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("untitled.ui", self)
        self.load_data_from_database()
        self.comboBox.currentTextChanged.connect(self.get_doctor_schedule)

    def get_doctor_schedule(self, doctor_name):
        conn = connect_to_db()
        cursor = conn.cursor()

        select_query = f"SELECT day_week, start, finish, break FROM shedule JOIN doctors " \
                       f"on doctors.id=shedule.id_doctor and doctors.name = '{doctor_name}'"
        cursor.execute(select_query)
        data = cursor.fetchall()

        self.tableWidget.setRowCount(0)
        for row_num, row_data in enumerate(data):
            self.tableWidget.insertRow(row_num)
            for col_num, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tableWidget.setItem(row_num, col_num, item)

        cursor.close()
        conn.close()

    def load_data_from_database(self):
        conn = connect_to_db()
        cursor = conn.cursor()

        select_query = "SELECT DISTINCT name FROM doctors"
        cursor.execute(select_query)
        data = cursor.fetchall()

        self.comboBox.clear()
        for row_data in data:
            doctor_name = row_data[0]
            self.comboBox.addItem(doctor_name)

        cursor.close()
        conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = EmployeeForm()
    form.show()
    sys.exit(app.exec_())