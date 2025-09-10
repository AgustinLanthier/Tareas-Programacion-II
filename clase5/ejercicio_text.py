
import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QLabel, QLineEdit, 
                             QPushButton, QTextEdit, QComboBox, QMessageBox,
                             QFileDialog, QGroupBox, QListWidget, QListWidgetItem, QSplitter)
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class SistemaDocentes(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión de Docentes")
        self.setGeometry(100, 100, 1000, 700)
        
        self.archivo_datos = "docentes.txt"
        
        self.configurar_interfaz()
        self.cargar_datos()
        
        # Estilo
        self.setStyleSheet("""
            QMainWindow { background-color: #f8f9fa; }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px;
                color: #495057;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #0056b3; }
            QPushButton:pressed { background-color: #004085; }
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                background-color: white;
            }
            QListWidget, QTextEdit {
                border: 1px solid #ced4da;
                border-radius: 4px;
                background-color: white;
            }
        """)

    def configurar_interfaz(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        panel_izquierdo = self.crear_panel_formulario()
        panel_derecho = self.crear_panel_lista()
        
        splitter.addWidget(panel_izquierdo)
        splitter.addWidget(panel_derecho)
        splitter.setSizes([400, 600])

    def crear_panel_formulario(self):
        widget = QWidget()
        layout = QVBoxLayout()
    
        
        grupo_form = QGroupBox("Datos del Docente")
        form_layout = QGridLayout()
        #Legajo
        self.legajo_edit = QLineEdit()
        form_layout.addWidget(QLabel("Legajo:"), 0, 0)
        self.legajo_edit.setValidator(QIntValidator(0, 1000, self))
        form_layout.addWidget(self.legajo_edit, 0, 1)
    
        #Nombre
        self.nombre_edit = QLineEdit()
        form_layout.addWidget(QLabel("Nombre:"), 1, 0)
        regex = QRegExp("[a-zA-Z\\s]+")
        self.nombre_edit.setValidator(QRegExpValidator(regex, self))
        form_layout.addWidget(self.nombre_edit, 1, 1)
        #Apellido
        self.apellido_edit = QLineEdit()
        form_layout.addWidget(QLabel("Apellido:"), 2, 0)
        self.apellido_edit.setValidator(QRegExpValidator(regex, self))
        form_layout.addWidget(self.apellido_edit, 2, 1)
        #DNI
        self.dni_edit = QLineEdit()
        form_layout.addWidget(QLabel("DNI:"), 3, 0)
        self.dni_edit.setValidator(QIntValidator(0, 10000000, self))
        form_layout.addWidget(self.dni_edit, 3, 1)
        #Email
        self.email_edit = QLineEdit()
        self.domain_edit = QComboBox()
        self.domain_edit.setFixedSize(120,35)
        self.domain_edit.addItems(["@gmail.com","@outlook.com","@yahoo.com","@hotmail.com"])

        self.email_funcion = QHBoxLayout()
        self.email_funcion.setSpacing(1)
        self.email_funcion.addWidget(self.email_edit)
        self.email_funcion.addWidget(self.domain_edit)

        self.email_nameDom = QWidget()
        self.email_nameDom.setLayout(self.email_funcion)

        form_layout.addWidget(QLabel("Email:"), 4, 0)
        form_layout.addWidget(self.email_nameDom, 4, 1, 1, 2)
        #Telefono
        self.telefono_edit = QLineEdit()
        self.code_country = QComboBox()
        self.code_country.setFixedSize(55,35)
        self.code_country.addItems(["+54", "+55", "+56"])
        
        self.tel_funcion = QHBoxLayout()
        self.tel_funcion.setSpacing(1)
        self.tel_funcion.addWidget(self.code_country)
        self.tel_funcion.addWidget(self.telefono_edit)

        self.tel_numCode = QWidget()
        self.tel_numCode.setLayout(self.tel_funcion)

        form_layout.addWidget(QLabel("Teléfono:"), 5, 0)
        form_layout.addWidget(self.tel_numCode, 5, 1, 1, 2)
        #Materia
        self.materia_edit = QComboBox()
        self.materia_edit.addItems(["Programacion I", "Programacion II", "Arquitectura y Sistemas Operativos", "Matematica I", "Ingles I"])
        form_layout.addWidget(QLabel("Materia:"), 6, 0)
        form_layout.addWidget(self.materia_edit, 6, 1)
        #Categoria
        self.categoria_combo = QComboBox()
        self.categoria_combo.addItems(["Titular", "Asociado", "Adjunto", "Auxiliar", "Interino"])
        form_layout.addWidget(QLabel("Categoría:"), 7, 0)
        form_layout.addWidget(self.categoria_combo, 7, 1)

        grupo_form.setLayout(form_layout)
        layout.addWidget(grupo_form)

        grupo_botones = QGroupBox("Acciones")
        botones_layout = QVBoxLayout()

        self.btn_agregar = QPushButton("Agregar Docente")
        self.btn_agregar.clicked.connect(self.agregar_docente)
        botones_layout.addWidget(self.btn_agregar)

        btn_buscar = QPushButton("Buscar Docente")
        btn_buscar.clicked.connect(self.buscar_docente)
        botones_layout.addWidget(btn_buscar)

        btn_modificar = QPushButton("Modificar Docente")
        btn_modificar.clicked.connect(self.modificar_docente)
        botones_layout.addWidget(btn_modificar)

        btn_eliminar = QPushButton("Eliminar Docente")
        btn_eliminar.clicked.connect(self.eliminar_docente)
        botones_layout.addWidget(btn_eliminar)

        btn_limpiar = QPushButton("Limpiar Formulario")
        btn_limpiar.clicked.connect(self.limpiar_formulario)
        botones_layout.addWidget(btn_limpiar)

        btn_exportar = QPushButton("Exportar a CSV")
        btn_exportar.clicked.connect(self.exportar_datos)
        botones_layout.addWidget(btn_exportar)

        grupo_botones.setLayout(botones_layout)
        layout.addWidget(grupo_botones)

        widget.setLayout(layout)
        return widget

    def crear_panel_lista(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        busqueda_layout = QHBoxLayout()
        busqueda_layout.addWidget(QLabel("Buscar:"))
        self.busqueda_edit = QLineEdit()
        self.busqueda_edit.setPlaceholderText("Apellido, Nombre o Legajo...")
        self.busqueda_edit.textChanged.connect(self.filtrar_lista)
        busqueda_layout.addWidget(self.busqueda_edit)
        layout.addLayout(busqueda_layout)
        
        self.lista_docentes = QListWidget()
        self.lista_docentes.itemClicked.connect(self.mostrar_detalles)
        layout.addWidget(self.lista_docentes)
        
        grupo_detalles = QGroupBox("Detalles del Docente Seleccionado")
        self.detalles_text = QTextEdit()
        self.detalles_text.setReadOnly(True)
        self.detalles_text.setMaximumHeight(200)
        detalles_layout = QVBoxLayout()
        detalles_layout.addWidget(self.detalles_text)
        grupo_detalles.setLayout(detalles_layout)
        layout.addWidget(grupo_detalles)
        
        widget.setLayout(layout)
        return widget

    def cargar_datos(self):
        if not os.path.exists(self.archivo_datos):
            return
        try:
            with open(self.archivo_datos, "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    datos = linea.strip().split("|")
                    if len(datos) == 8:
                        self.agregar_a_lista(datos)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar datos:\n{e}")

    def guardar_datos(self):
        try:
            with open(self.archivo_datos, "w", encoding="utf-8") as archivo:
                for i in range(self.lista_docentes.count()):
                    item = self.lista_docentes.item(i)
                    datos = item.data(Qt.UserRole)
                    archivo.write("|".join(datos) + "\n")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar datos:\n{e}")

    def agregar_docente(self):
        legajo = self.legajo_edit.text().strip()
        if not legajo:
            QMessageBox.warning(self, "Error", "El legajo es obligatorio")
            return
        for i in range(self.lista_docentes.count()):
            if self.lista_docentes.item(i).data(Qt.UserRole)[0] == legajo:
                QMessageBox.warning(self, "Error", "Ya existe un docente con ese legajo")
                return
        datos = [
            legajo,
            self.nombre_edit.text().strip(),
            self.apellido_edit.text().strip(),
            self.dni_edit.text().strip(),
            self.email_edit.text().strip(),
            self.telefono_edit.text().strip(),
            self.materia_edit.currentText(),
            self.categoria_combo.currentText(),
            self.domain_edit.currentText(),
            self.code_country.currentText()
        ]
        self.agregar_a_lista(datos)
        self.guardar_datos()
        self.limpiar_formulario()
        QMessageBox.information(self, "Éxito", "Docente agregado correctamente")

    def agregar_a_lista(self, datos):
        texto = f"{datos[2]}, {datos[1]} ({datos[0]})"
        item = QListWidgetItem(texto)
        item.setData(Qt.UserRole, datos)
        self.lista_docentes.addItem(item)

    def filtrar_lista(self):
        texto = self.busqueda_edit.text().lower()
        for i in range(self.lista_docentes.count()):
            item = self.lista_docentes.item(i)
            datos = item.data(Qt.UserRole)
            coincide = any(texto in campo.lower() for campo in [datos[0], datos[1], datos[2]])
            item.setHidden(not coincide)

    def mostrar_detalles(self, item):
        datos = item.data(Qt.UserRole)
        detalles = f"""
        INFORMACIÓN DEL DOCENTE
        ========================
        Legajo: {datos[0]}
        Nombre: {datos[1]}
        Apellido: {datos[2]}
        DNI: {datos[3]}
        Email: {datos[4] + datos[8]}
        Teléfono: {datos[9] + datos[5]}
        Materia: {datos[6]}
        Categoría: {datos[7]}
        """
        self.detalles_text.setPlainText(detalles)

    def buscar_docente(self):
        legajo = self.legajo_edit.text().strip()
        if not legajo:
            QMessageBox.warning(self, "Error", "Ingrese un legajo para buscar")
            return
        for i in range(self.lista_docentes.count()):
            item = self.lista_docentes.item(i)
            if item.data(Qt.UserRole)[0].lower() == legajo.lower():
                self.lista_docentes.setCurrentItem(item)
                self.mostrar_detalles(item)
                return
        QMessageBox.information(self, "No encontrado", f"No se encontró docente con legajo {legajo}")

    def modificar_docente(self):
        item = self.lista_docentes.currentItem()
        if not item:
            QMessageBox.warning(self, "Error", "Seleccione un docente para modificar")
            return
        datos = item.data(Qt.UserRole)
        self.legajo_edit.setText(datos[0])
        self.nombre_edit.setText(datos[1])
        self.apellido_edit.setText(datos[2])
        self.dni_edit.setText(datos[3])
        self.email_edit.setText(datos[4])
        self.telefono_edit.setText(datos[5])
        self.materia_edit.setText(datos[6])
        self.categoria_combo.setCurrentText(datos[7])
        self.btn_agregar.setText("Actualizar Docente")
        self.btn_agregar.clicked.disconnect()
        self.btn_agregar.clicked.connect(lambda: self.actualizar_docente(item))

    def actualizar_docente(self, item):
        datos = [
            self.legajo_edit.text().strip(),
            self.nombre_edit.text().strip(),
            self.apellido_edit.text().strip(),
            self.dni_edit.text().strip(),
            self.email_edit.text().strip(),
            self.telefono_edit.text().strip(),
            self.materia_edit.text().strip(),
            self.categoria_combo.currentText()
        ]
        item.setData(Qt.UserRole, datos)
        item.setText(f"{datos[2]}, {datos[1]} ({datos[0]})")
        self.guardar_datos()
        self.limpiar_formulario()
        self.btn_agregar.setText("Agregar Docente")
        self.btn_agregar.clicked.disconnect()
        self.btn_agregar.clicked.connect(self.agregar_docente)
        QMessageBox.information(self, "Éxito", "Docente actualizado correctamente")

    def eliminar_docente(self):
        item = self.lista_docentes.currentItem()
        if not item:
            QMessageBox.warning(self, "Error", "Seleccione un docente para eliminar")
            return
        datos = item.data(Qt.UserRole)
        respuesta = QMessageBox.question(self, "Confirmar", f"¿Eliminar a {datos[1]} {datos[2]}?",
                                         QMessageBox.Yes | QMessageBox.No)
        if respuesta == QMessageBox.Yes:
            self.lista_docentes.takeItem(self.lista_docentes.row(item))
            self.guardar_datos()
            QMessageBox.information(self, "Éxito", "Docente eliminado")

    def limpiar_formulario(self):
        self.legajo_edit.clear()
        self.nombre_edit.clear()
        self.apellido_edit.clear()
        self.dni_edit.clear()
        self.email_edit.clear()
        self.telefono_edit.clear()
        self.materia_edit.clear()
        self.categoria_combo.setCurrentIndex(0)
        self.btn_agregar.setText("Agregar Docente")
        self.btn_agregar.clicked.disconnect()
        self.btn_agregar.clicked.connect(self.agregar_docente)

    def exportar_datos(self):
        archivo, _ = QFileDialog.getSaveFileName(self, "Exportar datos", "docentes_export.csv", "CSV (*.csv)")
        if archivo:
            try:
                with open(archivo, "w", encoding="utf-8") as f:
                    f.write("Legajo,Nombre,Apellido,DNI,Email,Telefono,Materia,Categoria\n")
                    for i in range(self.lista_docentes.count()):
                        datos = self.lista_docentes.item(i).data(Qt.UserRole)
                        f.write(",".join(datos) + "\n")
                QMessageBox.information(self, "Éxito", "Datos exportados a CSV")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo exportar:\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    sistema = SistemaDocentes()
    sistema.show()
    sys.exit(app.exec_())

