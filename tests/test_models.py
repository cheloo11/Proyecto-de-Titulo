import unittest
from src.models.inventory_item import InventoryItem
from src.models.material import Material
from src.models.equipment import Equipment
from src.models.supplier import Supplier
from src.models.project import Project

class TestInventoryModels(unittest.TestCase):

    def test_inventory_item_creation(self):
        item = InventoryItem(name="Cement", quantity=100, location="Warehouse A")
        self.assertEqual(item.name, "Cement")
        self.assertEqual(item.quantity, 100)
        self.assertEqual(item.location, "Warehouse A")

    def test_material_creation(self):
        material = Material(name="Steel", quantity=50)
        self.assertEqual(material.name, "Steel")
        self.assertEqual(material.quantity, 50)

    def test_equipment_creation(self):
        equipment = Equipment(name="Excavator", quantity=2)
        self.assertEqual(equipment.name, "Excavator")
        self.assertEqual(equipment.quantity, 2)

    def test_supplier_creation(self):
        supplier = Supplier(name="ABC Supplies", contact="123-456-7890")
        self.assertEqual(supplier.name, "ABC Supplies")
        self.assertEqual(supplier.contact, "123-456-7890")

    def test_project_creation(self):
        project = Project(name="Building A", budget=1000000)
        self.assertEqual(project.name, "Building A")
        self.assertEqual(project.budget, 1000000)

if __name__ == '__main__':
    unittest.main()