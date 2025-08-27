
# Trabajo realizado por Agustin Lanthier y Marcos Ledesma
# Version de Agustin Lanthier
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 

class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de Usuario")
        self.setGeometry(100, 100, 400, 300)

        layout = QGridLayout()
        self.setLayout(layout)
        self.setStyleSheet("background-color: lightgrey")  

        titulo = QLabel("Formulario de Registro")
        tituloN = QLabel("Nombre:")
        nombre = QLineEdit()

        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-family:'Times New Roman';font-size: 30px; font-weight: bold; color: darkblue;")
        tituloN.setStyleSheet("font-family:'Times New Roman';font-size: 12px; font-weight: bold; ")


        layout.addWidget(titulo, 0, 0, 1, 2)
        layout.addWidget(tituloN, 1, 0)
        layout.addWidget(nombre, 1, 1)

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


        tituloPais = QLabel("País:")
        tituloPais.setStyleSheet("font-family:'Times New Roman';font-size: 12px; font-weight: bold; ")
        paises = QComboBox()
        paises.addItems(["Argentina","Uruguay","Chile","Brasil","Colombia"])

        layout.addWidget(tituloPais, 5,0)
        layout.addWidget(paises, 5,1)



        terminos = QCheckBox("Acepto los términos y condiciones")
        layout.addWidget(terminos,7,1)

        boton_registro = QPushButton("Registrarse")
        layout.addWidget(boton_registro, 8, 0, 1, 2)
        boton_registro.clicked.connect(lambda: self.validar_formulario(nombre, email, password, generos, paises, terminos,fecha_nac))
# -----------------------------------------------------------------------------
# Ejercicio extra: Agregar un campo de fecha de nacimiento y validación avanzada
# -----------------------------------------------------------------------------
# Teoría:
# - QDateEdit permite seleccionar una fecha desde un calendario.
# - Puedes obtener la fecha seleccionada con .date().toString() o .date().year(), etc.
#
# Consigna:
# - Agrega un QLabel "Fecha de nacimiento:" y un QDateEdit al lado, usando el grid.
# - Al hacer clic en "Registrarse", valida que la fecha no sea posterior a hoy y que el usuario tenga al menos 13 años.
# - Si la validación falla, muestra un mensaje de error; si es correcta, muestra un mensaje de éxito.
#
# Pista: Usa QDate.currentDate() para comparar fechas.
        tituloF = QLabel("Fecha de nacimiento:")
        tituloF.setStyleSheet("font-family:'Times New Roman';font-size: 12px; font-weight: bold; ")
        
        tituloN = QLabel("Fecha de nacimiento:")
        tituloN.setStyleSheet("font-family:'Times New Roman';font-size: 12px; font-weight: bold; ")
        fecha_nac = QDateEdit()
        fecha_nac.setCalendarPopup(True)
        fecha_nac.setDate(QDate.currentDate())  
        layout.addWidget(tituloN, 6, 0)
        layout.addWidget(fecha_nac, 6, 1)
        
    
    def validar_formulario(self, nombre, email, password, generos, paises, terminos, fecha_nac):
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
        hoy = QDate.currentDate()
        nacimiento = fecha_nac.date()

        if nacimiento > hoy:
            QMessageBox.warning(self, "Error", "La fecha de nacimiento no puede ser futura.")
            return
        if nacimiento > hoy.addYears(-13):
            QMessageBox.warning(self, "Error", "Debe tener al menos 13 años para registrarse.")
            return
        QMessageBox.information(self, "Registro Exitoso", "Te has registrado correctamente.")




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec_())
