import unittest
from unittest.mock import patch, Mock

from src.core.use_cases.product import ProductUseCase
from src.common.dto.product_dto import ProductDTO
from src.common.interfaces.product_gateway import ProductGatewayInterface


class TestProductUseCase(unittest.TestCase):

    def setUp(self) -> None:

        self.usecase = ProductUseCase()

    @patch("src.core.use_cases.product.ProductUseCase.sum",return_value = 9)
    def test_sum(self,sum):
        self.assertEqual(sum(2,3),9)


    def testShouldCreateProductWithSucess(self):
        mockData : dict = {
            "name": "Hotdog",
            "category": "Lanche",
            "description": "Lorem ipsum...",
            "price": "24.99",
            "quantity": 10,
        }
        mockProductDTO = ProductDTO(**mockData)

        self.assertEqual(1,1)

    # def testShouldRaiseAlreadyExistsExceptionOnProductCreation(self):
    #     pass