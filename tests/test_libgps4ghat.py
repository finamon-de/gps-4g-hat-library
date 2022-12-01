import unittest
import time

from gps4ghat import BG77X

class Gps4GhatTestCase(unittest.TestCase):

    def setUp(self):
        self.module = BG77X.BG77X(serial_port="COM4")

    def test_AT_OK(self):
        self.module.sendATcmd("AT")
        self.assertEqual(self.module.response, "AT\r\r\nOK\r\n")

    def test_AT_CPIN(self):
        self.module.sendATcmd("AT+CPIN?")
        self.assertEqual(self.module.response, "AT+CPIN?\r\r\n+CPIN: READY\r\n\r\nOK\r\n")

    def tearDown(self):
        self.module.sendATcmd("AT+QPOWD=1")
        time.sleep(2.)

if __name__ == '__main__':
    unittest.main()