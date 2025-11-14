import threading
import time
from server import RemoteServer
from calculator import Calculator
from client import RemoteProxy

def start_server():
    srv = RemoteServer()
    srv.register("calc", Calculator())
    srv.start()
    return srv

if __name__ == "__main__":
    server = start_server()
    time.sleep(0.3)  # allow server to start

    calc = RemoteProxy("calc")
    print("Add 5 + 7 =>", calc.add(5, 7))
    print("Subtract 10 - 3 =>", calc.subtract(10, 3))
    print("Multiply 4 * 6 =>", calc.multiply(4, 6))
    try:
        print("Divide 8 / 0 =>", calc.divide(8, 0))
    except RuntimeError as e:
        print("Division error (expected):", e)

    print("Divide 8 / 2 =>", calc.divide(8, 2))

    # Keep server a moment so user can manually test
    time.sleep(1)
