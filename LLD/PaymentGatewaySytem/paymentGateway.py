import random
import time
from abc import ABC, abstractmethod
from enum import Enum

class PaymentRequest:
    def __init__(self,sender,receiver,amount,currency):
        self.sender=sender
        self.receiver=receiver
        self.amount=amount
        self.currency=currency


# banking System interface and its concrete methods

class BankingSystem(ABC):
    def processPayment(self,amount):
        pass

class PaytmBankingSystem(BankingSystem):
    def processPayment(self,amount):
        r=random.randint(1,100)
        return r<80

class RazorpayBankingSystem(BankingSystem):
    def processPayment(self,amount):
        r=random.randint(1,100)
        return r<50


class RetryStrategy(ABC):
    @abstractmethod
    def retry(self,attempt):
        pass

class LinearRetryStrategy(RetryStrategy):
    def retry(self,attempt):
        delay = attempt       
        print(f"[LinearRetry] retry after {delay}s")
        time.sleep(delay)
        return
class ExponentialRetryStrategy(RetryStrategy):
    def retry(self,attempt):
        delay = 2 ** attempt       
        print(f"[ExponentialRetry] retry after {delay}s")
        time.sleep(delay)
        return
# paymentGateway , (templete design pattern) => validate-initiate-confirm and its
# concrete implementation via proxies

class PaymentGateway(ABC):
    def __init__(self,BankingSystem):
        self._bankingSystem=BankingSystem
    
    @abstractmethod
    def validatePayment(self,request):
        pass
    
    @abstractmethod
    def initiatePayment(self,request):
        pass

    @abstractmethod
    def confirmPayment(self,request):
        pass

    def processPayment(self,request:PaymentRequest):
        if not self.validatePayment(request):
            print(f"[paymentGateway] validation failed for {request.sender}")
            return False
        if not self.initiatePayment(request):
            print(f"[paymentGateway] initailaization failed for {request.sender}")
            return False
        if not self.confirmPayment(request):
            print(f"[paymentGateway] confirmation failed for {request.sender}")
            return False
        return True

class PaytmGateway(PaymentGateway):
    def __init__(self,BankingSystem):
        self._bankingSystem=BankingSystem
    
    def validatePayment(self,request):
        print(f"[Paytm] validating request for {request.sender}")
        if request.amount<=0 or request.currency!='INR':
            return False
        return True

    def initiatePayment(self,request):
        print(f"[Paytm] initiating request for {request.sender}")
        return self._bankingSystem.processPayment(request.amount)

    def confirmPayment(self,request):
        print(f"[Paytm] confirming request for {request.sender} to {request.receiver}")
        return True
    
class RazorpayGateway(PaymentGateway):
    def __init__(self,BankingSystem):
        self._bankingSystem=BankingSystem
    
    def validatePayment(self,request):
        print(f"[Razorpay] validating request for {request.sender}")
        if request.amount<=0:
            return False
        return True

    def initiatePayment(self,request):
        print(f"[Razorpay] initiating request for {request.sender}")
        return self._bankingSystem.processPayment(request.amount)

    def confirmPayment(self,request):
        print(f"[Razorpay] confirming request for {request.sender} to {request.receiver}")
        return True

class paymentGatewayProxy(PaymentGateway):
    def __init__(self,gateway,retries,retryType):
        self._realGateway=gateway
        self._retries=retries
        self._retryType=retryType
    
    def processPayment(self,request):
        res=False
        for attempt in range(self._retries+1):
            if attempt>0:
                self._retryType.retry(attempt)
            res=self._realGateway.processPayment(request)
            if res:
                break
        if not res:
            print(f"[Proxy] payment failed after retrying for {self._retries} times")
        return res
    # keeping other methods for interface completeness
    # we actually dont call these in our function since we are caling directly to the 
    # concrete gateway methods via processPayment
    def validatePayment(self,request):
        return self._realGateway.validatePayment(request)

    def initiatePayment(self,request):
        return self._realGateway.initiatePayment(request)

    def confirmPayment(self,request):
        return self._realGateway.confirmPayment(request)

class GatewayType(Enum):
    PAYTM=1
    RAZORPAY=2

class GatewayFactory:
    _instance=None
    @staticmethod
    def getInstance():
        if GatewayFactory._instance is None:
            GatewayFactory._instance=GatewayFactory()
        return GatewayFactory._instance

    def getGateway(self,gatewayType):
        if gatewayType==gatewayType.PAYTM:
            paytmGateway=PaytmGateway(PaytmBankingSystem())
            return paymentGatewayProxy(paytmGateway,3,LinearRetryStrategy())
        elif gatewayType==gatewayType.RAZORPAY:
            razorpayGateway=RazorpayGateway(RazorpayBankingSystem())
            return paymentGatewayProxy(razorpayGateway,4,ExponentialRetryStrategy())

#api-service    
class PaymentService:
    _instance=None
    def __init__(self):
        self._gateway=None

    @staticmethod
    def getInstance():
        if PaymentService._instance is None:
            PaymentService._instance=PaymentService()
        return PaymentService._instance
    
    def setGateway(self,gateway):
        self._gateway=None
        self._gateway=gateway

    def processPayment(self,request):
        if self._gateway==None:
            print(f"[PaymentService] error , please specify the service you want to use ")
            return False
        return self._gateway.processPayment(request)

class PaymentController:
    _instance=None
    @staticmethod
    def getInstance():
        if PaymentController._instance is None:
            PaymentController._instance=PaymentController()
        return PaymentController._instance
    def handlePayment(self,gatewayType,req):
        paymentGateway=GatewayFactory.getInstance().getGateway(gatewayType)
        PaymentService.getInstance().setGateway(paymentGateway)
        return PaymentService.getInstance().processPayment(req)

# client

if __name__=="__main__":
    req1=PaymentRequest("Suresh","Subham",1000.0,"INR")

    print("\n [client] Processing payment via Paytm \n")
    res1=PaymentController.getInstance().handlePayment(GatewayType.PAYTM,req1)
    if res1:
        print("=== PAYMENT SUCCESSFUL ===")
    else:
        print("=== PAYMENT FAILED === ")
    
    req2=PaymentRequest("Subham","Suresh",40.0,"USD")
    print("\n [client] Processing payment via RazorPay \n")
    res2=PaymentController.getInstance().handlePayment(GatewayType.RAZORPAY,req2)
    if res2:
        print("=== PAYMENT SUCCESSFUL ===")
    else:
        print("=== PAYMENT FAILED === ")
    