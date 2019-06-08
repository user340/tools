#!/usr/bin/env python

import unittest
from lib import speed_wifi_home
from typing import Any


class TestSpeedWifiHome(unittest.TestCase):
    def setUp(self):
        self.user = speed_wifi_home.SpeedWifiHome()
        self.conf = 'conf/speed_wifi_home.conf'

    def tearDown(self):
        self.user.browser.quit()

    def login(self) -> None:
        pass

    def __check_type(self, method: Any) -> None:
        testcases = [0, 0.123, True, None, [1, 2], {1, 2}, {'test': 'x'}]
        for testcase in testcases:
            self.assertRaises(TypeError, method, testcase)

    def test_webdriver(self) -> None:
        self.__check_type(speed_wifi_home.SpeedWifiHome)
        self.assertRaises(
            FileNotFoundError,
            speed_wifi_home.SpeedWifiHome,
            driver='x'
        )

    def test_parse_conf(self) -> None:
        self.__check_type(self.user.parse_conf)
        self.assertRaises(FileNotFoundError, self.user.parse_conf, 'jjklla')
        addr, user, passwd = self.user.parse_conf(self.conf)
        for i in addr, user, passwd:
            self.assertIsInstance(i, str)

    def test_login(self) -> None:
        testcases = [0, 0.123, True, None, [1, 2], {1, 2}, {'test': 'x'}]
        for i in testcases:
            for j in testcases:
                self.assertRaises(TypeError, self.user.login, i, j)
        addr, user, passwd = self.user.parse_conf(self.conf)
        self.user.login(addr, user, passwd)
        # print(self.user.browser.title)

    def test_get_traffic_of_last_three_days(self) -> None:
        self.test_login()
        ret = self.user.get_traffic_of_last_three_days()
        self.assertIsInstance(ret, str)
        print(ret)
