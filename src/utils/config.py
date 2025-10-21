# Configuration settings for the construction inventory application

class Config:
    DATABASE_PATH = 'path/to/database.db'
    LOGGING_LEVEL = 'DEBUG'
    WINDOW_TITLE = 'Construction Inventory System'
    WINDOW_SIZE = '800x600'
    DEFAULT_LANGUAGE = 'en'
    SUPPORTED_LANGUAGES = ['en', 'es', 'fr']
    ITEMS_PER_PAGE = 20
    AUTO_SAVE_INTERVAL = 300  # in seconds
    THEME = 'light'  # options: 'light', 'dark'