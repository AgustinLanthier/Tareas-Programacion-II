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
        self.setStyleSheet("background-color: #28292ad3")
        self.isMaximized = False
#-----------------------Top Bar-----------------------#

        self.new_bar = QWidget(self)
        self.new_bar.setStyleSheet("background-color: #000; color: white")
        self.new_bar.setFixedHeight(40)

        self.label_bar = QLabel("D&D: Dungeon & Dragons", self.new_bar)
        self.label_bar.setStyleSheet("margin-left: 10px; font-size: 16px; font-family: Magneto")
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

        layout_bar.setColumnStretch(0, 1)
        layout_bar.setColumnStretch(1, 0)
        layout_bar.setColumnStretch(2, 0)
        layout_bar.setContentsMargins(0, 0, 0, 0)

        container = QWidget()
        main_layout = QVBoxLayout(container)

        main_layout.addWidget(self.new_bar)
        self.create_area_panels(main_layout)
        self.setCentralWidget(container)
    #-----------Create Panels Design------------#
    def create_area_panels(self, main_layout):
        #---------The splitter is used to resize the panels-----·#
        splitter = QSplitter(Qt.Horizontal)
        #------Left Panel---------#
        l_panel = self.create_left_panel()
        splitter.addWidget(l_panel)
        #-------Central Panel------#
        c_panel = self.create_central_panel()
        splitter.addWidget(c_panel)
        
        #-------Right Panel------#
        r_panel = self.create_right_panel()
        splitter.addWidget(r_panel)
        
        splitter.setSizes([200, 500, 200])
        splitter.setChildrenCollapsible(False)

        splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #E58D05;
                width: 3px;
            }
            QSplitter::handle:hover {
                background-color: #FFA500;
            }
        """)


        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(splitter)
    #--------Create Left Panel-------------#
    def create_left_panel(self):
        panel = QWidget()
        panel.setStyleSheet("background-color: #3a3a3a;color: white;")
        division_layout = QVBoxLayout(panel)
        division_layout.setContentsMargins(0, 0, 0, 0)
        division_layout.setSpacing(0)
        #----------Up section----------#
        up_section = QWidget()
        up_layout = QVBoxLayout(up_section)
        up_section.setStyleSheet("background-color: #45484A; border: 2px solid #E58D05;")
        #-------Chronometer------------#

        time_label = QLabel("⏰ Tiempo de Campaña")
        time_label.setStyleSheet("color: white; font-weight: bold; font-size: 16px; padding: 10px; border-radius: 10px; font-family: Papyrus;")
        time_label.setAlignment(Qt.AlignCenter)
        up_layout.addWidget(time_label)
        up_layout.addStretch()
        self.display = QLabel ("00:00:00")
        self.display.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 24px;
                font-weight: bold;
                background-color: #2c2c2c;
                border: 2px solid #E58D05;
                border-radius: 10px;
                padding: 5px;
                
                margin: 0px;
            }
        """)

        self.display.setAlignment(Qt.AlignCenter)
        up_layout.addWidget(self.display)
        up_layout.addStretch()
        #-----------Controls-----------#
        controls_layout = QHBoxLayout()
        self.btn_init = QPushButton("▶️")
        self.btn_pause = QPushButton("⏸️")
        self.btn_restart = QPushButton("🔄")

        button_style = """
            QPushButton {
                background-color: #E58D05;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
                font-size: 16px;
                min-width: 40px;
            }
            QPushButton:hover {
                background-color: #8B4513;

            }
        """
        buttons_chronometer= [self.btn_init, self.btn_pause,self.btn_restart]
        for button in buttons_chronometer:
            button.setStyleSheet(button_style)
            controls_layout.addWidget(button)

        up_layout.addLayout(controls_layout)

        self.btn_init.clicked.connect(self.init_chronometer)
        self.btn_pause.clicked.connect(self.pause_chronometer)
        self.btn_restart.clicked.connect(self.restart_chronometer)

        self.time_transcurred = 0
        self.chronometer_active = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualize_chronometer)
        

        #----------Down section----------#
        down_section = QWidget()
        down_layout = QVBoxLayout(down_section)
        down_layout.setContentsMargins(10, 10, 10, 10)
        down_layout.setSpacing(5)
        down_section.setStyleSheet("background-color: #45484A; border: 2px solid #E58D05;")
        title = QLabel("⚙️ Interfaz")
        title.setStyleSheet("color: white; font-weight: bold; font-size: 16px; padding: 10px; border-radius: 10px; font-family: Papyrus; ")
        title.setAlignment(Qt.AlignCenter)
        title.setFixedHeight(40)
        down_layout.addWidget(title)
        down_layout.addStretch()
        #---------Buttons-----------#

        cam = QPushButton("⚔️ Campaña")
        pjs = QPushButton("📋 Personajes")
        best = QPushButton("💀 Bestiario")
        equip = QPushButton("🛡️ Equipamiento")
        inv = QPushButton("🎒 Inventario")
        game = QPushButton("🗺️ Juego")
        biblio = QPushButton("🔍 Biblioteca")

        buttons = [cam, pjs, best, equip, game, biblio, inv]
        for button in buttons:
            button.setStyleSheet("""
            QPushButton {
                color: white;
                font-style: italic;
                padding: 10px;
                border-radius: 10px;
                font-size: 14px;
                font-family: Palatino Linotype;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E58D05
            }
                                     """)
            down_layout.addWidget(button)
        #------Line for connect Inventario's button between up_section in right panel-----------#
        inv.clicked.connect(self.show_inventary)
        best.clicked.connect(self.show_bestiary)

        division_layout.addWidget(up_section)
        division_layout.addWidget(down_section)
        division_layout.setStretchFactor(up_section, 1)
        division_layout.setStretchFactor(down_section, 2)

        return panel

    #------Chronometer's Actions------#

    def init_chronometer(self):
        if not self.chronometer_active:
            self.chronometer_active = True
            self.timer.start(1000)

    def pause_chronometer(self):
        if self.chronometer_active:
            self.chronometer_active = False
            self.timer.stop()

    def restart_chronometer(self):
        self.chronometer_active = False
        self.timer.stop()
        self.time_transcurred = 0
        self.actualize_chronometer()

    def actualize_chronometer(self):
        if self.chronometer_active:
            self.time_transcurred += 1
        
        hours = self.time_transcurred // 3600
        minutes = (self.time_transcurred % 3600) // 60
        seconds = self.time_transcurred % 60
        
        time_formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.display.setText(time_formatted)

    #--------Create Right Panel-------------#
    def create_right_panel(self):
        panel = QWidget()
        panel.setStyleSheet("background-color: #3a3a3a; color: white;")
        division_layout = QVBoxLayout(panel)
        division_layout.setContentsMargins(0, 0, 0, 0)
        division_layout.setSpacing(0)
        #----------Up section----------#
        up_section = QWidget()
        up_section.setStyleSheet("background-color: #45484A;  border: 2px solid #E58D05;")
        up_layout = QVBoxLayout(up_section)   

        self.right_up_layout = up_layout

        title_waiting = QLabel("Selecciona 'Inventario' de la Interfaz")
        title_waiting.setStyleSheet("""
            color: #888;
            font-size: 14px;
            padding: 40px;
            text-align: center;
            font-style: italic;
            border: 0px;                       
        """)
        title_waiting.setAlignment(Qt.AlignCenter)
        up_layout.addWidget(title_waiting)
        up_layout.addStretch()
        #----------Down section----------#
        down_section = QWidget()
        down_section.setStyleSheet("background-color: #45484A; border: 2px solid #E58D05; ")
        down_layout = QVBoxLayout(down_section)  

        stats_label = QLabel("📊 Estadísticas")
        stats_label.setStyleSheet("color: white; font-weight: bold; font-size: 16px; padding: 10px; border-radius: 10px; font-family: Papyrus; ")
        stats_label.setAlignment(Qt.AlignCenter)

        down_layout.addWidget(stats_label)
        down_layout.addStretch()

        division_layout.addWidget(up_section)
        division_layout.addWidget(down_section)

        division_layout.setStretchFactor(up_section, 2)
        division_layout.setStretchFactor(down_section, 1)
        
        return panel
    #--------Create Central Panel-------------# 
    def create_central_panel(self):
        self.panel_central = QWidget()
        self.panel_central.setStyleSheet("background-color: #3a3a3a; color: white; border: 2px solid #E58D05;")
        self.layout_central = QVBoxLayout(self.panel_central)

        self.layout_central.setContentsMargins(0, 0, 0, 0)
        self.layout_central.setSpacing(0)
        
        self.background_label = QLabel()
        self.background_label.setAlignment(Qt.AlignCenter)
        self.background_label.setStyleSheet("background-color: #1a1a1a;")
        self.background_label.setText("Selecciona una opción de la Interfaz")
        self.background_label.setStyleSheet("background-color: #1a1a1a; color: #888; font-size: 18px; font-style: italic;")
        
        container_data = self.show_monsters()
        self.layout_central.addWidget(container_data)
        self.layout_central.addWidget(self.background_label)
        return self.panel_central
        
    #-------Show Inventary------#
    def show_inventary(self):
        
        self.clear_layout(self.right_up_layout)

        title = QLabel("🎒 Inventario")
        title.setStyleSheet("color: white; font-weight: bold; font-size: 16px; padding: 10px;  border: 2px solid #E58D05;border-radius: 10px; font-family: Papyrus; ")
        title.setAlignment(Qt.AlignCenter)
        title.setFixedHeight(40)
        self.right_up_layout.addWidget(title)

        list_inventory = QListWidget()
        list_inventory.setStyleSheet("""
            QListWidget {
                background-color: #2c2c2c;
                color: white;
                border: 2px solid #E58D05;
                border-radius: 10px;
                padding: 5px;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #5D4037;
            }
            QListWidget::item:selected {
                background-color: #E58D05;
                color: #2c2c2c;
            }
        """)
        #----Ejemplos-----#
        items = [
            "⚔️ Espada larga",
            "🛡️ Escudo de madera", 
            "🧪 Poción de vida",
            "💰 150 monedas de oro",
            "🔑 Llave antigua",
            "📜 Pergamino misterioso",
            "💎 Gema brillante",
            "🏹 Arco compuesto"
        ]
        
        for item in items:
            list_inventory.addItem(item)
        
        self.right_up_layout.addWidget(list_inventory)
        self.right_up_layout.addStretch()

    #---------Show Bestary------#
    def show_bestiary(self):
        self.clear_layout(self.layout_central)
        title_bestiary = QLabel("💀 Bestiario")
        title_bestiary.setStyleSheet("color: white; font-weight: bold; font-size: 16px; padding: 10px;  border: 2px solid #E58D05;border-radius: 10px; font-family: Papyrus; ")
        title_bestiary.setAlignment(Qt.AlignCenter)
    
        bestiary = QWidget()
        bestiary.setStyleSheet("border-image: url(libro.png) 0 0 0 0 stretch stretch; background-repeat: no-repeat; background-position: center; ")
        
        self.layout_central.addWidget(title_bestiary)
        self.layout_central.addWidget(bestiary)

        self.layout_central.setStretchFactor(title_bestiary,1)
        self.layout_central.setStretchFactor(bestiary, 9)

        return self.layout_central
    #--------Function for show monsters-------#
    def show_monsters(self):
        grid_monster = QGridLayout()
        image_monster = QWidget()
        image_monster.setStyleSheet("border-image: url() 0 0 0 0 stretch stretch; border: 2px solid black")
        grid_monster.addWidget(image_monster)
        
    #-------This method is used to clean the layout so that data does not accumulate------#
    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    def changeMaxMin(self):
        if not self.isMaximized:
            self.showMaximized()
            self.max_btn.setText("❐")  
            self.isMaximized = True
        else:
            self.showNormal()          # vuelve al tamaño original
            self.max_btn.setText("□")  
            self.isMaximized = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.inicial_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and hasattr(self, 'inicial_position'):
            self.move(event.globalPos() - self.inicial_position)
            event.accept()

    '''def resizeEvent(self, event):
        super().resizeEvent(event)
        self.new_bar.setFixedWidth(self.width())
        if hasattr(self, 'background_label') and self.background_label.isVisible():
            self.background_label.setFixedSize(self.panel_central.size())
    '''
app = QApplication(sys.argv)
ventana = CustomWindow()
ventana.show()
app.exec_()
