from typing import Union

from pydantic import BaseModel

from src.core.domain.enum.payment import PaymentStatusEnum


class CreatePaymentDTO(BaseModel):
    id: Union[int, None] = None
    order_id: Union[int, None] = None
    user_id: Union[int, None] = None
    amount: float
    provider: str
    status: PaymentStatusEnum

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "order_id": 1,
                    "user_id": 1,
                    "amount": 100.0,
                    "provider": "Stripe",
                    "status": "PENDING",
                }
            ]
        }
    }


class UpdatePaymentDTO(BaseModel):
    order_id: Union[int, None] = None
    user_id: Union[int, None] = None
    amount: float
    provider: str
    status: PaymentStatusEnum

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "order_id": 1,
                    "user_id": 1,
                    "amount": 100.0,
                    "provider": "Stripe",
                    "status": "PENDING",
                }
            ]
        }
    }


class PaymentDTO(BaseModel):
    id: int
    order_id: Union[int, None] = None
    user_id: Union[int, None] = None
    amount: float
    provider: str
    status: PaymentStatusEnum

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "order_id": 1,
                    "user_id": 1,
                    "amount": 100.0,
                    "provider": "Stripe",
                    "status": "PENDING",
                }
            ]
        }
    }
