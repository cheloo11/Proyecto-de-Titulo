from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QTableWidget, QTableWidgetItem, QHeaderView,
                            QAbstractItemView, QLineEdit, QComboBox, QSizePolicy,
                            QDialog, QFormLayout, QSpinBox, QDoubleSpinBox, QMessageBox,
                            QTextEdit, QDialogButtonBox, QGroupBox, QFrame, QSpacerItem)
from PyQt6.QtGui import QColor, QFont, QIntValidator
from PyQt6.QtCore import Qt
from ui.styles.common_styles import LABEL_STYLE, LABEL_INFO_STYLE, LABEL_BOLD_STYLE
from controllers.obra_controller import ObraController

#Definimos una función de estilo global para aplicarla a todos los diálogos
def apply_dialog_style(dialog):
    dialog.setStyleSheet("""
        QDialog {
            background-color: #f5f5f5;
        }
        QLabel {
            color: #2C2C2C;
            background-color: transparent;
            border: none;
        }
        QLineEdit, QSpinBox, QDoubleSpinBox, QTextEdit {
            color: #2C2C2C;
            background-color: white;
            border: 2px solid #ddd;
            border-radius: 6px;
            padding: 8px;
        }
        QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QTextEdit:focus {
            border-color: #FF6B35;
        }
        QComboBox {
            color: #2C2C2C;
            background-color: white;
            border: 2px solid #ddd;
            border-radius: 6px;
            padding: 8px;
            min-height: 20px;
        }
        QComboBox:focus {
            border-color: #FF6B35;
        }
        QComboBox::drop-down {
            border: none;
            width: 20px;
        }
        QComboBox QAbstractItemView {
            color: #2C2C2C;
            background-color: white;
            selection-background-color: #FF6B35;
            selection-color: white;
        }
        QGroupBox {
            color: #2C2C2C;
            background-color: transparent;
            border: 2px solid #ddd;
            border-radius: 8px;
            margin-top: 15px;
            padding-top: 15px;
            font-size: 14px;
        }
        QGroupBox::title {
            color: #2C2C2C;
            background-color: #f5f5f5;
            subcontrol-origin: margin;
            left: 15px;
            padding: 0 8px 0 8px;
            font-weight: bold;
            font-size: 14px;
            border: none;
        }
        QHeaderView::section {
            color: #2C2C2C;
            background-color: #f8f9fa;
            border: 1px solid #ddd;
            padding: 8px;
            font-weight: bold;
        }
        QTableWidget {
            background-color: white;
            border: 2px solid #ddd;
            border-radius: 6px;
            gridline-color: #eee;
        }
        QTableWidget::item {
            color: #2C2C2C;
            padding: 8px;
            border: none;
        }
        QTableWidget::item:selected {
            background-color: #FF6B35;
            color: white;
        }
        QCheckBox, QRadioButton {
            color: #2C2C2C;
            background-color: transparent;
        }
    """)

