import os

import httpx
from typing import Optional


class KitchenHTTPClient:

    def __int__(
            self
    ):
        self.url = os.getenv("ORDER_SERVICE_URL")

    @staticmethod
    def update_order_status(self, order_id: int, payment_status: str):

        payload : dict = {
            order_id : order_id,
            payment_status : True if payment_status == "CAPTURED" else False
        }

        response = httpx.put(
            url=self.url,
            json=payload,
            timeout=30
        )

        if response.status_code != 200:
            raise Exception("Can't update order status")
