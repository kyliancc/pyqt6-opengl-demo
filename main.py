import sys

from PyQt6.QtWidgets import QApplication

from glwidget import GLWidget
import resources


def main():
    app = QApplication(sys.argv)
    w = GLWidget()
    w.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
