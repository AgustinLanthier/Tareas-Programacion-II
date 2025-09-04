# trabajo realizado por Marcos Ledesma y Agustin Lanthier
# Version de Agustin Lanthier

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QMenuBar, 
                             QAction, QFileDialog, QMessageBox, QStatusBar,
                             QVBoxLayout, QWidget, QDialog, QLineEdit, QLabel, QPushButton, 
                             QGridLayout, QFontDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QFont
from PyQt5.QtPrintSupport import QPrintPreviewDialog, QPrinter
from theme import * 

# -------------------------------------------------------------------
# Extra: Buscar y Reemplazar
# -------------------------------------------------------------------
class BuscarReemplazarDialog(QDialog):
    def __init__(self, editor):
        super().__init__()
        self.setWindowTitle("Buscar y Reemplazar")
        self.editor = editor
        
        layout = QGridLayout()

        self.buscar_input = QLineEdit()
        self.reemplazar_input = QLineEdit()

        layout.addWidget(QLabel("Buscar:"), 0, 0)
        layout.addWidget(self.buscar_input, 0, 1)

        layout.addWidget(QLabel("Reemplazar con:"), 1, 0)
        layout.addWidget(self.reemplazar_input, 1, 1)

        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(self.buscar_texto)
        layout.addWidget(btn_buscar, 2, 0)

        btn_reemplazar = QPushButton("Reemplazar")
        btn_reemplazar.clicked.connect(self.reemplazar_texto)
        layout.addWidget(btn_reemplazar, 2, 1)

        self.setLayout(layout)

    def buscar_texto(self):
        texto = self.buscar_input.text()
        if texto:
            cursor = self.editor.document().find(texto)
            if not cursor.isNull():
                self.editor.setTextCursor(cursor)

    def reemplazar_texto(self):
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            cursor.insertText(self.reemplazar_input.text())

