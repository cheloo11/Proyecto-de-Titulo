from PyQt6.QtWidgets import QApplication
import sys
from ui.main_window import MainWindow
from ui.login_view import LoginView
from database.init_db import initialize_database

class InventoryApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        
        # Inicializar la base de datos
        if not initialize_database():
            print("Error: No se pudo inicializar la base de datos. La aplicación puede no funcionar correctamente.")
        
        # Iniciar con la ventana de login
        self.login_view = LoginView()
        self.login_view.login_success.connect(self.on_login_success)
        self.login_view.show()
        
        sys.exit(self.app.exec())
        
    def on_login_success(self, user_data):
        """Manejador para cuando el login es exitoso"""
        # Ocultar la ventana de login
        self.login_view.hide()
        
        # Crear y mostrar la ventana principal
        self.main_window = MainWindow()
        self.main_window.set_user(user_data)  # Pasar datos del usuario
        self.main_window.show()

if __name__ == "__main__":
    app = InventoryApp()