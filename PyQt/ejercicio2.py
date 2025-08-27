# Práctico PyQt5: Formulario de compra de pasaje de avión
# --------------------------------------------------------
#
# En este práctico, construirás paso a paso un formulario de compra de pasaje aéreo.
# Cada ejercicio suma widgets y lógica, guiando el aprendizaje de PyQt5 y QGridLayout.
#
# -----------------------------------------------------------------------------
# Ejercicio 1: Estructura básica y datos del pasajero
# -----------------------------------------------------------------------------
# Teoría:
# - QLabel muestra texto en la interfaz.
# - QLineEdit permite ingresar texto.
# - QGridLayout organiza los widgets en filas y columnas.
#
# Consigna:
# - Ventana 500x350, título “Compra de Pasaje Aéreo”.
# - QLabel grande y centrado: “Formulario de Compra”.
# - QLabel “Nombre:” y QLineEdit al lado.
# - QLabel “Apellido:” y QLineEdit al lado.
# - QLabel “DNI:” y QLineEdit al lado.
# Trabajo realizado por Agustin Lanthier y Marcos Ledesma
# Version de Agustin Lanthier

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Compra de Pasaje Aéreo")
        self.setGeometry(100, 100, 500, 350)
        layout = QGridLayout()
        self.setLayout(layout)

        titulo = QLabel("Formulario de compra")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-family:'Times New Roman';font-size: 40px; font-weight: bold; color: darkred;")

        nombre = QLineEdit()
        apellido = QLineEdit()
        dni = QLineEdit()
        tituloN = QLabel("Nombre:")
        tituloA = QLabel("Apellido:")
        tituloD = QLabel("DNI:")
        tituloN.setStyleSheet("font-family:'Times New Roman';font-size: 12px; font-weight: bold; ")
        tituloA.setStyleSheet("font-family:'Times New Roman';font-size: 12px; font-weight: bold; ")
        tituloD.setStyleSheet("font-family:'Times New Roman';font-size: 12px; font-weight: bold; ")

        layout.addWidget(titulo, 0, 0, 1, 2)
        layout.addWidget(tituloN, 1, 0)
        layout.addWidget(nombre, 1, 1)
        layout.addWidget(tituloA, 2, 0)
        layout.addWidget(apellido, 2, 1)
        layout.addWidget(tituloD, 3, 0)
        layout.addWidget(dni, 3, 1)

# -----------------------------------------------------------------------------
# Ejercicio 2: Selección de vuelo
# -----------------------------------------------------------------------------
# Teoría:
# - QComboBox permite elegir una opción de una lista desplegable.
# - QDateEdit permite seleccionar una fecha.
#
# Consigna:
# - Agregar QLabel “Origen:” y QComboBox con al menos 3 ciudades.
# - Agregar QLabel “Destino:” y QComboBox con al menos 3 ciudades.
# - Agregar QLabel “Fecha de vuelo:” y QDateEdit.
        tituloC = QLabel("Origen:")
        tituloC.setStyleSheet("font-family:'Times New Roman';font-size: 12px; font-weight: bold; ")
        ciudadesO = QComboBox()
        ciudadesO.addItems(["Washington D.C","Tokio","Buenos Aires","Rio de Janeiro"])
        layout.addWidget(tituloC, 4, 0)
        layout.addWidget(ciudadesO, 4, 1)

        tituloDestino = QLabel("Destino:")
        tituloDestino.setStyleSheet("font-family:'Times New Roman';font-size: 12px; font-weight: bold; ")
        ciudadesD = QComboBox()
        ciudadesD.addItems(["Washington D.C","Tokio","Buenos Aires","Rio de Janeiro"])
        layout.addWidget(tituloDestino, 5, 0)
        layout.addWidget(ciudadesD, 5, 1)

        tituloF = QLabel("Fecha de vuelo:")
        tituloF.setStyleSheet("font-family:'Times New Roman';font-size: 12px; font-weight: bold; ")
        fecha = QDateEdit()
        fecha.setCalendarPopup(True)
        layout.addWidget(tituloF, 6, 0)
        layout.addWidget(fecha, 6, 1)


