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
        self.map_server = "http://static-maps.yandex.ru/1.x/"
        self.map_file = "map.jpg"

        self.image = QLabel(self)
        self.image.move(10, 50)
        self.image.resize(580, 540)
        self.load_map()

    def load_map(self):
        self.map_params = {
            "ll": "37.530887,55.703118",
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

    def run(self):
        self.size = self.size / 2 if self.size >= 0.004 else self.size
        self.load_map()

    def run_1(self):
        self.size = self.size * 2 if self.size < 8 else self.size
        self.load_map()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = Map()
    m.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
