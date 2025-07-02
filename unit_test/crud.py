import unittest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from your_module import get_product, get_products, create_product, create_order, get_orders
import models, schemas

class TestProductFunctions(unittest.TestCase):

    @patch.object(Session, 'query')
    def test_get_product_found(self, mock_query):
        mock_session = Mock(spec=Session)
        mock_query.return_value.filter.return_value.first.return_value = models.Product(id=1, name='Test Product')
        result = get_product(mock_session, 1)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.name, 'Test Product')

    @patch.object(Session, 'query')
    def test_get_product_not_found(self, mock_query):
        mock_session = Mock(spec=Session)
        mock_query.return_value.filter.return_value.first.return_value = None
        result = get_product(mock_session, 1)
        self.assertIsNone(result)

    @patch.object(Session, 'query')
    def test_get_products(self, mock_query):
        mock_session = Mock(spec=Session)
        mock_query.return_value.offset.return_value.limit.return_value.all.return_value = [models.Product(id=1, name='Test Product 1'), models.Product(id=2, name='Test Product 2')]
        result = get_products(mock_session)
        self.assertEqual(len(result), 2)

    @patch.object(Session, 'add')
    @patch.object(Session, 'commit')
    @patch.object(Session, 'refresh')
    def test_create_product(self, mock_refresh, mock_commit, mock_add):
        mock_session = Mock(spec=Session)
        mock_add.return_value = None
        mock_commit.return_value = None
        mock_refresh.return_value = None
        product = schemas.ProductCreate(name='Test Product', description='Test Description', price=10.99, image_url='test_url')
        result = create_product(mock_session, product)
        self.assertIsNotNone(result)
        self.assertEqual(result.name, product.name)

    @patch.object(Session, 'add')
    @patch.object(Session, 'commit')
    def test_create_product_failure(self, mock_commit, mock_add):
        mock_session = Mock(spec=Session)
        mock_add.return_value = None
        mock_commit.side_effect = Exception('Test Exception')
        product = schemas.ProductCreate(name='Test Product', description='Test Description', price=10.99, image_url='test_url')
        with self.assertRaises(Exception):
            create_product(mock_session, product)

class TestOrderFunctions(unittest.TestCase):

    @patch.object(Session, 'add')
    @patch.object(Session, 'commit')
    @patch.object(Session, 'refresh')
    def test_create_order(self, mock_refresh, mock_commit, mock_add):
        mock_session = Mock(spec=Session)
        mock_add.return_value = None
        mock_commit.return_value = None
        mock_refresh.return_value = None
        order = schemas.OrderCreate(product_id=1, quantity=2, customer_name='Test Customer', customer_email='test@example.com', shipping_address='Test Address')
        result = create_order(mock_session, order)
        self.assertIsNotNone(result)
        self.assertEqual(result.product_id, order.product_id)

    @patch.object(Session, 'add')
    @patch.object(Session, 'commit')
    def test_create_order_failure(self, mock_commit, mock_add):
        mock_session = Mock(spec=Session)
        mock_add.return_value = None
        mock_commit.side_effect = Exception('Test Exception')
        order = schemas.OrderCreate(product_id=1, quantity=2, customer_name='Test Customer', customer_email='test@example.com', shipping_address='Test Address')
        with self.assertRaises(Exception):
            create_order(mock_session, order)

    @patch.object(Session, 'query')
    def test_get_orders(self, mock_query):
        mock_session = Mock(spec=Session)
        mock_query.return_value.offset.return_value.limit.return_value.all.return_value = [models.Order(id=1, product_id=1), models.Order(id=2, product_id=2)]
        result = get_orders(mock_session)
        self.assertEqual(len(result), 2)

if __name__ == '__main__':
    unittest.main()