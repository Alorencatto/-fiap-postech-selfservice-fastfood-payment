from typing import List

from fastapi import APIRouter, HTTPException

from src.common.dto.payment_dto import (
    CreatePaymentDTO,
    PaymentDTO,
    UpdatePaymentDTO,
    WebhookDTO,
)
from src.communication.controller.payment import PaymentController

# Postgresql
# from src.external.database.sqlalchemy.repositories.payment import PaymentRepository

# MongoDB
from src.external.database.mongo.repositories.payment import PaymentRepository

payment_repository = PaymentRepository()
payment_controller = PaymentController(payment_repository)

router = APIRouter(prefix="/payments", tags=["payments"])



@router.get("/{payment_id}", response_model=PaymentDTO)
async def get_payment_by_id(payment_id: int):
    payment = payment_controller.get_by_id(payment_id=payment_id)
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


@router.get("/order/{order_id}", response_model=PaymentDTO)
async def get_payment_by_order_id(order_id: int):
    payment = payment_controller.get_by_order_id(order_id=order_id)
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


@router.post("/", response_model=PaymentDTO)
async def create_payment(payment: CreatePaymentDTO):
    new_payment = payment_controller.create(payment=payment)
    return PaymentDTO(
        id=new_payment.id,
        order_id=new_payment.order_id,
        user_id=new_payment.user_id,
        amount=new_payment.amount,
        provider=new_payment.provider,
        qr_data=new_payment.qr_data,
        status=new_payment.status,
    )


@router.put("/{payment_id}", response_model=PaymentDTO)
async def update_payment(payment_id: int, payment: UpdatePaymentDTO):
    return payment_controller.update(
        payment_id=payment_id, updated_payment=payment
    )


@router.delete("/{payment_id}")
async def delete_payment(payment_id: int):
    if payment_controller.get_by_id(payment_id) is False:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment_controller.delete(payment_id=payment_id)


@router.post("/webhook", response_model=PaymentDTO)
async def webhook(webhook_data: WebhookDTO):
    payment = payment_controller.get_by_order_id(
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
    return payment_controller.update(
        payment_id=payment.id, updated_payment=updated_payment
    )
