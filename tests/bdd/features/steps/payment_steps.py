import httpx

from behave import given, then, when, use_fixture, fixture



@given(u'a new payment with order_id 123')
def given_a_payment_with_order_id(context):
    provider = "Stripe"
    amount = 99.9

    context.payment_data = {
        "user_id": 1,
        "order_id": context.order_id,
        "amount": amount,
        "provider": provider,
        "status": "PENDING"
    }

    @when(u'the payment is created')
    def step_when_create_payment(context):

        r = httpx.post(
            f"{context.base_url}/",
            json=context.payment_data
        )

        # assert r.status_code == 200 or r.status_code == 400

        if r.status_code == 200:
            print("Payment created!")
            payment_id : str = r.json().get("id")
            # TODO Chamar função de recuperar pagamento por id
        elif r.status_code == 400:
            print("Payment already created")
            context.status = "PENDING"

    @then(u'the payment with order_id "123" should be retrievable')
    def step_when_payment_retrieved(context):
        r = httpx.get(
            f"{context.base_url}/order/{context.order_id}",  # TODO
        )

        assert r.status_code == 200
        assert r.json().get("order_id") == 123


@given(u'a payment with order_id 123')
def given_a_payment_with_order_id_123(context):
    context.order_id = 123

    @when(u'the payment is paid')
    def when_the_payment_is_paid(context):
        r = httpx.post(
            f"{context.base_url}/webhook",
            json={
                "order_id": context.order_id,
                "payment_status": "CAPTURED"
            }
        )

        assert r.status_code == 200
        assert r.json().get("status") == "CAPTURED"


    @then(u'the payment with order_id "123" should have status == \'CAPTURED\'')
    def then_the_payment_with_order_id_should_have_captured_status(context):
        r = httpx.get(
            f"{context.base_url}/order/{context.order_id}",  # TODO
        )

        assert r.status_code == 200
        assert r.json().get("order_id") == 123
        assert r.json().get("status") == "CAPTURED"

