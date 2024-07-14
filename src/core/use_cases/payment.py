from typing import List
import uuid

from src.common.dto.payment_dto import CreatePaymentDTO, PaymentDTO
from src.common.interfaces.payment_gateway import PaymentGatewayInterface
from src.core.domain.entities.payment import PaymentEntity
from src.core.domain.exceptions import EntityAlreadyExistsError


class PaymentUseCase:

    @staticmethod
    def get_by_id(
        payment_id: str, payment_gateway: PaymentGatewayInterface
    ) -> PaymentEntity:
        return payment_gateway.get_by_id(payment_id=payment_id)

    @staticmethod
    def get_by_order_id(
        order_id: int, payment_gateway: PaymentGatewayInterface
    ) -> PaymentEntity:
        return payment_gateway.get_by_order_id(order_id=order_id)

    @staticmethod
    def create(
        payment: CreatePaymentDTO, payment_gateway: PaymentGatewayInterface
    ):
        if payment_gateway.get_by_order_id(order_id=payment.order_id):
            # raise Exception("Payment already exists") # TODO : Tratar melhor a devolução de resposta
            raise EntityAlreadyExistsError("Payment already exists") # TODO : Tratar melhor a devolução de resposta
        qr_data_response = PaymentUseCase.get_provider_qr_data(payment=payment)

        qr_data = qr_data_response["qr_data"]
        payment.id = str(uuid.uuid4())

        new_payment = PaymentEntity(**payment.model_dump(), qr_data=qr_data)
        return payment_gateway.create(payment=new_payment)

    @staticmethod
    def update(
        payment: PaymentEntity, payment_gateway: PaymentGatewayInterface
    ) -> PaymentEntity:
        return payment_gateway.update(payment=payment)

    @staticmethod
    def delete(
        payment_id: str, payment_gateway: PaymentGatewayInterface
    ) -> bool:
        return payment_gateway.delete(payment_id=payment_id)

    @staticmethod
    def get_provider_qr_data(payment: PaymentDTO):
        # send request to payment provider to get qr data
        return {"qr_data": "mock qr_data"}
