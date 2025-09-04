# Práctico PyQt5: Editor de Texto con Menús y Diálogos
# ------------------------------------------------
#
# Objetivo: Crear un editor de texto completo integrando todos los conceptos aprendidos:
# menús, diálogos, gestión de archivos, barras de estado y shortcuts de teclado.
#
# Este ejercicio te guiará para construir una aplicación profesional paso a paso.
#
# -----------------------------------------------------------------------------
# Ejercicio 1: Ventana principal con área de texto
# -----------------------------------------------------------------------------
# Teoría:
# - QMainWindow es la base para aplicaciones con menús y barras de herramientas.
# - QTextEdit permite editar texto con formato básico.
# - setCentralWidget() define el widget principal de la ventana.
#
# Consigna:
# - Crear ventana principal (QMainWindow) de 800x600, título "Editor de Texto".
# - Agregar QTextEdit como widget central.
# - Configurar texto inicial: "Escribe aquí tu texto..."

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QMenuBar, 
                             QAction, QFileDialog, QMessageBox, QStatusBar,
                             QVBoxLayout, QWidget)
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class EditorTexto(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editor de Texto Open Source")
        self.setGeometry(100, 100, 800, 600)

        self.setWindowIcon(QIcon('kali.png'))
        
        # COMPLETAR: Crear QTextEdit y establecerlo como widget central
        # self.editor = QTextEdit()
        # self.setCentralWidget(self.editor)
        # self.editor.setPlaceholderText("Escribe aquí tu texto...")
        self.hoja = QTextEdit()
        self.setCentralWidget(self.hoja)
        self.hoja.setPlaceholderText("Escribe aquí tu texto...")
        
        self.crear_menus()
        self.crear_barra_estado()
# -----------------------------------------------------------------------------
# Ejercicio 2: Crear la barra de menús
# -----------------------------------------------------------------------------
# Teoría:
# - menuBar() devuelve la barra de menús de QMainWindow.
# - addMenu() crea un menú nuevo.
# - QAction representa una acción que puede estar en menús o barras de herramientas.
#
# Consigna:
# - Crear menú "Archivo" con opciones: "Nuevo", "Abrir", "Guardar", "Salir".
# - Crear menú "Editar" con opciones: "Cortar", "Copiar", "Pegar".
# - Crear menú "Ayuda" con opción: "Acerca de".
      

    def crear_menus(self):
        # COMPLETAR: Obtener la barra de menús
        # menubar = self.menuBar()
        bar = self.menuBar()


        # COMPLETAR: Crear menú Archivo
        # menu_archivo = menubar.addMenu('&Archivo')
        archive = bar.addMenu('&Archivo')
        # COMPLETAR: Crear acciones para el menú Archivo
        # accion_nuevo = QAction('&Nuevo', self)
        new = QAction('&Nuevo', self)
        # accion_nuevo.setShortcut(QKeySequence.New)  
        new.setShortcut("Ctrl+N")
        # accion_nuevo.triggered.connect(self.nuevo_archivo)
        new.triggered.connect(self.nuevo_archivo)
        archive.addAction(new)


        # Repite para: Abrir (Ctrl+O), Guardar (Ctrl+S), Salir (Ctrl+Q)
        open = QAction('&Abrir', self)  
        open.setShortcut("Ctrl+O")
        open.triggered.connect(self.abrir_archivo)
        archive.addAction(open)

        save = QAction('&Guardar', self)  
        save.setShortcut("Ctrl+S")
        save.triggered.connect(self.guardar_archivo)
        archive.addAction(save)
        
        close = QAction('&Salir', self)  
        close.setShortcut("Ctrl+Q")
        close.triggered.connect(self.salir)
        archive.addAction(close)

        about = bar.addMenu('&Ayuda')
        help1 = QAction('&Acerca de', self)
        help1.setShortcut("Ctrl+H")
        help1.triggered.connect(self.acerca_de)
        about.addAction(help1)
        

# -----------------------------------------------------------------------------
# Ejercicio 3: Implementar funciones de archivo
# -----------------------------------------------------------------------------
# Teoría:
# - QFileDialog proporciona diálogos estándar para abrir/guardar archivos.
# - QFileDialog.getOpenFileName() abre diálogo para seleccionar archivo.
# - QFileDialog.getSaveFileName() abre diálogo para guardar archivo.
#
# Consigna:
# - Implementar nuevo_archivo(): limpiar el editor.
# - Implementar abrir_archivo(): usar QFileDialog para cargar archivo.
# - Implementar guardar_archivo(): usar QFileDialog para guardar texto.

    def nuevo_archivo(self):


        if self.hoja.document().isModified():
            msg_box = QMessageBox()
            msg_box.setWindowTitle('Nuevo Archivo')
            msg_box.setText('¿Desea guardar los cambios?')
            si_button = msg_box.addButton("Sí", QMessageBox.YesRole)
            no_button = msg_box.addButton("No", QMessageBox.NoRole)
            cancel_button = msg_box.addButton("Cancelar", QMessageBox.RejectRole)

            msg_box.exec_()
            respond = msg_box.clickedButton()

            if respond == si_button:
                self.guardar_archivo()
                self.hoja.clear()
                self.statusBar().showMessage('Documento guardado. El nuevo archivo esta disponible.')
            elif respond == no_button:
                self.hoja.clear()
                self.statusBar().showMessage('Cambios descartados. Archivo nuevo.')
            elif respond == cancel_button:
                pass
    
    def abrir_archivo(self):
        # COMPLETAR: Abrir diálogo de archivo y cargar contenido
        # archivo, _ = QFileDialog.getOpenFileName(self, 'Abrir archivo', '', 'Archivos de texto (*.txt)')
        # if archivo:
        #     try:
        #         with open(archivo, 'r', encoding='utf-8') as f:
        #             contenido = f.read()
        #             self.editor.setPlainText(contenido)
        #     except Exception as e:
        #         QMessageBox.warning(self, 'Error', f'No se pudo abrir el archivo:\n{e}')
        archivo, _ = QFileDialog.getOpenFileName(self, 'Abrir archivo', '', 'Archivos de texto (*.txt)')
        if archivo:
            try:
                with open(archivo, 'r', encoding = 'utf-8') as f:
                    contenido = f.read()
                    self.hoja.setPlainText(contenido)
                    self.statusBar().showMessage("Archivo abierto exitosamente.")    
            except Exception as e:
                self.statusBar().showMessage("Error.")
                QMessageBox.warning(self,'Error',f'No se pudo abrir el archivo: \n{e}')

    def guardar_archivo(self):
        archivo, _ = QFileDialog.getSaveFileName(self, 'Guardar archivo', '', 'Archivos de texto (*.txt);;Todos los archivos (*)')
        if archivo:
            try:
                with open(archivo, 'w', encoding='utf-8') as f:
                    f.write(self.hoja.toPlainText())
                    self.statusBar().showMessage(f'Archivo guardado en "{archivo}".')
            except Exception as e:
                self.statusBar().showMessage("Error.")
                QMessageBox.warning(self, 'Error', f'No se pudo guardar el archivo:\n{e}')


# -----------------------------------------------------------------------------
# Ejercicio 4: Agregar diálogos informativos
# -----------------------------------------------------------------------------
# Teoría:
# - QMessageBox permite mostrar mensajes, advertencias y preguntas al usuario.
# - QMessageBox.information() muestra información.
# - QMessageBox.question() hace preguntas con botones Sí/No.
#
# Consigna:
# - Implementar acerca_de(): mostrar información del programa.
# - Modificar salir(): preguntar si desea guardar antes de cerrar.

    def acerca_de(self):
        # COMPLETAR: Mostrar información del programa
        # QMessageBox.information(self, 'Acerca de', 
        #                        'Editor de Texto v1.0\n\nCreado con PyQt5\nPara aprender desarrollo de interfaces.')
         QMessageBox.information(self, 'Acerca de', 
                                'Nombre: Editor de texto Open Source\nVersion: v1.0\nCreado por: Lanthier Agustin, Marcos Ledesma\nSolo para Linux, porque es cool 🥵')
    
    def salir(self):
        # COMPLETAR: Preguntar si desea guardar antes de salir
        # respuesta = QMessageBox.question(self, 'Salir', 
        #                                 '¿Desea guardar los cambios antes de salir?',
        #                                 QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        # if respuesta == QMessageBox.Yes:
        #     self.guardar_archivo()
        # elif respuesta == QMessageBox.No:
        #     self.close()
        msg_box = QMessageBox()
        msg_box.setWindowTitle('Salir')
        msg_box.setText('¿Desea guardar los cambios?')
        si_button = msg_box.addButton("Sí", QMessageBox.YesRole)
        no_button = msg_box.addButton("No", QMessageBox.NoRole)
        cancel_button = msg_box.addButton("Cancelar", QMessageBox.RejectRole)
        
        msg_box.exec_()
        respond = msg_box.clickedButton()

        if respond == si_button:
            self.guardar_archivo()
            self.close()
        elif respond == no_button:
            self.close()
        elif respond == cancel_button:
            pass

# -----------------------------------------------------------------------------
# Ejercicio 5: Agregar barra de estado
# -----------------------------------------------------------------------------
# Teoría:
# - QStatusBar muestra información en la parte inferior de la ventana.
# - statusBar() devuelve la barra de estado de QMainWindow.
# - showMessage() muestra un mensaje temporal.
#
# Consigna:
# - Agregar barra de estado que muestre "Listo" al inicio.
# - Actualizar mensaje cuando se realizan acciones (abrir, guardar, etc.).

    def crear_barra_estado(self):
        # COMPLETAR: Crear y configurar barra de estado
        # self.statusBar().showMessage('Listo')
        self.statusBar().showMessage('Listo')
        self.hoja.cursorPositionChanged.connect(self.actualizar_cursor)
    
    def actualizar_cursor(self):
        cursor = self.hoja.textCursor()
        linea = cursor.blockNumber() + 1
        columna = cursor.columnNumber() + 1
        self.statusBar().showMessage(f'Linea: {linea}, Columna: {columna}')           

# -----------------------------------------------------------------------------
# Ejercicio 6: Integración completa
# -----------------------------------------------------------------------------
# Consigna:
# - Llamar todos los métodos de configuración en __init__.
# - Probar todas las funcionalidades del editor.
# - Personalizar colores, fuentes o agregar más opciones de menú.

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = EditorTexto()
    # COMPLETAR: Llamar métodos de configuración
    # editor.crear_menus()
    # editor.crear_barra_estado()
    editor.show()
    sys.exit(app.exec_())

# -----------------------------------------------------------------------------
# Ejercicio Extra: Mejoras opcionales
# -----------------------------------------------------------------------------
# - Agregar función "Buscar y reemplazar".
# - Implementar vista previa de impresión.
# - Añadir formato de texto (negrita, cursiva).
# - Crear diálogo de configuración de fuente.
# - Implementar funcionalidad de "Archivos recientes".
