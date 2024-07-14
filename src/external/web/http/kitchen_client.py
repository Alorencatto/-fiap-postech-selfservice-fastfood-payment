import os

import httpx
from typing import Optional


class KitchenHTTPClient:

    def __int__(
            self
    ):
        pass


    @staticmethod
    def update_order_status(order_id: int, payment_status: str):
        url = str(os.getenv("ORDER_SERVICE_URL"))

        url : str = "" #TODO

        payload : dict = {
            order_id : order_id,
            payment_status : True if payment_status == "CAPTURED" else False
        }

        response = httpx.put(
            url=url,
            json=payload,
            timeout=30
        )

        if response.status_code != 200:
            raise Exception("Can't update order status")
