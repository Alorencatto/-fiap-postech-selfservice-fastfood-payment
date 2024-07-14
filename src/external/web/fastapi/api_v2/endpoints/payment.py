from typing import List

from fastapi import APIRouter, HTTPException

from src.common.dto.payment_dto import (
    CreatePaymentDTO,
    PaymentDTO,
    UpdatePaymentDTO,
    WebhookDTO,
)
from src.communication.controller.payment import PaymentController
from src.external.web.http.kitchen_client import KitchenHTTPClient

# Postgresql
# from src.external.database.sqlalchemy.repositories.payment import PaymentRepository

# MongoDB
from src.external.database.mongo.repositories.payment import PaymentRepository

payment_repository = PaymentRepository()
payment_controller = PaymentController(payment_repository)

router = APIRouter(prefix="/payments", tags=["payments"])


class HTTPAPIAdapter:

    def __init__(self, payment_controller: PaymentController) -> None:
        self.__payment_controller = payment_controller

        self.router = APIRouter()

        self.router.add_api_route("/{payment_id}", self.get_payment_by_id, methods=["GET"])
        self.router.add_api_route("/order/{order_id}", self.get_payment_by_order_id, methods=["GET"])

        self.router.add_api_route("/", self.create_payment, methods=["POST"])
        self.router.add_api_route("/webhook", self.webhook, methods=["POST"])

        self.router.add_api_route("/{payment_id}", self.update_payment, methods=["PUT"])

        self.router.add_api_route("/{payment_id}", self.delete_payment, methods=["DELETE"])

    def get_payment_by_id(self, payment_id: str) -> PaymentDTO:
        payment = self.__payment_controller.get_by_id(payment_id=payment_id)
        if payment is None:
            raise HTTPException(status_code=404, detail="Payment not found")
        return PaymentDTO(
            id=payment.id,
            user_id=payment.user_id,
            order_id=payment.order_id,
            amount=payment.amount,
            provider=payment.provider,
            qr_data=payment.qr_data,
            status=payment.status,
        )

    def get_payment_by_order_id(self, order_id: int) -> PaymentDTO:
        payment = self.__payment_controller.get_by_order_id(order_id=order_id)
        if payment is None:
            raise HTTPException(status_code=404, detail="Payment not found")
        return PaymentDTO(
            id=payment.id,
            user_id=payment.user_id,
            order_id=payment.order_id,
            amount=payment.amount,
            provider=payment.provider,
            qr_data=payment.qr_data,
            status=payment.status,
        )

    def create_payment(self, payment: CreatePaymentDTO) -> PaymentDTO:
        new_payment = self.__payment_controller.create(payment=payment)
        return PaymentDTO(
            id=new_payment.id,
            order_id=new_payment.order_id,
            user_id=new_payment.user_id,
            amount=new_payment.amount,
            provider=new_payment.provider,
            qr_data=new_payment.qr_data,
            status=new_payment.status,
        )

    def update_payment(self, payment_id: str, payment: UpdatePaymentDTO) -> PaymentDTO:

        payment = self.__payment_controller.update(
            payment_id=payment_id, updated_payment=payment
        )

        return PaymentDTO(
            id=payment.id,
            order_id=payment.order_id,
            user_id=payment.user_id,
            amount=payment.amount,
            provider=payment.provider,
            qr_data=payment.qr_data,
            status=payment.status,
        )

    def delete_payment(self, payment_id: str) -> bool:
        if not self.__payment_controller.get_by_id(payment_id):
            raise HTTPException(status_code=404, detail="Payment not found")
        return self.__payment_controller.delete(payment_id=payment_id)

    def webhook(self, webhook_data: WebhookDTO) -> PaymentDTO:
        payment = self.__payment_controller.get_by_order_id(
            order_id=webhook_data.order_id
        )
        if payment is None:
            raise HTTPException(status_code=404, detail="Payment not found")

        updated_payment = UpdatePaymentDTO(
            order_id=payment.order_id,
            user_id=payment.user_id,
            qr_data=payment.qr_data,
            amount=payment.amount,
            provider=payment.provider,
            status=webhook_data.payment_status,
        )
        
        # TODO : Saga? Todos na mesma transação?
        # TODO : Voltar a atualização do pedido
        # self.__payment_controller.update_order(payment.order_id)

        KitchenHTTPClient.update_order_status(order_id=payment.order_id, payment_status=webhook_data.payment_status)


        return self.__payment_controller.update(
            payment_id=payment.id, updated_payment=updated_payment
        )
