# Construction Inventory System

This project is a desktop inventory system designed for a construction company, built using PyQt6. It provides a user-friendly interface for managing various aspects of inventory, including materials, equipment, suppliers, and reports.

## Features

- **Inventory Management**: View and manage all inventory items.
- **Materials Management**: Add, edit, and delete materials in the inventory.
- **Equipment Management**: Manage tools and equipment used in construction projects.
- **Supplier Management**: Keep track of suppliers and their information.
- **Reports Generation**: Generate and view various reports related to inventory and usage.

## Project Structure

```
construction-inventory
├── src
│   ├── main.py                  # Entry point of the application
│   ├── ui                       # UI components
│   │   ├── main_window.py       # Main window interface
│   │   ├── inventory_view.py     # Inventory management view
│   │   ├── materials_view.py      # Materials management view
│   │   ├── equipment_view.py      # Equipment management view
│   │   ├── suppliers_view.py      # Suppliers management view
│   │   ├── reports_view.py        # Reports generation view
│   │   └── dialogs               # Dialogs for adding/editing items
│   ├── models                    # Data models
│   ├── controllers               # Controllers for managing logic
│   ├── database                  # Database management
│   └── utils                     # Utility functions
├── resources                     # Resources like styles
│   └── styles
│       └── main_style.qss       # Stylesheet for the application
├── tests                         # Unit tests
├── requirements.txt              # Project dependencies
└── README.md                     # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd construction-inventory
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/main.py
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for details.