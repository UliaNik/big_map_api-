import sys
import requests

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtCore import Qt

SCREEN_SIZE = [600, 600]


class Map(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(600, 200, *SCREEN_SIZE)
        self.setWindowTitle('Карта')

        self.size = 0.002
        self.l1 = 37.530887
        self.l2 = 55.703118
        self.map_server = "http://static-maps.yandex.ru/1.x/"
        self.map_file = "map.jpg"

        self.image = QLabel(self)
        self.image.move(10, 50)
        self.image.resize(580, 540)
        self.load_map()

    def load_map(self):
        self.map_params = {
            "ll": str(self.l1) + "," + str(self.l2),
            "spn": str(self.size) + "," + str(self.size),
            "l": "map"}
        response = requests.get(self.map_server, params=self.map_params)
        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.run()
        elif event.key() == Qt.Key_PageDown:
            self.run_1()
        elif event.key() == Qt.Key_Up:
            self.run_2()
        elif event.key() == Qt.Key_Down:
            self.run_3()
        elif event.key() == Qt.Key_Right:
            self.run_4()
        elif event.key() == Qt.Key_Left:
            self.run_5()

    def run(self):
        self.size = self.size / 2 if self.size >= 0.004 else self.size
        self.load_map()

    def run_1(self):
        self.size = self.size * 2 if self.size < 8 else self.size
        self.load_map()

    def run_2(self):
        self.l2 = self.l2 + self.size if self.l2 < 80 - self.size else self.l2
        self.load_map()

    def run_3(self):
        self.l2 = self.l2 - self.size if self.l2 > 43 + self.size else self.l2
        self.load_map()

    def run_4(self):
        self.l1 = self.l1 + self.size if self.l1 < 180 - self.size else self.l1
        self.load_map()

    def run_5(self):
        self.l1 = self.l1 - self.size if self.l1 > 20 + self.size else self.l1
        self.load_map()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = Map()
    m.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
