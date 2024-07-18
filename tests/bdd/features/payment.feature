Feature: Payment Management
    As a user
    I want to manage payments
    So that I can create, retrieve, update, and delete payments

Scenario: Create a payment
    Given a new payment with order_id 123
    When the payment is created
    Then the payment with order_id "123" should be retrievable

Scenario: Update order status to CAPTURED
    Given a payment with order_id 123
    When the payment is paid
    Then the payment with order_id "123" should have status == 'CAPTURED'