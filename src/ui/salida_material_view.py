from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                           QTableWidget, QTableWidgetItem, QHeaderView, QFrame,
                           QAbstractItemView, QLineEdit, QComboBox, QGroupBox,
                           QFormLayout, QSpinBox, QDateEdit, QTextEdit, QSpacerItem, QSizePolicy,
                           QDialog, QDialogButtonBox)
from PyQt6.QtGui import QIcon, QColor, QPixmap
from PyQt6.QtCore import Qt, QDate, QSize, QTimer
from ui.styles.common_styles import (INPUT_STYLE, SPINBOX_STYLE, COMBO_STYLE, DATE_STYLE,
                                   BUTTON_PRIMARY_STYLE, BUTTON_SECONDARY_STYLE, BUTTON_TERTIARY_STYLE,
                                   GROUP_STYLE, TABLE_STYLE, LABEL_INFO_STYLE, LABEL_BOLD_STYLE, LABEL_STYLE)
from controllers.material_controller import MaterialController
from controllers.obra_controller import ObraController
from controllers.contratista_controller import ContratistaController
from controllers.movimiento_controller import MovimientoController
from PyQt6.QtWidgets import QMessageBox

class SalidaMaterialView(QWidget):
    """Vista para registro de salida/despacho de materiales"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        # Cargar despachos recientes al iniciar
        self.load_despachos_recientes()

    def init_ui(self):
        # Layout principal con márgenes más pequeños para mejor responsividad
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # Header compacto y responsivo
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                          stop: 0 #2C2C2C, stop: 1 #1F1F1F);
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 10px;
            }
        """)
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(10, 10, 10, 10)
        
        title = QLabel("Salida/Despacho de Materiales")
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
        
        # Formulario de salida
        form_group = QGroupBox("Información del Despacho")
        form_group.setStyleSheet(GROUP_STYLE)
        form_layout = QFormLayout(form_group)
        
        # Campos del formulario
        self.codigo_input = QLineEdit()
        self.codigo_input.setText("...") 
        self.codigo_input.setReadOnly(True)  
        
        self.material_label = QLabel("Material no seleccionado")
        self.material_label.setStyleSheet(LABEL_INFO_STYLE)
        
        self.stock_label = QLabel("Stock disponible: --")
        self.stock_label.setStyleSheet(LABEL_BOLD_STYLE)
        
        self.cantidad_input = QSpinBox()
        self.cantidad_input.setRange(1, 1000)
        self.cantidad_input.setValue(1)
        
        self.obra_combo = QComboBox()
        # Cargar obras activas desde controlador
        self.obra_combo.addItem("Seleccione una obra")
        try:
            obras = ObraController.get_all_obras()
            for o in obras:
                if o.get("estado", "activa").lower() == "activa":
                    self.obra_combo.addItem(f"{o.get('codigo')} - {o.get('nombre')}", o.get("id"))
        except Exception as e:
            print(f"Error cargando obras: {e}")
        
        self.contratista_combo = QComboBox()
        # Cargar contratistas activos
        self.contratista_combo.addItem("Seleccione un contratista")
        try:
            contratistas = ContratistaController.get_all()
            for c in contratistas:
                if str(c.get("estado", "Activo")).lower() == "activo":
                    self.contratista_combo.addItem(f"{c.get('codigo')} - {c.get('nombre')}", c.get("id"))
        except Exception as e:
            print(f"Error cargando contratistas: {e}")
        
        self.fecha_input = QDateEdit()
        self.fecha_input.setDate(QDate.currentDate())
        self.fecha_input.setCalendarPopup(True)
        
        self.observaciones_input = QTextEdit()
        self.observaciones_input.setPlaceholderText("Motivo del despacho, observaciones...")
        self.observaciones_input.setMaximumHeight(60)
        self.observaciones_input.setMinimumHeight(60)
        
        # Aplicar estilos
        self.codigo_input.setStyleSheet(INPUT_STYLE)
        self.observaciones_input.setStyleSheet(INPUT_STYLE)
        self.cantidad_input.setStyleSheet(SPINBOX_STYLE)
        self.obra_combo.setStyleSheet(COMBO_STYLE)
        self.contratista_combo.setStyleSheet(COMBO_STYLE)
        self.fecha_input.setStyleSheet(DATE_STYLE)
        
        # Crear labels manualmente con estilos
        codigo_label = QLabel("Código del Material:")
        material_label_form = QLabel("Material:")
        stock_label_form = QLabel("Stock Actual:")
        cantidad_label = QLabel("Cantidad a Despachar:")
        obra_label = QLabel("Obra Destino:")
        contratista_label = QLabel("Contratista:")
        fecha_label = QLabel("Fecha de Despacho:")
        observaciones_label = QLabel("Observaciones:")
        
        # Aplicar estilos a todos los labels del formulario
        for label in [codigo_label, material_label_form, stock_label_form, cantidad_label, 
                     obra_label, contratista_label, fecha_label, observaciones_label]:
            label.setStyleSheet(LABEL_STYLE)
        
        # Agregar campos al formulario con labels estilizados
        form_layout.addRow(codigo_label, self.codigo_input)
        form_layout.addRow(material_label_form, self.material_label)
        form_layout.addRow(stock_label_form, self.stock_label)
        form_layout.addRow(cantidad_label, self.cantidad_input)
        form_layout.addRow(obra_label, self.obra_combo)
        form_layout.addRow(contratista_label, self.contratista_combo)
        form_layout.addRow(fecha_label, self.fecha_input)
        form_layout.addRow(observaciones_label, self.observaciones_input)
        
        # Layout horizontal para formulario y panel de funciones
        content_layout = QHBoxLayout()
        content_layout.setSpacing(15) 
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Crear panel de funciones 
        functions_panel = QGroupBox("Funciones")
        functions_panel.setStyleSheet(GROUP_STYLE)
        functions_panel.setMinimumWidth(250)  # Ancho mínimo en lugar de fijo
        functions_panel.setMaximumWidth(350)  # Ancho máximo para que no crezca demasiado
        functions_layout = QVBoxLayout(functions_panel)
        functions_layout.setSpacing(20)  # Más espacio entre botones
        
        # Espaciador superior para centrar verticalmente
        functions_layout.addStretch()
        
        # Botón Escanear Material
        self.btn_escanear = QPushButton("Escanear Material")
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
        
        # Botón Registrar Despacho
        self.btn_despachar = QPushButton("Registrar Despacho")
        self.btn_despachar.setStyleSheet(BUTTON_PRIMARY_STYLE + """
            QPushButton {
                min-height: 40px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #e55a2b;
            }
        """)
        functions_layout.addWidget(self.btn_despachar)
        # conectar acción de registrar despacho
        self.btn_despachar.clicked.connect(self.on_registrar_despacho)
        
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
        
        # Tabla de despachos recientes
        recent_group = QGroupBox("Despachos Recientes")
        recent_group.setStyleSheet(GROUP_STYLE)
        recent_layout = QVBoxLayout(recent_group)
        
        self.table_despachos = QTableWidget()
        self.table_despachos.setColumnCount(7)
        self.table_despachos.setHorizontalHeaderLabels([
            "Fecha", "Material", "Cantidad", "Obra", "Contratista", "Usuario", "Estado"
        ])
        self.table_despachos.setStyleSheet(TABLE_STYLE)
        
        recent_layout.addWidget(self.table_despachos)
        main_layout.addWidget(recent_group)
    
    def clear_form(self):
        """Limpia todos los campos del formulario"""
        # Resetear código a estado inicial
        self.codigo_input.setText("...")
        
        # Resetear información del material
        self.material_label.setText("Material no seleccionado")
        self.stock_label.setText("Stock disponible: --")
        
        # Resetear campos numéricos y desplegables
        self.cantidad_input.setValue(1)  
        self.obra_combo.setCurrentIndex(0) 
        self.contratista_combo.setCurrentIndex(0)  
        
        # Resetear fecha a la actual
        self.fecha_input.setDate(QDate.currentDate())
        
        # Limpiar observaciones
        self.observaciones_input.clear()
        
        # Enfocar el primer campo para facilitar el siguiente ingreso
        self.codigo_input.setFocus()
    
    def open_barcode_scanner(self):
        """Abre el modal para escanear código de barras"""
        scanner_dialog = BarcodeScannerDialog(self)
        if scanner_dialog.exec() == QDialog.DialogCode.Accepted:
            barcode = scanner_dialog.get_barcode()
            if barcode:
                self.codigo_input.setText(barcode)
                # Buscar material por código y poblar datos
                try:
                    material = MaterialController.get_material_by_code(barcode)
                    if material:
                        # material es un dict desde controller
                        self.material_label.setText(material.get("nombre"))
                        self.stock_label.setText(f"Stock disponible: {material.get('stock')}")
                        # guardar id en el widget para usar luego
                        self.codigo_input.setProperty("material_id", material.get("id"))
                    else:
                        QMessageBox.warning(self, "Material no encontrado", "No se encontró un material con ese código.")
                except Exception as e:
                    print(f"Error buscando material: {e}")
                    QMessageBox.warning(self, "Error", "Ocurrió un error al buscar el material.")

    def load_despachos_recientes(self):
        """Carga los movimientos de tipo salida recientes en la tabla"""
        try:
            # Limpiar tabla
            self.table_despachos.setRowCount(0)
            
            # Obtener movimientos recientes
            movimientos = MovimientoController.get_all_movimientos()
            if not movimientos:
                return
                
            # Filtrar solo movimientos de tipo 'salida'
            salidas = [m for m in movimientos if m["tipo_movimiento"] == "salida"]
            
            # Añadir a la tabla
            for i, salida in enumerate(salidas):
                self.table_despachos.insertRow(i)
                
                # Mapear datos a columnas de la tabla
                self.table_despachos.setItem(i, 0, QTableWidgetItem(str(salida["fecha"])))
                self.table_despachos.setItem(i, 1, QTableWidgetItem(salida["material_nombre"]))
                self.table_despachos.setItem(i, 2, QTableWidgetItem(str(salida["cantidad"])))
                self.table_despachos.setItem(i, 3, QTableWidgetItem(salida["obra_nombre"]))
                self.table_despachos.setItem(i, 4, QTableWidgetItem(salida["contratista_nombre"]))
                self.table_despachos.setItem(i, 5, QTableWidgetItem(str(salida["usuario_id"])))
                self.table_despachos.setItem(i, 6, QTableWidgetItem("Completado"))
                
            # Ajustar columnas al contenido
            self.table_despachos.resizeColumnsToContents()
            
        except Exception as e:
            print(f"Error al cargar despachos recientes: {e}")
            
    def on_registrar_despacho(self):
        """Valida el formulario y registra la salida/despacho de material."""
        # Obtener id del material buscado
        material_id = self.codigo_input.property("material_id")
        if not material_id:
            QMessageBox.warning(self, "Sin material", "Por favor, escanee o seleccione un material antes de registrar el despacho.")
            return

        try:
            cantidad = int(self.cantidad_input.value())
        except Exception:
            QMessageBox.warning(self, "Cantidad inválida", "Ingrese una cantidad válida.")
            return

        # Obtener obra y contratista seleccionados
        obra_index = self.obra_combo.currentIndex()
        obra_id = self.obra_combo.itemData(obra_index)
        if not obra_id:
            QMessageBox.warning(self, "Obra inválida", "Seleccione una obra destino.")
            return

        contratista_index = self.contratista_combo.currentIndex()
        contratista_id = self.contratista_combo.itemData(contratista_index)
        if not contratista_id:
            QMessageBox.warning(self, "Contratista inválido", "Seleccione un contratista.")
            return

        fecha = self.fecha_input.date().toString(Qt.DateFormat.ISODate)
        observaciones = self.observaciones_input.toPlainText().strip()
        
        # Obtener id_usuario de la ventana principal
        id_usuario = None
        try:
            main_window = self.window()  
            if hasattr(main_window, 'current_user') and main_window.current_user:
                id_usuario = main_window.current_user.get('id')
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            
        if not id_usuario:
            QMessageBox.warning(self, "Error de sesión", "No se pudo obtener el usuario actual. Por favor, inicie sesión nuevamente.")
            return

        # Construir movimiento
        movimiento = {
            "id_material": material_id,
            "id_obra": obra_id,
            "id_usuario": id_usuario,  
            "id_contratista": contratista_id,
            "tipo_movimiento": "salida",
            "cantidad": cantidad,
            "fecha": fecha,
            "observaciones": observaciones
        }

        # Intentar registrar via controlador
        success, msg = MovimientoController.registrar_salida(movimiento)
        if success:
            QMessageBox.information(self, "Despacho registrado", msg)
            self.clear_form()
            # Refrescar tabla de despachos recientes
            self.load_despachos_recientes()
        else:
            QMessageBox.warning(self, "Error al registrar", msg)

class BarcodeScannerDialog(QDialog):
    """Modal para escanear códigos de barras"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.barcode = ""
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Escanear Código de Barras")
        self.setModal(True)
        self.setFixedSize(450, 250)  # Aumentar tamaño del modal
        
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
        title.setWordWrap(True) 
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