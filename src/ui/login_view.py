from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                            QPushButton, QFormLayout, QFrame, QMessageBox,
                            QCheckBox, QHBoxLayout, QGridLayout)
from PyQt6.QtCore import Qt, pyqtSignal
from auth.authentication import AuthService

class LoginView(QWidget):
    """Ventana de inicio de sesión"""
    
    # Señal que se emite cuando el login es exitoso
    login_success = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventario J&M - Inicio de Sesión")
        self.setFixedSize(400, 500)
        self.setStyleSheet("background-color: #2C2C2C;")
        self.init_ui()
        
    def init_ui(self):
        """Inicializar la interfaz de usuario"""
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Logo y título
        logo_container = QFrame()
        logo_container.setStyleSheet("background-color: #FF6B35; border-radius: 10px;")
        logo_layout = QVBoxLayout(logo_container)
        
        title = QLabel("Inventario J&M")
        title.setStyleSheet("""
            color: white; 
            font-size: 24px; 
            font-weight: bold;
            padding: 15px;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(title)
        
        subtitle = QLabel("Sistema de Gestión de Inventario")
        subtitle.setStyleSheet("""
            color: white; 
            font-size: 14px;
            padding-bottom: 15px;
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(subtitle)
        
        main_layout.addWidget(logo_container)
        
        # Formulario de login
        login_frame = QFrame()
        login_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
            QLabel {
                color: black;
                font-size: 14px;
                font-weight: bold;
                padding: 5px;
            }
        """)
        
        form_layout = QGridLayout(login_frame)
        form_layout.setContentsMargins(5, 15, 10, 15) 
        form_layout.setSpacing(10) 

        # Usuario
        user_label = QLabel("Usuario:")
        user_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        user_label.setStyleSheet("""
            QLabel {
                color: black;
                font-size: 14px;
                font-weight: bold;
                padding: 5px 0px 5px 0px;  /* Reducimos padding horizontal */
                margin-right: 0px;
            }
        """)
        
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Ingrese su nombre de usuario")
        self.user_input.setMinimumWidth(200)
        self.user_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ddd;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
                color: #333;
                background-color: white;
            }
            QLineEdit::placeholder {
                color: #999;
            }
            QLineEdit:focus {
                border-color: #FF6B35;
            }
        """)
        
        # Contraseña
        password_label = QLabel("Contraseña:")
        password_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        password_label.setStyleSheet("""
            QLabel {
                color: black;
                font-size: 14px;
                font-weight: bold;
                padding: 5px 0px 5px 0px;  /* Reducimos padding horizontal */
                margin-right: 0px;
            }
        """)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Ingrese su contraseña")
        self.password_input.setMinimumWidth(200) 
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ddd;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
                color: #333;
                background-color: white;
            }
            QLineEdit::placeholder {
                color: #999;
            }
            QLineEdit:focus {
                border-color: #FF6B35;
            }
        """)
        
        # Recordarme CAMBIAR
        remember_layout = QHBoxLayout()
        remember_layout.setContentsMargins(0, 0, 0, 0)
        remember_layout.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        remember_layout.addStretch() 
        self.remember_checkbox = QCheckBox("Recordarme")
        self.remember_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 13px;
                color: black;
                font-weight: normal;
                background-color: transparent;
            }
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
                background-color: white;
                border: 1px solid #888;
                border-radius: 2px;
            }
            QCheckBox::indicator:checked {
                background-color: #FF6B35;
            }
        """)
        remember_layout.addWidget(self.remember_checkbox)
        remember_layout.addStretch() 
        
        # Botón de inicio de sesión 
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.setFixedWidth(200)
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #FF6B35;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E55A2B;
            }
            QPushButton:pressed {
                background-color: #CC4A1F;
            }
        """)
        self.login_button.clicked.connect(self.authenticate)
        button_layout.addWidget(self.login_button)
        
        # Agregar widgets al grid layout
        form_layout.addWidget(user_label, 0, 0, 1, 1)
        form_layout.addWidget(self.user_input, 0, 1, 1, 2)
        form_layout.addWidget(password_label, 1, 0, 1, 1)
        form_layout.addWidget(self.password_input, 1, 1, 1, 2)
        
        # Agregamos el layout del checkbox y el botón
        form_layout.addLayout(remember_layout, 2, 0, 1, 3)
        form_layout.addLayout(button_layout, 3, 0, 1, 3)
        
        # Ajustar las columnas del grid 
        form_layout.setColumnStretch(0, 0) 
        form_layout.setColumnStretch(1, 2)  
        form_layout.setColumnStretch(2, 0) 
        
        form_layout.setHorizontalSpacing(3)  
        
        main_layout.addWidget(login_frame)
        
        # Footer
        footer = QLabel("© 2025 Constructora J&M - Sistema de Inventario v1.0")
        footer.setStyleSheet("color: #aaa; font-size: 12px;")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(footer)
        
        self.setLayout(main_layout)
    
    def authenticate(self):
        """Método que autentica al usuario contra la base de datos"""
        username = self.user_input.text()
        password = self.password_input.text()
        
        # Validación básica
        if not username or not password:
            QMessageBox.warning(self, "Error", "Por favor complete todos los campos.")
            return
            
        # Usar el servicio de autenticación
        result = AuthService.authenticate_user(username, password)
        
        if result["autenticado"]:
            # Solo emitir la señal, sin mostrar el mensaje emergente
            self.login_success.emit(result)
        elif "error" in result:
            QMessageBox.critical(self, "Error", f"Error de autenticación: {result['error']}")
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")