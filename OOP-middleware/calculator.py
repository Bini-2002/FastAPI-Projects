"""Example remote object: Calculator"""
from remote_base import RemoteObject

class Calculator(RemoteObject):
    def add(self, a: float, b: float) -> float:
        return a + b
    def subtract(self, a: float, b: float) -> float:
        return a - b
    def multiply(self, a: float, b: float) -> float:
        return a * b
    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Division by zero")
        return a / b
