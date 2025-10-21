from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QFrame
from PyQt6.QtCore import Qt
from ui.styles.common_styles import BUTTON_PRIMARY_STYLE, TABLE_STYLE

class ReportsView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
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
                                          stop: 0 #FF6B35, stop: 1 #E55A2B);
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 10px;
            }
        """)
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(10, 10, 10, 10)
        
        title = QLabel("Reportes")
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
        
        # Tabla de reportes
        self.reports_table = QTableWidget()
        self.reports_table.setColumnCount(3)
        self.reports_table.setHorizontalHeaderLabels(["Tipo de reporte", "Fecha", "Detalles"])
        self.reports_table.setStyleSheet(TABLE_STYLE)
        main_layout.addWidget(self.reports_table)
        
        # Botón para generar reporte
        self.generate_report_button = QPushButton("Generar Reporte")
        self.generate_report_button.setStyleSheet(BUTTON_PRIMARY_STYLE)
        main_layout.addWidget(self.generate_report_button)