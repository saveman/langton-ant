import random
import sys
from langtonant.ant import Engine
from PySide6 import QtCore, QtWidgets, QtGui


class EngineWrapper(QtCore.QObject):
    def __init__(self, parent):
        super().__init__(parent)

        self.__engine = Engine()

    def execute(self):
        self.__engine.execute_step()

    def prepare_image(self):
        bitmap = self.__engine.get_board()

        image = QtGui.QImage(QtCore.QSize(bitmap.width(), bitmap.heigth()), QtGui.QImage.Format.Format_RGB32)

        for y in range(bitmap.heigth()):
            for x in range(bitmap.width()):
                value = bitmap.get(x, y)
                image.setPixel(x, y, QtGui.qRgb(255, 255, 255) if value == 0 else QtGui.qRgb(0, 0, 0))

        return image


class MainWindow(QtWidgets.QMainWindow):
    REFRESH_TIME_MS = 100

    def __init__(self, engine: EngineWrapper):
        super().__init__()

        self.__engine = engine

        self.__refresh_timer = QtCore.QTimer(self)
        self.__refresh_timer.setInterval(self.REFRESH_TIME_MS)
        self.__refresh_timer.timeout.connect(self.__on_refresh_timeout)
        self.__refresh_timer.start()

        self.__label = QtWidgets.QLabel()

        self.setCentralWidget(self.__label)

        # self.layout = QtWidgets.QVBoxLayout(self)
        # self.layout.addWidget(self.text)
        # self.layout.addWidget(self.button)
        #  self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def __on_refresh_timeout(self):
        for i in range(100):
            self.__engine.execute()

        img = self.__engine.prepare_image()
        self.__label.setPixmap(QtGui.QPixmap.fromImage(img))


class LangtonAntAppQt:
    def __init__(self) -> None:
        pass

    def run(self):
        app = QtWidgets.QApplication([])

        engine = EngineWrapper(app)

        widget = MainWindow(engine)
        widget.resize(800, 600)
        widget.show()

        sys.exit(app.exec())
