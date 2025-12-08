from abc import ABC,abstractmethod


# Notification System
# its an abstract class where the content is created 


class Notification(ABC):
    
    @abstractmethod
    def get_content(self):
        pass

class SimpleNotification(Notification):
    
    def __init__(self,content):
        self._content=content
    
    def get_content(self):
        return self._content

# Decorators used to wake the static content on the top of the current content dynamically on the runtime

class NotificationDecorator(Notification):
    
    def __init__(self,notification):
        self.notification=notification

class TimeStampDecorator(NotificationDecorator):
    
    def get_content(self):
        return "10-10-10"+self.notification.get_content()

class SignatureDecorator(NotificationDecorator):
    
    def __init__(self,sign,notification):
        #super().__init__(notification)
        self._sign=sign
        self._notification=notification
    
    def get_content(self):
        return self._notification.get_content()+self._sign

# observer pattern
class Observer(ABC):
    
    @abstractmethod
    def update(self):
        pass

class Observable(ABC):
    
    @abstractmethod
    def add_observer(self,observer):
        pass
    
    @abstractmethod
    def remove_observer(self,observer):
        pass
    
    @abstractmethod
    def notify_observers(self):
        pass

class NotificationObservable(Observable):
    
    def __init__(self):
        self._observer=[]
        self._currentNotification=None
    
    def add_observer(self,observer):
        self._observer.append(observer)
    
    def remove_observer(self,observer):
        self._observer.remove(observer)
    
    def notify_observers(self):
        for instance in self._observer:
            instance.update()
    
    def set_notification(self,notification:Notification):
        self._currentNotification=notification
        self.notify_observers()
    
    def get_notification(self):
        return self._currentNotification
    
    def get_notification_content(self):
        return self._currentNotification.get_content()

# concrete observers
class Logger(Observer):
    
    def __init__(self,observable):
        self._observable=observable
    
    def update(self):
        print("NEW LOGGER NOTICIATION,",self._observable.get_notification_content())


class NotificationStrategy(ABC):
    
    @abstractmethod
    def send_notification(self,content):
        pass

class EmailStrategy(NotificationStrategy):
    
    def __init__(self,email):
        self._email=email
    
    def send_notification(self,content):
        print(f'Email notification received to {self._email} content : {content}')

class SMSStrategy(NotificationStrategy):
    
    def __init__(self,phoneno):
        self._phoneno=phoneno
    
    def send_notification(self,content):
        print(f'SMS notification send to {self._phoneno} content:{content}')

class PopUpStrategy(NotificationStrategy):
    
    def send_notification(self,content):
        print(f'Content Popped Up : {content}')

# strategy pattern 

class NotificationEngine(Observer):
    
    def __init__(self,observable):
        self._observable=observable
        self._strategies=[]
    
    def add_notification_strategy(self,strategy):
        self._strategies.append(strategy)
    
    def update(self):
        content=self._observable.get_notification_content()
        for strat in self._strategies:
            strat.send_notification(content)

# singleton , one instance all the servers

class NotificationSerice:
    _instance=None
    
    def __init__(self):
        self._observable=NotificationObservable()
        self._dbHistory=[]

    @staticmethod
    def get_instance():
        if NotificationSerice._instance is None:
            NotificationSerice._instance=NotificationSerice()
        return NotificationSerice._instance

    def get_observable(self):
        return self._observable

    def send_notification(self,noticiation:Notification):
        self._observable.set_notification(noticiation)
        self._dbHistory.append(noticiation)


if __name__=="__main__":
    notification_service=NotificationSerice.get_instance()

    observable=notification_service.get_observable()

    logger=Logger(observable)

    engine=NotificationEngine(observable)
    engine.add_notification_strategy(EmailStrategy("abc@gmail.com"))
    engine.add_notification_strategy(SMSStrategy("9876543210"))
    engine.add_notification_strategy(PopUpStrategy())

    observable.add_observer(logger)
    observable.add_observer(engine)

    notif=SimpleNotification("Your Order has been Shipped !!")
    notif=TimeStampDecorator(notif)
    notif=SignatureDecorator("customer-care",notif)
    
    notification_service.send_notification(notif)


    
