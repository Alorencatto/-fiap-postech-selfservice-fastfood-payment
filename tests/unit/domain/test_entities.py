import unittest

import pydantic_core

from src.core.domain.entities.payment import PaymentEntity
# from domain.entities.payment import PaymentEntity


class TestPayment(unittest.TestCase):

    def testShouldCheckInvalidPaymentEnum(self):
        with self.assertRaises(pydantic_core._pydantic_core.ValidationError):
            PaymentEntity(
                order_id=1,
                user_id=1,
                amount=0.99,
                provider="visa",
                status="CAPTUREDE"
            )

    def testShouldCheckValidPaymentEnum(self):
        PaymentEntity(
            order_id=1,
            user_id=1,
            amount=0.99,
            provider="visa",
            status="CAPTURED"
        )
