import unittest
from server import RemoteServer
from calculator import Calculator
from client import RemoteProxy
import time

class RemoteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = RemoteServer(port=5001)
        cls.server.register("calc", Calculator())
        cls.server.start()
        time.sleep(0.2)
        cls.calc = RemoteProxy("calc", port=5001)

    def test_add(self):
        self.assertEqual(self.calc.add(2,3), 5)

    def test_divide_by_zero(self):
        with self.assertRaises(RuntimeError):
            self.calc.divide(1,0)

if __name__ == '__main__':
    unittest.main()
