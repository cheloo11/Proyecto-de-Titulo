from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout,  
    QWidget, QLabel, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QDialog, QMessageBox, QGroupBox,
    QAbstractItemView, QSpinBox, QDoubleSpinBox, QSizePolicy,
    QTextEdit, QDialogButtonBox, QFrame, QSpacerItem, QComboBox, QFormLayout
)
from PyQt6.QtGui import QColor, QFont, QIntValidator, QIcon
from PyQt6.QtCore import Qt
from ui.styles.common_styles import LABEL_STYLE, LABEL_INFO_STYLE, LABEL_BOLD_STYLE
from controllers.material_controller import MaterialController

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
        self.setWindowTitle("Ver Detalle de Material")
        self.setMinimumSize(500, 320)
        apply_dialog_style(self)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # --- Buscar Material ---
        search_group = QGroupBox("Buscar Material")
        search_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
        search_layout = QHBoxLayout(search_group)
        search_layout.setContentsMargins(10, 10, 10, 10)
        search_layout.setSpacing(10)
        
        code_label = QLabel("Código de Barras:")
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Ingrese código de barras")
        search_btn = QPushButton("Buscar")
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF6B35;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 18px;
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
        search_btn.clicked.connect(self.search_product)
        
        search_layout.addWidget(code_label)
        search_layout.addWidget(self.code_input, 1)
        search_layout.addWidget(search_btn)
        
        # --- Detalles del Material ---
        details_group = QGroupBox("Detalles del Material")
        details_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
        details_layout = QGridLayout(details_group)
        details_layout.setContentsMargins(10, 15, 10, 15)
        details_layout.setHorizontalSpacing(15)
        details_layout.setVerticalSpacing(10)
        
        # Primera columna
        details_layout.addWidget(QLabel("Código:"), 0, 0)
        self.product_code = QLabel("-")
        details_layout.addWidget(self.product_code, 0, 1)
        
        details_layout.addWidget(QLabel("Nombre:"), 1, 0)
        self.product_name = QLabel("-")
        details_layout.addWidget(self.product_name, 1, 1)
        
        details_layout.addWidget(QLabel("Descripción:"), 2, 0)
        self.product_description = QLabel("-")
        self.product_description.setWordWrap(True)
        details_layout.addWidget(self.product_description, 2, 1)
        
        # Segunda columna
        details_layout.addWidget(QLabel("Cantidad:"), 0, 2)
        self.product_stock = QLabel("-")
        details_layout.addWidget(self.product_stock, 0, 3)
        
        details_layout.addWidget(QLabel("Unidad:"), 1, 2)
        self.product_unit = QLabel("-")
        details_layout.addWidget(self.product_unit, 1, 3)
        
        details_layout.addWidget(QLabel("Stock Mínimo:"), 2, 2)
        self.product_min_stock = QLabel("-")
        details_layout.addWidget(self.product_min_stock, 2, 3)
        
        details_layout.addWidget(QLabel("Precio Unitario:"), 3, 2)
        self.product_price = QLabel("-")
        details_layout.addWidget(self.product_price, 3, 3)
        
        # Limpiar estilos de los labels de datos
        info_style = """
            QLabel { 
                color: #2C2C2C; 
                background-color: transparent;
                border: none;
                padding: 3px;
            }
        """
        self.product_code.setStyleSheet(info_style)
        self.product_name.setStyleSheet(info_style)
        self.product_description.setStyleSheet(info_style)
        self.product_stock.setStyleSheet(info_style)
        self.product_unit.setStyleSheet(info_style)
        self.product_min_stock.setStyleSheet(info_style)
        self.product_price.setStyleSheet(info_style)
        
        # Botón de cerrar
        self.close_button = QPushButton("Cerrar")
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #FF6B35;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 18px;
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
        self.close_button.clicked.connect(self.accept)
        
        # Agregar al layout principal
        layout.addWidget(search_group)
        layout.addWidget(details_group)
        layout.addWidget(self.close_button, 0, Qt.AlignmentFlag.AlignRight)
    
    def search_product(self):
        code = self.code_input.text()
        if not code:
            QMessageBox.warning(self, "Error", "Por favor ingrese un código de barras.")
            return
        material = MaterialController.get_material_by_code(code)
        if material:
            self.product_code.setText(material['codigo'])
            self.product_name.setText(material['nombre'])
            self.product_description.setText(material['descripcion'])
            self.product_stock.setText(f"{material['stock']} {material['unidad_medida']}")
            self.product_unit.setText(material['unidad_medida'])
            self.product_min_stock.setText(str(material['stock_min']))
            self.product_price.setText(f"${material['precio']}")
        else:
            QMessageBox.information(self, "Material no encontrado", 
                             f"No se encontró ningún material con el código {code}.")
            self.product_code.setText("-")
            self.product_name.setText("-")
            self.product_description.setText("-")
            self.product_stock.setText("-")
            self.product_unit.setText("-")
            self.product_min_stock.setText("-")
            self.product_price.setText("-")
            

