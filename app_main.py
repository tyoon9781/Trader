import sys
from PyQt5.QtWidgets import QApplication
import qdarkstyle
from trader.views import Trader


def main():
    """
    @author : tyoon9781
    """

    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    trader = Trader()
    trader.show()
    sys.exit(app.exec())

    raise RuntimeError


if __name__ == "__main__":
    main()
    