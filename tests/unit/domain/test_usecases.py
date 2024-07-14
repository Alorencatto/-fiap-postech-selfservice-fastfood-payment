from unittest import TestCase
from unittest.mock import Mock

from src.common.dto.payment_dto import PaymentDTO
from src.common.interfaces.payment_gateway import PaymentGatewayInterface
from src.core.domain.entities.payment import PaymentEntity
from src.core.use_cases.payment import PaymentUseCase
from src.communication.gateway.payment import PaymentGateway


class TestPaymentUseCase(TestCase):

    def setUp(self) -> None:

        self.payment_id: str = "d41d5943-2877-48b1-ab44-8475b438a07b"
        self.order_id: int = 1
        self.user_id: int = 1
        self.qr_data: str = "mock qr_data"
        self.provider = "Stripe"
        self.amount = 99.9

        self.mock_payment_entity = PaymentEntity(
            id=self.payment_id,
            order_id=self.order_id,
            user_id=self.user_id,
            amount=self.amount,
            provider=self.provider,
            qr_data=self.qr_data,
            status="PENDING"
        )

        self.mock_payment_DTO = PaymentDTO(
            id=self.payment_id,
            order_id=self.order_id,
            user_id=self.user_id,
            amount=self.amount,
            provider=self.provider,
            qr_data=self.qr_data,
            status="PENDING"
        )

        self.payment_gateway_interface = Mock(spec=PaymentGateway)
        self.payment_use_case = PaymentUseCase()


    def testShouldProviderQrDataExecuteWithSucess(self):

        response = self.payment_use_case.get_provider_qr_data(payment=self.mock_payment_DTO)
        
        self.assertEqual(response,{"qr_data": "mock qr_data"})


    def testShouldCreatePaymentWithSuccess(self):

        self.payment_gateway_interface.get_by_order_id.return_value = self.mock_payment_entity
        self.payment_use_case.get_provider_qr_data.return_value = {"qr_data": "mock qr_data"}