# Modal para Agregar Material
class AddProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Nuevo Material")
        self.setMinimumSize(500, 400)
        apply_dialog_style(self) 
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Crear QGroupBox para el formulario
        form_group = QGroupBox("Información del Material")
        form_layout = QFormLayout(form_group)
        
        # Campos para agregar material según los requerimientos
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Ingrese el código de barras")
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre completo del material")
        
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Descripción detallada del material...")
        self.description_input.setMaximumHeight(100)
        
        self.stock_input = QDoubleSpinBox()
        self.stock_input.setRange(0, 10000)
        self.stock_input.setDecimals(2)
        self.stock_input.setSuffix("")
        
        self.min_stock_input = QDoubleSpinBox()
        self.min_stock_input.setRange(0, 10000)
        self.min_stock_input.setDecimals(2)
        self.min_stock_input.setSuffix("")
        
        self.unit_input = QLineEdit()
        self.unit_input.setPlaceholderText("Ej. Kg, Unidades, Metros, etc.")
        
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0, 100000)
        self.price_input.setPrefix("$")
        self.price_input.setDecimals(2)
        
        # Agregar campos al formulario
        form_layout.addRow("Código de Barras*:", self.code_input)
        form_layout.addRow("Nombre*:", self.name_input)
        form_layout.addRow("Descripción:", self.description_input)
        form_layout.addRow("Cantidad:", self.stock_input)
        form_layout.addRow("Unidad de Medida:", self.unit_input)
        form_layout.addRow("Precio Unitario*:", self.price_input)
        form_layout.addRow("Stock Mínimo:", self.min_stock_input)
        
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
        # Validar campos obligatorios
        if not self.code_input.text():
            QMessageBox.warning(self, "Error", "Por favor ingrese el código de barras del material.")
            return
            
        if not self.name_input.text():
            QMessageBox.warning(self, "Error", "Por favor ingrese el nombre del material.")
            return
        
        if self.price_input.value() <= 0:
            QMessageBox.warning(self, "Error", "El precio debe ser mayor que cero.")
            return
            
        # Recopilar datos del formulario
        codigo = self.code_input.text()
        nombre = self.name_input.text()
        descripcion = self.description_input.toPlainText()
        cantidad = self.stock_input.value()
        unidad_medida = self.unit_input.text()
        monto_unitario = self.price_input.value()
        stock_minimo = self.min_stock_input.value()
        
        # Agregar material usando el controlador 
        success, message = MaterialController.add_material(
            nombre, descripcion, codigo, cantidad, unidad_medida, monto_unitario, stock_minimo
        )
        
        if success:
            QMessageBox.information(self, "Éxito", message)
            # Actualizar la tabla en la ventana principal
            if hasattr(self.parent(), "load_materials"):
                self.parent().load_materials()
            self.accept()
        else:
            QMessageBox.warning(self, "Error", message)


