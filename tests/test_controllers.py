from PyQt6.QtWidgets import QApplication
import unittest
from src.controllers.inventory_controller import InventoryController
from src.models.inventory_item import InventoryItem

class TestInventoryController(unittest.TestCase):
    def setUp(self):
        self.controller = InventoryController()
        self.test_item = InventoryItem(name="Test Item", quantity=10, location="Warehouse")

    def test_add_item(self):
        self.controller.add_item(self.test_item)
        self.assertIn(self.test_item, self.controller.get_all_items())

    def test_remove_item(self):
        self.controller.add_item(self.test_item)
        self.controller.remove_item(self.test_item)
        self.assertNotIn(self.test_item, self.controller.get_all_items())

    def test_update_item(self):
        self.controller.add_item(self.test_item)
        self.test_item.quantity = 20
        self.controller.update_item(self.test_item)
        updated_item = self.controller.get_item(self.test_item.name)
        self.assertEqual(updated_item.quantity, 20)

if __name__ == '__main__':
    unittest.main()