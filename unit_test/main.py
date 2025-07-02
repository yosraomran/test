import unittest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import app, get_db, crud, models, schemas
from database import SessionLocal, engine
from pydantic import ValidationError

client = TestClient(app)

class TestApp(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.db = SessionLocal()

    async def asyncTearDown(self):
        self.db.close()

    def test_read_root(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_read_products_page(self):
        response = client.get("/products")
        self.assertEqual(response.status_code, 200)

    def test_read_order_page(self):
        response = client.get("/order")
        self.assertEqual(response.status_code, 200)

    def test_read_contact_page(self):
        response = client.get("/contact")
        self.assertEqual(response.status_code, 200)

    @patch.object(crud, 'create_product')
    def test_create_product(self, mock_create_product):
        product_data = schemas.ProductCreate(name="Test Product", price=10.99)
        mock_create_product.return_value = schemas.Product(id=1, name="Test Product", price=10.99)
        response = client.post("/api/products/", json=product_data.dict())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": 1, "name": "Test Product", "price": 10.99})

    @patch.object(crud, 'get_products')
    def test_read_products(self, mock_get_products):
        mock_get_products.return_value = [schemas.Product(id=1, name="Test Product", price=10.99)]
        response = client.get("/api/products/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{"id": 1, "name": "Test Product", "price": 10.99}])

    @patch.object(crud, 'get_product')
    def test_read_product_found(self, mock_get_product):
        mock_get_product.return_value = schemas.Product(id=1, name="Test Product", price=10.99)
        response = client.get("/api/products/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": 1, "name": "Test Product", "price": 10.99})

    @patch.object(crud, 'get_product')
    def test_read_product_not_found(self, mock_get_product):
        mock_get_product.return_value = None
        response = client.get("/api/products/100")
        self.assertEqual(response.status_code, 404)

    @patch.object(crud, 'create_order')
    @patch.object(crud, 'get_product')
    def test_create_order_product_found(self, mock_get_product, mock_create_order):
        mock_get_product.return_value = schemas.Product(id=1, name="Test Product", price=10.99)
        mock_create_order.return_value = schemas.Order(id=1, product_id=1)
        order_data = schemas.OrderCreate(product_id=1)
        response = client.post("/api/orders/", json=order_data.dict())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": 1, "product_id": 1})

    @patch.object(crud, 'get_product')
    def test_create_order_product_not_found(self, mock_get_product):
        mock_get_product.return_value = None
        order_data = schemas.OrderCreate(product_id=100)
        response = client.post("/api/orders/", json=order_data.dict())
        self.assertEqual(response.status_code, 404)

    @patch.object(crud, 'get_orders')
    def test_read_orders(self, mock_get_orders):
        mock_get_orders.return_value = [schemas.Order(id=1, product_id=1)]
        response = client.get("/api/orders/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{"id": 1, "product_id": 1}])

if __name__ == '__main__':
    unittest.main()