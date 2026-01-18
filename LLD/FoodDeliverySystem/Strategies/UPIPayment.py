from Strategies.IPaymentStrategy import IPaymentStrategy
class UPIPayment(IPaymentStrategy):
    def __init__(self, upi_id: str):
        self.upi_id = upi_id
    
    def pay(self, amount: float) -> bool:
        print(f"Processing UPI payment of ${amount:.2f} for UPI ID {self.upi_id}.")
        # Here, you would integrate with a real UPI payment gateway
        print("Payment successful.")
        return True