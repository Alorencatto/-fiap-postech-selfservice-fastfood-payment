import os
import httpx


BASE_URL = "http://127.0.0.1:8000"




def before_all(context):

    base_url : str = os.getenv("BASE_URL", "http://127.0.0.1:8000")

    context.base_url = base_url
    context.order_id = 123
    context.status = "PENDING"
    # context.payment_id = None

# def before_scenario(context, scenario):
#     if context.order_id:
#         clean_payment_by_order_id(context, context.order_id)
#     # context.order_id = None  # Reset the SKU before each scenario
#
#
# def after_scenario(context, scenario):
#     if context.order_id:
#         clean_payment_by_order_id(context, context.order_id)