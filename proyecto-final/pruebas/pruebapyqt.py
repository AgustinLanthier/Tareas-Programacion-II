
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import os
class CustomWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("background-color: #555")
        self.isMaximized = False
#-----------------------Top Bar-----------------------#

        self.new_bar = QWidget(self)
        self.new_bar.setStyleSheet("background-color: #000; color: white")
        self.new_bar.setFixedHeight(40)

        self.label_bar = QLabel("D&D: Dungeon & Dragons", self.new_bar)
        self.label_bar.setStyleSheet("margin-left: 10px; font-size: 16px")
        #---------Close--------#
        self.close_btn = QPushButton("✕", self.new_bar)
        self.close_btn.setFixedSize(40, 40)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #900005
            }
                                     """)
        self.close_btn.clicked.connect(self.close)
        #--------Minimized----------#
        self.min_btn = QPushButton("_", self.new_bar)
        self.min_btn.setFixedSize(40,40)
        self.min_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #900005
            }
                                     """)  
        self.min_btn.clicked.connect(self.showMinimized)    
        #----------Maximized------------#
        self.max_btn = QPushButton("□", self.new_bar)
        self.max_btn.setFixedSize(40,40)
        self.max_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #900005
            }
                                     """)  
        self.max_btn.clicked.connect(self.changeMaxMin)
#-----------Uso de GridLayout para filas y columnas-----------------#        
        layout_bar = QGridLayout(self.new_bar)
        layout_bar.addWidget(self.label_bar, 0, 0)
        layout_bar.addWidget(self.min_btn, 0, 1)
        layout_bar.addWidget(self.max_btn, 0, 2)
        layout_bar.addWidget(self.close_btn, 0, 3)

        layout_bar.setColumnStretch(0, 10)
        layout_bar.setColumnStretch(1, 0)
        layout_bar.setColumnStretch(2, 0)
        layout_bar.setContentsMargins(0, 0, 0, 0)

        container = QWidget()
        layout = QVBoxLayout(container)

        #----------Imagen------------#
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setStyleSheet("background-color: #000; margin: 0px;")
        image = QPixmap("descarga.jpg")
        if not image.isNull():
            image = image.scaled(880, 550)
            image_label.setPixmap(image)
        else:
            image_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold; background-color: #000;")

        layout.addWidget(self.new_bar)
        layout.addWidget(image_label)
        layout.addStretch()
        self.setCentralWidget(container)

        
    def changeMaxMin(self):
        if not self.isMaximized:
            self.showMaximized()
            self.max_btn.setText("❐")  # cambia el ícono
            self.isMaximized = True
        else:
            self.showNormal()          # vuelve al tamaño original
            self.max_btn.setText("□")  # restaura el ícono
            self.isMaximized = False
app = QApplication(sys.argv)
ventana = CustomWindow()
ventana.show()
app.exec_()
     


