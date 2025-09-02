# Práctico PyQt5: Uso de múltiples ventanas (Herramientas y Contexto)
# -------------------------------------------------------------------
#
# Objetivo: Aprender a crear y manejar dos ventanas simultáneas en PyQt5.
# Una ventana será de herramientas (con botones como Guardar, Abrir, Buscar, etc.)
# y la otra mostrará el contexto: un formulario de afiliados al Club Atlético Chacarita Juniors.
#
# Cada ejercicio suma widgets y lógica, guiando al alumno en el uso de PyQt5, QGridLayout y manejo de ventanas.


# -----------------------------------------------------------------------------
# Ejercicio 4: Conectar botones de herramientas con el formulario
# -----------------------------------------------------------------------------
# Teoría:
# - Los botones pueden ejecutar funciones que interactúan con la otra ventana.
# - Puedes pasar referencias entre ventanas para manipular datos.
#
# Consigna:
# - Haz que el botón "Guardar" muestre un mensaje con los datos ingresados en el formulario.
# - El botón "Salir" debe cerrar ambas ventanas.
#
# -----------------------------------------------------------------------------
# Ejercicio 5: Personalización visual y validaciones
# -----------------------------------------------------------------------------
# Consigna:
# - Cambia colores, fuentes y tamaño de los widgets para una interfaz moderna.
# - Valida que los campos obligatorios estén completos antes de guardar.
#
# -----------------------------------------------------------------------------
# Sugerencia:
# - Usa QDateEdit para la self.fecha de nacimiento.
# - Usa QMessageBox para mostrar mensajes.
#
# -----------------------------------------------------------------------------
# Esqueleto inicial:

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *

