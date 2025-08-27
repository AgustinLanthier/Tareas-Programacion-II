# Práctico PyQt5: Construcción guiada de una interfaz completa
# ------------------------------------------------------------
#
# Objetivo: Construir paso a paso un formulario de registro moderno y funcional.
# Cada ejercicio suma widgets y lógica, guiando al alumno en el uso de PyQt5 y QGridLayout.
#
# -----------------------------------------------------------------------------
# Ejercicio 1: Estructura básica y primer campo
# -----------------------------------------------------------------------------
# Teoría:
# - QLabel muestra texto en la interfaz.
# - QLineEdit permite ingresar texto.
# - QGridLayout organiza los widgets en filas y columnas.
#
# Consigna:
# - Ventana 400x300, título “Registro de Usuario”.
# - QLabel grande y centrado: “Formulario de Registro”.
# - QLabel “Nombre:” y QLineEdit al lado, usando QGridLayout.
# Trabajo realizado por Agustin Lanthier y Marcos Ledesma
# Version de Agustin Lanthier
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt  # Esto nos ayuda a alinear el texto al centro

class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de Usuario")
        self.setGeometry(100, 100, 400, 300)

        layout = QGridLayout()
        self.setLayout(layout)
        #Ejercicio 7
        self.setStyleSheet("background-color: lightgrey")  # Fondo gris claro para la ventana

        #Ejercicio 1
        titulo = QLabel("Formulario de Registro")
        tituloN = QLabel("Nombre:")
        nombre = QLineEdit()

        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-family:'Times New Roman';font-size: 30px; font-weight: bold; color: darkblue;")
        tituloN.setStyleSheet("font-family:'Times New Roman';font-size: 12px; font-weight: bold; ")


        layout.addWidget(titulo, 0, 0, 1, 2)
        layout.addWidget(tituloN, 1, 0)
        layout.addWidget(nombre, 1, 1)


# -----------------------------------------------------------------------------
# Ejercicio 2: Más campos de texto
# -----------------------------------------------------------------------------
# Teoría:
# - QLineEdit puede usarse para email y contraseña.
# - setEchoMode(QLineEdit.Password) oculta el texto del input.
# Consigna:
# - Agregar debajo los campos “Email:” y “Contraseña:” (QLabel + QLineEdit).
# - El campo contraseña debe ocultar el texto.    

        tituloE = QLabel("Email:")
        tituloE.setStyleSheet("font-family:'Times New Roman';font-size: 12px; font-weight: bold; ")
        email = QLineEdit()
        layout.addWidget(tituloE, 2,0)
        layout.addWidget(email, 2,1)

        tituloP = QLabel("Contraseña:")
        tituloP.setStyleSheet("font-family:'Times New Roman';font-size: 12px; font-weight: bold; ")
        password = QLineEdit()
        password.setEchoMode(QLineEdit.Password)
        layout.addWidget(tituloP, 3,0)
        layout.addWidget(password, 3,1)


# -----------------------------------------------------------------------------
# Ejercicio 3: Selección de género
# -----------------------------------------------------------------------------
# Teoría:
# - QRadioButton permite seleccionar una opción.
# - QButtonGroup agrupa los radio buttons para que solo uno esté activo.
#
# Consigna:
# - Agregar dos QRadioButton: “Masculino” y “Femenino”, en la misma fila.
# - Usar QButtonGroup para agruparlos.

        tituloG = QLabel("Géneros:")
        tituloG.setStyleSheet("font-family:'Times New Roman';font-size: 12px; font-weight: bold; ")
        masculino = QRadioButton("Masculino")
        femenino = QRadioButton("Femenino")

        generos = QButtonGroup()
        generos.addButton(masculino)
        generos.addButton(femenino)
        
        orientar = QHBoxLayout()
        orientar.setSpacing(10)
        orientar.addWidget(masculino)
        orientar.addWidget(femenino)

        genero_widget = QWidget()
        genero_widget.setLayout(orientar)

        layout.addWidget(tituloG, 4,0)
        layout.addWidget(genero_widget, 4,1)

# -----------------------------------------------------------------------------
# Ejercicio 4: Selección de país
# -----------------------------------------------------------------------------
# Teoría:
# - QComboBox permite elegir una opción de una lista desplegable.
#
# Consigna:
# - Agregar QLabel “País:” y QComboBox con al menos 5 países.

        tituloPais = QLabel("País:")
        tituloPais.setStyleSheet("font-family:'Times New Roman';font-size: 12px; font-weight: bold; ")
        paises = QComboBox()
        paises.addItems(["Argentina","Uruguay","Chile","Brasil","Colombia"])

        layout.addWidget(tituloPais, 5,0)
        layout.addWidget(paises, 5,1)



# -----------------------------------------------------------------------------
# Ejercicio 5: Checkbox de términos
# -----------------------------------------------------------------------------
# Teoría:
# - QCheckBox permite aceptar o rechazar condiciones.
#
# Consigna:
# - Agregar QCheckBox: “Acepto los términos y condiciones”.

        terminos = QCheckBox("Acepto los términos y condiciones")
        layout.addWidget(terminos,6,1)
# -----------------------------------------------------------------------------
# Ejercicio 6: Botón de envío y validación
# -----------------------------------------------------------------------------
# Teoría:
# - QPushButton ejecuta una función al hacer clic.
# - QMessageBox muestra mensajes emergentes.
#
# Consigna:
# - Agregar QPushButton “Registrarse”.
# - Al hacer clic, validar que todos los campos estén completos y el checkbox marcado.
# - Mostrar mensaje de éxito o error.
        boton_registro = QPushButton("Registrarse")
        layout.addWidget(boton_registro, 7, 0, 1, 2)
        boton_registro.clicked.connect(lambda: self.validar_formulario(nombre, email, password, generos, paises, terminos))

# -----------------------------------------------------------------------------
# Ejercicio 7: Personalización visual
# -----------------------------------------------------------------------------
# Consigna:
# - Cambiar colores de fondo, fuentes y tamaño de los widgets.
# - Centrar el formulario en la ventana.
        
        #Realizado al comienzo del init()
    def validar_formulario(self, nombre, email, password, generos, paises, terminos):
        # Validación: Verificamos si los campos están completos y si el checkbox está marcado
        if not nombre.text() or not email.text() or not password.text():
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return
        if not generos.checkedButton():
            QMessageBox.warning(self, "Error", "Debe seleccionar un género.")
            return
        if not paises.currentText():
            QMessageBox.warning(self, "Error", "Debe seleccionar un país.")
            return
        if not terminos.isChecked():
            QMessageBox.warning(self, "Error", "Debe aceptar los términos y condiciones.")
            return

            # Si todo está bien, mostramos el mensaje de éxito
        QMessageBox.information(self, "Registro Exitoso", "Te has registrado correctamente.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec_())
