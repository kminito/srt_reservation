import unittest
import os
from srt_reservation import main, exceptions, validation

srt_id = os.environ.get('srt_id')
srt_psw = os.environ.get('srt_psw')


class SRTTestCase(unittest.TestCase):
    def setUp(self):
        self.srt = main.SRT("동탄", "동대구", "20220118", "08")

    def test_login(self):
        self.srt.run_driver()
        self.srt.set_log_info(srt_id, srt_psw)
        self.srt.login()
        login_check = self.srt.check_login()

        self.assertTrue(login_check)