# -------------------------------------------------------------------
# Clase principal del Editor
# -------------------------------------------------------------------
class EditorTexto(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editor de Texto Open source")
        self.setGeometry(100, 100, 800, 600)
        
        self.editor = QTextEdit()
        self.setCentralWidget(self.editor)
        self.editor.setPlaceholderText("Escribe aquí tu texto...")
        self.archivo_actual = None

        # Complementos
        self.crear_menus()
        self.crear_barra_estado()

# -------------------------------------------------------------------
# Menús
# -------------------------------------------------------------------
    def crear_menus(self):
        bar_menu = self.menuBar()
        
        #=== FILE MENU ===#
        menu_file = bar_menu.addMenu('&Archivo')
        
        new_file = QAction('&Nuevo', self)
        new_file.setShortcut(QKeySequence.New)
        new_file.triggered.connect(self.nuevo_archivo)
        new_file.setShortcutContext(Qt.ApplicationShortcut)
        menu_file.addAction(new_file)
        menu_file.addSeparator()

        open_file = QAction('&Abrir', self)
        open_file.setShortcut(QKeySequence.Open)
        open_file.triggered.connect(self.abrir_archivo)
        open_file.setShortcutContext(Qt.ApplicationShortcut)
        menu_file.addAction(open_file)
        menu_file.addSeparator()

        save_file = QAction('&Guardar', self)
        save_file.setShortcut(QKeySequence.Save)
        save_file.triggered.connect(self.guardar_archivo)
        save_file.setShortcutContext(Qt.ApplicationShortcut)
        menu_file.addAction(save_file)
        menu_file.addSeparator()

        saveas_file = QAction('&Guardar Como', self)
        saveas_file.setShortcut(QKeySequence.SaveAs)
        saveas_file.triggered.connect(self.guardar_como)
        saveas_file.setShortcutContext(Qt.ApplicationShortcut)
        menu_file.addAction(saveas_file)
        menu_file.addSeparator()

        close_file = QAction('&Salir', self)
        close_file.setShortcut(QKeySequence.Quit)
        close_file.triggered.connect(self.salir)
        close_file.setShortcutContext(Qt.ApplicationShortcut)
        menu_file.addAction(close_file)
        menu_file.addSeparator()
        
        # === EDIT MENU ===#
        menu_edit = bar_menu.addMenu('&Editar')

        cut_text = QAction('&Cortar', self)
        cut_text.setShortcut(QKeySequence.Cut)
        cut_text.triggered.connect(self.editor.cut)
        cut_text.setShortcutContext(Qt.ApplicationShortcut)
        menu_edit.addAction(cut_text)
        menu_edit.addSeparator()

        copy_text = QAction('&Copiar', self)
        copy_text.setShortcut(QKeySequence.Copy)
        copy_text.triggered.connect(self.editor.copy)
        copy_text.setShortcutContext(Qt.ApplicationShortcut)
        menu_edit.addAction(copy_text)
        menu_edit.addSeparator()

        paste_text = QAction('&Pegar', self)
        paste_text.setShortcut(QKeySequence.Paste)
        paste_text.triggered.connect(self.editor.paste)
        paste_text.setShortcutContext(Qt.ApplicationShortcut)
        menu_edit.addAction(paste_text)
        menu_edit.addSeparator()
        
        # === HELP MENU ===#
        help_menu = bar_menu.addMenu('A&yuda')
        
        about_this = QAction('&Acerca de...', self)
        about_this.setShortcut(QKeySequence.HelpContents)
        about_this.triggered.connect(self.acerca_de)
        help_menu.addAction(about_this)

        # === FORMAT MENU ===#
        menu_format = bar_menu.addMenu('&Formato')

        bold_action = QAction('&Negrita', self)
        bold_action.setShortcut("Ctrl+B")
        bold_action.triggered.connect(self.texto_negrita)
        menu_format.addAction(bold_action)

        italic_action = QAction('&Cursiva', self)
        italic_action.setShortcut("Ctrl+I")
        italic_action.triggered.connect(self.texto_cursiva)
        menu_format.addAction(italic_action)

        underline_action = QAction('&Subrayado', self)
        underline_action.setShortcut("Ctrl+U")
        underline_action.triggered.connect(self.texto_subrayado)
        menu_format.addAction(underline_action)

        font_action = QAction('&Fuente...', self)
        font_action.triggered.connect(self.configurar_fuente)
        menu_format.addAction(font_action)

        # === TOOLS MENU ===#
        menu_tools = bar_menu.addMenu('&Herramientas')

        search_replace_action = QAction('&Buscar/Reemplazar', self)
        search_replace_action.setShortcut("Ctrl+F")
        search_replace_action.triggered.connect(self.buscar_reemplazar)
        menu_tools.addAction(search_replace_action)

        preview_action = QAction('&Vista previa de impresión', self)
        preview_action.triggered.connect(self.vista_previa)
        menu_tools.addAction(preview_action)

# -------------------------------------------------------------------
# Funciones de archivo
# -------------------------------------------------------------------
    def nuevo_archivo(self):
        if self.editor.document().isModified():
            respuesta = QMessageBox.question(self, 'Nuevo archivo',
                                           '¿Desea guardar los cambios?',
                                           QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if respuesta == QMessageBox.Yes:
                self.guardar_archivo()
            elif respuesta == QMessageBox.Cancel:
                return
        
        self.editor.clear()
        self.archivo_actual = None
        self.setWindowTitle("Editor - Nuevo documento")
        self.statusBar().showMessage("Nuevo documento creado", 2000)
    
    def abrir_archivo(self):
        archivo, _ = QFileDialog.getOpenFileName(
            self, 'Abrir archivo', '', 'Archivos de texto (*.txt);;Todos los archivos (*.*)' 
        )
        
        if archivo:
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                    self.editor.setPlainText(contenido)
                
                self.archivo_actual = archivo
                self.setWindowTitle(f"Editor - {archivo}")
                self.statusBar().showMessage(f"Archivo abierto: {archivo}", 3000)
                
            except Exception as e:
                QMessageBox.critical(self, 'Error',
                                   f'No se pudo abrir el archivo:\n{str(e)}')
    
    def guardar_archivo(self):
        if self.archivo_actual:
            self._escribir_archivo(self.archivo_actual)
        else:
            self.guardar_como()
    
    def guardar_como(self):
        archivo, _ = QFileDialog.getSaveFileName(
            self, 'Guardar archivo como', '', 'Archivos de texto (*.txt);;Todos los archivos (*.*)'
        )
        if archivo:
            if not archivo.lower().endswith(".txt"):
                archivo += ".txt"
            self._escribir_archivo(archivo) 
    
    def _escribir_archivo(self, archivo):
        try:
            with open(archivo, 'w', encoding='utf-8') as f:
                f.write(self.editor.toPlainText())
            
            self.archivo_actual = archivo
            self.setWindowTitle(f"Editor - {archivo}")
            self.statusBar().showMessage(f"Archivo guardado: {archivo}", 3000)
            self.editor.document().setModified(False)
            
        except Exception as e:
            QMessageBox.critical(self, 'Error al guardar',
                               f'No se pudo guardar el archivo:\n{str(e)}')

# -------------------------------------------------------------------
# Diálogos
# -------------------------------------------------------------------
    def acerca_de(self):
        QMessageBox.about(self, 'Acerca de Editor',
                         '''<h3>Aplicacion Open source</h3>
                         <p>Creado por Marcos Ledesma y Agustin Lahthier</p>
                         <p>DE TUP1 de UTNFRVT</p>
                         <p>Es open source no apto para windwos</p>''')
    
    def salir(self):
        respuesta = QMessageBox.question(self, 'Salir', 
                                         '¿Desea guardar los cambios antes de salir?',
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if respuesta == QMessageBox.Yes:
            self.guardar_archivo()
        elif respuesta == QMessageBox.No:
            self.close()

# -------------------------------------------------------------------
# Barra de estado
# -------------------------------------------------------------------
    def crear_barra_estado(self):
        self.statusBar().showMessage('Listo')
        self.editor.cursorPositionChanged.connect(self.actualizar_cursor)

    def actualizar_cursor(self):
        cursor = self.editor.textCursor() 
        linea = cursor.blockNumber() + 1   
        columna = cursor.columnNumber() + 1 
        self.statusBar().showMessage(f'Línea: {linea}, Columna: {columna}')

# -------------------------------------------------------------------
# Funciones extra (Formato, Buscar, Imprimir)
# -------------------------------------------------------------------
    def texto_negrita(self):
        fmt = self.editor.currentCharFormat()
        fmt.setFontWeight(QFont.Bold if fmt.fontWeight() != QFont.Bold else QFont.Normal)
        self.editor.setCurrentCharFormat(fmt)

    def texto_cursiva(self):
        fmt = self.editor.currentCharFormat()
        fmt.setFontItalic(not fmt.fontItalic())
        self.editor.setCurrentCharFormat(fmt)

    def texto_subrayado(self):
        fmt = self.editor.currentCharFormat()
        fmt.setFontUnderline(not fmt.fontUnderline())
        self.editor.setCurrentCharFormat(fmt)

    def configurar_fuente(self):
        fuente, ok = QFontDialog.getFont()
        if ok:
            self.editor.setFont(fuente)

    def buscar_reemplazar(self):
        dialogo = BuscarReemplazarDialog(self.editor)
        dialogo.exec_()

    def vista_previa(self):
        printer = QPrinter(QPrinter.HighResolution)
        preview = QPrintPreviewDialog(printer, self)
        preview.paintRequested.connect(self.editor.print_)
        preview.exec_()

# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = EditorTexto() 
    app.setStyleSheet(chaca_theme) 
    editor.show()
    sys.exit(app.exec_())
