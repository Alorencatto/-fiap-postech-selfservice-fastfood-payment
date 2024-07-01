from typing import List

from src.common.interfaces.payment_repository import PaymentRepositoryInterface
from src.core.domain.entities.payment import PaymentEntity
from src.external.database.sqlalchemy.mappers.payment_mapper import (
    PaymentDetailsMapper,
)
from src.external.database.sqlalchemy.models.payment import PaymentDetailsModel
from src.external.database.sqlalchemy.session_mixin import use_database_session


class PaymentRepository(PaymentRepositoryInterface):

    def get_many_by_user_id(self, user_id: int) -> List[PaymentEntity]:
        with use_database_session() as session:
            payments = (
                session.query(PaymentDetailsModel)
                .filter_by(user_id=user_id)
                .all()
            )
            return (
                [
                    PaymentDetailsMapper.model_to_entity(payment)
                    for payment in payments
                ]
                if payments
                else []
            )

    def get_by_id(self, payment_id: int) -> PaymentEntity:
        with use_database_session() as session:
            payment = (
                session.query(PaymentDetailsModel)
                .filter_by(id=payment_id)
                .first()
            )
            return (
                PaymentDetailsMapper.model_to_entity(payment)
                if payment
                else None
            )

    def get_by_order_id(self, order_id: int) -> PaymentEntity:
        # with use_database_session() as session:
        #     payment = (
        #         session.query(PaymentDetailsModel)
        #         .filter_by(order_id=order_id)
        #         .first()
        #     )
        #     return (
        #         PaymentDetailsMapper.model_to_entity(payment)
        #         if payment
        #         else None
        #     )
        # app.payments.find_one()
        return PaymentEntity()

    def create(self, payment: PaymentEntity) -> PaymentEntity:
        # with use_database_session() as session:
        #     payment_model = PaymentDetailsMapper.entity_to_model(payment)
        #     session.add(payment_model)
        #     session.commit()
        #     session.flush()
        #     return PaymentDetailsMapper.model_to_entity(payment_model)
        return PaymentEntity()

    def update(self, payment: PaymentEntity) -> PaymentEntity:
        with use_database_session() as session:
            payment_model = (
                session.query(PaymentDetailsModel)
                .filter_by(id=payment.id)
                .first()
            )
            if payment_model:
                payment_model.provider = payment.provider
                payment_model.status = payment.status
                payment_model.amount = payment.amount
                session.commit()
            return PaymentDetailsMapper.model_to_entity(payment_model)

    def delete(self, payment_id: int) -> bool:
        with use_database_session() as session:
            payment = (
                session.query(PaymentDetailsModel)
                .filter_by(id=payment_id)
                .first()
            )
            if payment:
                session.delete(payment)
                session.commit()
                return True
            return False
