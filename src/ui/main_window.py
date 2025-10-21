from PyQt6.QtWidgets import (QMainWindow, QTabWidget, QVBoxLayout, QWidget, 
                           QHBoxLayout, QPushButton, QLabel, QStackedWidget)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt, QSize

# Importar las vistas desde sus respectivos archivos
from ui.welcome_view import WelcomeView
from ui.inventory_view import InventoryView
from ui.entrada_material_view import EntradaMaterialView
from ui.salida_material_view import SalidaMaterialView
from ui.components.sidebar_button import SideBarButton
from ui.reports_view import ReportsView
from ui.obras_view import ObrasView
from ui.contratistas_view import ContratistasView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Inventario de Construcción")
        self.setGeometry(100, 100, 1200, 800)
        
        self.init_ui()

    def init_ui(self):
        # Ocultar la barra de menú 
        self.menuBar().setVisible(False)
        
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Crear la barra lateral
        sidebar = self.create_sidebar()
        
        # Crear instancias de las vistas
        self.welcome_view = WelcomeView()
        self.inventory_view = InventoryView()
        self.entrada_material_view = EntradaMaterialView()
        self.salida_material_view = SalidaMaterialView()
        self.obras_view = ObrasView()
        self.contratistas_view = ContratistasView()
        self.reports_view = ReportsView()
        
        # Agregar vistas al stacked widget
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.welcome_view)        
        self.stacked_widget.addWidget(self.inventory_view)     
        self.stacked_widget.addWidget(self.entrada_material_view)
        self.stacked_widget.addWidget(self.salida_material_view) 
        self.stacked_widget.addWidget(self.obras_view)        
        self.stacked_widget.addWidget(self.contratistas_view)   
        self.stacked_widget.addWidget(self.reports_view)       
    
        
        # Agregar barra lateral y contenido principal al layout
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stacked_widget, 1)
        
        # Establecer el widget central
        self.setCentralWidget(central_widget)
        self.setMinimumSize(1200, 800)
        
    def create_sidebar(self):
        # Sidebar
        self.sidebar = QWidget()
        self.sidebar.setMinimumWidth(200)
        self.sidebar.setMaximumWidth(200)
        self.sidebar.setStyleSheet("background-color: #2C2C2C;")
        
        # Layout para la barra lateral
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # Logo o título en la barra lateral
        logo_container = QWidget()
        logo_container.setStyleSheet("background-color: #FF6B35; padding: 15px;")
        logo_layout = QVBoxLayout(logo_container)
        logo_label = QLabel("J&M Inventario")
        logo_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(logo_label)
        
        # Botones del sidebar
        self.btn_welcome = SideBarButton("Inicio")
        self.btn_inventory = SideBarButton("Inventario")
        self.btn_entrada_material = SideBarButton("Entrada de Material")
        self.btn_salida_material = SideBarButton("Salida de Material")
        self.btn_obras = SideBarButton("Obras")
        self.btn_contratistas = SideBarButton("Contratistas")
        self.btn_reports = SideBarButton("Reportes")

        # Conectar eventos de botones
        self.btn_welcome.clicked.connect(lambda: self.change_page(0))
        self.btn_inventory.clicked.connect(lambda: self.change_page(1))
        self.btn_entrada_material.clicked.connect(lambda: self.change_page(2))
        self.btn_salida_material.clicked.connect(lambda: self.change_page(3))
        self.btn_obras.clicked.connect(lambda: self.change_page(4))
        self.btn_contratistas.clicked.connect(lambda: self.change_page(5))
        self.btn_reports.clicked.connect(lambda: self.change_page(6))

        # Agregar widgets a la barra lateral
        sidebar_layout.addWidget(logo_container)
        sidebar_layout.addWidget(self.btn_welcome)
        sidebar_layout.addWidget(self.btn_inventory)
        sidebar_layout.addWidget(self.btn_entrada_material)
        sidebar_layout.addWidget(self.btn_salida_material)
        sidebar_layout.addWidget(self.btn_obras)
        sidebar_layout.addWidget(self.btn_contratistas)
        sidebar_layout.addWidget(self.btn_reports)
        sidebar_layout.addStretch()
        
        return self.sidebar

    def change_page(self, index):
        # Desmarcar todos los botones
        buttons = [self.btn_welcome, self.btn_inventory, 
                  self.btn_entrada_material, self.btn_salida_material,
                  self.btn_obras, self.btn_contratistas, self.btn_reports]
        for button in buttons:
            button.setChecked(False)
        # Marcar el botón seleccionado
        buttons[index].setChecked(True)
        # Cambiar la página
        self.stacked_widget.setCurrentIndex(index)

    def set_user(self, user_data):
        """Establece los datos del usuario actual"""
        self.current_user = user_data
        
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #f5f5f5;
                color: #333333;
            }
            QLabel {
                color: #333333;
                background-color: transparent;
            }
            QLineEdit, QTextEdit, QComboBox, QDateEdit {
                background-color: white;
                color: #333333;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 4px;
            }
            QPushButton {
                background-color: #FF6B35;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E55A2B;
            }
            QTableWidget {
                background-color: white;
                color: #333333;
                gridline-color: #dddddd;
                border: 1px solid #cccccc;
            }
            QHeaderView::section {
                background-color: #2C2C2C;
                color: white;
                padding: 6px;
                border: 1px solid #444444;
            }
            /* Estilos específicos para el menú lateral */
            #sidebarFrame {
                background-color: #2C2C2C;
            }
            #sidebarFrame QLabel, #sidebarFrame QPushButton {
                color: white;
            }
        """)
        
        self.setWindowTitle(f"Inventario J&M - {user_data['nombre']}")
        
        if hasattr(self, 'statusBar'):
            self.statusBar().showMessage(f"Usuario: {user_data['nombre']} | Perfil: {user_data['perfil']}")