# Modal para Editar Producto
class EditProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Material")
        self.setMinimumSize(500, 450)
        apply_dialog_style(self) 

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | 
            QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.button(QDialogButtonBox.StandardButton.Save).setText("Guardar Cambios")
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancelar")
        self.button_box.accepted.connect(self.accept_with_validation)
        self.button_box.rejected.connect(self.reject)
        
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Sección de búsqueda
        search_group = QGroupBox("Buscar Material a Editar")
        search_layout = QHBoxLayout(search_group)
        
        code_label = QLabel("Código de Barras:")
        self.search_code_input = QLineEdit()
        self.search_code_input.setPlaceholderText("Ingrese el código de barras del material a editar")
        
        search_btn = QPushButton("Buscar")
        search_btn.setText("Buscar")
        search_btn.clicked.connect(self.search_product)
        
        search_layout.addWidget(code_label)
        search_layout.addWidget(self.search_code_input, 1)
        search_layout.addWidget(search_btn)
        
        # Sección de edición
        edit_group = QGroupBox("Editar Datos")
        self.form_layout = QFormLayout(edit_group)
        
        # Campos para editar según la tabla de materiales
        self.code_display = QLabel("-")
        self.name_input = QLineEdit()
        self.description_input = QTextEdit()
        self.stock_input = QDoubleSpinBox()
        self.stock_input.setRange(0, 10000)
        self.stock_input.setDecimals(2)
        self.unit_input = QLineEdit()
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0, 100000)
        self.price_input.setDecimals(2)
        self.min_stock_input = QDoubleSpinBox()
        self.min_stock_input.setRange(0, 10000)
        self.min_stock_input.setDecimals(2)
        
        # Agregar campos al formulario
        self.form_layout.addRow("Código de Barras:", self.code_display)
        self.form_layout.addRow("Nombre:", self.name_input)
        self.form_layout.addRow("Descripción:", self.description_input)
        self.form_layout.addRow("Cantidad:", self.stock_input)
        self.form_layout.addRow("Unidad de Medida:", self.unit_input)
        self.form_layout.addRow("Precio Unitario:", self.price_input)
        self.form_layout.addRow("Stock Mínimo:", self.min_stock_input)
        
        # Agregar todo al layout principal
        layout.addWidget(search_group)
        layout.addWidget(edit_group)
        layout.addWidget(self.button_box)
        
        self.enable_form_fields(False)
        
    def enable_form_fields(self, enable=True):
        self.name_input.setEnabled(enable)
        self.description_input.setEnabled(enable)
        self.stock_input.setEnabled(enable)
        self.unit_input.setEnabled(enable)
        self.price_input.setEnabled(enable)
        self.min_stock_input.setEnabled(enable)
        self.button_box.button(QDialogButtonBox.StandardButton.Save).setEnabled(enable)
        
    def search_product(self):
        code = self.search_code_input.text()
        if not code:
            QMessageBox.warning(self, "Error", "Por favor ingrese un código de barras.")
            self.enable_form_fields(False)
            return
        
        material = MaterialController.get_material_by_code(code)
        if material:
            self.material_id = material["id"]
            self.code_display.setText(material["codigo"])
            self.name_input.setText(material["nombre"])
            self.description_input.setText(material["descripcion"])
            try:
                self.stock_input.setValue(float(material["stock"]))
            except Exception:
                self.stock_input.setValue(0)
            self.unit_input.setText(material["unidad_medida"])
            try:
                self.price_input.setValue(float(material["precio"]))
            except Exception:
                self.price_input.setValue(0)
            try:
                self.min_stock_input.setValue(float(material["stock_min"]))
            except Exception:
                self.min_stock_input.setValue(0)
            self.enable_form_fields(True)
        else:
            QMessageBox.information(self, "Material no encontrado", 
                             f"No se encontró ningún material con el código {code}.")
            self.code_display.setText("-")
            self.name_input.setText("")
            self.description_input.setText("")
            self.stock_input.setValue(0)
            self.unit_input.setText("")
            self.price_input.setValue(0)
            self.min_stock_input.setValue(0)
            self.enable_form_fields(False)
    
    def accept_with_validation(self):
        if not self.name_input.text():
            QMessageBox.warning(self, "Error", "Por favor ingrese el nombre del material.")
            return
        if self.price_input.value() <= 0:
            QMessageBox.warning(self, "Error", "El precio debe ser mayor que cero.")
            return
        
        nombre = self.name_input.text()
        descripcion = self.description_input.toPlainText()
        codigo_barra = self.code_display.text()
        cantidad = self.stock_input.value()
        unidad_medida = self.unit_input.text()
        monto_unitario = self.price_input.value()
        stock_minimo = self.min_stock_input.value()
        
        success, message = MaterialController.update_material(
            self.material_id, nombre, descripcion, codigo_barra, cantidad, unidad_medida, monto_unitario, stock_minimo
        )
        
        if success:
            QMessageBox.information(self, "Éxito", message)
            if hasattr(self.parent(), "load_materials"):
                self.parent().load_materials()
            self.accept()
        else:
            QMessageBox.warning(self, "Error", message)


