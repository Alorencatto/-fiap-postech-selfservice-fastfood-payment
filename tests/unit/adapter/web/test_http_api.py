from unittest import TestCase
from unittest.mock import Mock
from fastapi import HTTPException

from src.common.dto.payment_dto import CreatePaymentDTO, PaymentDTO, UpdatePaymentDTO, WebhookDTO
from src.communication.controller.payment import PaymentController
from src.core.domain.entities.payment import PaymentEntity
from src.core.domain.exceptions import EntityAlreadyExistsError
from src.external.web.fastapi.api_v2.endpoints.payment import HTTPAPIAdapter


class TestHTTPAPIAdapter(TestCase):

    def setUp(self) -> None:
        # Arrange
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

        self.mock_create_payment_DTO = CreatePaymentDTO(
            order_id=self.order_id,
            amount=self.amount,
            provider=self.provider,
            status="PENDING"
        )

        self.mock_update_payment_DTO = UpdatePaymentDTO(
            order_id=self.order_id,
            user_id=self.user_id,
            qr_data=self.qr_data,
            amount=self.amount,
            provider=self.provider,
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

        self.mock_webhook_DTO = WebhookDTO(
            order_id = self.order_id,
            payment_status="CAPTURED"
        )

        self.payment_controller = Mock(spec=PaymentController)
        self.httpAdapter = HTTPAPIAdapter(payment_controller=self.payment_controller)

    # Create / Update

    def testShouldRaiseExceptionOnPaymentCreation(self):
        # Act
        self.payment_controller.create.side_effect = EntityAlreadyExistsError("Payment already exists")

        # Assert
        with self.assertRaises(EntityAlreadyExistsError):
            self.httpAdapter.create_payment(payment=self.mock_create_payment_DTO)

    def testShouldCreatePaymentWithSuccess(self):
        # Act
        self.payment_controller.create.return_value = self.mock_payment_entity
        response = self.httpAdapter.create_payment(payment=self.mock_create_payment_DTO)

        # Assert
        self.assertEqual(response, self.mock_payment_DTO)

    def testShouldUpdatePaymentWithSuccess(self):
        # Act
        self.payment_controller.update.return_value = self.mock_payment_entity
        response = self.httpAdapter.update_payment(payment_id=self.payment_id, payment=self.mock_update_payment_DTO)

        # Assert
        self.assertEqual(response, self.mock_payment_DTO)

    # Delete

    def testShouldRaiseExceptionOnPaymentDelete(self):
        # Act
        self.payment_controller.get_by_id.return_value = None

        # Assert
        with self.assertRaises(HTTPException) as context:
            self.httpAdapter.delete_payment(payment_id=self.payment_id)

    def testShouldDeletePaymentWithSuccess(self):
        # Act
        self.payment_controller.get_by_id.return_value = self.mock_payment_entity
        response = self.httpAdapter.delete_payment(payment_id=self.payment_id)

        # Assert
        # self.assertEqual(response,True)

    # Webhook
    def testShouldExecuteWebhookMethodWithSuccess(self):
        # Act
        self.payment_controller.get_by_order_id.return_value = self.mock_payment_entity
        self.payment_controller.update.return_value = self.mock_payment_DTO

        response = self.httpAdapter.webhook(webhook_data=self.mock_webhook_DTO)

        # Assert
        self.assertEqual(response,self.mock_payment_DTO)


    # Get

    def testShouldGetPaymentByIdWithSuccess(self):
        # Act
        self.payment_controller.get_by_id.return_value = self.mock_payment_entity
        response = self.httpAdapter.get_payment_by_id(payment_id=self.payment_id)

        # Assert
        self.assertEqual(response, self.mock_payment_DTO)

    def testShouldRaiseNotFoundExceptionOnPaymentQueryById(self):
        # Act
        self.payment_controller.get_by_id.return_value = None

        # Assert
        with self.assertRaises(HTTPException) as context:
            self.httpAdapter.get_payment_by_id(payment_id=self.payment_id)

    def testShouldGetPaymentByOrderIdWithSuccess(self):
        # Act
        self.payment_controller.get_by_order_id.return_value = self.mock_payment_entity
        response = self.httpAdapter.get_payment_by_order_id(order_id=self.order_id)

        # Assert
        self.assertEqual(response, self.mock_payment_DTO)

    def testShouldRaiseNotFoundExceptionOnPaymentQueryByOrderId(self):
        # Act
        self.payment_controller.get_by_order_id.return_value = None

        # Assert
        with self.assertRaises(HTTPException) as context:
            self.httpAdapter.get_payment_by_order_id(order_id=self.order_id)
