

class CreditCardPayment(IPaymentStrategy):
    def __init__(self, card_number: str, card_holder: str, cvv: str, expiry_date: str):
        self.card_number = card_number
        self.card_holder = card_holder
        self.cvv = cvv
        self.expiry_date = expiry_date
    
    def pay(self, amount: float) -> bool:
        print(f"Processing credit card payment of ${amount:.2f} for card holder {self.card_holder}.")
        # Here, you would integrate with a real payment gateway
        print("Payment successful.")
        return True
    