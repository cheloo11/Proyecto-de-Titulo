from PyQt6.QtWidgets import QPushButton

class SideBarButton(QPushButton):
    """Botón personalizado para la barra lateral"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(50)
        self.setCheckable(True)
        self.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 10px 15px;
                border: none;
                border-left: 4px solid transparent;
                background-color: #2C2C2C;
                color: #ecf0f1;
                font-size: 14px;
            }
            QPushButton:checked {
                border-left: 4px solid #FF6B35;
                background-color: #3A3A3A;
                font-weight: bold;
                color: #FF6B35;
            }
        """)