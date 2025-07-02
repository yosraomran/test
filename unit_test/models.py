import unittest
from unittest.mock import patch, Mock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from models import Order, Product

class TestProductModel(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def tearDown(self):
        self.session.close()

    def test_product_init(self):
        product = Product(id=1, name='Test Product', description='Test Description', price=10.99)
        self.session.add(product)
        self.session.commit()
        result = self.session.query(Product).first()
        self.assertEqual(result.name, 'Test Product')

    def test_product_name_index(self):
        product1 = Product(id=1, name='Test Product 1', description='Test Description', price=10.99)
        product2 = Product(id=2, name='Test Product 2', description='Test Description', price=10.99)
        self.session.add(product1)
        self.session.add(product2)
        self.session.commit()
        result = self.session.query(Product).filter_by(name='Test Product 1').first()
        self.assertIsNotNone(result)

    def test_product_price(self):
        product = Product(id=1, name='Test Product', description='Test Description', price=-10.99)
        self.session.add(product)
        with self.assertRaises(ValueError):
            self.session.commit()

    def test_product_name_required(self):
        product = Product(id=1, description='Test Description', price=10.99)
        self.session.add(product)
        with self.assertRaises(ValueError):
            self.session.commit()

    @patch.object(Product, 'name', new_callable=Mock)
    def test_product_name_validation(self, mock_name):
        mock_name.side_effect = ['Test Product', 'Very long product name that should raise an error']
        product = Product(id=1, name=mock_name, description='Test Description', price=10.99)
        self.session.add(product)
        with self.assertRaises(ValueError):
            self.session.commit()

class TestOrderModel(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def tearDown(self):
        self.session.close()

    def test_order_init(self):
        order = Order(id=1)
        self.session.add(order)
        self.session.commit()
        result = self.session.query(Order).first()
        self.assertEqual(result.id, 1)

    def test_order_id_primary_key(self):
        order1 = Order(id=1)
        order2 = Order(id=1)
        self.session.add(order1)
        self.session.add(order2)
        with self.assertRaises(Exception):
            self.session.commit()

if __name__ == '__main__':
    unittest.main()