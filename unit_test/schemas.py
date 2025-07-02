import unittest
from unittest.mock import MagicMock
from pydantic import ValidationError
from your_module import OrderBase, ProductBase, ProductCreate, Product

class TestOrderBase(unittest.TestCase):

    def test_valid_order(self):
        order = OrderBase(
            product_id=1,
            quantity=2,
            customer_name="John Doe",
            customer_email="john@example.com",
            shipping_address="123 Main St"
        )
        self.assertEqual(order.product_id, 1)
        self.assertEqual(order.quantity, 2)
        self.assertEqual(order.customer_name, "John Doe")
        self.assertEqual(order.customer_email, "john@example.com")
        self.assertEqual(order.shipping_address, "123 Main St")

    def test_invalid_product_id(self):
        with self.assertRaises(ValidationError):
            OrderBase(
                product_id="a",
                quantity=2,
                customer_name="John Doe",
                customer_email="john@example.com",
                shipping_address="123 Main St"
            )

    def test_invalid_quantity(self):
        with self.assertRaises(ValidationError):
            OrderBase(
                product_id=1,
                quantity="a",
                customer_name="John Doe",
                customer_email="john@example.com",
                shipping_address="123 Main St"
            )

    def test_invalid_customer_name(self):
        with self.assertRaises(ValidationError):
            OrderBase(
                product_id=1,
                quantity=2,
                customer_name=123,
                customer_email="john@example.com",
                shipping_address="123 Main St"
            )

    def test_invalid_customer_email(self):
        with self.assertRaises(ValidationError):
            OrderBase(
                product_id=1,
                quantity=2,
                customer_name="John Doe",
                customer_email=123,
                shipping_address="123 Main St"
            )

    def test_invalid_shipping_address(self):
        with self.assertRaises(ValidationError):
            OrderBase(
                product_id=1,
                quantity=2,
                customer_name="John Doe",
                customer_email="john@example.com",
                shipping_address=123
            )


class TestProductBase(unittest.TestCase):

    def test_valid_product(self):
        product = ProductBase(
            name="Product 1",
            price=10.99,
            image_url="https://example.com/image1.jpg"
        )
        self.assertEqual(product.name, "Product 1")
        self.assertEqual(product.price, 10.99)
        self.assertEqual(product.image_url, "https://example.com/image1.jpg")

    def test_product_with_description(self):
        product = ProductBase(
            name="Product 1",
            description="This is product 1",
            price=10.99,
            image_url="https://example.com/image1.jpg"
        )
        self.assertEqual(product.name, "Product 1")
        self.assertEqual(product.description, "This is product 1")
        self.assertEqual(product.price, 10.99)
        self.assertEqual(product.image_url, "https://example.com/image1.jpg")

    def test_product_without_description(self):
        product = ProductBase(
            name="Product 1",
            price=10.99,
            image_url="https://example.com/image1.jpg"
        )
        self.assertEqual(product.name, "Product 1")
        self.assertIsNone(product.description)
        self.assertEqual(product.price, 10.99)
        self.assertEqual(product.image_url, "https://example.com/image1.jpg")

    def test_invalid_name(self):
        with self.assertRaises(ValidationError):
            ProductBase(
                name=123,
                price=10.99,
                image_url="https://example.com/image1.jpg"
            )

    def test_invalid_price(self):
        with self.assertRaises(ValidationError):
            ProductBase(
                name="Product 1",
                price="a",
                image_url="https://example.com/image1.jpg"
            )

    def test_invalid_image_url(self):
        with self.assertRaises(ValidationError):
            ProductBase(
                name="Product 1",
                price=10.99,
                image_url=123
            )


class TestProductCreate(unittest.TestCase):

    def test_valid_product_create(self):
        product_create = ProductCreate(
            name="Product 1",
            price=10.99,
            image_url="https://example.com/image1.jpg"
        )
        self.assertEqual(product_create.name, "Product 1")
        self.assertEqual(product_create.price, 10.99)
        self.assertEqual(product_create.image_url, "https://example.com/image1.jpg")

    def test_product_create_with_description(self):
        product_create = ProductCreate(
            name="Product 1",
            description="This is product 1",
            price=10.99,
            image_url="https://example.com/image1.jpg"
        )
        self.assertEqual(product_create.name, "Product 1")
        self.assertEqual(product_create.description, "This is product 1")
        self.assertEqual(product_create.price, 10.99)
        self.assertEqual(product_create.image_url, "https://example.com/image1.jpg")


class TestProduct(unittest.TestCase):

    def test_valid_product(self):
        product = Product(
            id=1,
            name="Product 1",
            price=10.99,
            image_url="https://example.com/image1.jpg"
        )
        self.assertEqual(product.id, 1)
        self.assertEqual(product.name, "Product 1")
        self.assertEqual(product.price, 10.99)
        self.assertEqual(product.image_url, "https://example.com/image1.jpg")

    def test_product_with_description(self):
        product = Product(
            id=1,
            name="Product 1",
            description="This is product 1",
            price=10.99,
            image_url="https://example.com/image1.jpg"
        )
        self.assertEqual(product.id, 1)
        self.assertEqual(product.name, "Product 1")
        self.assertEqual(product.description, "This is product 1")
        self.assertEqual(product.price, 10.99)
        self.assertEqual(product.image_url, "https://example.com/image1.jpg")

    def test_invalid_id(self):
        with self.assertRaises(ValidationError):
            Product(
                id="a",
                name="Product 1",
                price=10.99,
                image_url="https://example.com/image1.jpg"
            )

if __name__ == '__main__':
    unittest.main()