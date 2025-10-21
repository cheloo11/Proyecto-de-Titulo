from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QTableWidget, QTableWidgetItem, QHeaderView,
                            QAbstractItemView, QLineEdit, QComboBox, QSizePolicy,
                            QDialog, QFormLayout, QMessageBox,
                            QDialogButtonBox, QGroupBox, QFrame, QSpacerItem)
from PyQt6.QtGui import QColor, QIntValidator
from PyQt6.QtCore import Qt
from ui.styles.common_styles import LABEL_STYLE, LABEL_INFO_STYLE, LABEL_BOLD_STYLE

from controllers.contratista_controller import ContratistaController

# Función global con estilos
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
        QLineEdit, QComboBox {
            color: #2C2C2C;
            background-color: white;
            border: 2px solid #ddd;
            border-radius: 6px;
            padding: 8px;
        }
        QLineEdit:focus, QComboBox:focus {
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
    """)

# Modal para Ver Detalle (permite buscar por código)
class ViewDetailDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ver Detalle de Contratista")
        self.setMinimumSize(500, 350)
        apply_dialog_style(self)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Sección de búsqueda por código
        search_group = QGroupBox("Buscar Contratista")
        search_layout = QHBoxLayout(search_group)
        
        code_label = QLabel("Código:")
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Ingrese el código del contratista")
        
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
        search_btn.clicked.connect(self.search_contractor)
        
        search_layout.addWidget(code_label)
        search_layout.addWidget(self.code_input, 1)
        search_layout.addWidget(search_btn)
        
        # Sección de detalles del contratista
        details_group = QGroupBox("Detalles del Contratista")
        details_layout = QFormLayout(details_group)
        
        self.contractor_code = QLabel("-")
        self.contractor_name = QLabel("-")
        self.contractor_company = QLabel("-")
        self.contractor_phone = QLabel("-")
        self.contractor_status = QLabel("-")
        
        value_style = """
            QLabel {
                font-weight: bold; 
                color: #2C2C2C; 
                padding: 8px;
                background-color: transparent;
                border: none;
            }
        """
        self.contractor_code.setStyleSheet(value_style)
        self.contractor_name.setStyleSheet(value_style)
        self.contractor_company.setStyleSheet(value_style)
        self.contractor_phone.setStyleSheet(value_style)
        self.contractor_status.setStyleSheet(value_style)
        
        details_layout.addRow(QLabel("Código:"), self.contractor_code)
        details_layout.addRow(QLabel("Nombre:"), self.contractor_name)
        details_layout.addRow(QLabel("Empresa:"), self.contractor_company)
        details_layout.addRow(QLabel("Teléfono:"), self.contractor_phone)
        details_layout.addRow(QLabel("Estado:"), self.contractor_status)
        
        # Botón cerrar
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
        
        layout.addWidget(search_group)
        layout.addWidget(details_group)
        layout.addWidget(button_box)
        self.setLayout(layout)
    
    def search_contractor(self):
        code = self.code_input.text()
        if not code:
            QMessageBox.warning(self, "Error", "Por favor ingrese un código de contratista.")
            return
        contratista = ContratistaController.get_by_code(code)
        if contratista:
            self.contractor_code.setText(contratista["codigo"])
            self.contractor_name.setText(contratista["nombre"])
            self.contractor_company.setText(contratista["empresa"])
            self.contractor_phone.setText(contratista["telefono"])
            self.contractor_status.setText(contratista["estado"])
        else:
            QMessageBox.information(self, "Contratista no encontrado", 
                                 f"No se encontró ningún contratista con el código {code}.")
            self.contractor_code.setText("-")
            self.contractor_name.setText("-")
            self.contractor_company.setText("-")
            self.contractor_phone.setText("-")
            self.contractor_status.setText("-")


# Modal para Agregar Contratista
class AddProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Nuevo Contratista")
        self.setMinimumSize(500, 400)
        apply_dialog_style(self) 
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        # Crear QGroupBox para el formulario de contratista
        form_group = QGroupBox("Información del Contratista")
        form_layout = QFormLayout(form_group)
        # Campos para agregar contratista
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Ej. CT001")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre completo del contratista")
        self.company_input = QLineEdit()
        self.company_input.setPlaceholderText("Empresa del contratista")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Teléfono de contacto")
        self.phone_input.setValidator(QIntValidator())
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Activo", "Inactivo"])
        # Agregar campos al formulario
        form_layout.addRow("Código*:", self.code_input)
        form_layout.addRow("Nombre*:", self.name_input)
        form_layout.addRow("Empresa:", self.company_input)
        form_layout.addRow("Teléfono:", self.phone_input)
        form_layout.addRow("Estado:", self.status_combo)
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
            QMessageBox.warning(self, "Error", "Por favor ingrese el código del contratista.")
            return
            
        if not self.name_input.text():
            QMessageBox.warning(self, "Error", "Por favor ingrese el nombre del contratista.")
            return
        
        codigo = self.code_input.text()
        nombre = self.name_input.text()
        empresa = self.company_input.text()
        telefono = self.phone_input.text()
        estado = self.status_combo.currentText()
        success = ContratistaController.add(codigo, nombre, empresa, telefono, estado)
        if success:
            QMessageBox.information(self, "Éxito", "Contratista agregado correctamente.")
            if hasattr(self.parent(), "load_contratistas"):
                self.parent().load_contratistas()
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "No se pudo agregar el contratista.")


# Modal para Editar Producto
class EditProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Contratista")
        self.setMinimumSize(500, 450)
        apply_dialog_style(self) 
        self.contratista_id = None  # Id inicializado aquí
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
        layout = QVBoxLayout(self)
        search_group = QGroupBox("Buscar Contratista a Editar")
        search_layout = QHBoxLayout(search_group)
        search_layout.setContentsMargins(12, 8, 12, 8)
        search_layout.setSpacing(10)
        search_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        code_label = QLabel("Código:")
        self.search_code_input = QLineEdit()
        self.search_code_input.setPlaceholderText("Ingrese el código del contratista a editar")
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
        search_btn.clicked.connect(self.search_product)
        search_layout.addWidget(code_label)
        search_layout.addWidget(self.search_code_input, 1)
        search_layout.addWidget(search_btn)
        edit_group = QGroupBox("Editar Datos del Contratista")
        self.form_layout = QFormLayout(edit_group)
        self.code_display = QLabel("-")
        self.code_display.setStyleSheet("QLabel {font-weight: bold; color: #2C2C2C; background-color: transparent; border: none; min-height: 10px; padding: 2px 8px 2px 8px;}")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre completo del contratista")
        self.company_input = QLineEdit()
        self.company_input.setPlaceholderText("Empresa del contratista")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Teléfono de contacto")
        self.phone_input.setValidator(QIntValidator())
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Activo", "Inactivo"])
        self.status_combo.setMinimumWidth(120)
        self.status_combo.setStyleSheet("QComboBox {border: 2px solid #ddd; border-radius: 6px; padding: 8px; background-color: white; color: #2C2C2C; min-height: 20px;} QComboBox:focus {border-color: #FF6B35;} QComboBox::drop-down {border: none; width: 20px;} QComboBox QAbstractItemView {color: #2C2C2C; background-color: white; selection-background-color: #FF6B35; selection-color: white;}")
        self.form_layout.addRow("Código:", self.code_display)
        self.form_layout.addRow("Nombre*:", self.name_input)
        self.form_layout.addRow("Empresa:", self.company_input)
        self.form_layout.addRow("Teléfono:", self.phone_input)
        self.form_layout.addRow("Estado:", self.status_combo)
        self.button_box.button(QDialogButtonBox.StandardButton.Save).setEnabled(False)
        self.button_box.accepted.connect(self.accept_with_validation)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(search_group)
        layout.addWidget(edit_group)
        layout.addWidget(self.button_box)
        self.enable_form_fields(False)
        
    def enable_form_fields(self, enable=True):
        self.name_input.setEnabled(enable)
        self.company_input.setEnabled(enable)
        self.phone_input.setEnabled(enable)
        self.status_combo.setEnabled(enable)
        self.button_box.button(QDialogButtonBox.StandardButton.Save).setEnabled(enable)
        
    def search_product(self):
        code = self.search_code_input.text()
        if not code:
            QMessageBox.warning(self, "Error", "Por favor ingrese un código de contratista.")
            return
        contratista = ContratistaController.get_by_code(code)
        if contratista:
            self.contratista_id = contratista["id"]
            self.code_display.setText(contratista["codigo"])
            self.name_input.setText(contratista["nombre"])
            self.company_input.setText(contratista["empresa"])
            self.phone_input.setText(contratista["telefono"])
            estado_index = self.status_combo.findText(contratista["estado"], Qt.MatchFlag.MatchFixedString)
            if estado_index >= 0:
                self.status_combo.setCurrentIndex(estado_index)
            self.enable_form_fields(True)
        else:
            QMessageBox.information(self, "Contratista no encontrado", 
                                 f"No se encontró ningún contratista con el código {code}.")
            self.code_display.setText("-")
            self.name_input.clear()
            self.company_input.clear()
            self.phone_input.clear()
            self.status_combo.setCurrentText("Activo")
            self.enable_form_fields(False)
    
    def accept_with_validation(self):
        if not self.name_input.text():
            QMessageBox.warning(self, "Error", "Por favor ingrese el nombre del contratista.")
            return
        nombre = self.name_input.text()
        empresa = self.company_input.text()
        telefono = self.phone_input.text()
        estado = self.status_combo.currentText()
        success = ContratistaController.update(self.contratista_id, nombre, empresa, telefono, estado)
        if success:
            QMessageBox.information(self, "Éxito", "Contratista actualizado correctamente.")
            if hasattr(self.parent(), "load_contratistas"):
                self.parent().load_contratistas()
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "No se pudo actualizar el contratista.")


# Modal para Eliminar Producto
class DeleteProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Eliminar Contratista")
        self.setMinimumSize(450, 300)
        apply_dialog_style(self)
        self.contratista_id = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Sección de búsqueda
        search_group = QGroupBox("Buscar Contratista a Eliminar")
        search_layout = QHBoxLayout(search_group)

        code_label = QLabel("Código:")
        self.search_code_input = QLineEdit()
        self.search_code_input.setPlaceholderText("Ingrese el código del contratista a eliminar")

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

        # Información del contratista
        info_group = QGroupBox("Información del Contratista")
        info_layout = QFormLayout(info_group)

        self.contractor_code = QLabel("-")
        self.contractor_name = QLabel("-")
        self.contractor_company = QLabel("-")
        self.contractor_phone = QLabel("-")
        self.contractor_status = QLabel("-")

        value_style = """
            QLabel {
                font-weight: bold;
                color: #2C2C2C;
                padding: 8px;
                background-color: transparent;
                border: none;
            }
        """
        self.contractor_code.setStyleSheet(value_style)
        self.contractor_name.setStyleSheet(value_style)
        self.contractor_company.setStyleSheet(value_style)
        self.contractor_phone.setStyleSheet(value_style)
        self.contractor_status.setStyleSheet(value_style)

        info_layout.addRow("Código:", self.contractor_code)
        info_layout.addRow("Nombre:", self.contractor_name)
        info_layout.addRow("Empresa:", self.contractor_company)
        info_layout.addRow("Teléfono:", self.contractor_phone)
        info_layout.addRow("Estado:", self.contractor_status)

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

        layout.addWidget(search_group)
        layout.addWidget(info_group)
        layout.addWidget(warning_label)
        layout.addWidget(self.button_box)

    def search_product(self):
        code = self.search_code_input.text()
        if not code:
            QMessageBox.warning(self, "Error", "Por favor ingrese un código de contratista.")
            self.contratista_id = None
            return
        contratista = ContratistaController.get_by_code(code)
        if contratista:
            self.contratista_id = contratista["id"]
            self.contractor_code.setText(contratista["codigo"])
            self.contractor_name.setText(contratista["nombre"])
            self.contractor_company.setText(contratista["empresa"])
            self.contractor_phone.setText(contratista["telefono"])
            self.contractor_status.setText(contratista["estado"])
            self.button_box.button(QDialogButtonBox.StandardButton.Yes).setEnabled(True)
        else:
            QMessageBox.information(self, "Contratista no encontrado",
                f"No se encontró ningún contratista con el código {code}.")
            self.contratista_id = None
            self.contractor_code.setText("-")
            self.contractor_name.setText("-")
            self.contractor_company.setText("-")
            self.contractor_phone.setText("-")
            self.contractor_status.setText("-")
            self.button_box.button(QDialogButtonBox.StandardButton.Yes).setEnabled(False)

    def confirm_delete(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirmar eliminación")
        msg_box.setText(f"¿Está seguro que desea eliminar permanentemente el contratista {self.contractor_code.text()}?")
        msg_box.setInformativeText("Esta acción no se puede deshacer.")
        msg_box.setIcon(QMessageBox.Icon.Question)
        yes_button = msg_box.addButton("Sí, eliminar", QMessageBox.ButtonRole.YesRole)
        no_button = msg_box.addButton("Cancelar", QMessageBox.ButtonRole.NoRole)
        msg_box.setDefaultButton(no_button)
        msg_box.exec()
        if msg_box.clickedButton() == yes_button and self.contratista_id:
            success = ContratistaController.delete(self.contratista_id)
            if success:
                QMessageBox.information(self, "Éxito", "Contratista eliminado correctamente.")
                if hasattr(self.parent(), "load_contratistas"):
                    self.parent().load_contratistas()
                self.accept()
            else:
                QMessageBox.warning(self, "Error", "No se pudo eliminar el contratista.")

class ContratistasView(QWidget):
    """Vista principal de contratistas, estructura copiada de inventario"""
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # Header
        header_label = QLabel("Gestión de contratistas")
        header_label.setStyleSheet("QLabel {color: white; font-size: 22px; font-weight: bold; background: transparent; border: none;}")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_frame = QFrame()
        header_frame.setStyleSheet("QFrame {background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #FF6B35, stop: 1 #E55A2B); border-radius: 8px; padding: 15px; margin-bottom: 10px;}")
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(10, 10, 10, 10)
        header_layout.addWidget(header_label)
        main_layout.addWidget(header_frame)

        # Botones CRUD 
        self.add_btn = QPushButton("Agregar")
        self.add_btn.setStyleSheet("QPushButton {background-color: #FF6B35; color: white; border: none; border-radius: 8px; padding: 12px 20px; font-size: 14px; font-weight: bold; min-width: 150px;} QPushButton:hover {background-color: #E55A2B;} QPushButton:pressed {background-color: #CC4A1F;}")
        self.add_btn.clicked.connect(self.open_add_dialog)

        self.edit_btn = QPushButton("Editar")
        self.edit_btn.setStyleSheet("QPushButton {background-color: #222; color: white; border: none; border-radius: 8px; padding: 12px 20px; font-size: 14px; font-weight: bold; min-width: 150px;} QPushButton:hover {background-color: #111;} QPushButton:pressed {background-color: #000;}")
        self.edit_btn.clicked.connect(self.open_edit_dialog)

        self.delete_btn = QPushButton("Eliminar")
        self.delete_btn.setStyleSheet("QPushButton {background-color: #8B4513; color: white; border: none; border-radius: 8px; padding: 12px 20px; font-size: 14px; font-weight: bold; min-width: 150px;} QPushButton:hover {background-color: #7A3A0F;} QPushButton:pressed {background-color: #69300A;}")
        self.delete_btn.clicked.connect(self.open_delete_dialog)

        crud_layout = QHBoxLayout()
        crud_layout.setSpacing(15)
        crud_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        crud_layout.addWidget(self.add_btn)
        crud_layout.addWidget(self.edit_btn)
        crud_layout.addWidget(self.delete_btn)
        crud_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        main_layout.addLayout(crud_layout)


        # Línea divisora
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("QFrame {background-color: #ddd; max-height: 2px;}")
        main_layout.addWidget(separator)

        # Filtro y búsqueda en una sola fila
        filter_layout = QHBoxLayout()
        filter_label = QLabel("Filtro:")
        filter_label.setStyleSheet("QLabel {color: #2C2C2C; font-weight: bold; background-color: transparent; border: none;}")
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Ambos", "Activo", "Inactivo"])
        self.filter_combo.setMinimumWidth(150)
        self.filter_combo.setStyleSheet("QComboBox {border: 2px solid #ddd; border-radius: 6px; padding: 8px; background-color: white; color: #2C2C2C; min-height: 20px;} QComboBox:focus {border-color: #FF6B35;} QComboBox::drop-down {border: none; width: 20px;} QComboBox QAbstractItemView {color: #2C2C2C; background-color: white; selection-background-color: #FF6B35; selection-color: white;}")

        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Buscar contratista...")
        self.search_field.setMinimumWidth(250)
        self.search_field.setStyleSheet("QLineEdit {border: 2px solid #ddd; border-radius: 6px; padding: 8px; color: #2C2C2C; background-color: white;} QLineEdit:focus {border-color: #FF6B35;}")
        search_btn = QPushButton("Buscar")
        search_btn.setStyleSheet("QPushButton {background-color: #FF6B35; color: white; border: none; border-radius: 6px; padding: 10px 20px; font-weight: bold; font-size: 14px;} QPushButton:hover {background-color: #E55A2B;} QPushButton:pressed {background-color: #CC4A1F;}")

        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_combo)
        filter_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        filter_layout.addWidget(self.search_field)
        filter_layout.addWidget(search_btn)
        main_layout.addLayout(filter_layout)

        # Tabla de contratistas
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(5)
        self.inventory_table.setHorizontalHeaderLabels([
            "Código", "Nombre", "Empresa", "Teléfono", "Estado"
        ])
        self.inventory_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.inventory_table.verticalHeader().setVisible(False)
        self.inventory_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.inventory_table.setStyleSheet("QTableWidget {background-color: white; border: 2px solid #ddd; border-radius: 6px; gridline-color: #eee;} QTableWidget::item {padding: 8px; color: #2C2C2C; border: none;} QTableWidget::item:selected {background-color: #FF6B35; color: white;} QHeaderView::section {background-color: #f8f9fa; color: #2C2C2C; padding: 8px; border: 1px solid #ddd; font-weight: bold;}")

        # Ajuste de tamaño de columnas para cubrir todo el ancho
        self.inventory_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Código
        self.inventory_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Nombre
        self.inventory_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Empresa
        self.inventory_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # Teléfono
        self.inventory_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)  # Estado

        self.inventory_table.doubleClicked.connect(self.handle_double_click)
        main_layout.addWidget(self.inventory_table)
        self.setLayout(main_layout)
        self.load_contratistas()
    
    def load_contratistas(self):
        contratistas = ContratistaController.get_all()
        filtro = self.filter_combo.currentText()
        texto_busqueda = self.search_field.text().lower()
        datos_filtrados = []
        for c in contratistas:
            if filtro != "Ambos" and c["estado"] != filtro:
                continue
            if texto_busqueda and texto_busqueda not in c["nombre"].lower() and texto_busqueda not in c["codigo"].lower():
                continue
            datos_filtrados.append(c)
        self.inventory_table.setRowCount(len(datos_filtrados))
        for row, c in enumerate(datos_filtrados):
            code_item = QTableWidgetItem(c["codigo"])
            name_item = QTableWidgetItem(c["nombre"])
            company_item = QTableWidgetItem(c["empresa"])
            phone_item = QTableWidgetItem(c["telefono"])
            status_item = QTableWidgetItem(c["estado"])
            code_item.setForeground(QColor("#2C2C2C"))
            name_item.setForeground(QColor("#2C2C2C"))
            company_item.setForeground(QColor("#2C2C2C"))
            phone_item.setForeground(QColor("#2C2C2C"))
            status_item.setForeground(QColor("#2C2C2C"))
            self.inventory_table.setItem(row, 0, code_item)
            self.inventory_table.setItem(row, 1, name_item)
            self.inventory_table.setItem(row, 2, company_item)
            self.inventory_table.setItem(row, 3, phone_item)
            self.inventory_table.setItem(row, 4, status_item)
    
    # Métodos para abrir los modales
    def open_add_dialog(self):
        dialog = AddProductDialog(self)
        dialog.exec()
        
    def open_view_dialog(self):
        dialog = ViewDetailDialog(self)
        selected_rows = self.inventory_table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            code = self.inventory_table.item(row, 0).text()
            dialog.code_input.setText(code)
            dialog.search_contractor()
        dialog.exec()
        
    def open_edit_dialog(self):
        dialog = EditProductDialog(self)
        selected_rows = self.inventory_table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            code = self.inventory_table.item(row, 0).text()
            dialog.search_code_input.setText(code)
            dialog.search_product()
        dialog.exec()
        
    def open_delete_dialog(self):
        dialog = DeleteProductDialog(self)
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