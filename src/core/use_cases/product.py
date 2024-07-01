from typing import List

from src.common.dto.product_dto import ProductDTO, ProductResponseDTO
from src.common.interfaces.product_gateway import ProductGatewayInterface
from src.core.domain.entities.product import ProductEntity
from src.core.domain.exceptions import EntityAlreadyExistsError, NotFoundError
from src.external.database.sqlalchemy.mappers.product_mapper import (
    ProductMapper,
)


class ProductUseCase:
    @staticmethod
    def create(
        product: ProductDTO, product_gateway: ProductGatewayInterface
    ) -> ProductEntity:

        existing_product: ProductEntity = product_gateway.get_by_product_name(
            product_name=product.name
        )

        if existing_product:
            raise EntityAlreadyExistsError(
                f"Product with this name ({product.name}) already exists"
            )
        return product_gateway.create(product=product)

    @staticmethod
    def update(
        product: ProductEntity, product_gateway: ProductGatewayInterface
    ) -> ProductEntity:
        existing_product = product_gateway.get_by_id(product.id)

        if not existing_product:
            raise NotFoundError(f"Product with ID {product.id} not found")

        return product_gateway.update(product)

    @staticmethod
    def get_by_id(
        product_id: int, product_gateway: ProductGatewayInterface
    ) -> ProductResponseDTO:
        product = product_gateway.get_by_id(product_id)

        if not product:
            raise NotFoundError(f"Product with ID {product_id} not found")

        return ProductMapper.entity_to_dto(product)

    @staticmethod
    def list_all(
        product_gateway: ProductGatewayInterface,
    ) -> List[ProductResponseDTO]:
        products = product_gateway.list_all()
        product_list = list()

        for product in products:
            product_list.append(
                ProductResponseDTO(
                    id=product.id,
                    name=product.name,
                    description=product.description,
                    price=product.price,
                    category=product.category.name,
                    quantity=product.quantity,
                )
            )
        return product_list

    @staticmethod
    def list_by_category(
        category: str, product_gateway: ProductGatewayInterface
    ) -> List[ProductResponseDTO]:
        products = product_gateway.list_by_category(category)
        product_list = list()

        for product in products:
            product_list.append(ProductMapper.entity_to_dto(product))
        return product_list

    @staticmethod
    def delete(
        product_id: int, product_gateway: ProductGatewayInterface
    ) -> bool:
        return product_gateway.delete(product_id)

    def sum(self,a,b):
        return a + b
