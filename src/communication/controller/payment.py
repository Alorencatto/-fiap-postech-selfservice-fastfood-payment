from src.common.dto.payment_dto import CreatePaymentDTO, UpdatePaymentDTO
from src.common.interfaces.payment_repository import PaymentRepositoryInterface
from src.communication.gateway.payment import PaymentGateway
from src.core.domain.entities.payment import PaymentEntity
from src.core.use_cases.payment import PaymentUseCase


class PaymentController:
    def __init__(self, payment_repository: PaymentRepositoryInterface):
        self.payment_repository = payment_repository

    def get_by_id(self, payment_id: str):
        payment_gateway = PaymentGateway(self.payment_repository)
        return PaymentUseCase.get_by_id(
            payment_id=payment_id, payment_gateway=payment_gateway
        )

    def get_by_order_id(self, order_id: int):
        payment_gateway = PaymentGateway(self.payment_repository)
        return PaymentUseCase.get_by_order_id(
            order_id=order_id, payment_gateway=payment_gateway
        )

    def create(self, payment: CreatePaymentDTO):
        payment_gateway = PaymentGateway(self.payment_repository)
        return PaymentUseCase.create(
            payment=payment, payment_gateway=payment_gateway
        )

    def update(self, payment_id: str, updated_payment: UpdatePaymentDTO):
        payment_gateway = PaymentGateway(self.payment_repository)
        payment = PaymentEntity(id=payment_id, **updated_payment.model_dump())
        return PaymentUseCase.update(
            payment=payment,
            payment_gateway=payment_gateway,
        )

    def delete(self, payment_id: str):
        payment_gateway = PaymentGateway(self.payment_repository)
        return PaymentUseCase.delete(
            payment_id=payment_id, payment_gateway=payment_gateway
        )
