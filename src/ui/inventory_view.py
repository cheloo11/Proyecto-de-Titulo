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

# --- ESTILOS CENTRALIZADOS ---
# Definimos una función de estilo global para aplicarla a todos los diálogos
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
        
        /* --- ESTILOS DE BOTONES CENTRALIZADOS --- */

        /* * REGLA GENERAL PARA BOTONES DE DIÁLOGO:
         * Esta es la regla clave. Define el tamaño y la fuente
         * para CUALQUIER QPushButton DENTRO de un QDialogButtonBox.
         */
        QDialogButtonBox QPushButton {
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: bold;
            font-size: 14px;
            min-width: 100px; /* <- La propiedad clave */
        }

        /* * REGLAS ESPECÍFICAS (POR ID):
         * Ahora, los ID solo se usan para cambiar los COLORES.
         * El tamaño y la fuente ya están definidos arriba.
         */

        /* Botón Principal (Naranja) */
        QPushButton#BotonPrincipal {
            background-color: #FF6B35;
            color: white;
        }
        QPushButton#BotonPrincipal:hover {
            background-color: #E55A2B;
        }
        QPushButton#BotonPrincipal:pressed {
            background-color: #CC4A1F;
        }

        /* Botón Cancelar (Gris Oscuro) */
        QPushButton#BotonCancelar {
            background-color: #2C2C2C;
            color: white;
        }
        QPushButton#BotonCancelar:hover {
            background-color: #1a1a1a;
        }
        QPushButton#BotonCancelar:pressed {
            background-color: #0F0F0F;
        }

        /* Botón Advertencia (Marrón) */
        QPushButton#BotonAdvertencia {
            background-color: #8B4513;
            color: white;
        }
        QPushButton#BotonAdvertencia:hover {
            background-color: #704010;
        }
        QPushButton#BotonAdvertencia:pressed {
            background-color: #5C300A;
        }

        /* Botón Peligro (Rojo) */
        QPushButton#BotonPeligro {
            background-color: #D32F2F;
            color: white;
        }
        QPushButton#BotonPeligro:hover {
            background-color: #B71C1C;
        }
        QPushButton#BotonPeligro:pressed {
            background-color: #9A1919;
        }
    """)

# --- CLASE BASE PARA DIÁLOGOS DE BÚSQUEDA ---
# Esta clase maneja la lógica de búsqueda de producto que se repetía
class BaseSearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        apply_dialog_style(self)
        self.material = None
        self.material_id = None

    def _create_search_group(self, placeholder_text="Ingrese código de barras"):
        """Crea el QGroupBox de búsqueda estándar."""
        search_group = QGroupBox("Buscar Material")
        search_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
        search_layout = QHBoxLayout(search_group)
        search_layout.setContentsMargins(10, 10, 10, 10)
        search_layout.setSpacing(10)
        
        code_label = QLabel("Código de Barras:")
        self.search_code_input = QLineEdit()
        self.search_code_input.setPlaceholderText(placeholder_text)
        
        search_btn = QPushButton("Buscar")
        search_btn.setObjectName("BotonPrincipal") # Estilo centralizado
        search_btn.clicked.connect(self.search_product)
        
        search_layout.addWidget(code_label)
        search_layout.addWidget(self.search_code_input, 1)
        search_layout.addWidget(search_btn)
        return search_group

    def search_product(self):
        """Lógica de búsqueda centralizada."""
        code = self.search_code_input.text()
        if not code:
            QMessageBox.warning(self, "Error", "Por favor ingrese un código de barras.")
            self.material = None
            self._clear_fields()
            self._set_buttons_enabled(False)
            return

        self.material = MaterialController.get_material_by_code(code)
        
        if self.material:
            self.material_id = self.material.get("id") # Usar .get para seguridad
            self._fill_fields(self.material)
            self._set_buttons_enabled(True)
        else:
            QMessageBox.information(self, "Material no encontrado", f"No se encontró ningún material con el código {code}.")
            self.material = None
            self._clear_fields()
            self._set_buttons_enabled(False)

    # --- Métodos "Abstractos" (a implementar por clases hijas) ---
    
    def _fill_fields(self, material):
        """Rellena los campos del diálogo con la info del material."""
        raise NotImplementedError("La clase hija debe implementar _fill_fields")

    def _clear_fields(self):
        """Limpia los campos del diálogo."""
        raise NotImplementedError("La clase hija debe implementar _clear_fields")
        
    def _set_buttons_enabled(self, enabled):
        """Habilita o deshabilita botones (ej. Guardar) tras la búsqueda."""
        pass # Por defecto no hace nada


# --- DIÁLOGOS REFACTORIZADOS ---

# Modal para Ver Detalle (ahora hereda de BaseSearchDialog)
class ViewDetailDialog(BaseSearchDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ver Detalle de Material")
        self.setMinimumSize(500, 320)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # --- Buscar Material (de la clase base) ---
        search_group = self._create_search_group("Ingrese código de barras")
        # Renombramos el QLineEdit para coherencia interna
        self.code_input = self.search_code_input 
        
        # --- Detalles del Material ---
        details_group = QGroupBox("Detalles del Material")
        details_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
    
        details_layout = QGridLayout(details_group)
        details_layout.setContentsMargins(10, 15, 10, 15)
        details_layout.setHorizontalSpacing(15)
        details_layout.setVerticalSpacing(10)
        
        # Labels de info
        self.product_code = QLabel("-")
        self.product_name = QLabel("-")
        self.product_description = QLabel("-")
        self.product_description.setWordWrap(True)
        self.product_stock = QLabel("-")
        self.product_unit = QLabel("-")
        self.product_min_stock = QLabel("-")
        self.product_price = QLabel("-")
        self.product_estado = QLabel("-")
        
        # Primera columna
        details_layout.addWidget(QLabel("Código:"), 0, 0)
        details_layout.addWidget(self.product_code, 0, 1)
        details_layout.addWidget(QLabel("Nombre:"), 1, 0)
        details_layout.addWidget(self.product_name, 1, 1)
        details_layout.addWidget(QLabel("Descripción:"), 2, 0)
        details_layout.addWidget(self.product_description, 2, 1)
        
        # Segunda columna
        details_layout.addWidget(QLabel("Cantidad:"), 0, 2)
        details_layout.addWidget(self.product_stock, 0, 3)
        details_layout.addWidget(QLabel("Unidad:"), 1, 2)
        details_layout.addWidget(self.product_unit, 1, 3)
        details_layout.addWidget(QLabel("Stock Mínimo:"), 2, 2)
        details_layout.addWidget(self.product_min_stock, 2, 3)
        details_layout.addWidget(QLabel("Precio Unitario:"), 3, 2)
        details_layout.addWidget(self.product_price, 3, 3)
        details_layout.addWidget(QLabel("Estado:"), 3, 0)
        details_layout.addWidget(self.product_estado, 3, 1)
        
        # Botón de cerrar
        self.close_button = QPushButton("Cerrar")
        self.close_button.setObjectName("BotonPrincipal") # Estilo centralizado
        self.close_button.clicked.connect(self.accept)
        
        # Agregar al layout principal
        layout.addWidget(search_group)
        layout.addWidget(details_group)
        layout.addWidget(self.close_button, 0, Qt.AlignmentFlag.AlignRight)
    
    # --- Implementación de métodos abstractos ---
    
    def _fill_fields(self, material):
        self.product_code.setText(material['codigo_barra'])
        self.product_name.setText(material['nombre'])
        self.product_description.setText(material['descripcion'])
        self.product_stock.setText(f"{material['cantidad']} {material['unidad_medida']}")
        self.product_unit.setText(material['unidad_medida'])
        self.product_min_stock.setText(str(material['stock_minimo']))
        self.product_price.setText(f"${material['monto_unitario']}")
        self.product_estado.setText(material['estado'])
        
    def _clear_fields(self):
        self.product_code.setText("-")
        self.product_name.setText("-")
        self.product_description.setText("-")
        self.product_stock.setText("-")
        self.product_unit.setText("-")
        self.product_min_stock.setText("-")
        self.product_price.setText("-")
        self.product_estado.setText("-")

# Modal para Agregar Material (No necesita búsqueda, solo estilos)
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
        
        # Campos para agregar material
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
        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["activo", "inactivo"])
        self.estado_combo.setCurrentText("activo")
        
        # Agregar campos al formulario
        form_layout.addRow("Código de Barras*:", self.code_input)
        form_layout.addRow("Nombre*:", self.name_input)
        form_layout.addRow("Descripción:", self.description_input)
        form_layout.addRow("Cantidad*:", self.stock_input)
        form_layout.addRow("Unidad de Medida:", self.unit_input)
        form_layout.addRow("Precio Unitario*:", self.price_input)
        form_layout.addRow("Stock Mínimo*:", self.min_stock_input)
        form_layout.addRow("Estado:", self.estado_combo)  # <-- Nuevo campo
        
        # Nota sobre campos obligatorios
        note_label = QLabel("* Campos obligatorios")
        note_label.setStyleSheet("color: #FF6B35; font-style: italic; background-color: transparent; border: none;")
        
        # Botones de acción
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | 
            QDialogButtonBox.StandardButton.Cancel
        )
        # Aplicar estilos centralizados
        button_box.button(QDialogButtonBox.StandardButton.Save).setText("Guardar")
        button_box.button(QDialogButtonBox.StandardButton.Save).setObjectName("BotonPrincipal")
        button_box.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancelar")
        button_box.button(QDialogButtonBox.StandardButton.Cancel).setObjectName("BotonCancelar")
        
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
        if self.stock_input.value() <= 0:
            QMessageBox.warning(self, "Error", "La cantidad debe ser mayor que cero.")
            return
        if self.price_input.value() <= 0:
            QMessageBox.warning(self, "Error", "El precio debe ser mayor que cero.")
            return
        if self.min_stock_input.value() <= 0:
            QMessageBox.warning(self, "Error", "El stock mínimo debe ser mayor que cero.")
            return
            
        # Recopilar datos del formulario
        codigo_barra = self.code_input.text()
        nombre = self.name_input.text()
        descripcion = self.description_input.toPlainText()
        cantidad = self.stock_input.value()
        unidad_medida = self.unit_input.text()
        monto_unitario = self.price_input.value()
        stock_minimo = self.min_stock_input.value()
        estado = self.estado_combo.currentText()  # <-- Nuevo campo
        
        # Agregar material usando el controlador 
        success, message = MaterialController.add_material(
            nombre, descripcion, codigo_barra, cantidad, unidad_medida, monto_unitario, stock_minimo, estado
        )
        
        if success:
            QMessageBox.information(self, "Éxito", message)
            # Actualizar la tabla en la ventana principal
            if hasattr(self.parent(), "load_materials"):
                self.parent().load_materials()
            self.accept()
        else:
            QMessageBox.warning(self, "Error", message)

# Modal para Editar Producto (ahora hereda de BaseSearchDialog)
class EditProductDialog(BaseSearchDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Material")
        self.setMinimumSize(500, 450)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save |
            QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.button(QDialogButtonBox.StandardButton.Save).setText("Guardar Cambios")
        self.button_box.button(QDialogButtonBox.StandardButton.Save).setObjectName("BotonPrincipal")
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancelar")
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setObjectName("BotonCancelar")
        
        self.button_box.accepted.connect(self.accept_with_validation)
        self.button_box.rejected.connect(self.reject)
        
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Sección de búsqueda (de la clase base)
        search_group = self._create_search_group("Ingrese el código de barras del material a editar")
        
        # Sección de edición
        edit_group = QGroupBox("Editar Datos")
        self.form_layout = QFormLayout(edit_group)
        
        # Campos para editar
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
        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["activo", "inactivo"])
        
        # Agregar campos al formulario
        self.form_layout.addRow("Código de Barras:", self.code_display)
        self.form_layout.addRow("Nombre:", self.name_input)
        self.form_layout.addRow("Descripción:", self.description_input)
        self.form_layout.addRow("Cantidad:", self.stock_input)
        self.form_layout.addRow("Unidad de Medida:", self.unit_input)
        self.form_layout.addRow("Precio Unitario:", self.price_input)
        self.form_layout.addRow("Stock Mínimo:", self.min_stock_input)
        self.form_layout.addRow("Estado:", self.estado_combo)
        
        # Agregar todo al layout principal
        layout.addWidget(search_group)
        layout.addWidget(edit_group)
        layout.addWidget(self.button_box)
        
        self._set_buttons_enabled(False) # Deshabilitar formulario al inicio
        
    # --- Implementación de métodos abstractos ---
    
    def _fill_fields(self, material):
        self.material_id = material["id"]
        self.code_display.setText(material["codigo_barra"])
        self.name_input.setText(material["nombre"])
        self.description_input.setText(material["descripcion"])
        try:
            self.stock_input.setValue(float(material["cantidad"]))
        except Exception:
            self.stock_input.setValue(0)
        self.unit_input.setText(material["unidad_medida"])
        try:
            self.price_input.setValue(float(material["monto_unitario"]))
        except Exception:
            self.price_input.setValue(0)
        try:
            self.min_stock_input.setValue(float(material["stock_minimo"]))
        except Exception:
            self.min_stock_input.setValue(0)
        # Permitir seleccionar cualquier estado, incluso cambiar de inactivo a activo
        self.estado_combo.setCurrentText(material.get("estado", "activo"))

    def _clear_fields(self):
        self.code_display.setText("-")
        self.name_input.setText("")
        self.description_input.setText("")
        self.stock_input.setValue(0)
        self.unit_input.setText("")
        self.price_input.setValue(0)
        self.min_stock_input.setValue(0)
        self.estado_combo.setCurrentText("activo")
        
    def _set_buttons_enabled(self, enable=True):
        """Habilita/deshabilita los campos del formulario y el botón Guardar."""
        self.name_input.setEnabled(enable)
        self.description_input.setEnabled(enable)
        self.stock_input.setEnabled(enable)
        self.unit_input.setEnabled(enable)
        self.price_input.setEnabled(enable)
        self.min_stock_input.setEnabled(enable)
        self.estado_combo.setEnabled(enable)
        self.button_box.button(QDialogButtonBox.StandardButton.Save).setEnabled(enable)
    
    # --- Lógica de guardado ---
    
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
        estado = self.estado_combo.currentText()  # <-- Esto permite cambiar el estado

        # Asegúrate que el método update_material en el controlador y modelo acepte el campo estado
        success, message = MaterialController.update_material(
            self.material_id, nombre, descripcion, codigo_barra, cantidad, unidad_medida, monto_unitario, stock_minimo, estado
        )
        
        if success:
            QMessageBox.information(self, "Éxito", message)
            if hasattr(self.parent(), "load_materials"):
                self.parent().load_materials()
            self.accept()
        else:
            QMessageBox.warning(self, "Error", message)

# --- DIÁLOGO UNIFICADO PARA DESACTIVAR/ELIMINAR ---
# Reemplaza a DeactivateProductDialog y RemoveProductDialog
class ConfirmActionDialog(BaseSearchDialog):
    def __init__(self, mode, parent=None):
        super().__init__(parent)
        
        # 'mode' puede ser 'deactivate' o 'remove'
        self.mode = mode
        self.setMinimumSize(450, 300)
        self.init_ui()

        # Configurar el diálogo según el modo
        if self.mode == 'deactivate':
            self.setWindowTitle("Desactivar Material")
            self.warning_label.setText("⚠️ ADVERTENCIA: Esta acción desactivará el material, pero no lo eliminará de la base de datos.")
            self.yes_button.setText("Desactivar")
            self.yes_button.setObjectName("BotonAdvertencia") # Estilo marrón
        
        elif self.mode == 'remove':
            self.setWindowTitle("Eliminar Material")
            self.warning_label.setText("⚠️ ADVERTENCIA: Esta acción eliminará el material permanentemente.")
            self.yes_button.setText("Eliminar")
            self.yes_button.setObjectName("BotonPeligro") # Estilo rojo

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Grupo de búsqueda (de la clase base)
        search_group = self._create_search_group("Ingrese el código del material")
        
        # Grupo de información
        info_group = QGroupBox("Información del Material")
        info_layout = QFormLayout(info_group)
        self.product_code = QLabel("-")
        self.product_name = QLabel("-")
        self.product_category = QLabel("-")
        self.product_stock = QLabel("-")
        
        value_style = "QLabel { font-weight: bold; color: #2C2C2C; padding: 8px; background-color: transparent; border: none; }"
        self.product_code.setStyleSheet(value_style)
        self.product_name.setStyleSheet(value_style)
        self.product_category.setStyleSheet(value_style)
        self.product_stock.setStyleSheet(value_style)
        self.product_name.setWordWrap(True)
        
        info_layout.addRow("Código:", self.product_code)
        info_layout.addRow("Nombre:", self.product_name)
        info_layout.addRow("Categoría:", self.product_category)
        info_layout.addRow("Stock actual:", self.product_stock)
        
        # Etiqueta de advertencia (el texto se define en __init__)
        self.warning_label = QLabel("...")
        self.warning_label.setStyleSheet("""
            QLabel { color: #8B4513; font-weight: bold; margin-top: 10px;
                     background-color: transparent; border: none; }
        """)
        self.warning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Botones
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Yes |
                                           QDialogButtonBox.StandardButton.Cancel)
        self.yes_button = self.button_box.button(QDialogButtonBox.StandardButton.Yes)
        
        cancel_button = self.button_box.button(QDialogButtonBox.StandardButton.Cancel)
        cancel_button.setText("Cancelar")
        cancel_button.setObjectName("BotonCancelar")
        
        self.yes_button.setEnabled(False) # Deshabilitado hasta buscar
        
        self.button_box.accepted.connect(self.confirm_action)
        self.button_box.rejected.connect(self.reject)
        
        layout.addWidget(search_group)
        layout.addWidget(info_group)
        layout.addWidget(self.warning_label)
        layout.addWidget(self.button_box)

    # --- Implementación de métodos abstractos ---

    def _fill_fields(self, material):
        self.material_id = material["id"]
        self.product_code.setText(material["codigo_barra"])
        self.product_name.setText(material["nombre"])
        self.product_category.setText("Material") # Asumiendo "Material"
        self.product_stock.setText(str(material["cantidad"]))
        
    def _clear_fields(self):
        self.product_code.setText("-")
        self.product_name.setText("-")
        self.product_category.setText("-")
        self.product_stock.setText("-")
        
    def _set_buttons_enabled(self, enabled):
        self.yes_button.setEnabled(enabled)

    # --- Lógica de confirmación unificada ---

    def confirm_action(self):
        # Configurar textos de confirmación según el modo
        if self.mode == 'deactivate':
            title = "Confirmar desactivación"
            text = f"¿Está seguro que desea desactivar el material {self.product_code.text()}?"
            info_text = "El material permanecerá en la base de datos como inactivo."
            yes_text = "Sí, desactivar"
        else: # 'remove'
            title = "Confirmar eliminación"
            text = f"¿Está seguro que desea eliminar permanentemente el material {self.product_code.text()}?"
            info_text = "Esta acción no se puede deshacer."
            yes_text = "Sí, eliminar"

        # Mostrar QMessageBox de confirmación
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setInformativeText(info_text)
        msg_box.setIcon(QMessageBox.Icon.Question)
        yes_button = msg_box.addButton(yes_text, QMessageBox.ButtonRole.YesRole)
        no_button = msg_box.addButton("Cancelar", QMessageBox.ButtonRole.NoRole)
        msg_box.setDefaultButton(no_button)
        msg_box.exec()
        
        if msg_box.clickedButton() == yes_button:
            # Ejecutar la acción del controlador según el modo
            if self.mode == 'deactivate':
                success, message = MaterialController.deactivate_material(self.material_id)
            else:
                success, message = MaterialController.delete_material(self.material_id)
            
            # Mostrar resultado
            if success:
                QMessageBox.information(self, "Éxito", message)
                if hasattr(self.parent(), "load_materials"):
                    self.parent().load_materials()
                self.accept()
            else:
                QMessageBox.warning(self, "Error", message)

# --- VISTA PRINCIPAL DEL INVENTARIO (Refactorizada) ---

class InventoryView(QWidget):
    """Vista principal del inventario similar a la imagen"""
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # Header (Sin cambios)
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
        
        # Botones CRUD (Sin cambios de estilo, ya que no están en un QDialog)
        crud_layout = QHBoxLayout()
        crud_layout.setSpacing(15)
        crud_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        self.add_btn = QPushButton("Agregar Material")
        self.add_btn.setStyleSheet("QPushButton {background-color: #FF6B35; color: white; border: none; border-radius: 8px; padding: 12px 20px; font-size: 14px; font-weight: bold; min-width: 150px;} QPushButton:hover {background-color: #E55A2B;} QPushButton:pressed {background-color: #CC4A1F;}")
        self.add_btn.clicked.connect(self.open_add_dialog)

        self.view_btn = QPushButton("Ver Detalle")
        self.view_btn.setStyleSheet("QPushButton {background-color: #222; color: white; border: none; border-radius: 8px; padding: 12px 20px; font-size: 14px; font-weight: bold; min-width: 150px;} QPushButton:hover {background-color: #111;} QPushButton:pressed {background-color: #000;}")
        self.view_btn.clicked.connect(self.open_view_dialog)

        self.edit_btn = QPushButton("Editar Material")
        self.edit_btn.setStyleSheet("QPushButton {background-color: #8B4513; color: white; border: none; border-radius: 8px; padding: 12px 20px; font-size: 14px; font-weight: bold; min-width: 150px;} QPushButton:hover {background-color: #7A3A0F;} QPushButton:pressed {background-color: #69300A;}")
        self.edit_btn.clicked.connect(self.open_edit_dialog)

        self.delete_btn = QPushButton("Desactivar Material")
        self.delete_btn.setStyleSheet("QPushButton {background-color: #888; color: white; border: none; border-radius: 8px; padding: 12px 20px; font-size: 14px; font-weight: bold; min-width: 150px;} QPushButton:hover {background-color: #aaa;} QPushButton:pressed {background-color: #666;}")
        self.delete_btn.clicked.connect(self.open_delete_dialog) # <-- MÉTODO REFACTORIZADO

        self.remove_btn = QPushButton("🗑️")
        self.remove_btn.setToolTip("Eliminar Material")
        self.remove_btn.setFixedSize(40, 40)
        self.remove_btn.setStyleSheet("QPushButton {background-color: #D32F2F; color: white; border: none; border-radius: 8px; font-size: 13px; font-weight: bold;} QPushButton:hover {background-color: #B71C1C;}")
        self.remove_btn.clicked.connect(self.open_remove_dialog) # <-- MÉTODO REFACTORIZADO

        crud_layout.addWidget(self.add_btn)
        crud_layout.addWidget(self.view_btn)
        crud_layout.addWidget(self.edit_btn)
        crud_layout.addWidget(self.delete_btn)
        crud_layout.addWidget(self.remove_btn)
        crud_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        # Separador (Sin cambios)
        separator = QWidget()
        separator.setFixedHeight(1)
        separator.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        separator.setStyleSheet("background-color: #ddd;")
        
        # Área de filtros (Sin cambios)
        filter_layout = QHBoxLayout()
        category_label = QLabel("Categoría:")
        category_label.setStyleSheet("color: #2C2C2C; font-weight: bold; background-color: transparent; border: none;")
        category_combo = QComboBox()
        category_combo.addItem("Todas las categorías")
        category_combo.addItem("Repuestos")
        # ... (más categorías)
        category_combo.setMinimumWidth(150)
        category_combo.setStyleSheet("""
            QComboBox { border: 2px solid #ddd; border-radius: 6px; padding: 8px; background-color: white; color: #2C2C2C; min-height: 20px; }
            QComboBox:focus { border-color: #FF6B35; }
            QComboBox::drop-down { border: none; width: 20px; }
            QComboBox QAbstractItemView { color: #2C2C2C; background-color: white; selection-background-color: #FF6B35; selection-color: white; }
        """)

        filter_label = QLabel("Filtro:")
        filter_label.setStyleSheet("color: #2C2C2C; font-weight: bold; background-color: transparent; border: none;")
        filter_combo = QComboBox()
        filter_combo.addItem("Todo el inventario")
        filter_combo.addItem("En stock solamente")
        filter_combo.addItem("Bajo stock")
        filter_combo.addItem("Sin stock")
        filter_combo.setMinimumWidth(150)
        filter_combo.setStyleSheet("""
            QComboBox { border: 2px solid #ddd; border-radius: 6px; padding: 8px; background-color: white; color: #2C2C2C; min-height: 20px; }
            QComboBox:focus { border-color: #FF6B35; }
            QComboBox::drop-down { border: none; width: 20px; }
            QComboBox QAbstractItemView { color: #2C2C2C; background-color: white; selection-background-color: #FF6B35; selection-color: white; }
        """)

        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(5)
        
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Buscar material...")
        self.search_field.setMinimumWidth(250)
        self.search_field.setStyleSheet("""
            QLineEdit { border: 2px solid #ddd; border-radius: 6px; padding: 8px; color: #2C2C2C; background-color: white; }
            QLineEdit:focus { border-color: #FF6B35; }
        """)
        self.search_field.returnPressed.connect(self.search_materials)  # <-- Para buscar con Enter
        self.search_field.textChanged.connect(self.on_search_text_changed)

        self.search_btn = QPushButton("Buscar")
        self.search_btn.setStyleSheet("""
            QPushButton { background-color: #FF6B35; color: white; border: none; border-radius: 6px; padding: 10px 20px; font-weight: bold; font-size: 14px; }
            QPushButton:hover { background-color: #E55A2B; }
            QPushButton:pressed { background-color: #CC4A1F; }
        """)
        self.search_btn.clicked.connect(self.search_materials)  # <-- Para buscar con click
        
        search_layout.addWidget(self.search_field)
        search_layout.addWidget(self.search_btn)
        
        filter_layout.addWidget(category_label)
        filter_layout.addWidget(category_combo)
        filter_layout.addSpacing(20)
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(filter_combo)
        filter_layout.addStretch()
        filter_layout.addWidget(search_container)
        
        # Tabla de inventario (Sin cambios)
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(8) 
        self.inventory_table.setHorizontalHeaderLabels([
            "Código", "Nombre", "Descripción", "Cantidad", "Unidad", "Precio", "Stock Mín.", "Estado"
        ])
        self.inventory_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.inventory_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.inventory_table.verticalHeader().setVisible(False)
        self.inventory_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.inventory_table.setStyleSheet("""
            QTableWidget { background-color: white; border: 2px solid #ddd; border-radius: 6px; gridline-color: #eee; }
            QTableWidget::item { padding: 8px; color: #2C2C2C; border: none; }
            QTableWidget::item:selected { background-color: #FF6B35; color: white; }
            QHeaderView::section { background-color: #f8f9fa; color: #2C2C2C; padding: 8px; border: 1px solid #ddd; font-weight: bold; }
        """)
        
        self.load_materials()
        
        # Agregar todos los elementos al layout principal
        main_layout.addLayout(crud_layout)
        main_layout.addWidget(separator)
        main_layout.addLayout(filter_layout)
        main_layout.addWidget(self.inventory_table)
        
        self.setLayout(main_layout)
    
 
    # --- Métodos para abrir los modales (Refactorizados) ---
    
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
            dialog.code_input.setText(code) # code_input es el search_code_input
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
        """Método simplificado para abrir el diálogo de desactivación."""
        dialog = ConfirmActionDialog(mode='deactivate', parent=self)
        
        # Si hay una fila seleccionada, obtener el código para buscarlo automáticamente
        selected_rows = self.inventory_table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            code = self.inventory_table.item(row, 0).text()
            dialog.search_code_input.setText(code)
            dialog.search_product()
        dialog.exec()
         
    def open_remove_dialog(self):
        """Método simplificado para abrir el diálogo de eliminación."""
        dialog = ConfirmActionDialog(mode='remove', parent=self)
        
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
                code_item = QTableWidgetItem(material['codigo_barra'])
                name_item = QTableWidgetItem(material['nombre'])
                desc_item = QTableWidgetItem(material['descripcion'][:30] + '...' if len(material['descripcion']) > 30 else material['descripcion'])
                stock_item = QTableWidgetItem(str(material['cantidad']))
                unit_item = QTableWidgetItem(material['unidad_medida'])
                price_item = QTableWidgetItem(str(material['monto_unitario']))
                min_stock_item = QTableWidgetItem(str(material['stock_minimo']))
                estado_item = QTableWidgetItem(material['estado'])
                
                # Guardar el ID como dato de usuario para operaciones posteriores
                code_item.setData(Qt.ItemDataRole.UserRole, material['id'])
                
                # (Opcional) Definir color de texto si el estilo de la tabla no lo toma
                text_color = QColor("#2C2C2C")
                code_item.setForeground(text_color)
                name_item.setForeground(text_color)
                desc_item.setForeground(text_color)
                stock_item.setForeground(text_color)
                unit_item.setForeground(text_color)
                price_item.setForeground(text_color)
                min_stock_item.setForeground(text_color)
                estado_item.setForeground(text_color)
                
                # Agregar items a la tabla
                self.inventory_table.setItem(row, 0, code_item)
                self.inventory_table.setItem(row, 1, name_item)
                self.inventory_table.setItem(row, 2, desc_item)
                self.inventory_table.setItem(row, 3, stock_item)
                self.inventory_table.setItem(row, 4, unit_item)
                self.inventory_table.setItem(row, 5, price_item)
                self.inventory_table.setItem(row, 6, min_stock_item)
                self.inventory_table.setItem(row, 7, estado_item)
    
    def search_materials(self):
        search_text = self.search_field.text().strip()
        if not search_text:
            self.load_materials()  # <-- Esto ya recarga la tabla completa
            return
        materials = MaterialController.search_materials(search_text)
        self.display_materials(materials)

    def display_materials(self, materials):
        self.inventory_table.setRowCount(0)
        if materials:
            self.inventory_table.setRowCount(len(materials))
            for row, material in enumerate(materials):
                code_item = QTableWidgetItem(material['codigo_barra'])
                name_item = QTableWidgetItem(material['nombre'])
                desc_item = QTableWidgetItem(material['descripcion'][:30] + '...' if len(material['descripcion']) > 30 else material['descripcion'])
                stock_item = QTableWidgetItem(str(material['cantidad']))
                unit_item = QTableWidgetItem(material['unidad_medida'])
                price_item = QTableWidgetItem(str(material['monto_unitario']))
                min_stock_item = QTableWidgetItem(str(material['stock_minimo']))
                estado_item = QTableWidgetItem(material['estado'])
                code_item.setData(Qt.ItemDataRole.UserRole, material['id'])
                text_color = QColor("#2C2C2C")
                code_item.setForeground(text_color)
                name_item.setForeground(text_color)
                desc_item.setForeground(text_color)
                stock_item.setForeground(text_color)
                unit_item.setForeground(text_color)
                price_item.setForeground(text_color)
                min_stock_item.setForeground(text_color)
                estado_item.setForeground(text_color)
                self.inventory_table.setItem(row, 0, code_item)
                self.inventory_table.setItem(row, 1, name_item)
                self.inventory_table.setItem(row, 2, desc_item)
                self.inventory_table.setItem(row, 3, stock_item)
                self.inventory_table.setItem(row, 4, unit_item)
                self.inventory_table.setItem(row, 5, price_item)
                self.inventory_table.setItem(row, 6, min_stock_item)
                self.inventory_table.setItem(row, 7, estado_item)
    
    def on_search_text_changed(self, text):
        if not text.strip():
            self.load_materials()