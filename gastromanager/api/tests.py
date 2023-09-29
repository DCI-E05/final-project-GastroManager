from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Address, InventoryItem, StockItemName, StockItem, StaffMember


class AddressModelTest(TestCase):
    def test_address_creation(self):
        address = Address.objects.create(
            line_1="123 Main St",
            city="Anytown",
            state="Anystate",
            postal_code="12345",
            country="Anyland",
        )
        self.assertEqual(address.line_1, "123 Main St")


class InventoryItemModelTest(TestCase):
    def test_inventory_item_creation(self):
        inventory_item = InventoryItem.objects.create(
            name="TestItem",
            quantity=10,
            production_date="2023-01-01",
            expiration_date="2023-12-31",
            comment="Test",
        )
        self.assertEqual(inventory_item.name, "TestItem")
        self.assertEqual(inventory_item.quantity, 10)
        self.assertEqual(inventory_item.production_date, "2023-01-01")
        self.assertEqual(inventory_item.expiration_date, "2023-12-31")
        self.assertEqual(inventory_item.comment, "Test")


class StockItemNameModelTest(TestCase):
    def test_stock_item_name_creation(self):
        stock_item_name = StockItemName.objects.create(item_name="TestStockItemName")
        self.assertEqual(stock_item_name.item_name, "TestStockItemName")


class StockItemModelTest(TestCase):
    def test_stock_item_creation(self):
        stock_item_name = StockItemName.objects.create(item_name="TestStockItemName")
        stock_item = StockItem.objects.create(
            name=stock_item_name,
            size=3,
            quantity=5,
            production_date="2023-01-01",
            expiration_date="2024-01-01",
        )
        self.assertEqual(stock_item.name.item_name, "TestStockItemName")
        self.assertEqual(stock_item.size, 3)
        self.assertEqual(stock_item.quantity, 5)


class StaffMemberModelTest(TestCase):
    def test_staff_member_creation(self):
        address = Address.objects.create(
            line_1="123 Main St",
            city="Anytown",
            state="Anystate",
            postal_code="12345",
            country="Anyland",
        )
        staff_member = StaffMember.objects.create(
            name="John Doe",
            date_of_birth="1990-01-01",
            address=address,
            email="john.doe@example.com",
            phone="123-456-7890",
        )
        self.assertEqual(staff_member.name, "John Doe")
        self.assertEqual(staff_member.email, "john.doe@example.com")


class InventoryViewTest(APITestCase):
    def test_inventory_list(self):
        InventoryItem.objects.create(
            name="TestItem",
            quantity=10,
            production_date="2023-01-01",
            expiration_date="2024-01-01",
        )
        response = self.client.get(reverse("inventory_view"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_inventory_create(self):
        data = {
            "name": "NewItem",
            "quantity": 5,
            "production_date": "2023-01-02",
            "expiration_date": "2023-12-31",
            "comment": "test",
        }
        response = self.client.post(reverse("inventory_view"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InventoryItem.objects.count(), 1)
        self.assertEqual(InventoryItem.objects.get().name, "NewItem")


class StockNameViewTest(APITestCase):
    def test_stock_name_list(self):
        StockItemName.objects.create(item_name="TestStockName")
        response = self.client.get(reverse("stock_name_view"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_stock_name_create(self):
        data = {"item_name": "NewItemName"}
        response = self.client.post(reverse("stock_name_view"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(StockItemName.objects.count(), 1)
        self.assertEqual(StockItemName.objects.get().item_name, "NewItemName")


class StockViewTest(APITestCase):
    def setUp(self):
        self.stock_item_name = StockItemName.objects.create(
            item_name="TestStockItemName"
        )

    def test_stock_list(self):
        StockItem.objects.create(
            name=self.stock_item_name,
            size=3,
            quantity=5,
            production_date="2023-01-01",
            expiration_date="2024-01-01",
        )
        response = self.client.get(reverse("stock_view"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_stock_create(self):
        data = {
            "name": self.stock_item_name.id,
            "size": 3,
            "quantity": 5,
            "production_date": "2023-01-02",
            "expiration_date": "2024-01-02",
            "comment": "test",
        }
        response = self.client.post(reverse("stock_view"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(StockItem.objects.count(), 1)
        self.assertEqual(StockItem.objects.get().name.item_name, "TestStockItemName")


class StaffViewTest(APITestCase):
    def test_staff_list(self):
        address = Address.objects.create(
            line_1="test street 123",
            city="Testcity",
            state="Teststate",
            postal_code="12345",
            country="Testcountry",
        )
        StaffMember.objects.create(
            name="John Doe",
            date_of_birth="1990-01-01",
            email="john.doe@example.com",
            phone="123-456-7890",
            address=address,
        )
        response = self.client.get(reverse("staff_view"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_staff_create(self):
        self.client.force_authenticate(user=None)
        address = Address.objects.create(
            line_1="test street 123",
            city="Testcity",
            state="Teststate",
            postal_code="12345",
            country="Testcountry",
        )
        data = {
            "name": "Jane Doe",
            "date_of_birth": "1991-01-01",
            "address": address.id,
            "email": "jane.doe@example.com",
            "phone": "123-456-7891",
        }
        response = self.client.post(reverse("staff_view"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(StaffMember.objects.count(), 1)
        self.assertEqual(StaffMember.objects.get().name, "Jane Doe")