# Modal para Eliminar Material
class DeleteProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Eliminar Material")
        self.setMinimumSize(450, 300)
        apply_dialog_style(self) 
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Sección de búsqueda
        search_group = QGroupBox("Buscar Material a Eliminar")
        search_layout = QHBoxLayout(search_group)
        
        code_label = QLabel("Código:")
        self.search_code_input = QLineEdit()
        self.search_code_input.setPlaceholderText("Ingrese el código del material a eliminar")
        
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
        search_btn.clicked.connect(self.search_product)
        
        search_layout.addWidget(code_label)
        search_layout.addWidget(self.search_code_input, 1)
        search_layout.addWidget(search_btn)
        
        # Información del producto
        info_group = QGroupBox("Información del Material")
        info_layout = QFormLayout(info_group)
        
        self.product_code = QLabel("-")
        self.product_name = QLabel("-")
        self.product_category = QLabel("-")
        self.product_stock = QLabel("-")
        
        # Estilo para las etiquetas 
        value_style = """
            QLabel {
                font-weight: bold; 
                color: #2C2C2C; 
                padding: 8px;
                background-color: transparent;
                border: none;
            }
        """
        self.product_code.setStyleSheet(value_style)
        self.product_name.setStyleSheet(value_style)
        self.product_category.setStyleSheet(value_style)
        self.product_stock.setStyleSheet(value_style)
        
        # Asegurarse de que el nombre pueda mostrarse en varias líneas
        self.product_name.setWordWrap(True)
        
        # Agregar campos al formulario de información
        info_layout.addRow("Código:", self.product_code)
        info_layout.addRow("Nombre:", self.product_name)
        info_layout.addRow("Categoría:", self.product_category)
        info_layout.addRow("Stock actual:", self.product_stock)
        
        # Advertencia
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
        
        # Botones de acción
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
        
        # Agregar todo al layout principal
        layout.addWidget(search_group)
        layout.addWidget(info_group)
        layout.addWidget(warning_label)
        layout.addWidget(self.button_box)
        
    def search_product(self):
        code = self.search_code_input.text()
        
        if not code:
            QMessageBox.warning(self, "Error", "Por favor ingrese un código de producto.")
            return
            
        # Buscar material usando el controlador
        material = MaterialController.get_material_by_code(code)
        
        if material:
            # Guardar el ID para la eliminación posterior
            self.material_id = material["id"]
            
            # Mostrar información del material
            self.product_code.setText(material["codigo"])
            self.product_name.setText(material["nombre"])

            self.product_category.setText("Material") 
            
            self.product_stock.setText(str(material["stock"]))
            
            # Habilitar el botón de eliminar
            self.button_box.button(QDialogButtonBox.StandardButton.Yes).setEnabled(True)
        else:
            QMessageBox.information(self, "Material no encontrado", 
                             f"No se encontró ningún material con el código {code}.")
            
            # Limpiar y deshabilitar
            self.product_code.setText("-")
            self.product_name.setText("-")
            self.product_category.setText("-")
            self.product_stock.setText("-")
            self.button_box.button(QDialogButtonBox.StandardButton.Yes).setEnabled(False)
    
    def confirm_delete(self):
        # Confirmación adicional
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirmar eliminación")
        msg_box.setText(f"¿Está seguro que desea eliminar permanentemente el producto {self.product_code.text()}?")
        msg_box.setInformativeText("Esta acción no se puede deshacer.")
        msg_box.setIcon(QMessageBox.Icon.Question)
        
        # Crear botones personalizados con estilos
        yes_button = msg_box.addButton("Sí, eliminar", QMessageBox.ButtonRole.YesRole)
        no_button = msg_box.addButton("Cancelar", QMessageBox.ButtonRole.NoRole)
        
        msg_box.setDefaultButton(no_button)
        msg_box.exec()
        
        if msg_box.clickedButton() == yes_button:
            # Eliminar material usando el controlador
            success, message = MaterialController.delete_material(self.material_id)
            
            if success:
                QMessageBox.information(self, "Éxito", message)
                # Actualizar la tabla en la ventana principal
                if hasattr(self.parent(), "load_materials"):
                    self.parent().load_materials()
                self.accept()
            else:
                QMessageBox.warning(self, "Error", message)


