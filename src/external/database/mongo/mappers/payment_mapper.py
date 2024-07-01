from typing import cast

from src.core.domain.entities.payment import PaymentEntity
from src.core.domain.enum.payment import PaymentStatusEnum
from src.external.database.sqlalchemy.models.payment import PaymentDetailsModel


class PaymentDetailsMapper:
    @staticmethod
    def model_to_entity(payment_model: PaymentDetailsModel) -> PaymentEntity:
        return PaymentEntity(
            id=cast(int, payment_model.id),
            order_id=cast(int, payment_model.order_id),
            user_id=cast(int, payment_model.user_id),
            amount=cast(float, payment_model.amount),
            provider=cast(str, payment_model.provider),
            qr_data=cast(str, payment_model.qr_data),
            status=cast(PaymentStatusEnum, payment_model.status),
        )

    @staticmethod
    def entity_to_model(payment_entity: PaymentEntity) -> PaymentDetailsModel:
        return PaymentDetailsModel(
            id=payment_entity.id,
            order_id=payment_entity.order_id,
            user_id=payment_entity.user_id,
            amount=payment_entity.amount,
            provider=payment_entity.provider,
            qr_data=payment_entity.qr_data,
            status=payment_entity.status,
        )
