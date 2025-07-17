import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    stylesheet = """
        QStatusBar {
            padding: 3px;
            font-size: 14px;
            font-weight: bold;
            color: orange;
        }
    """
    app.setStyleSheet(stylesheet)

    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())
    #mostrar_ventana()