class VentanaHerramientas(QWidget):
    def __init__(self, ventana_formulario):
        super().__init__()
        self.setWindowTitle("Herramientas")
        self.setGeometry(650, 100, 200, 300)
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, self.width(), self.height())

        self.blur = QGraphicsBlurEffect()
        self.blur.setBlurRadius(5)  # Ajustá el valor (más alto = más difuso)
        self.label.setGraphicsEffect(self.blur)
        # Mostrar la imagen inicial
        self.actualizar_fondo()
        
        # -----------------------------------------------------------------------------
        # Ejercicio 2: Crear la ventana de herramientas
        # -----------------------------------------------------------------------------
        # Teoría:
        # - Otra instancia de QWidget puede funcionar como ventana secundaria.
        # - QPushButton permite crear botones de acción.
        # - QVBoxLayout organiza widgets en columna.
        #
        # Consigna:
        # - Crear una ventana secundaria de 200x300, título "Herramientas".
        # - Agregar botones: "Guardar", "Abrir", "Buscar", "Salir".
        self.guardar = QPushButton("Guardar")
        self.abrir = QPushButton("Abrir")
        self.buscar = QPushButton("Buscar")
        self.salir = QPushButton("Salir")

        self.guardar.setStyleSheet("color: darkred;font-weight: bold; background-color: white; border: 2px solid black; border-radius: 8px; padding: 7px 15px;")
        self.abrir.setStyleSheet("color: darkred;font-weight: bold; background-color: white; border: 2px solid black; border-radius: 8px; padding: 7px 15px;")
        self.buscar.setStyleSheet("color: darkred;font-weight: bold; background-color: white; border: 2px solid black; border-radius: 8px; padding: 7px 15px;")
        self.salir.setStyleSheet("color: darkred;font-weight: bold; background-color: white; border: 2px solid black; border-radius: 8px; padding: 7px 15px;")


        layout.addWidget(self.guardar)
        layout.addWidget(self.abrir)
        layout.addWidget(self.buscar)
        layout.addWidget(self.salir)

        # -----------------------------------------------------------------------------
        # Ejercicio 4: Conectar botones de herramientas con el formulario
        # -----------------------------------------------------------------------------
        # Teoría:
        # - Los botones pueden ejecutar funciones que interactúan con la otra ventana.
        # - Puedes pasar referencias entre ventanas para manipular datos.
        #
        # Consigna:
        # - Haz que el botón "Guardar" muestre un mensaje con los datos ingresados en el formulario.
        # - El botón "Salir" debe cerrar ambas ventanas.
        self.guardar.clicked.connect(self.mostrar_datos)
        self.salir.clicked.connect(self.cerrar_aplicacion)

        # Guardar la referencia de la ventana de formulario para acceder a sus datos
        self.ventana_formulario = ventana_formulario

    def mostrar_datos(self):
        # Obtener los datos del formulario
        nombre = self.ventana_formulario.nombre.text()
        apellido = self.ventana_formulario.apellido.text()
        dni = self.ventana_formulario.dni.text()
        fecha = self.ventana_formulario.fecha.date()

        if not nombre or not apellido or not dni or not fecha:
            QMessageBox.warning(self, "Campos incompletos", "Por favor, complete todos los campos.")
            return 
        hoy = QDate.currentDate()
        if fecha > hoy:
            QMessageBox.warning(self, "Error", "La fecha de nacimiento no puede ser futura.")
            return

        fecha_minima = hoy.addYears(-18)
        if fecha > fecha_minima:
            QMessageBox.warning(self, "Error", "Debe tener al menos 18 años para registrarse.")
            return
        # Mostrar los datos en un mensaje
        QMessageBox.information(self, "Datos del Formulario", f"Nombre: {nombre}\nApellido: {apellido}\nDNI: {dni}\nFecha de nacimiento: {fecha.toString()}")

    def cerrar_aplicacion(self):
        # Cerrar ambas ventanas
        self.ventana_formulario.close()
        self.close()


    def actualizar_fondo(self):
        # Cargar imagen original y pasarla a gris
        imagen = QImage("fondo.png").convertToFormat(QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(imagen)

        # Escalar al tamaño actual de la ventana
        self.label.setPixmap(pixmap.scaled(self.size()))

    def resizeEvent(self, event):
        # Cada vez que se redimensiona, se vuelve a escalar
        self.label.setGeometry(0, 0, self.width(), self.height())
        self.actualizar_fondo()

class VentanaFormulario(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Afiliados - Chacarita Juniors") # Aguante boca
        self.setGeometry(100, 100, 500, 350)
        layout = QGridLayout()
        self.setLayout(layout)
        self.setStyleSheet("background-color: white")
        
        # -----------------------------------------------------------------------------
        # Ejercicio 1: Crear la ventana de contexto (formulario de afiliados)
        # -----------------------------------------------------------------------------
        # Teoría:
        # - QWidget es la base para crear ventanas.
        # - QGridLayout organiza los widgets en filas y columnas.
        # - QLabel y QLineEdit permiten mostrar e ingresar datos.
        #
        # Consigna:
        # - Crear una ventana principal (QWidget) de 500x350, título "Afiliados - Chacarita Juniors".
        # - Agregar QLabel grande y centrado: "Formulario de Afiliación".
        # - Agregar QLabel y QLineEdit para Nombre, Apellido, DNI y Fecha de nacimiento.
        tituloA = QLabel("Formulario de Afiliación")
        tituloA.setAlignment(Qt.AlignCenter)
        tituloA.setStyleSheet("font-family:'Times New Roman';font-size: 30px; font-weight: bold; color: red;")

        self.tituloN = QLabel("Nombre:")
        self.tituloN.setStyleSheet("font-family:'Times New Roman';font-size: 12px; font-weight: bold;")
        self.tituloApellido = QLabel("Apellido:")
        self.tituloApellido.setStyleSheet("font-family:'Times New Roman';font-size: 12px; font-weight: bold;")
        self.tituloD = QLabel("DNI:")
        self.tituloD.setStyleSheet("font-family:'Times New Roman';font-size: 12px; font-weight: bold;")
        self.tituloF = QLabel("Fecha de nacimiento:")
        self.tituloF.setStyleSheet("font-family:'Times New Roman';font-size: 12px; font-weight: bold;")

        self.nombre = QLineEdit()
        self.apellido = QLineEdit()
        self.dni = QLineEdit()
        self.fecha = QDateEdit()
        self.fecha.setCalendarPopup(True)
        self.fecha.setDate(QDate.currentDate())

        self.foto = QLabel(self)
        self.escudo = QPixmap("escudo.png")
        self.escudo = self.escudo.scaled(150, 150, Qt.KeepAspectRatio)
        self.foto.setPixmap(self.escudo)
        self.foto.setAlignment(Qt.AlignCenter)  
        layout.addWidget(self.foto, 1, 0, 1, 2)

        layout.addWidget(tituloA, 0, 0, 1, 2)
        layout.addWidget(self.tituloN, 2, 0)
        layout.addWidget(self.tituloApellido, 3, 0)
        layout.addWidget(self.tituloD, 4, 0)
        layout.addWidget(self.tituloF, 5, 0)

        layout.addWidget(self.nombre, 2, 1)
        layout.addWidget(self.apellido, 3, 1)
        layout.addWidget(self.dni, 4, 1)
        layout.addWidget(self.fecha, 5, 1)

        self.abrir_herramientas = QPushButton("Abrir Herramientas", self)
        self.abrir_herramientas.clicked.connect(self.abrir_herramientas_func)

        self.abrir_herramientas.setStyleSheet("font-weight: bold; background-color: lightgrey; border: 2px solid black; border-radius: 8px; padding: 7px 15px;")
        layout.addWidget(self.abrir_herramientas, 8, 0, 1, 2)

        self.ventana_herramientas = None

        btn_play = QPushButton("▶ Reproducir Hinchada")
        btn_play.clicked.connect(self.reproducir_cancion)
        layout.addWidget(btn_play, 6, 0)

        # Botón Pausar/Continuar
        btn_pause = QPushButton("⏸ Pausar/Continuar")
        btn_pause.clicked.connect(self.pausar_cancion)
        layout.addWidget(btn_pause, 6, 1)


        self.player = QMediaPlayer()
        url = QUrl.fromLocalFile("cancion.mp3")  
        self.player.setMedia(QMediaContent(url))

    def reproducir_cancion(self):
        self.player.play()

    def pausar_cancion(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        elif self.player.state() == QMediaPlayer.PausedState:
            self.player.play()



    def abrir_herramientas_func(self):
        if self.ventana_herramientas is None:
            self.ventana_herramientas = VentanaHerramientas(self)  # Pasar la referencia de la ventana de formulario
        self.ventana_herramientas.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    ventana_form = VentanaFormulario()
    ventana_form.show()
    
    sys.exit(app.exec_())

