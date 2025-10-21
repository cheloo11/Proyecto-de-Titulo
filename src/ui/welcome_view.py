from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QFrame, QSizePolicy, QSpacerItem)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QPixmap

class WelcomeView(QWidget):
    """Vista de bienvenida para la página principal"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0) 
        
        # Panel superior compacto y responsivo
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                          stop: 0 #FF6B35, stop: 1 #E55A2B);
                margin: 0;
                padding: 10px;
            }
        """)
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(15, 15, 15, 15)
        
        # Contenedor para logo y título en una sola fila
        top_container = QWidget()
        top_container.setStyleSheet("background-color: transparent;")
        top_layout = QHBoxLayout(top_container)
        top_layout.setContentsMargins(0, 0, 0, 0)
        
        # Logo más compacto
        logo_label = QLabel("J&M")
        logo_label.setFixedSize(60, 60)
        logo_label.setStyleSheet("""
            background-color: white;
            color: #2c3e50;
            font-weight: bold;
            font-size: 20px;
            border-radius: 30px;
        """)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Contenedor para título y subtítulo
        title_container = QWidget()
        title_container.setStyleSheet("background-color: transparent;")
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        # Título de bienvenida
        welcome_label = QLabel("Bienvenido al Inventario de la Constructora J&M")
        welcome_label.setStyleSheet("""
            QLabel {
                color: white; 
                font-size: 20px; 
                font-weight: bold;
                background-color: transparent;
            }
        """)
        
        # Subtítulo
        subtitle = QLabel("Sistema integral de gestión de materiales")
        subtitle.setStyleSheet("""
            QLabel {
                color: #ecf0f1; 
                font-size: 16px;
                background-color: transparent;
            }
        """)
        
        title_layout.addWidget(welcome_label)
        title_layout.addWidget(subtitle)
        
        # Agregar elementos al contenedor superior
        top_layout.addWidget(logo_label)
        top_layout.addWidget(title_container, 1)
        
        # Agregar el contenedor superior al header
        header_layout.addWidget(top_container)
        
        # Contenedor para el contenido principal
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                padding: 20px;
            }
        """)
        content_layout = QVBoxLayout(content_frame)
        
        # Mensaje de bienvenida central
        welcome_message = QLabel("Utilice la barra lateral para navegar por las diferentes secciones del sistema")
        welcome_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_message.setStyleSheet("""
            QLabel {
                font-size: 16px; 
                color: #555; 
                margin: 40px 0;
                background-color: transparent;
            }
        """)
        
        # Pie de página
        footer = QLabel("© 2025 Constructora J&M - Sistema de Inventario v1.0")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("""
            QLabel {
                color: #6c757d; 
                margin-top: 15px;
                background-color: transparent;
            }
        """)
        
        # Agregar elementos al contenido principal
        content_layout.addStretch(1)
        content_layout.addWidget(welcome_message)
        content_layout.addStretch(1)
        content_layout.addWidget(footer)
        
        # Agregar los frames principales al layout principal
        main_layout.addWidget(header_frame)
        main_layout.addWidget(content_frame, 1)
        
        self.setLayout(main_layout)