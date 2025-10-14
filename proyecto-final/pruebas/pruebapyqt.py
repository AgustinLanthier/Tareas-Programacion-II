'''
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("background-color: #222")

#-----------------------Top Bar-----------------------#

        self.new_bar = QWidget(self)
        self.new_bar.setStyleSheet("background-color: #000; color: white")
        self.new_bar.setFixedHeight(40)

        self.label_bar = QLabel("D&D: Dungeon & Dragons", self.new_bar)
        self.label_bar.setStyleSheet("margin-left: 10px; font-size: 16px")

        self.close_btn = QPushButton("✕", self.new_bar)
        self.close_btn.setFixedSize(40, 40)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                backgroun-color: #900005
            }
                                     """)
        
app = QApplication(sys.argv)
ventana = CustomWindow()
ventana.show()
app.exec_()
'''           

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
import sys

class DnDWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dungeons & Dragons - PyQt Edition")
        self.setGeometry(100, 100, 900, 600)
        self.setWindowIcon(QIcon("icono.png"))
        self.setWindowOpacity(0.95)
        self.setStyleSheet("""
            QMainWindow {
                background-image: url('fondo_dnd.jpg');
                background-repeat: no-repeat;
                background-position: center;
            }
            QPushButton {
                background-color: rgba(50, 50, 50, 180);
                color: #f2f2f2;
                border: 2px solid #aa0000;
                border-radius: 8px;
                font-size: 16px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgba(100, 0, 0, 200);
            }
            QLabel {
                color: #ffd700;
                font-size: 20px;
                font-family: 'Papyrus';
            }
        """)

        # Etiqueta de título
        self.label = QLabel("Bienvenido, panflin", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(200, 50, 500, 60)

        # Botón
        self.button = QPushButton("Comenzar Aventura", self)
        self.button.setGeometry(350, 400, 200, 50)

app = QApplication(sys.argv)
window = DnDWindow()
window.show()
app.exec_()