# -----------------------------------------------------------------------------
# Ejercicio 3: Clase y cantidad de pasajeros
# -----------------------------------------------------------------------------
# Teoría:
# - QRadioButton permite seleccionar una opción (Ej: clase turista o ejecutiva).
# - QSpinBox permite elegir un número (Ej: cantidad de pasajeros).
#
# Consigna:
# - Agregar QRadioButton para “Turista” y “Ejecutiva”.
# - Agregar QLabel “Cantidad de pasajeros:” y QSpinBox (mínimo 1, máximo 10).

        tituloClase = QLabel("Clase: ")
        tituloClase.setStyleSheet("font-family:'Times New Roman';font-size: 12px; font-weight: bold; ")
        turista = QRadioButton("Turista")
        ejecutivo = QRadioButton("Ejecutivo")

        clases = QButtonGroup()
        clases.addButton(turista)
        clases.addButton(ejecutivo)
        
        orientar = QHBoxLayout()
        orientar.setSpacing(10)
        orientar.addWidget(turista)
        orientar.addWidget(ejecutivo)

        clases_widget = QWidget()
        clases_widget.setLayout(orientar)

        layout.addWidget(tituloClase, 7,0)
        layout.addWidget(clases_widget, 7,1)

        tituloPasajeros = QLabel("Cantidad de pasajeros:")
        tituloPasajeros.setStyleSheet("font-family:'Times New Roman';font-size: 12px; font-weight: bold; ")
        cantidad = QSpinBox()
        cantidad.setRange(1,10)
        cantidad.setValue(1)
        cantidad.setSingleStep(1)

        layout.addWidget(tituloPasajeros, 8,0)
        layout.addWidget(cantidad, 8,1)


# -----------------------------------------------------------------------------
# Ejercicio 4: Confirmación y resumen
# -----------------------------------------------------------------------------
# Teoría:
# - QPushButton ejecuta una función al hacer clic.
# - QMessageBox muestra mensajes emergentes.
#
# Consigna:
# - Agregar QPushButton “Comprar”.
# - Al hacer clic, mostrar un resumen de la compra en un QMessageBox.
        botonComprar = QPushButton("Comprar")
        botonComprar.setStyleSheet("font-size: 14px; font-weight: bold; background-color: darkred; color: white; padding: 6px; border-radius: 6px;")
        layout.addWidget(botonComprar, 9, 0, 1, 2, alignment=Qt.AlignCenter)

        def confirmarCompra():
            # Validaciones
            if not nombre.text().strip():
                QMessageBox.warning(self, "Error", "Debe ingresar el nombre.")
                return
            if not apellido.text().strip():
                QMessageBox.warning(self, "Error", "Debe ingresar el apellido.")
                return
            if not dni.text().strip():
                QMessageBox.warning(self, "Error", "Debe ingresar el DNI.")
                return
            if not (turista.isChecked() or ejecutivo.isChecked()):
                QMessageBox.warning(self, "Error", "Debe seleccionar una clase (Turista o Ejecutivo).")
                return
            if ciudadesO.currentText() == ciudadesD.currentText():
                QMessageBox.warning(self, "Error", "El origen y destino no pueden ser iguales.")
                return

            # Si pasa todas las validaciones → resumen
            clase = "Turista" if turista.isChecked() else "Ejecutivo"
            resumen = f"""
            --- RESUMEN DE COMPRA ---

            Nombre: {nombre.text()}
            Apellido: {apellido.text()}
            DNI: {dni.text()}

            Origen: {ciudadesO.currentText()}
            Destino: {ciudadesD.currentText()}
            Fecha: {fecha.date().toString("dd/MM/yyyy")}

            Clase: {clase}
            Cantidad de pasajeros: {cantidad.value()}
            """
            QMessageBox.information(self, "Confirmación de compra", resumen)

        botonComprar.clicked.connect(confirmarCompra)

# -----------------------------------------------------------------------------
# Ejercicio 5: Personalización visual
# -----------------------------------------------------------------------------
# Consigna:
# - Cambiar colores, fuentes y tamaño de los widgets para una interfaz moderna.
# - Centrar el formulario en la ventana.


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec_())
