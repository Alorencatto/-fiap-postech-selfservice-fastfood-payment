import unittest

from pydantic import ValidationError

from src.core.domain.entities.product import ProductEntity

class TestProduct(unittest.TestCase):

    def testShouldReturnProductWithSucess(self):
        product = ProductEntity(
            name="test product",
            category="test category"
        )
        
        self.assertEqual(product.name,"test product")

    def testShouldRaiseExceptionOnProductCreationWhithoutCategory(self):
        with self.assertRaises(ValidationError):

            product = ProductEntity(
                name="test product"
            )
            self.assertEqual(product.name, "test product")
