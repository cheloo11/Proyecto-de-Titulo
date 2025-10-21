"""
Estilos comunes para toda la aplicación
Paleta de colores J&M: Naranja #FF6B35, Gris Oscuro #2C2C2C, Marrón #8B4513
"""

# Estilos para labels y texto
LABEL_STYLE = """
    QLabel {
        background-color: transparent;
        color: black;
    }
"""

LABEL_INFO_STYLE = """
    QLabel {
        background-color: transparent;
        color: #666; 
        font-style: italic;
    }
"""

LABEL_BOLD_STYLE = """
    QLabel {
        background-color: transparent;
        color: #666; 
        font-weight: bold;
    }
"""

# Estilos para campos de entrada con placeholders negros
INPUT_STYLE = """
    QLineEdit, QTextEdit {
        border: 2px solid #bdc3c7;
        border-radius: 6px;
        padding: 8px;
        font-size: 14px;
        background-color: white;
        color: black;
    }
    QLineEdit:focus, QTextEdit:focus {
        border-color: #FF6B35;
    }
    QLineEdit::placeholder, QTextEdit::placeholder {
        color: black;
        font-style: normal;
    }
"""

SPINBOX_STYLE = """
    QSpinBox, QDoubleSpinBox {
        border: 2px solid #bdc3c7;
        border-radius: 6px;
        padding: 8px;
        font-size: 14px;
        background-color: white;
        color: black;
    }
    QSpinBox:focus, QDoubleSpinBox:focus {
        border-color: #FF6B35;
    }
"""

COMBO_STYLE = """
    QComboBox {
        border: 2px solid #bdc3c7;
        border-radius: 6px;
        padding: 8px;
        font-size: 14px;
        background-color: white;
        color: black;
    }
    QComboBox:focus {
        border-color: #FF6B35;
    }
    QComboBox::drop-down {
        border: none;
        width: 20px;
        background-color: white;
    }
    QComboBox::down-arrow {
        image: none;
        border: 2px solid black;
        width: 6px;
        height: 6px;
        border-top: none;
        border-right: none;
        margin-right: 8px;
    }
    QComboBox QAbstractItemView {
        background-color: white;
        color: black;
        border: 2px solid #bdc3c7;
        border-radius: 6px;
        selection-background-color: #FF6B35;
        selection-color: white;
        outline: none;
    }
    QComboBox QAbstractItemView::item {
        padding: 8px;
        border: none;
        background-color: white;
        color: black;
    }
    QComboBox QAbstractItemView::item:selected {
        background-color: #FF6B35;
        color: white;
    }
    QComboBox QAbstractItemView::item:hover {
        background-color: #FFA07A;
        color: black;
    }
"""

