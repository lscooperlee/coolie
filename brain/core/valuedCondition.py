
from threading import Condition

class ValuedCondition(object):

    def __init__(self):
        self.condition = Condition()
        self.value = None
        self.hasValue = False

    def put(self, value):
        with self.condition:
            self.value = value
            self.hasValue = True
            self.condition.notify()

    def peek(self):
        return self.value

    def get(self):
        with self.condition:
            while not self.hasValue:
                self.condition.wait()
            self.hasValue = False
            return self.value