class InventoryView(QWidget):
    """Vista principal del inventario similar a la imagen"""
    def __init__(self):
        super().__init__()
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
        
        title = QLabel("Gestión de Inventario")
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
        
        # Botones CRUD 
        crud_layout = QHBoxLayout()
        crud_layout.setSpacing(15)
        
        # Espaciador para centrar botones
        crud_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        # Botón Agregar
        self.add_btn = QPushButton("Agregar Material")
        self.add_btn.setStyleSheet("QPushButton {background-color: #FF6B35; color: white; border: none; border-radius: 8px; padding: 12px 20px; font-size: 14px; font-weight: bold; min-width: 150px;} QPushButton:hover {background-color: #E55A2B;} QPushButton:pressed {background-color: #CC4A1F;}")
        self.add_btn.clicked.connect(self.open_add_dialog)

        # Botón Ver 
        self.view_btn = QPushButton("Ver Detalle")
        self.view_btn.setStyleSheet("QPushButton {background-color: #222; color: white; border: none; border-radius: 8px; padding: 12px 20px; font-size: 14px; font-weight: bold; min-width: 150px;} QPushButton:hover {background-color: #111;} QPushButton:pressed {background-color: #000;}")
        self.view_btn.clicked.connect(self.open_view_dialog)

        # Botón Editar
        self.edit_btn = QPushButton("Editar Material")
        self.edit_btn.setStyleSheet("QPushButton {background-color: #8B4513; color: white; border: none; border-radius: 8px; padding: 12px 20px; font-size: 14px; font-weight: bold; min-width: 150px;} QPushButton:hover {background-color: #7A3A0F;} QPushButton:pressed {background-color: #69300A;}")
        self.edit_btn.clicked.connect(self.open_edit_dialog)

        # Botón Eliminar 
        self.delete_btn = QPushButton("Eliminar Material")
        self.delete_btn.setStyleSheet("QPushButton {background-color: #888; color: white; border: none; border-radius: 8px; padding: 12px 20px; font-size: 14px; font-weight: bold; min-width: 150px;} QPushButton:hover {background-color: #aaa;} QPushButton:pressed {background-color: #666;}")
        self.delete_btn.clicked.connect(self.open_delete_dialog)

        # Agregar botones al layout CRUD
        crud_layout.addWidget(self.add_btn)
        crud_layout.addWidget(self.view_btn)
        crud_layout.addWidget(self.edit_btn)
        crud_layout.addWidget(self.delete_btn)
        # Espaciador para centrar botones
        crud_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        # Separador visual
        separator = QWidget()
        separator.setFixedHeight(1)
        separator.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        separator.setStyleSheet("background-color: #ddd;")
        
        # Área de filtros superior
        filter_layout = QHBoxLayout()
        
        # Combobox para categoría
        category_label = QLabel("Categoría:")
        category_label.setStyleSheet("""
            QLabel {
                color: #2C2C2C; 
                font-weight: bold;
                background-color: transparent;
                border: none;
            }
        """)
        # Combobox para categoría con estilo mejorado
        category_combo = QComboBox()
        category_combo.addItem("Todas las categorías")
        category_combo.addItem("Repuestos")
        category_combo.addItem("Accesorios")
        category_combo.addItem("Herramientas eléctricas")
        category_combo.addItem("Herramientas manuales")
        category_combo.setMinimumWidth(150)
        category_combo.setStyleSheet("""
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
        filter_combo.addItem("Todo el inventario")
        filter_combo.addItem("En stock solamente")
        filter_combo.addItem("Bajo stock")
        filter_combo.addItem("Sin stock")
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
        search_field.setPlaceholderText("Buscar material...")
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
        filter_layout.addWidget(category_label)
        filter_layout.addWidget(category_combo)
        filter_layout.addSpacing(20)
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(filter_combo)
        filter_layout.addStretch()
        filter_layout.addWidget(search_container)
        
        # Tabla de inventario
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(7) 
        self.inventory_table.setHorizontalHeaderLabels([
            "Código", "Nombre", "Descripción", "Cantidad", "Unidad", "Precio", "Stock Mín."
        ])
        
        # Configuración de la tabla
        self.inventory_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.inventory_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
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
        
        self.load_materials()
        
        # Agregar todos los elementos al layout principal
        main_layout.addLayout(crud_layout)
        main_layout.addWidget(separator)
        main_layout.addLayout(filter_layout)
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
            dialog.search_product()
        dialog.exec()
        
    def open_edit_dialog(self):
        dialog = EditProductDialog(self)
        # Si hay una fila seleccionada, obtener el código para buscarlo automáticamente
        selected_rows = self.inventory_table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            code = self.inventory_table.item(row, 0).text()
            dialog.search_code_input.setText(code)
            dialog.search_product()
        dialog.exec()
        
    def open_delete_dialog(self):
        dialog = DeleteProductDialog(self)
        # Si hay una fila seleccionada, obtener el código para buscarlo automáticamente
        selected_rows = self.inventory_table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            code = self.inventory_table.item(row, 0).text()
            dialog.search_code_input.setText(code)
            dialog.search_product()
        dialog.exec()
        
    def handle_double_click(self):
        """Al hacer doble clic en una fila, abre el diálogo de detalles"""
        self.open_view_dialog()
    
    def load_materials(self):
        """Carga los materiales desde la base de datos y los muestra en la tabla"""
        # Obtener materiales del controlador
        materials = MaterialController.get_all_materials()
        
        # Limpiar la tabla
        self.inventory_table.setRowCount(0)
        
        # Llenar la tabla con datos reales
        if materials:
            self.inventory_table.setRowCount(len(materials))
            for row, material in enumerate(materials):
                # Crear items con color de texto explícitamente definido
                code_item = QTableWidgetItem(material['codigo'])
                name_item = QTableWidgetItem(material['nombre'])
                desc_item = QTableWidgetItem(material['descripcion'][:30] + '...' if len(material['descripcion']) > 30 else material['descripcion'])
                stock_item = QTableWidgetItem(str(material['stock']))
                unit_item = QTableWidgetItem(material['unidad_medida'])
                price_item = QTableWidgetItem(str(material['precio']))
                min_stock_item = QTableWidgetItem(str(material['stock_min']))
                
                # Guardar el ID como dato de usuario para operaciones posteriores
                code_item.setData(Qt.ItemDataRole.UserRole, material['id'])
                
                code_item.setForeground(QColor("#2C2C2C"))
                name_item.setForeground(QColor("#2C2C2C"))
                desc_item.setForeground(QColor("#2C2C2C"))
                stock_item.setForeground(QColor("#2C2C2C"))
                unit_item.setForeground(QColor("#2C2C2C"))
                price_item.setForeground(QColor("#2C2C2C"))
                min_stock_item.setForeground(QColor("#2C2C2C"))
                
                # Agregar items a la tabla
                self.inventory_table.setItem(row, 0, code_item)
                self.inventory_table.setItem(row, 1, name_item)
                self.inventory_table.setItem(row, 2, desc_item)
                self.inventory_table.setItem(row, 3, stock_item)
                self.inventory_table.setItem(row, 4, unit_item)
                self.inventory_table.setItem(row, 5, price_item)
                self.inventory_table.setItem(row, 6, min_stock_item)