DATE_STYLE = """
    QDateEdit {
        border: 2px solid #bdc3c7;
        border-radius: 6px;
        padding: 8px;
        font-size: 14px;
        background-color: white;
        color: black;
    }
    QDateEdit:focus {
        border-color: #FF6B35;
    }
    QDateEdit::drop-down {
        border: none;
        width: 20px;
        background-color: white;
    }
    QDateEdit::down-arrow {
        image: none;
        border: 2px solid black;
        width: 6px;
        height: 6px;
        border-top: none;
        border-right: none;
        margin-right: 8px;
    }
    /* Calendario principal */
    QCalendarWidget {
        background-color: white;
        border: 2px solid #FF6B35;
        border-radius: 12px;
        font-family: 'Segoe UI', Arial, sans-serif;
        min-width: 350px;
        min-height: 280px;
    }
    
    /* Encabezado del calendario */
    QCalendarWidget QWidget#qt_calendar_navigationbar {
        background-color: #FF6B35;
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
        border-bottom: 2px solid #e55a2b;
        min-height: 50px;
    }
    
    /* Botones de navegación */
    QCalendarWidget QToolButton {
        background-color: transparent;
        color: white;
        border: none;
        font-size: 18px;
        font-weight: bold;
        padding: 8px;
        border-radius: 6px;
        min-width: 40px;
        min-height: 35px;
    }
    QCalendarWidget QToolButton:hover {
        background-color: rgba(255, 255, 255, 0.2);
        border-radius: 6px;
    }
    QCalendarWidget QToolButton:pressed {
        background-color: rgba(255, 255, 255, 0.3);
    }
    
    /* Selector de mes y año */
    QCalendarWidget QMenu {
        background-color: white;
        color: #2C2C2C;
        border: 2px solid #FF6B35;
        border-radius: 8px;
        padding: 5px;
        font-size: 14px;
    }
    QCalendarWidget QMenu::item {
        padding: 8px 12px;
        border-radius: 4px;
    }
    QCalendarWidget QMenu::item:selected {
        background-color: #FF6B35;
        color: white;
    }
    
    QCalendarWidget QSpinBox {
        background-color: transparent;
        color: white;
        border: none;
        font-size: 16px;
        font-weight: bold;
        min-width: 80px;
        padding: 5px;
    }
    QCalendarWidget QSpinBox::up-button,
    QCalendarWidget QSpinBox::down-button {
        background-color: transparent;
        border: none;
    }
    
    /* Encabezados de días de la semana */
    QCalendarWidget QHeaderView::section {
        background-color: #2C2C2C;
        color: white;
        border: none;
        font-weight: bold;
        font-size: 13px;
        padding: 8px;
        text-align: center;
    }
    
    /* Tabla de días */
    QCalendarWidget QTableView {
        background-color: white;
        color: #2C2C2C;
        border: none;
        gridline-color: #f0f0f0;
        selection-background-color: #FF6B35;
        selection-color: white;
        font-size: 14px;
        font-weight: 500;
    }
    
    /* Celdas de días */
    QCalendarWidget QAbstractItemView:enabled {
        background-color: white;
        color: #2C2C2C;
    }
    
    /* Día seleccionado */
    QCalendarWidget QAbstractItemView:selected {
        background-color: #FF6B35;
        color: white;
        border-radius: 6px;
        font-weight: bold;
    }
    
    /* Día actual */
    QCalendarWidget QTableView::item:focus {
        background-color: #8B4513;
        color: white;
        border: 2px solid #FF6B35;
        border-radius: 6px;
        font-weight: bold;
    }
    
    /* Días de otros meses */
    QCalendarWidget QTableView::item:disabled {
        color: #bdc3c7;
    }
    
    /* Hover en días */
    QCalendarWidget QTableView::item:hover {
        background-color: #FFA07A;
        border-radius: 6px;
        color: #2C2C2C;
    }
"""

# Estilos para botones - colores sólidos sin hover
BUTTON_PRIMARY_STYLE = """
    QPushButton {
        background-color: #FF6B35;
        color: white;
        border: none;
        padding: 12px 20px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: bold;
        min-width: 150px;
    }
"""

BUTTON_SECONDARY_STYLE = """
    QPushButton {
        background-color: #2C2C2C;
        color: white;
        border: none;
        padding: 12px 20px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: bold;
        min-width: 150px;
    }
"""

BUTTON_TERTIARY_STYLE = """
    QPushButton {
        background-color: #8B4513;
        color: white;
        border: none;
        padding: 12px 20px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: bold;
        min-width: 150px;
    }
"""

# Estilos para grupos y frames
GROUP_STYLE = """
    QGroupBox {
        font-weight: bold;
        border: 2px solid #bdc3c7;
        border-radius: 8px;
        margin-top: 10px;
        padding-top: 15px;
        background-color: white;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px;
        color: #2C2C2C;
    }
"""

# Estilos para tablas
TABLE_STYLE = """
    QTableWidget {
        background-color: white;
        border: 2px solid #bdc3c7;
        border-radius: 8px;
        gridline-color: #ecf0f1;
        font-size: 12px;
    }
    QTableWidget::item {
        padding: 8px;
        border: none;
    }
    QTableWidget::item:selected {
        background-color: #FF6B35;
        color: white;
    }
    QHeaderView::section {
        background-color: #2C2C2C;
        color: white;
        padding: 10px;
        border: none;
        font-weight: bold;
    }
"""