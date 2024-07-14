import abc
from typing import List

from src.core.domain.entities.payment import PaymentEntity


class PaymentGatewayInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_by_id(self, payment_id: str) -> PaymentEntity:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_by_order_id(self, order_id: int) -> PaymentEntity:
        raise NotImplementedError()

    @abc.abstractmethod
    def create(self, payment: PaymentEntity) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def delete(self, payment_id: str) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def update(payment: PaymentEntity) -> PaymentEntity:
        raise NotImplementedError()