# Modal para Ver Detalle (permite buscar por código)
class ViewDetailDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ver Detalle de Obra")
        self.setMinimumSize(600, 400)
        apply_dialog_style(self)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Sección de búsqueda por código
        search_group = QGroupBox("Buscar Obra")
        search_layout = QHBoxLayout(search_group)
        
        code_label = QLabel("Código:")
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Ingrese el código de la obra")
        
        search_btn = QPushButton("Buscar")
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF6B35;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #E55A2B;
            }
            QPushButton:pressed {
                background-color: #CC4A1F;
            }
        """)
        search_btn.clicked.connect(self.search_obra)
        
        search_layout.addWidget(code_label)
        search_layout.addWidget(self.code_input, 1)
        search_layout.addWidget(search_btn)
        
        # Sección de detalles de la obra con los nuevos campos
        details_group = QGroupBox("Detalles de la Obra")
        details_layout = QFormLayout(details_group)
        
        self.obra_id = None 
        self.obra_code = QLabel("-")
        self.obra_name = QLabel("-")
        self.obra_address = QLabel("-") 
        self.obra_start_date = QLabel("-")  
        self.obra_end_date = QLabel("-")  
        self.obra_manager = QLabel("-")
        
        # Estilo para las etiquetas de valores
        value_style = """
            QLabel {
                font-weight: bold; 
                color: #2C2C2C; 
                padding: 8px;
                background-color: transparent;
                border: none;
            }
        """
        self.obra_code.setStyleSheet(value_style)
        self.obra_name.setStyleSheet(value_style)
        self.obra_address.setStyleSheet(value_style)
        self.obra_start_date.setStyleSheet(value_style)
        self.obra_end_date.setStyleSheet(value_style)
        self.obra_manager.setStyleSheet(value_style)
        
        # Hacer que las etiquetas tengan saltos de línea si es necesario
        self.obra_name.setWordWrap(True)
        self.obra_address.setWordWrap(True)
        
        # Agregar campos al formulario con los nuevos campos
        details_layout.addRow(QLabel("Código:"), self.obra_code)
        details_layout.addRow(QLabel("Nombre:"), self.obra_name)
        details_layout.addRow(QLabel("Dirección:"), self.obra_address)
        details_layout.addRow(QLabel("Fecha Inicio:"), self.obra_start_date)
        details_layout.addRow(QLabel("Fecha Fin:"), self.obra_end_date)
        details_layout.addRow(QLabel("Jefe Responsable:"), self.obra_manager)
        
        # Botones de acción
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.button(QDialogButtonBox.StandardButton.Close).setText("Cerrar")
        button_box.button(QDialogButtonBox.StandardButton.Close).setStyleSheet("""
            QPushButton {
                background-color: #2C2C2C;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #1a1a1a;
            }
            QPushButton:pressed {
                background-color: #0F0F0F;
            }
        """)
        button_box.rejected.connect(self.reject)
        
        # Agregar todos los elementos al layout principal
        layout.addWidget(search_group)
        layout.addWidget(details_group)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def search_obra(self):
        code = self.code_input.text()
        
        if not code:
            QMessageBox.warning(self, "Error", "Por favor ingrese un código de obra.")
            return
            
        obra = ObraController.get_obra_by_code(code)
        
        if obra:
            self.obra_id = obra["id"]
            self.obra_code.setText(obra["codigo"])
            self.obra_name.setText(obra["nombre"])
            self.obra_address.setText(obra["direccion"])
            self.obra_start_date.setText(obra["fecha_inicio"])
            self.obra_end_date.setText(obra["fecha_fin"])
            self.obra_manager.setText(obra["jefe_responsable"])
        else:
            QMessageBox.information(self, "Obra no encontrada", 
                             f"No se encontró ninguna obra con el código {code}.")
            self.obra_id = None
            self.obra_code.setText("-")
            self.obra_name.setText("-")
            self.obra_address.setText("-")
            self.obra_start_date.setText("-")
            self.obra_end_date.setText("-")
            self.obra_manager.setText("-")

# Modal para Agregar Obra
class AddProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Nueva Obra")
        self.setMinimumSize(500, 300)
        apply_dialog_style(self) 
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Crear QGroupBox para el formulario
        form_group = QGroupBox("Información de la Obra")
        form_layout = QFormLayout(form_group)
        
        # Campos para agregar obra con los nuevos campos
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Ej. OB-001")
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre completo de la obra")
        
        self.address_input = QLineEdit() 
        self.address_input.setPlaceholderText("Dirección completa")
        
        self.start_date_input = QLineEdit()
        self.start_date_input.setPlaceholderText("DD/MM/AAAA")
        
        self.end_date_input = QLineEdit()
        self.end_date_input.setPlaceholderText("DD/MM/AAAA")
        
        self.manager_input = QLineEdit()
        self.manager_input.setPlaceholderText("Nombre del jefe responsable")
        
        # Nuevo campo para estado
        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["activa", "terminada"])
        
        # Agregar campos al formulario
        form_layout.addRow("Código*:", self.code_input)
        form_layout.addRow("Nombre*:", self.name_input)
        form_layout.addRow("Dirección*:", self.address_input)
        form_layout.addRow("Fecha Inicio*:", self.start_date_input)
        form_layout.addRow("Fecha Fin*:", self.end_date_input)
        form_layout.addRow("Jefe Responsable*:", self.manager_input)
        form_layout.addRow("Estado*:", self.estado_combo)
        
        # Nota sobre campos obligatorios
        note_label = QLabel("* Campos obligatorios")
        note_label.setStyleSheet("""
            QLabel {
                color: #FF6B35; 
                font-style: italic;
                background-color: transparent;
                border: none;
            }
        """)
        
        # Botones de acción
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.button(QDialogButtonBox.StandardButton.Save).setText("Guardar")
        button_box.button(QDialogButtonBox.StandardButton.Save).setStyleSheet("""
            QPushButton {
                background-color: #FF6B35;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #E55A2B;
            }
            QPushButton:pressed {
                background-color: #CC4A1F;
            }
        """)
        button_box.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancelar")
        button_box.button(QDialogButtonBox.StandardButton.Cancel).setStyleSheet("""
            QPushButton {
                background-color: #2C2C2C;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #1a1a1a;
            }
            QPushButton:pressed {
                background-color: #0F0F0F;
            }
        """)
        
        button_box.accepted.connect(self.accept_with_validation)
        button_box.rejected.connect(self.reject)
        
        # Agregar todo al layout principal
        layout.addWidget(form_group)
        layout.addWidget(note_label)
        layout.addWidget(button_box)
        
    def accept_with_validation(self):
        # Validar campos obligatorios con los nuevos campos
        if not self.code_input.text():
            QMessageBox.warning(self, "Error", "Por favor ingrese el código de la obra.")
            return
            
        if not self.name_input.text():
            QMessageBox.warning(self, "Error", "Por favor ingrese el nombre de la obra.")
            return
        
        if not self.address_input.text():
            QMessageBox.warning(self, "Error", "Por favor ingrese la dirección de la obra.")
            return
            
        if not self.start_date_input.text():
            QMessageBox.warning(self, "Error", "Por favor ingrese la fecha de inicio.")
            return
            
        if not self.end_date_input.text():
            QMessageBox.warning(self, "Error", "Por favor ingrese la fecha de fin estimada.")
            return
            
        if not self.manager_input.text():
            QMessageBox.warning(self, "Error", "Por favor ingrese el jefe responsable.")
            return
            
        # Obtener datos del formulario
        codigo = self.code_input.text()
        nombre = self.name_input.text()
        direccion = self.address_input.text()
        fecha_inicio = self.start_date_input.text()
        fecha_fin = self.end_date_input.text()
        jefe_responsable = self.manager_input.text()
        estado = self.estado_combo.currentText()
        
        # Agregar obra usando el controlador
        success, message = ObraController.add_obra(
            nombre, codigo, direccion, fecha_inicio, fecha_fin, jefe_responsable, estado
        )
        
        if success:
            QMessageBox.information(self, "Éxito", message)
            # Actualizar la tabla en la ventana principal
            if hasattr(self.parent(), "load_obras"):
                self.parent().load_obras()
            self.accept()
        else:
            QMessageBox.warning(self, "Error", message)


# Modal para Editar Obra
class EditProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Obra")
        self.setMinimumSize(500, 350)
        apply_dialog_style(self) 

        # Crear button_box aquí antes de llamar a init_ui
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | 
            QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.button(QDialogButtonBox.StandardButton.Save).setText("Guardar Cambios")
        self.button_box.button(QDialogButtonBox.StandardButton.Save).setStyleSheet("""
            QPushButton {
                background-color: #FF6B35;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #E55A2B;
            }
            QPushButton:pressed {
                background-color: #CC4A1F;
            }
        """)
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancelar")
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setStyleSheet("""
            QPushButton {
                background-color: #2C2C2C;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #1a1a1a;
            }
            QPushButton:pressed {
                background-color: #0F0F0F;
            }
        """)
        
        self.init_ui()
        
    def init_ui(self):
        # Definir y configurar todos los componentes
        layout = QVBoxLayout(self)
        
        # Sección de búsqueda con texto negro
        search_group = QGroupBox("Buscar Obra a Editar")
        search_layout = QHBoxLayout(search_group)
        search_layout.setContentsMargins(12, 8, 12, 8)
        search_layout.setSpacing(10)
        search_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        code_label = QLabel("Código:")
        
        self.search_code_input = QLineEdit()
        self.search_code_input.setPlaceholderText("Ingrese el código de la obra a editar")
        self.search_code_input.setMinimumHeight(32)
        self.search_code_input.setStyleSheet("QLineEdit {padding: 6px;}")
        
        search_btn = QPushButton("Buscar")
        search_btn.setFixedHeight(34)
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF6B35;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #E55A2B;
            }
            QPushButton:pressed {
                background-color: #CC4A1F;
            }
        """)
        search_btn.clicked.connect(self.search_obra)
        
        search_layout.addWidget(code_label)
        search_layout.addWidget(self.search_code_input, 1)
        search_layout.addWidget(search_btn)
        
        # Sección de edición
        edit_group = QGroupBox("Editar Datos de la Obra")
        self.form_layout = QFormLayout(edit_group)
        
        # Campos para editar 
        self.code_display = QLabel("-")
        self.code_display.setStyleSheet("""
            QLabel {
                font-weight: bold; 
                color: #2C2C2C;
                background-color: transparent;
                border: none;
            }
        """)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre de la obra")
        
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Ubicación de la obra")
        
        self.manager_input = QLineEdit()
        self.manager_input.setPlaceholderText("Nombre del responsable")
        
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Activa", "Finalizada", "Suspendida"])
        
        # Etiquetas para campos
        code_label_form = QLabel("Código:")
        name_label = QLabel("Nombre*:")
        location_label = QLabel("Ubicación*:")
        manager_label = QLabel("Responsable*:")
        status_label = QLabel("Estado:")
        
        # Agregar campos al formulario con etiquetas negras
        self.form_layout.addRow(code_label_form, self.code_display)
        self.form_layout.addRow(name_label, self.name_input)
        self.form_layout.addRow(location_label, self.location_input)
        self.form_layout.addRow(manager_label, self.manager_input)
        self.form_layout.addRow(status_label, self.status_combo)
        
        # Configuración de botones
        self.button_box.button(QDialogButtonBox.StandardButton.Save).setEnabled(False)
        self.button_box.accepted.connect(self.accept_with_validation)
        self.button_box.rejected.connect(self.reject)
        
        # Agregar todo al layout principal
        layout.addWidget(search_group)
        layout.addWidget(edit_group)
        layout.addWidget(self.button_box)
        
        self.enable_form_fields(False)
        
    def enable_form_fields(self, enable=True):
        """Habilita o deshabilita los campos del formulario"""
        self.name_input.setEnabled(enable)
        self.location_input.setEnabled(enable)
        self.manager_input.setEnabled(enable)
        self.status_combo.setEnabled(enable)
        self.button_box.button(QDialogButtonBox.StandardButton.Save).setEnabled(enable)
        
    def search_obra(self):
        code = self.search_code_input.text()
        
        if not code:
            QMessageBox.warning(self, "Error", "Por favor ingrese un código de obra.")
            return
            
        # Buscar obra usando el controlador real
        obra = ObraController.get_obra_by_code(code)
        
        if obra:
            # Guardar el ID para la eliminación posterior
            self.obra_id = obra["id"]
            
            # Mostrar información del material
            self.obra_code.setText(obra["codigo"])
            self.obra_name.setText(obra["nombre"])
            self.obra_location.setText(obra["direccion"])
            self.obra_manager.setText(obra["jefe_responsable"])
            self.obra_status.setText(obra["estado"])
            
            # Habilitar el botón de eliminar
            self.button_box.button(QDialogButtonBox.StandardButton.Yes).setEnabled(True)
        else:
            QMessageBox.information(self, "Obra no encontrada", 
                             f"No se encontró ninguna obra con el código {code}.")
            
            # Limpiar y deshabilitar
            self.obra_id = None  
            self.obra_code.setText("-")
            self.obra_name.setText("-")
            self.obra_location.setText("-")
            self.obra_manager.setText("-")
            self.obra_status.setText("-")
            self.button_box.button(QDialogButtonBox.StandardButton.Yes).setEnabled(False)

    def accept_with_validation(self):
        # Validar campos obligatorios
        if not self.name_input.text():
            QMessageBox.warning(self, "Error", "Por favor ingrese el nombre de la obra.")
            return
        
        if not self.location_input.text():
            QMessageBox.warning(self, "Error", "Por favor ingrese la ubicación de la obra.")
            return
            
        if not self.manager_input.text():
            QMessageBox.warning(self, "Error", "Por favor ingrese el responsable de la obra.")
            return
            
        # Obtener datos del formulario
        nombre = self.name_input.text()
        direccion = self.location_input.text()
        fecha_inicio = "01/01/2023" 
        fecha_fin = "31/12/2023"    
        jefe_responsable = self.manager_input.text()
        estado = self.status_combo.currentText()
        
        # Actualizar obra usando el controlador
        success, message = ObraController.update_obra(
            self.obra_id, nombre, direccion, fecha_inicio, fecha_fin, jefe_responsable, estado
        )
        
        if success:
            QMessageBox.information(self, "Éxito", message)
            # Actualizar la tabla en la ventana principal
            if hasattr(self.parent(), "load_obras"):
                self.parent().load_obras()
            self.accept()
        else:
            QMessageBox.warning(self, "Error", message)


