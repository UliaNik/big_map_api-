import sys
import requests

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow

SCREEN_SIZE = [600, 600]
size = "0.002,0.002"
map_params = {
    "ll": "37.530887,55.703118",
    "spn": size,
    "l": "map"
}

map_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_server, params=map_params)

if not response:
    print("Ошибка выполнения запроса:")
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

map_file = "map.jpg"
with open(map_file, "wb") as file:
    file.write(response.content)


class Map(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(600, 200, *SCREEN_SIZE)
        self.setWindowTitle('Карта')

        self.pixmap = QPixmap('map.jpg')
        self.image = QLabel(self)
        self.image.move(10, 50)
        self.image.resize(580, 540)
        self.image.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = Map()
    m.show()
    sys.exit(app.exec())
