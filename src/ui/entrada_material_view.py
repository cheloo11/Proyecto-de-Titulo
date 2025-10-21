from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                           QTableWidget, QTableWidgetItem, QHeaderView, QFrame,
                           QAbstractItemView, QLineEdit, QComboBox, QGroupBox,
                           QFormLayout, QSpinBox, QDateEdit, QTextEdit, QSpacerItem, QSizePolicy,
                           QDialog, QDialogButtonBox)
from PyQt6.QtGui import QIcon, QColor, QPixmap
from PyQt6.QtCore import Qt, QDate, QSize, QTimer
from ui.styles.common_styles import (INPUT_STYLE, SPINBOX_STYLE, COMBO_STYLE, DATE_STYLE,
                                   BUTTON_PRIMARY_STYLE, BUTTON_SECONDARY_STYLE, BUTTON_TERTIARY_STYLE,
                                   GROUP_STYLE, TABLE_STYLE, LABEL_STYLE)

class EntradaMaterialView(QWidget):
    """Vista para registro de entrada de materiales"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # Layout principal
        main_layout = QVBoxLayout(self)
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
        
        title = QLabel("Entrada de Materiales")
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
        
        # Formulario de entrada
        form_group = QGroupBox("Información del Material")
        form_group.setStyleSheet(GROUP_STYLE)
        form_layout = QFormLayout(form_group)
        
        # Campos del formulario
        self.codigo_input = QLineEdit()
        self.codigo_input.setText("...") 
        self.codigo_input.setReadOnly(True) 
        
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre del material")
        
        self.cantidad_input = QSpinBox()
        self.cantidad_input.setRange(1, 10000)
        self.cantidad_input.setValue(1)
        
        self.unidad_combo = QComboBox()
        self.unidad_combo.addItems(["Unidades", "Metros", "Kilogramos", "Litros", "Cajas"])
        
        self.proveedor_input = QLineEdit()
        self.proveedor_input.setPlaceholderText("Nombre del proveedor")
        
        self.fecha_input = QDateEdit()
        self.fecha_input.setDate(QDate.currentDate())
        self.fecha_input.setCalendarPopup(True)
        
        self.observaciones_input = QTextEdit()
        self.observaciones_input.setPlaceholderText("Observaciones adicionales...")
        self.observaciones_input.setMaximumHeight(60)
        self.observaciones_input.setMinimumHeight(60)
        
        # Aplicar estilos
        self.codigo_input.setStyleSheet(INPUT_STYLE)
        self.nombre_input.setStyleSheet(INPUT_STYLE)
        self.proveedor_input.setStyleSheet(INPUT_STYLE)
        self.observaciones_input.setStyleSheet(INPUT_STYLE)
        self.cantidad_input.setStyleSheet(SPINBOX_STYLE)
        self.unidad_combo.setStyleSheet(COMBO_STYLE)
        self.fecha_input.setStyleSheet(DATE_STYLE)
        
        # Crear labels manualmente con estilos
        codigo_label = QLabel("Código:")
        nombre_label = QLabel("Nombre del Material:")
        cantidad_label = QLabel("Cantidad:")
        unidad_label = QLabel("Unidad de Medida:")
        proveedor_label = QLabel("Proveedor:")
        fecha_label = QLabel("Fecha de Ingreso:")
        observaciones_label = QLabel("Observaciones:")
        
        # Aplicar estilos a todos los labels
        for label in [codigo_label, nombre_label, cantidad_label, unidad_label, 
                     proveedor_label, fecha_label, observaciones_label]:
            label.setStyleSheet(LABEL_STYLE)
        
        # Agregar campos al formulario con labels estilizados
        form_layout.addRow(codigo_label, self.codigo_input)
        form_layout.addRow(nombre_label, self.nombre_input)
        form_layout.addRow(cantidad_label, self.cantidad_input)
        form_layout.addRow(unidad_label, self.unidad_combo)
        form_layout.addRow(proveedor_label, self.proveedor_input)
        form_layout.addRow(fecha_label, self.fecha_input)
        form_layout.addRow(observaciones_label, self.observaciones_input)
        
        # Layout horizontal para formulario y panel de funciones
        content_layout = QHBoxLayout()
        content_layout.setSpacing(15)  
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Crear panel de funciones 
        functions_panel = QGroupBox("Funciones")
        functions_panel.setStyleSheet(GROUP_STYLE)
        functions_panel.setMinimumWidth(250)  # Ancho mínimo 
        functions_panel.setMaximumWidth(350)  # Ancho máximo 
        functions_layout = QVBoxLayout(functions_panel)
        functions_layout.setSpacing(20)  
        
        # Espaciador superior para centrar verticalmente
        functions_layout.addStretch()
        
        # Botón Registrar Entrada
        self.btn_registrar = QPushButton("Registrar Entrada")
        self.btn_registrar.setStyleSheet(BUTTON_PRIMARY_STYLE + """
            QPushButton {
                min-height: 40px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #e55a2b;
            }
        """)
        functions_layout.addWidget(self.btn_registrar)
        
        # Botón Escanear Código de Barras
        self.btn_escanear = QPushButton("Escanear Código")
        self.btn_escanear.setStyleSheet(BUTTON_SECONDARY_STYLE + """
            QPushButton {
                min-height: 40px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #1a1a1a;
            }
        """)
        self.btn_escanear.clicked.connect(self.open_barcode_scanner)
        functions_layout.addWidget(self.btn_escanear)
        
        # Botón Limpiar Formulario
        self.btn_limpiar = QPushButton("Limpiar Formulario")
        self.btn_limpiar.setStyleSheet(BUTTON_TERTIARY_STYLE + """
            QPushButton {
                min-height: 40px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #704010;
            }
        """)
        self.btn_limpiar.clicked.connect(self.clear_form)
        functions_layout.addWidget(self.btn_limpiar)
        
        # Espaciador inferior para centrar verticalmente
        functions_layout.addStretch()
        
        # Agregar panel de funciones 
        content_layout.addWidget(functions_panel, 1)  
        
        # Agregar formulario 
        content_layout.addWidget(form_group, 3) 
        
        # Agregar el layout horizontal al layout principal
        main_layout.addLayout(content_layout)
        
        # Tabla de entradas recientes
        recent_group = QGroupBox("Entradas Recientes")
        recent_group.setStyleSheet(GROUP_STYLE)
        recent_layout = QVBoxLayout(recent_group)
        
        self.table_entradas = QTableWidget()
        self.table_entradas.setColumnCount(6)
        self.table_entradas.setHorizontalHeaderLabels([
            "Fecha", "Código", "Material", "Cantidad", "Proveedor", "Usuario"
        ])
        self.table_entradas.setStyleSheet(TABLE_STYLE)
        
        recent_layout.addWidget(self.table_entradas)
        main_layout.addWidget(recent_group)
    
    def clear_form(self):
        """Limpia todos los campos del formulario"""
        # Resetear código a estado inicial
        self.codigo_input.setText("...")
        
        # Limpiar campos de texto
        self.nombre_input.clear()
        self.proveedor_input.clear()
        self.observaciones_input.clear()
        
        # Resetear campos numéricos y desplegables
        self.cantidad_input.setValue(1)  
        self.unidad_combo.setCurrentIndex(0) 
        
        # Resetear fecha a la actual
        self.fecha_input.setDate(QDate.currentDate())
        
        # Enfocar el primer campo para facilitar el siguiente ingreso
        self.codigo_input.setFocus()
    
    def open_barcode_scanner(self):
        """Abre el modal para escanear código de barras"""
        scanner_dialog = BarcodeScannerDialog(self)
        if scanner_dialog.exec() == QDialog.DialogCode.Accepted:
            barcode = scanner_dialog.get_barcode()
            if barcode:
                self.codigo_input.setText(barcode)

class BarcodeScannerDialog(QDialog):
    """Modal para escanear códigos de barras"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.barcode = ""
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Escanear Código de Barras")
        self.setModal(True)
        self.setFixedSize(450, 250) 
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título
        title = QLabel("Esperando lectura del código de barras...")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2C2C2C;
                padding: 10px;
            }
        """)
        title.setWordWrap(True)  # Permitir que el texto se ajuste
        layout.addWidget(title)
        
        # Área de entrada 
        self.barcode_input = QLineEdit()
        self.barcode_input.setPlaceholderText("Código aparecerá aquí...")
        self.barcode_input.returnPressed.connect(self.on_barcode_scanned)
        self.barcode_input.setStyleSheet("""
            QLineEdit {
                font-size: 14px;
                padding: 12px;
                border: 2px solid #FF6B35;
                border-radius: 6px;
                background-color: white;
                min-height: 20px;
            }
        """)
        layout.addWidget(self.barcode_input)
        
        # Instrucciones
        instructions = QLabel("Escanee el código de barras o escriba manualmente y presione Enter")
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions.setStyleSheet("""
            QLabel {
                color: #666;
                font-size: 12px;
                padding: 5px;
            }
        """)
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Solo botón Cancelar
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel)
        buttons.rejected.connect(self.reject)
        buttons.setStyleSheet("""
            QPushButton {
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                background-color: #8B4513;
                color: white;
                border: none;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #704010;
            }
        """)
        layout.addWidget(buttons)
        
        # Focus en el input para recibir el escaneo
        self.barcode_input.setFocus()
    
    def on_barcode_scanned(self):
        """Se ejecuta cuando se escaneó un código"""
        self.barcode = self.barcode_input.text().strip()
        if self.barcode:
            self.accept()
    
    def get_barcode(self):
        """Retorna el código escaneado"""
        return self.barcode