# Modal para Eliminar Obra
class DeleteProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Eliminar Obra")
        self.setMinimumSize(450, 300)
        apply_dialog_style(self) 
        self.obra_id = None 
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Sección de búsqueda
        search_group = QGroupBox("Buscar Obra a Eliminar")
        search_layout = QHBoxLayout(search_group)
        
        code_label = QLabel("Código:")
        self.search_code_input = QLineEdit()
        self.search_code_input.setPlaceholderText("Ingrese el código de la obra a eliminar")
        
        search_btn = QPushButton("Buscar")
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF6B35;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #E55A2B;
            }
            QPushButton:pressed {
                background-color: #CC4A1F;
            }
        """)
        search_btn.clicked.connect(self.search_obra)
        
        search_layout.addWidget(code_label)
        search_layout.addWidget(self.search_code_input, 1)
        search_layout.addWidget(search_btn)
        
        # Información de la obra
        info_group = QGroupBox("Información de la Obra")
        info_layout = QFormLayout(info_group)
        
        self.obra_code = QLabel("-")
        self.obra_name = QLabel("-")
        self.obra_location = QLabel("-")
        self.obra_manager = QLabel("-")
        self.obra_status = QLabel("-")
        
        value_style = """
            QLabel {
                font-weight: bold; 
                color: #2C2C2C; 
                padding: 8px;
                background-color: transparent;
                border: none;
            }
        """
        self.obra_code.setStyleSheet(value_style)
        self.obra_name.setStyleSheet(value_style)
        self.obra_location.setStyleSheet(value_style)
        self.obra_manager.setStyleSheet(value_style)
        self.obra_status.setStyleSheet(value_style)
        
        self.obra_name.setWordWrap(True)
        self.obra_location.setWordWrap(True)
        
        info_layout.addRow("Código:", self.obra_code)
        info_layout.addRow("Nombre:", self.obra_name)
        info_layout.addRow("Ubicación:", self.obra_location)
        info_layout.addRow("Responsable:", self.obra_manager)
        info_layout.addRow("Estado:", self.obra_status)
        
        warning_label = QLabel("⚠️ ADVERTENCIA: Esta acción no se puede deshacer.")
        warning_label.setStyleSheet("""
            QLabel {
                color: #8B4513; 
                font-weight: bold; 
                margin-top: 10px;
                background-color: transparent;
                border: none;
            }
        """)
        warning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Yes | 
            QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.button(QDialogButtonBox.StandardButton.Yes).setText("Eliminar")
        self.button_box.button(QDialogButtonBox.StandardButton.Yes).setStyleSheet("""
            QPushButton {
                background-color: #8B4513;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #704010;
            }
            QPushButton:pressed {
                background-color: #5C300A;
            }
        """)
        self.button_box.button(QDialogButtonBox.StandardButton.Yes).setEnabled(False)
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancelar")
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setStyleSheet("""
            QPushButton {
                background-color: #2C2C2C;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #1a1a1a;
            }
            QPushButton:pressed {
                background-color: #0F0F0F;
            }
        """)
        
        self.button_box.accepted.connect(self.confirm_delete)
        self.button_box.rejected.connect(self.reject)
        
        layout.addWidget(search_group)
        layout.addWidget(info_group)
        layout.addWidget(warning_label)
        layout.addWidget(self.button_box)
        
    def search_obra(self):
        code = self.search_code_input.text()
        
        if not code:
            QMessageBox.warning(self, "Error", "Por favor ingrese un código de obra.")
            self.obra_id = None
            return
        
        obra = ObraController.get_obra_by_code(code)
        
        if obra:
            self.obra_id = obra["id"]
            self.obra_code.setText(obra["codigo"])
            self.obra_name.setText(obra["nombre"])
            self.obra_location.setText(obra["direccion"])
            self.obra_manager.setText(obra["jefe_responsable"])
            self.obra_status.setText(obra["estado"])
            self.button_box.button(QDialogButtonBox.StandardButton.Yes).setEnabled(True)
        else:
            QMessageBox.information(self, "Obra no encontrada", 
                                 f"No se encontró ninguna obra con el código {code}.")
            self.obra_id = None
            self.obra_code.setText("-")
            self.obra_name.setText("-")
            self.obra_location.setText("-")
            self.obra_manager.setText("-")
            self.obra_status.setText("-")
            self.button_box.button(QDialogButtonBox.StandardButton.Yes).setEnabled(False)
    
    def confirm_delete(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirmar eliminación")
        msg_box.setText(f"¿Está seguro que desea eliminar permanentemente la obra {self.obra_code.text()}?")
        msg_box.setInformativeText("Esta acción no se puede deshacer.")
        msg_box.setIcon(QMessageBox.Icon.Question)
        
        yes_button = msg_box.addButton("Sí, eliminar", QMessageBox.ButtonRole.YesRole)
        no_button = msg_box.addButton("Cancelar", QMessageBox.ButtonRole.NoRole)
        
        msg_box.setDefaultButton(no_button)
        msg_box.exec()
        
        if msg_box.clickedButton() == yes_button and self.obra_id:
            success, message = ObraController.delete_obra(self.obra_id)
            if success:
                QMessageBox.information(self, "Éxito", message)
                if hasattr(self.parent(), "load_obras"):
                    self.parent().load_obras()
                self.accept()
            else:
                QMessageBox.warning(self, "Error", message)
        

class ObrasView(QWidget):
    """Vista para gestión de obras (listar, agregar, editar, eliminar)."""
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # Header compacto y responsivo
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                          stop: 0 #FF6B35, stop: 1 #E55A2B);
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 10px;
            }
        """)
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(10, 10, 10, 10)
        
        title = QLabel("Gestión de Obras")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background: transparent;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        header_layout.addWidget(title)
        main_layout.addWidget(header_frame)
        
        # Botones CRUD con diseño mejorado
        crud_layout = QHBoxLayout()
        crud_layout.setSpacing(15)
        
        # Espaciador para centrar botones
        crud_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        # Botón Agregar 
        self.add_btn = QPushButton("Agregar")
        self.add_btn.setStyleSheet("QPushButton {background-color: #FF6B35; color: white; border: none; border-radius: 8px; padding: 12px 20px; font-size: 14px; font-weight: bold; min-width: 150px;} QPushButton:hover {background-color: #E55A2B;} QPushButton:pressed {background-color: #CC4A1F;}")
        self.add_btn.clicked.connect(self.open_add_dialog)

        # Botón Editar 
        self.edit_btn = QPushButton("Editar")
        self.edit_btn.setStyleSheet("QPushButton {background-color: #222; color: white; border: none; border-radius: 8px; padding: 12px 20px; font-size: 14px; font-weight: bold; min-width: 150px;} QPushButton:hover {background-color: #111;} QPushButton:pressed {background-color: #000;}")
        self.edit_btn.clicked.connect(self.open_edit_dialog)

        # Botón Eliminar 
        self.delete_btn = QPushButton("Eliminar")
        self.delete_btn.setStyleSheet("QPushButton {background-color: #8B4513; color: white; border: none; border-radius: 8px; padding: 12px 20px; font-size: 14px; font-weight: bold; min-width: 150px;} QPushButton:hover {background-color: #7A3A0F;} QPushButton:pressed {background-color: #69300A;}")
        self.delete_btn.clicked.connect(self.open_delete_dialog)

        # Agregar botones al layout CRUD
        crud_layout.addWidget(self.add_btn)
        crud_layout.addWidget(self.edit_btn)
        crud_layout.addWidget(self.delete_btn)
        # Espaciador para centrar botones
        crud_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        # Agregar layout de botones al principal
        main_layout.addLayout(crud_layout)
        
        # Separador visual
        separator = QWidget()
        separator.setFixedHeight(1)
        separator.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        separator.setStyleSheet("background-color: #ddd;")
        main_layout.addWidget(separator)
        
        # Área de filtros superior
        filter_layout = QHBoxLayout()
        
        # Combobox para filtro
        filter_label = QLabel("Filtro:")
        filter_label.setStyleSheet("""
            QLabel {
                color: #2C2C2C; 
                font-weight: bold;
                background-color: transparent;
                border: none;
            }
        """)
        # Combobox para filtro con estilo mejorado
        filter_combo = QComboBox()
        filter_combo.addItem("Todas las obras")
        filter_combo.addItem("Obras activas")
        filter_combo.addItem("Obras finalizadas")
        filter_combo.addItem("Obras suspendidas")
        filter_combo.setMinimumWidth(150)
        filter_combo.setStyleSheet("""
            QComboBox {
                border: 2px solid #ddd;
                border-radius: 6px;
                padding: 8px;
                background-color: white;
                color: #2C2C2C;
                min-height: 20px;
            }
            QComboBox:focus {
                border-color: #FF6B35;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox QAbstractItemView {
                color: #2C2C2C;
                background-color: white;
                selection-background-color: #FF6B35;
                selection-color: white;
            }
        """)

        # Grupo de búsqueda
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(5)
        
        # Campo de búsqueda mejorado
        search_field = QLineEdit()
        search_field.setPlaceholderText("Buscar obra...")
        search_field.setMinimumWidth(250)
        search_field.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ddd;
                border-radius: 6px;
                padding: 8px;
                color: #2C2C2C;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #FF6B35;
            }
        """)
        
        # Botón de buscar
        search_btn = QPushButton("Buscar")
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF6B35;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #E55A2B;
            }
            QPushButton:pressed {
                background-color: #CC4A1F;
            }
        """)
        
        # Agregar widgets al layout de búsqueda
        search_layout.addWidget(search_field)
        search_layout.addWidget(search_btn)
        
        # Agregar widgets al layout de filtros
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(filter_combo)
        filter_layout.addStretch()
        filter_layout.addWidget(search_container)
        
        main_layout.addLayout(filter_layout)
        
        # Tabla de obras
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(7) 
        self.inventory_table.setHorizontalHeaderLabels([
            "Código", "Nombre", "Dirección", "Fecha Inicio", "Fecha Fin", "Jefe Responsable", "Estado"
        ])
        
        # Configuración de la tabla
        self.inventory_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.inventory_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.inventory_table.verticalHeader().setVisible(False)
        self.inventory_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.inventory_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 2px solid #ddd;
                border-radius: 6px;
                gridline-color: #eee;
            }
            QTableWidget::item {
                padding: 8px;
                color: #2C2C2C;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #FF6B35;
                color: white;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                color: #2C2C2C;
                padding: 8px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
        """)
        
        # Configuración de anchos de columnas
        self.inventory_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Código
        self.inventory_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)          # Nombre (mantiene el stretch)
        self.inventory_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)          # Dirección
        self.inventory_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Fecha Inicio
        self.inventory_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Fecha Fin
        self.inventory_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Jefe Responsable
        self.inventory_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # Estado

        # Establecer anchos mínimos para evitar columnas demasiado estrechas
        self.inventory_table.setColumnWidth(0, 80)  
        self.inventory_table.setColumnWidth(3, 100)   
        self.inventory_table.setColumnWidth(4, 100)  
        self.inventory_table.setColumnWidth(5, 150)   
        self.inventory_table.setColumnWidth(6, 100)   
        
        # Cargar datos reales en vez de datos de ejemplo
        self.load_obras()
        
        # Doble clic en fila para ver detalles
        self.inventory_table.doubleClicked.connect(self.handle_double_click)
        
        # Agregar todos los elementos al layout principal
        main_layout.addWidget(self.inventory_table)
        
        self.setLayout(main_layout)
    
    # Métodos para abrir los modales
    def open_add_dialog(self):
        dialog = AddProductDialog(self)
        dialog.exec()
        
    def open_view_dialog(self):
        dialog = ViewDetailDialog(self)
        # Si hay una fila seleccionada, obtener el código para buscarlo automáticamente
        selected_rows = self.inventory_table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            code = self.inventory_table.item(row, 0).text()
            dialog.code_input.setText(code)
            dialog.search_obra()
        dialog.exec()
        
    def open_edit_dialog(self):
        dialog = EditProductDialog(self)
        # Si hay una fila seleccionada, obtener el código para buscarlo automáticamente
        selected_rows = self.inventory_table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            code = self.inventory_table.item(row, 0).text()
            dialog.search_code_input.setText(code)
            dialog.search_obra()
        dialog.exec()
        
    def open_delete_dialog(self):
        dialog = DeleteProductDialog(self)
        # Si hay una fila seleccionada, obtener el código para buscarlo automáticamente
        selected_rows = self.inventory_table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            code = self.inventory_table.item(row, 0).text()
            dialog.search_code_input.setText(code)
            dialog.search_obra()
        dialog.exec()
        
    def handle_double_click(self):
        """Al hacer doble clic en una fila, abre el diálogo de detalles"""
        self.open_view_dialog()
    
    # Añadir nuevo método para cargar obras desde la base de datos
    def load_obras(self):
        """Carga las obras desde la base de datos y las muestra en la tabla"""
        obras = ObraController.get_all_obras()
        
        self.inventory_table.setRowCount(len(obras))
        for row, obra in enumerate(obras):
            code_item = QTableWidgetItem(obra['codigo'])
            code_item.setData(Qt.ItemDataRole.UserRole, obra['id'])  # ID para uso interno
            
            name_item = QTableWidgetItem(obra['nombre'])
            address_item = QTableWidgetItem(obra['direccion'])
            start_date_item = QTableWidgetItem(obra['fecha_inicio'])
            end_date_item = QTableWidgetItem(obra['fecha_fin'])
            manager_item = QTableWidgetItem(obra['jefe_responsable'])
            estado_item = QTableWidgetItem(obra['estado'])
            
            # Asegurar que el texto use la paleta J&M
            code_item.setForeground(QColor("#2C2C2C"))
            name_item.setForeground(QColor("#2C2C2C"))
            address_item.setForeground(QColor("#2C2C2C"))
            start_date_item.setForeground(QColor("#2C2C2C"))
            end_date_item.setForeground(QColor("#2C2C2C"))
            manager_item.setForeground(QColor("#2C2C2C"))
            estado_item.setForeground(QColor("#2C2C2C"))
            
            # Agregar items a la tabla
            self.inventory_table.setItem(row, 0, code_item)
            self.inventory_table.setItem(row, 1, name_item)
            self.inventory_table.setItem(row, 2, address_item)
            self.inventory_table.setItem(row, 3, start_date_item)
            self.inventory_table.setItem(row, 4, end_date_item)
            self.inventory_table.setItem(row, 5, manager_item)
            self.inventory_table.setItem(row, 6, estado_item)