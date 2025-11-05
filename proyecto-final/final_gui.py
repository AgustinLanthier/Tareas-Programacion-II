from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import os
import importlib.util
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))
from monstruos import obtener_monstruos, obtener_detalle_monstruo
from pj import obtener_razas, obtener_clases
from database import DatabaseManager
from items import obtener_detalle_item_por_nombre, obtener_todos_items
from hechizos import obtener_hechizos, obtener_detalle_hechizo

class CustomWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("background-color: #28292ad3")
        self.isMaximized = False
        
        self.modulos = {}
        self.modulo_actual = None
        self.db = DatabaseManager()
        
        self.cargar_modulos()
        self.init_ui()
        
    def cargar_modulos(self):
        modulos_config = {
            'Personajes': 'core.pj',
            'Bestiario': 'core.monstruos', 
            'Equipamiento': 'core.items',
            'Hechizos': 'core.hechizos',
        }
        
        for nombre, ruta in modulos_config.items():
            try:
                self.modulos[nombre] = {
                    'nombre': nombre,
                    'ruta': ruta,
                    'instancia': None
                }
            except Exception as e:
                print(f"Error cargando módulo {nombre}: {e}")

    def init_ui(self):
        self.new_bar = QWidget(self)
        self.new_bar.setStyleSheet("background-color: #000; color: white")
        self.new_bar.setFixedHeight(40)

        self.label_bar = QLabel("D&D: Dungeon & Dragons", self.new_bar)
        self.label_bar.setStyleSheet("margin-left: 10px; font-size: 16px; font-family: Magneto")
        
        self.min_btn = QPushButton("_", self.new_bar)
        self.max_btn = QPushButton("□", self.new_bar) 
        self.close_btn = QPushButton("✕", self.new_bar)
        
        for btn in [self.min_btn, self.max_btn, self.close_btn]:
            btn.setFixedSize(40, 40)
            btn.setStyleSheet("""
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
        self.max_btn.clicked.connect(self.changeMaxMin)
        self.close_btn.clicked.connect(self.close)
        
        layout_bar = QGridLayout(self.new_bar)
        layout_bar.addWidget(self.label_bar, 0, 0)
        layout_bar.addWidget(self.min_btn, 0, 1)
        layout_bar.addWidget(self.max_btn, 0, 2)
        layout_bar.addWidget(self.close_btn, 0, 3)
        layout_bar.setColumnStretch(0, 1)
        layout_bar.setContentsMargins(0, 0, 0, 0)

        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.addWidget(self.new_bar)
        self.create_area_panels(main_layout)
        self.setCentralWidget(container)

    def create_area_panels(self, main_layout):
        splitter = QSplitter(Qt.Horizontal)
        
        splitter.addWidget(self.create_left_panel())
        splitter.addWidget(self.create_central_panel())
        splitter.addWidget(self.create_right_panel())
        
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

    def create_left_panel(self):
        panel = QWidget()
        panel.setStyleSheet("background-color: #3a3a3a; color: white;")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        up_section = self.create_chronometer_section()
        layout.addWidget(up_section)
        
        down_section = self.create_module_selector()
        layout.addWidget(down_section)
        
        layout.setStretchFactor(up_section, 1)
        layout.setStretchFactor(down_section, 2)
        
        return panel

    def create_chronometer_section(self):
        section = QWidget()
        section.setStyleSheet("background-color: #45484A; border: 2px solid #E58D05;")
        layout = QVBoxLayout(section)
        
        time_label = QLabel("Tiempo de Campaña")
        time_label.setStyleSheet("color: white; font-weight: bold; font-size: 16px; padding: 10px; border-radius: 10px; font-family: Papyrus;")
        time_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(time_label)
        
        self.display = QLabel("00:00:00")
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
        layout.addWidget(self.display)
        
        controls_layout = QHBoxLayout()
        self.btn_init = QPushButton("Iniciar")
        self.btn_pause = QPushButton("Pausar")
        self.btn_restart = QPushButton("Reiniciar")
        
        button_style = """
            QPushButton {
                background-color: #E58D05;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
                font-size: 12px;
                min-width: 40px;
            }
            QPushButton:hover {
                background-color: #8B4513;
            }
        """
        
        for button in [self.btn_init, self.btn_pause, self.btn_restart]:
            button.setStyleSheet(button_style)
            controls_layout.addWidget(button)
        
        layout.addLayout(controls_layout)
        
        self.time_transcurred = 0
        self.chronometer_active = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualize_chronometer)
        self.btn_init.clicked.connect(self.init_chronometer)
        self.btn_pause.clicked.connect(self.pause_chronometer)
        self.btn_restart.clicked.connect(self.restart_chronometer)
        
        return section

    def create_module_selector(self):
        section = QWidget()
        section.setStyleSheet("background-color: #45484A; border: 2px solid #E58D05;")
        layout = QVBoxLayout(section)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        title = QLabel("Interfaz")
        title.setStyleSheet("color: white; font-weight: bold; font-size: 16px; padding: 10px; border-radius: 10px; font-family: Papyrus;")
        title.setAlignment(Qt.AlignCenter)
        title.setFixedHeight(40)
        layout.addWidget(title)
        
        self.boton_modulos = {}
        modulos = ['Personajes', 'Bestiario', 'Equipamiento', 'Hechizos']
        
        for modulo in modulos:
            btn = QPushButton(modulo)
            btn.setStyleSheet("""
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
                QPushButton:checked {
                    background-color: #E58D05;
                    border: 2px solid #8B4513;
                }
            """)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, m=modulo: self.cargar_modulo(m))
            layout.addWidget(btn)
            self.boton_modulos[modulo] = btn
        
        layout.addStretch()
        return section

    def create_central_panel(self):
        self.panel_central = QWidget()
        self.panel_central.setStyleSheet("background-color: #3a3a3a; color: white; border: 2px solid #E58D05;")
        self.layout_central = QVBoxLayout(self.panel_central)
        self.layout_central.setContentsMargins(0, 0, 0, 0)
        self.layout_central.setSpacing(0)
        
        self.label_bienvenida = QLabel("Selecciona un modulo para comenzar")
        self.label_bienvenida.setAlignment(Qt.AlignCenter)
        self.label_bienvenida.setStyleSheet("""
            color: #888;
            font-size: 18px;
            padding: 40px;
            font-style: italic;
        """)
        self.layout_central.addWidget(self.label_bienvenida)
        
        return self.panel_central

    def create_right_panel(self):
        panel = QWidget()
        panel.setStyleSheet("background-color: #3a3a3a; color: white;")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.seccion_lista = QWidget()
        self.seccion_lista.setStyleSheet("background-color: #45484A; border: 2px solid #E58D05;")
        self.layout_lista = QVBoxLayout(self.seccion_lista)
        self.layout_lista.setContentsMargins(5, 5, 5, 5)
        
        self.label_titulo_lista = QLabel("Lista")
        self.label_titulo_lista.setStyleSheet("color: white; font-weight: bold; padding: 5px;")
        self.layout_lista.addWidget(self.label_titulo_lista)
        
        self.lista_widget = QListWidget()
        self.lista_widget.setStyleSheet("""
            QListWidget {
                background-color: #2c2c2c;
                color: white;
                border: 1px solid #E58D05;
                border-radius: 5px;
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
        self.lista_widget.itemClicked.connect(self.on_item_seleccionado)
        self.layout_lista.addWidget(self.lista_widget)
        
        self.seccion_opciones = QWidget()
        self.seccion_opciones.setStyleSheet("background-color: #45484A; border: 2px solid #E58D05;")
        self.layout_opciones = QVBoxLayout(self.seccion_opciones)
        self.layout_opciones.setContentsMargins(5, 5, 5, 5)
        
        self.label_titulo_opciones = QLabel("Opciones")
        self.label_titulo_opciones.setStyleSheet("color: white; font-weight: bold; padding: 5px;")
        self.layout_opciones.addWidget(self.label_titulo_opciones)
        
        self.widget_opciones = QWidget()
        self.layout_opciones_dinamico = QVBoxLayout(self.widget_opciones)
        self.layout_opciones.addWidget(self.widget_opciones)
        
        layout.addWidget(self.seccion_lista)
        layout.addWidget(self.seccion_opciones)
        layout.setStretchFactor(self.seccion_lista, 2)
        layout.setStretchFactor(self.seccion_opciones, 1)
        
        self.seccion_lista.hide()
        self.seccion_opciones.hide()
        
        return panel

    
    def cargar_modulo(self, nombre_modulo):
        for btn in self.boton_modulos.values():
            btn.setChecked(False)
        self.boton_modulos[nombre_modulo].setChecked(True)
        
        self.limpiar_ui()
        
        modulo = self.obtener_modulo(nombre_modulo)
        
        if modulo:
            self.label_titulo_lista.setText(f"{self.obtener_nombre_lista(modulo)}")
            self.label_titulo_opciones.setText("Acciones")
            
            items = self.obtener_lista_modulo(modulo)
            if items:
                self.actualizar_lista(items)
                self.seccion_lista.show()
            else:
                self.seccion_lista.hide()
            
            opciones = self.obtener_opciones_modulo(modulo)
            if opciones:
                self.actualizar_opciones(opciones, modulo)
                self.seccion_opciones.show()
            else:
                self.seccion_opciones.hide()
            
            vista_default = self.obtener_vista_default_modulo(modulo)
            if vista_default:
                self.mostrar_en_central(vista_default)
            else:
                self.mostrar_vista_bienvenida(nombre_modulo)
        
        self.modulo_actual = modulo

    def obtener_nombre_lista(self, modulo):
        nombres = {
            'Personajes': 'Jugadores',
            'Bestiario': 'Monstruos', 
            'Equipamiento': 'Items',
            'Hechizos': 'Hechizos',
        }
        return nombres.get(modulo['nombre'], 'Lista')

    def limpiar_ui(self):
        self.lista_widget.clear()
        self.clear_layout(self.layout_opciones_dinamico)
        self.clear_layout(self.layout_central)

    def actualizar_lista(self, items):
        self.lista_widget.clear()
        for item in items:
            self.lista_widget.addItem(str(item))

    def actualizar_opciones(self, opciones, modulo):
        self.clear_layout(self.layout_opciones_dinamico)
        
        for opcion in opciones:
            btn = QPushButton(opcion)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #E58D05;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 8px;
                    margin: 2px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #8B4513;
                }
            """)
            btn.clicked.connect(lambda checked, o=opcion, m=modulo: self.ejecutar_opcion(o, m))
            self.layout_opciones_dinamico.addWidget(btn)
        
        self.layout_opciones_dinamico.addStretch()

    def mostrar_en_central(self, widget):
        self.clear_layout(self.layout_central)
        self.layout_central.addWidget(widget)

    def mostrar_vista_bienvenida(self, nombre_modulo):
        label = QLabel(f"{nombre_modulo}\n\nSelecciona un elemento de la lista o usa las acciones disponibles")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: #888; font-size: 16px; padding: 40px; font-style: italic;")
        self.layout_central.addWidget(label)

    def on_item_seleccionado(self, item):
        if self.modulo_actual:
            nombre_item = item.text()
            vista_detalle = self.obtener_vista_detalle_modulo(self.modulo_actual, nombre_item)
            if vista_detalle:
                self.mostrar_en_central(vista_detalle)

    def ejecutar_opcion(self, opcion, modulo):
        resultado = self.ejecutar_opcion_modulo(modulo, opcion)
        if resultado:
            self.mostrar_en_central(resultado)
        
        if modulo['nombre'] == 'Personajes' and opcion in ['Crear Jugador', 'Crear Personaje']:
            items = self.obtener_lista_modulo(modulo)
            self.actualizar_lista(items)
    
    def obtener_modulo(self, nombre):
        return self.modulos.get(nombre, {'nombre': nombre})

    def obtener_lista_modulo(self, modulo):
        nombre_modulo = modulo['nombre']
        
        if nombre_modulo == 'Bestiario':
            monstruos_data = obtener_monstruos()
            return [monster['nombre'] for monster in monstruos_data]
        
        elif nombre_modulo == 'Personajes':
            jugadores = self.db.obtener_jugadores()
            return [f"{j['nombre_jugador']}" for j in jugadores]

        elif nombre_modulo == 'Equipamiento':
                items = obtener_todos_items()
                return [item['nombre'] for item in items]
        elif nombre_modulo == 'Hechizos':  
                hechizos_data = obtener_hechizos()
                return [hechizo['nombre'] for hechizo in hechizos_data]
        return []

    def obtener_opciones_modulo(self, modulo):
        nombre_modulo = modulo['nombre']
        
        if nombre_modulo == 'Personajes':
            return ['Crear Jugador', 'Crear Personaje']
        elif nombre_modulo == 'Bestiario':
            return ['Actualizar Lista']
        elif nombre_modulo == 'Equipamiento':
            return ['Ver Equipo Normal', 'Ver Objetos Mágicos', 'Actualizar Lista']
        elif nombre_modulo == 'Hechizos':  
            return ['Actualizar Lista']
        return []

    def obtener_vista_default_modulo(self, modulo):
        nombre_modulo = modulo['nombre']
        
        if nombre_modulo == 'Bestiario':
            return self.crear_vista_manual_monstruos()
        
        label = QLabel(f"Vista de {nombre_modulo}\n\nSelecciona un elemento para ver detalles")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: white; font-size: 14px; padding: 20px;")
        return label

    def crear_vista_manual_monstruos(self):
        container = QWidget()
        container.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                                      stop:0 #5D4037, stop:1 #8D6E63);
            border: 5px solid #E58D05; 
            border-radius: 15px;
            color: white;
        """)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(30, 30, 30, 30)
        
        titulo = QLabel("MANUAL DEL BESTIARIO D&D")
        titulo.setStyleSheet("""
            color: #E58D05; 
            font-size: 28px; 
            font-weight: bold; 
            font-family: Papyrus;
            padding: 20px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
            border: 2px solid #E58D05;
        """)
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)
        
        instruccion = QLabel("Selecciona un monstruo de la lista para visualizar sus detalles")
        instruccion.setStyleSheet("""
            color: #FFD700; 
            font-size: 16px; 
            padding: 15px;
            font-style: italic;
            font-family: Garamond;
        """)
        instruccion.setAlignment(Qt.AlignCenter)
        layout.addWidget(instruccion)
        
        separador = QLabel("• • • • • • • • • • • • • • • • • • • •")
        separador.setStyleSheet("color: #E58D05; font-size: 16px; padding: 10px;")
        separador.setAlignment(Qt.AlignCenter)
        layout.addWidget(separador)
        
        fuente = QLabel("Datos obtenidos de la API oficial de D&D 5e")
        fuente.setStyleSheet("color: #B0B0B0; font-size: 12px; padding: 10px;")
        fuente.setAlignment(Qt.AlignCenter)
        layout.addWidget(fuente)
        
        layout.addStretch()
        return container

    def cargar_imagen_desde_url(self, url):
        try:
            if not url:
                return None
                
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                return pixmap
        except Exception as e:
            print(f"Error cargando imagen desde {url}: {e}")
        return None

    def obtener_vista_detalle_modulo(self, modulo, item_nombre):
        nombre_modulo = modulo['nombre']
        
        if nombre_modulo == 'Bestiario':
            monstruos_data = obtener_monstruos()
            for monster in monstruos_data:
                if monster['nombre'] == item_nombre:
                    monster_index = monster['index']
                    detalle = obtener_detalle_monstruo(monster_index)
                    return self.crear_ficha_monstruo_detallada(detalle)
        
        elif nombre_modulo == 'Personajes':
            jugador = self.db.buscar_jugador_por_nombre(item_nombre)
            if jugador:
                return self.crear_vista_jugador(jugador)
        
        elif nombre_modulo == 'Equipamiento':
                detalle = obtener_detalle_item_por_nombre(item_nombre)
                if detalle:
                    return self.crear_ficha_item_detallada(detalle)
        elif nombre_modulo == 'Hechizos':  # <- Nuevo módulo
                hechizos_data = obtener_hechizos()
                for hechizo in hechizos_data:
                    if hechizo['nombre'] == item_nombre:
                        detalle = obtener_detalle_hechizo(hechizo['index'])
                        return self.crear_ficha_hechizo(detalle)
        return self.crear_vista_generica_detalle(nombre_modulo, item_nombre)

    
    def crear_ficha_monstruo_detallada(self, detalle):
        widget = QWidget()
        widget.setStyleSheet("""
            background: #3a3a3a; 
            color: white; 
            border: 2px solid #E58D05;
            border-radius: 10px;
        """)
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #2c2c2c;
                width: 15px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #E58D05;
                border-radius: 7px;
            }
        """)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        
        header = QLabel(detalle['nombre'].upper())
        header.setStyleSheet("""
            color: #E58D05; 
            font-size: 24px; 
            font-weight: bold; 
            font-family: Papyrus;
            padding: 15px;
            border-bottom: 2px solid #E58D05;
            text-align: center;
        """)
        content_layout.addWidget(header)
        
        main_container = QWidget()
        main_layout = QHBoxLayout(main_container)
        
        left_column = QWidget()
        left_layout = QVBoxLayout(left_column)
        left_layout.setAlignment(Qt.AlignTop)
        
        imagen_url = detalle.get('imagen')
        if imagen_url:
            pixmap = self.cargar_imagen_desde_url(imagen_url)
            if pixmap and not pixmap.isNull():
                pixmap = pixmap.scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                imagen_label = QLabel()
                imagen_label.setPixmap(pixmap)
                imagen_label.setStyleSheet("""
                    border: 3px solid #E58D05;
                    border-radius: 10px;
                    background: #2c2c2c;
                    padding: 5px;
                """)
                imagen_label.setAlignment(Qt.AlignCenter)
                left_layout.addWidget(imagen_label)
            else:
                placeholder = QLabel("Imagen no disponible")
                placeholder.setStyleSheet("""
                    color: #888;
                    font-style: italic;
                    padding: 100px 20px;
                    border: 2px dashed #E58D05;
                    border-radius: 10px;
                    text-align: center;
                """)
                placeholder.setAlignment(Qt.AlignCenter)
                left_layout.addWidget(placeholder)
        
        left_layout.addStretch()
        
        right_column = QWidget()
        right_layout = QVBoxLayout(right_column)
        
        info_title = QLabel("INFORMACION BASICA")
        info_title.setStyleSheet("color: #FFD700; font-weight: bold; font-size: 16px; padding: 10px 0px;")
        right_layout.addWidget(info_title)
        
        grid_info = QGridLayout()
        grid_info.setSpacing(8)
        
        info_basica = [
            ("Tamaño:", detalle.get('tamaño', 'N/A')),
            ("Tipo:", detalle.get('tipo', 'N/A')),
            ("Alineamiento:", detalle.get('alineamiento', 'N/A')),
            ("Clase de Armadura:", str(detalle.get('clase_de_armadura', 'N/A'))),
            ("Puntos de Golpe:", str(detalle.get('puntos_de_golpe', 'N/A'))),
            ("Challenge Rating:", str(detalle.get('cr', 'N/A')))
        ]
        
        for i, (label, value) in enumerate(info_basica):
            lbl = QLabel(label)
            lbl.setStyleSheet("color: #E58D05; font-weight: bold;")
            val = QLabel(value)
            val.setStyleSheet("color: white;")
            grid_info.addWidget(lbl, i, 0)
            grid_info.addWidget(val, i, 1)
        
        right_layout.addLayout(grid_info)
        
        right_layout.addSpacing(15)
        carac_title = QLabel("CARACTERISTICAS")
        carac_title.setStyleSheet("color: #FFD700; font-weight: bold; font-size: 16px; padding: 10px 0px;")
        right_layout.addWidget(carac_title)
        
        grid_carac = QGridLayout()
        grid_carac.setSpacing(10)
        
        caracteristicas = detalle.get('caracteristicas', {})
        stats = [
            ("Fuerza", caracteristicas.get('fuerza', 'N/A')),
            ("Destreza", caracteristicas.get('destreza', 'N/A')),
            ("Constitucion", caracteristicas.get('constitucion', 'N/A')),
            ("Inteligencia", caracteristicas.get('inteligencia', 'N/A')),
            ("Sabiduria", caracteristicas.get('sabiduria', 'N/A')),
            ("Carisma", caracteristicas.get('carisma', 'N/A'))
        ]
        
        for i, (nombre, valor) in enumerate(stats):
            lbl = QLabel(nombre)
            lbl.setStyleSheet("color: #E58D05; font-weight: bold;")
            val = QLabel(str(valor))
            val.setStyleSheet("color: white; background: #2c2c2c; padding: 5px; border-radius: 3px;")
            grid_carac.addWidget(lbl, i//3, (i%3)*2)
            grid_carac.addWidget(val, i//3, (i%3)*2+1)
        
        right_layout.addLayout(grid_carac)
        right_layout.addStretch()
        
        main_layout.addWidget(left_column)
        main_layout.addWidget(right_column)
        main_layout.setStretch(0, 1) 
        main_layout.setStretch(1, 2)  
        
        content_layout.addWidget(main_container)
        
        acciones = detalle.get('acciones', [])
        if acciones:
            content_layout.addSpacing(20)
            acc_title = QLabel("ACCIONES")
            acc_title.setStyleSheet("color: #FFD700; font-weight: bold; font-size: 16px; padding: 10px 0px;")
            content_layout.addWidget(acc_title)
            
            for accion in acciones:
                if accion.get('nombre'):
                    acc_name = QLabel(accion.get('nombre', 'Sin nombre'))
                    acc_name.setStyleSheet("color: #E58D05; font-weight: bold; padding: 5px 0px; font-size: 14px;")
                    content_layout.addWidget(acc_name)
                    
                if accion.get('descripcion'):
                    acc_desc = QLabel(accion.get('descripcion', 'Sin descripcion'))
                    acc_desc.setStyleSheet("color: white; padding: 5px 15px; font-size: 12px; background: #2c2c2c; border-radius: 5px;")
                    acc_desc.setWordWrap(True)
                    content_layout.addWidget(acc_desc)
                
                content_layout.addSpacing(10)
        
        content_layout.addStretch()
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
        
        return widget

    def crear_vista_jugador(self, jugador):
        widget = QWidget()
        widget.setStyleSheet("background: #3a3a3a; color: white;")
        layout = QVBoxLayout(widget)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #2c2c2c;
                width: 15px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #E58D05;
                border-radius: 7px;
            }
        """)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        
        header = QLabel(f"JUGADOR: {jugador['nombre_jugador']}")
        header.setStyleSheet("color: #E58D05; font-size: 24px; font-weight: bold; padding: 10px; text-align: center;")
        content_layout.addWidget(header)
        
        info_layout = QHBoxLayout()
        email_label = QLabel(f"Email: {jugador.get('email', 'N/A')}")
        telefono_label = QLabel(f"Teléfono: {jugador.get('telefono', 'N/A')}")
        
        for label in [email_label, telefono_label]:
            label.setStyleSheet("color: white; padding: 5px;")
            info_layout.addWidget(label)
        
        info_layout.addStretch()
        content_layout.addLayout(info_layout)
        
        personajes = self.db.obtener_personajes_por_jugador(jugador['id'])
        
        if personajes:
            personajes_title = QLabel("PERSONAJES:")
            personajes_title.setStyleSheet("color: #FFD700; font-weight: bold; font-size: 16px; padding: 10px 0px;")
            content_layout.addWidget(personajes_title)
            
            for pj in personajes:
                pj_widget = self.crear_tarjeta_personaje(pj)
                content_layout.addWidget(pj_widget)
        else:
            sin_personajes = QLabel("Este jugador no tiene personajes creados")
            sin_personajes.setStyleSheet("color: #888; font-style: italic; padding: 20px; text-align: center;")
            content_layout.addWidget(sin_personajes)
        
        content_layout.addStretch()
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
        
        return widget

    def crear_tarjeta_personaje(self, personaje):
        widget = QWidget()
        widget.setStyleSheet("""
            background: #45484A;
            border: 1px solid #E58D05;
            border-radius: 8px;
            padding: 10px;
            margin: 5px;
        """)
        layout = QVBoxLayout(widget)
        
        info_principal = QLabel(f"{personaje['nombre_personaje']} - Nivel {personaje['nivel']} {personaje['raza']} {personaje['clase']}")
        info_principal.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        layout.addWidget(info_principal)
        
        stats_layout = QHBoxLayout()
        
        stats = [
            ("FUE", personaje.get('fuerza', 0)),
            ("DES", personaje.get('destreza', 0)),
            ("CON", personaje.get('constitucion', 0)),
            ("INT", personaje.get('inteligencia', 0)),
            ("SAB", personaje.get('sabiduria', 0)),
            ("CAR", personaje.get('carisma', 0))
        ]
        
        for abrev, valor in stats:
            stat_widget = QWidget()
            stat_layout = QVBoxLayout(stat_widget)
            
            stat_label = QLabel(abrev)
            stat_label.setStyleSheet("color: #E58D05; font-size: 10px; text-align: center;")
            
            stat_valor = QLabel(str(valor))
            stat_valor.setStyleSheet("color: white; font-weight: bold; font-size: 12px; text-align: center;")
            
            modificador = (valor - 10) // 2
            mod_label = QLabel(f"{modificador:+d}")
            mod_label.setStyleSheet("color: #90EE90; font-size: 10px; text-align: center;")
            
            stat_layout.addWidget(stat_label)
            stat_layout.addWidget(stat_valor)
            stat_layout.addWidget(mod_label)
            stat_layout.setContentsMargins(2, 2, 2, 2)
            
            stats_layout.addWidget(stat_widget)
        
        layout.addLayout(stats_layout)
        
        hp_label = QLabel(f"PG: {personaje.get('puntos_golpe_actuales', 0)}/{personaje.get('puntos_golpe_max', 0)}")
        hp_label.setStyleSheet("color: #FF6B6B; font-size: 12px;")
        layout.addWidget(hp_label)
        
        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.setStyleSheet("""
            QPushButton {
                background-color: #FF6B6B;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 3px 8px;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #FF5252;
            }
        """)
        btn_eliminar.clicked.connect(lambda checked, p=personaje: self.eliminar_personaje(p))
        layout.addWidget(btn_eliminar)
        
        return widget

    def crear_formulario_jugador(self):
        widget = QWidget()
        widget.setStyleSheet("background: #3a3a3a; color: white; padding: 20px;")
        layout = QVBoxLayout(widget)
        
        titulo = QLabel("NUEVO JUGADOR")
        titulo.setStyleSheet("color: #E58D05; font-size: 20px; font-weight: bold; padding: 10px; text-align: center;")
        layout.addWidget(titulo)
        
        # Formulario simple
        form_layout = QVBoxLayout()
        
        self.nombre_jugador_input = QLineEdit()
        self.nombre_jugador_input.setPlaceholderText("Nombre del jugador")
        
        self.email_jugador_input = QLineEdit()
        self.email_jugador_input.setPlaceholderText("Email (opcional)")
        
        self.telefono_jugador_input = QLineEdit()
        self.telefono_jugador_input.setPlaceholderText("Teléfono (opcional)")
        
        for campo in [self.nombre_jugador_input, self.email_jugador_input, self.telefono_jugador_input]:
            campo.setStyleSheet("background: #2c2c2c; color: white; border: 1px solid #E58D05; padding: 8px; margin: 5px;")
            form_layout.addWidget(campo)
        
        layout.addLayout(form_layout)
        
        btn_guardar = QPushButton("Guardar Jugador")
        btn_guardar.setStyleSheet("""
            QPushButton {
                background-color: #E58D05;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #8B4513;
            }
        """)
        btn_guardar.clicked.connect(self.guardar_jugador)
        layout.addWidget(btn_guardar)
        
        layout.addStretch()
        return widget

    def crear_formulario_personaje(self):

        widget = QWidget()
        widget.setStyleSheet("background: #3a3a3a; color: white; padding: 20px;")
        layout = QVBoxLayout(widget)
        
        titulo = QLabel("NUEVO PERSONAJE")
        titulo.setStyleSheet("color: #E58D05; font-size: 20px; font-weight: bold; padding: 10px; text-align: center;")
        layout.addWidget(titulo)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #2c2c2c;
                width: 15px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #E58D05;
                border-radius: 7px;
            }
        """)
        
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        
        basic_layout = QGridLayout()
        
        self.nombre_pj_input = QLineEdit()
        self.nivel_pj_input = QSpinBox()
        self.nivel_pj_input.setRange(1, 20)
        self.nivel_pj_input.setValue(1)
        
        jugadores = self.db.obtener_jugadores()
        self.jugador_pj_combo = QComboBox()
        self.jugador_pj_combo.addItems([j['nombre_jugador'] for j in jugadores])
        
        razas = obtener_razas()
        clases = obtener_clases()
        
        self.raza_pj_combo = QComboBox()
        self.raza_pj_combo.addItems([raza['nombre'] for raza in razas])
        
        self.clase_pj_combo = QComboBox()
        self.clase_pj_combo.addItems([clase['nombre'] for clase in clases])
        
        campos_basicos = [
            ("Jugador:", self.jugador_pj_combo),
            ("Nombre:", self.nombre_pj_input),
            ("Raza:", self.raza_pj_combo),
            ("Clase:", self.clase_pj_combo),
            ("Nivel:", self.nivel_pj_input)
        ]
        
        for i, (label, campo) in enumerate(campos_basicos):
            lbl = QLabel(label)
            lbl.setStyleSheet("color: #E58D05; font-weight: bold;")
            campo.setStyleSheet("background: #2c2c2c; color: white; border: 1px solid #E58D05; padding: 5px;")
            basic_layout.addWidget(lbl, i, 0)
            basic_layout.addWidget(campo, i, 1)
        
        form_layout.addLayout(basic_layout)
        
        stats_title = QLabel("CARACTERISTICAS")
        stats_title.setStyleSheet("color: #FFD700; font-weight: bold; font-size: 16px; padding: 20px 0px 10px 0px;")
        form_layout.addWidget(stats_title)
        
        stats_layout = QGridLayout()
        
        self.fuerza_input = QSpinBox()
        self.destreza_input = QSpinBox()
        self.constitucion_input = QSpinBox()
        self.inteligencia_input = QSpinBox()
        self.sabiduria_input = QSpinBox()
        self.carisma_input = QSpinBox()
        
        stats_inputs = [
            ("Fuerza:", self.fuerza_input),
            ("Destreza:", self.destreza_input),
            ("Constitucion:", self.constitucion_input),
            ("Inteligencia:", self.inteligencia_input),
            ("Sabiduria:", self.sabiduria_input),
            ("Carisma:", self.carisma_input)
        ]
        
        for spinbox in [self.fuerza_input, self.destreza_input, self.constitucion_input,
                       self.inteligencia_input, self.sabiduria_input, self.carisma_input]:
            spinbox.setRange(1, 20)
            spinbox.setValue(10)
            spinbox.setStyleSheet("background: #2c2c2c; color: white; border: 1px solid #E58D05; padding: 5px;")
        
        for i, (label, input_field) in enumerate(stats_inputs):
            lbl = QLabel(label)
            lbl.setStyleSheet("color: #E58D05; font-weight: bold;")
            stats_layout.addWidget(lbl, i//2, (i%2)*2)
            stats_layout.addWidget(input_field, i//2, (i%2)*2+1)
        
        form_layout.addLayout(stats_layout)
        
        hp_layout = QHBoxLayout()
        hp_label = QLabel("Puntos de Golpe:")
        hp_label.setStyleSheet("color: #E58D05; font-weight: bold;")
        
        self.pg_max_input = QSpinBox()
        self.pg_max_input.setRange(1, 200)
        self.pg_max_input.setValue(6)
        self.pg_max_input.setStyleSheet("background: #2c2c2c; color: white; border: 1px solid #E58D05; padding: 5px;")
        
        self.pg_actual_input = QSpinBox()
        self.pg_actual_input.setRange(0, 200)
        self.pg_actual_input.setValue(6)
        self.pg_actual_input.setStyleSheet("background: #2c2c2c; color: white; border: 1px solid #E58D05; padding: 5px;")
        
        hp_layout.addWidget(hp_label)
        hp_layout.addWidget(QLabel("Max:"))
        hp_layout.addWidget(self.pg_max_input)
        hp_layout.addWidget(QLabel("Actual:"))
        hp_layout.addWidget(self.pg_actual_input)
        hp_layout.addStretch()
        
        form_layout.addLayout(hp_layout)
        
        form_layout.addStretch()
        
        btn_guardar = QPushButton("Crear Personaje")
        btn_guardar.setStyleSheet("""
            QPushButton {
                background-color: #E58D05;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #8B4513;
            }
        """)
        btn_guardar.clicked.connect(self.guardar_personaje)
        form_layout.addWidget(btn_guardar)
        
        scroll.setWidget(form_widget)
        layout.addWidget(scroll)
        
        return widget
    
    def crear_ficha_item_detallada(self, detalle):
        widget = QWidget()
        widget.setStyleSheet("""
            background: #3a3a3a; 
            color: white; 
            border: 2px solid #E58D05;
            border-radius: 10px;
            padding: 15px;
        """)
        layout = QVBoxLayout(widget)
        
        nombre = QLabel(detalle['nombre'])
        nombre.setStyleSheet("color: #E58D05; font-size: 24px; font-weight: bold; padding: 10px;")
        layout.addWidget(nombre)
        
        info_layout = QGridLayout()
        
        if 'categoria' in detalle:
            info_layout.addWidget(QLabel("Categoría:"), 0, 0)
            info_layout.addWidget(QLabel(detalle['categoria']), 0, 1)
        
        if 'tipo' in detalle:
            info_layout.addWidget(QLabel("Tipo:"), 0, 0)
            info_layout.addWidget(QLabel(detalle['tipo']), 0, 1)
        
        if 'rareza' in detalle:
            info_layout.addWidget(QLabel("Rareza:"), 1, 0)
            info_layout.addWidget(QLabel(detalle['rareza']), 1, 1)
        
        if 'costo' in detalle and detalle['costo']:
            costo = f"{detalle['costo'].get('quantity', 0)} {detalle['costo'].get('unit', '')}"
            info_layout.addWidget(QLabel("Costo:"), 2, 0)
            info_layout.addWidget(QLabel(costo), 2, 1)
        
        if 'peso' in detalle and detalle['peso']:
            info_layout.addWidget(QLabel("Peso:"), 3, 0)
            info_layout.addWidget(QLabel(str(detalle['peso'])), 3, 1)
        
        layout.addLayout(info_layout)
        
        # Descripción
        if detalle.get('descripcion'):
            desc_label = QLabel("Descripción:")
            desc_label.setStyleSheet("color: #FFD700; font-weight: bold; padding-top: 15px;")
            layout.addWidget(desc_label)
            
            desc_text = QLabel(detalle['descripcion'])
            desc_text.setStyleSheet("color: white; padding: 10px; background: #2c2c2c; border-radius: 5px;")
            desc_text.setWordWrap(True)
            layout.addWidget(desc_text)
        
        layout.addStretch()
        return widget

    def guardar_jugador(self):
        jugador = {
            'nombre': self.nombre_jugador_input.text(),
            'email': self.email_jugador_input.text(),
            'telefono': self.telefono_jugador_input.text()
        }
        
        if jugador['nombre']:
            if self.db.guardar_jugador(jugador):
                items = self.obtener_lista_modulo({'nombre': 'Personajes'})
                self.actualizar_lista(items)
                
                success_label = QLabel("Jugador creado exitosamente")
                success_label.setAlignment(Qt.AlignCenter)
                success_label.setStyleSheet("color: #90EE90; font-size: 16px; padding: 20px;")
                self.mostrar_en_central(success_label)

    def guardar_personaje(self):
        nombre_jugador = self.jugador_pj_combo.currentText()
        jugador = self.db.buscar_jugador_por_nombre(nombre_jugador)
        
        if jugador and self.nombre_pj_input.text():
            personaje = {
                'nombre_personaje': self.nombre_pj_input.text(),
                'raza': self.raza_pj_combo.currentText(),
                'clase': self.clase_pj_combo.currentText(),
                'nivel': self.nivel_pj_input.value(),
                'fuerza': self.fuerza_input.value(),
                'destreza': self.destreza_input.value(),
                'constitucion': self.constitucion_input.value(),
                'inteligencia': self.inteligencia_input.value(),
                'sabiduria': self.sabiduria_input.value(),
                'carisma': self.carisma_input.value(),
                'puntos_golpe_max': self.pg_max_input.value(),
                'puntos_golpe_actuales': self.pg_actual_input.value(),
                'jugador_id': jugador['id']
            }
            
            if self.db.guardar_personaje(personaje):
                vista_actual = self.crear_vista_jugador(jugador)
                self.mostrar_en_central(vista_actual)

    def eliminar_personaje(self, personaje):
        jugador_id = personaje['jugador_id']
        if self.db.eliminar_personaje(personaje['id']):
            jugador = self.db.buscar_jugador_por_nombre(personaje['nombre_jugador'])
            if jugador:
                vista_actual = self.crear_vista_jugador(jugador)
                self.mostrar_en_central(vista_actual)

    def crear_ficha_monstruo_error(self, nombre_monstruo):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        error_label = QLabel(f"Error al cargar {nombre_monstruo}\n\nIntenta actualizar la lista o verifica tu conexion")
        error_label.setAlignment(Qt.AlignCenter)
        error_label.setStyleSheet("color: #FF6B6B; font-size: 16px; padding: 40px;")
        layout.addWidget(error_label)
        
        return widget

    def crear_vista_generica_detalle(self, modulo_nombre, item_nombre):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        titulo = QLabel(item_nombre)
        titulo.setStyleSheet("color: #E58D05; font-size: 20px; font-weight: bold; padding: 10px;")
        layout.addWidget(titulo)
        
        contenido = QLabel(f"Detalles de {item_nombre} en {modulo_nombre}\n\n(Integracion pendiente con modulo especifico)")
        contenido.setStyleSheet("color: white; font-size: 14px; padding: 20px;")
        contenido.setWordWrap(True)
        layout.addWidget(contenido)
        
        layout.addStretch()
        return widget
    def crear_ficha_hechizo(self, detalle):
        """Crea una ficha detallada para hechizos"""
        widget = QWidget()
        widget.setStyleSheet("""
            background: #3a3a3a; 
            color: white; 
            border: 2px solid #E58D05;
            border-radius: 10px;
        """)
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Scroll area para contenido
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #2c2c2c;
                width: 15px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #E58D05;
                border-radius: 7px;
            }
        """)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        
        # Encabezado con nombre y nivel
        nivel_texto = "Truco" if detalle.get('nivel', 0) == 0 else f"Nivel {detalle.get('nivel', '')}"
        header = QLabel(f"{detalle['nombre']} - {nivel_texto}")
        header.setStyleSheet("""
            color: #E58D05; 
            font-size: 24px; 
            font-weight: bold; 
            font-family: Papyrus;
            padding: 15px;
            border-bottom: 2px solid #E58D05;
            text-align: center;
        """)
        content_layout.addWidget(header)
        
        # Información básica en grid
        grid_info = QGridLayout()
        grid_info.setSpacing(10)
        
        info_basica = [
            ("Escuela:", detalle.get('escuela', 'N/A')),
            ("Tiempo de Lanzamiento:", detalle.get('tiempo_de_lanzamiento', 'N/A')),
            ("Alcance:", detalle.get('alcance', 'N/A')),
            ("Duración:", detalle.get('duracion', 'N/A'))
        ]
        
        for i, (label, value) in enumerate(info_basica):
            lbl = QLabel(label)
            lbl.setStyleSheet("color: #E58D05; font-weight: bold;")
            val = QLabel(str(value))
            val.setStyleSheet("color: white;")
            grid_info.addWidget(lbl, i, 0)
            grid_info.addWidget(val, i, 1)
        
        content_layout.addLayout(grid_info)
        
        # Componentes
        componentes = detalle.get('componentes', [])
        if componentes:
            comp_layout = QHBoxLayout()
            comp_label = QLabel("Componentes:")
            comp_label.setStyleSheet("color: #E58D05; font-weight: bold;")
            comp_layout.addWidget(comp_label)
            
            comp_text = ", ".join(componentes)
            if detalle.get('materiales'):
                comp_text += f" ({detalle['materiales']})"
            
            comp_valor = QLabel(comp_text)
            comp_valor.setStyleSheet("color: white;")
            comp_layout.addWidget(comp_valor)
            comp_layout.addStretch()
            
            content_layout.addLayout(comp_layout)
        
        # Clases que pueden usar el hechizo
        clases = detalle.get('clases', [])
        if clases:
            clases_layout = QHBoxLayout()
            clases_label = QLabel("Clases:")
            clases_label.setStyleSheet("color: #E58D05; font-weight: bold;")
            clases_layout.addWidget(clases_label)
            
            clases_text = ", ".join(clases)
            clases_valor = QLabel(clases_text)
            clases_valor.setStyleSheet("color: white;")
            clases_layout.addWidget(clases_valor)
            clases_layout.addStretch()
            
            content_layout.addLayout(clases_layout)
        
        # Descripción
        descripcion = detalle.get('descripcion', '')
        if descripcion:
            desc_label = QLabel("Descripción:")
            desc_label.setStyleSheet("color: #FFD700; font-weight: bold; font-size: 16px; padding: 15px 0px 5px 0px;")
            content_layout.addWidget(desc_label)
            
            desc_text = QLabel(descripcion)
            desc_text.setStyleSheet("color: white; padding: 10px; background: #2c2c2c; border-radius: 5px;")
            desc_text.setWordWrap(True)
            content_layout.addWidget(desc_text)
        
        content_layout.addStretch()
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
        
        return widget
    def ejecutar_opcion_modulo(self, modulo, opcion):
        nombre_modulo = modulo['nombre']
        
        if nombre_modulo == 'Bestiario' and opcion == 'Actualizar Lista':
            items = self.obtener_lista_modulo(modulo)
            self.actualizar_lista(items)
            return None
        
        elif nombre_modulo == 'Personajes':
            if opcion == 'Crear Jugador':
                return self.crear_formulario_jugador()
            elif opcion == 'Crear Personaje':
                return self.crear_formulario_personaje()
        elif nombre_modulo == 'Hechizos':  # <- Nuevo módulo
            if opcion == 'Actualizar Lista':
                items = self.obtener_lista_modulo(modulo)
                self.actualizar_lista(items)
                return None
        return None
   
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
            self.showNormal()
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = CustomWindow()
    ventana.show()
    sys.exit(app.exec_())
