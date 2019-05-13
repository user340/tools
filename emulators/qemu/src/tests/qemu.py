#!/usr/bin/env python

import unittest
import os
from lib import qemu


class TestQemuImg(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.img = 'testimg'
        self.qmdir = os.path.expanduser('~/.qm')
        #  ~/.qm/testimg/testimg.qcow2
        self.vm = os.path.join(self.qmdir, self.img, self.img + '.qcow2')
        self.qm = qemu.QemuImg(qmdir=self.qmdir)

    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def __check_assertRaises_number(self, exception, function, excepted=[]):
        for test in 0.1, -0.1, 0, 1, -1:
            if test in excepted:
                continue
            self.assertRaises(exception, function, test)

    def __check_assertRaises_data_structure(self, exception,
                                            function, excepted=[]):
        for test in [['test', 'test'], {'test', 'test'}, {'test': 'test'}]:
            if test in excepted:
                continue
            self.assertRaises(exception, function, test)

    def test_parse_size(self):
        # Abnormal test
        self.__check_assertRaises_number(
            TypeError,
            self.qm.parse_size,
            excepted=[1, -1, 0]
        )
        self.__check_assertRaises_data_structure(TypeError, self.qm.parse_size)
        self.assertRaises(TypeError, self.qm.parse_size)
        self.assertRaises(ValueError, self.qm.parse_size, '10UB')
        self.assertRaises(ValueError, self.qm.parse_size, 0)
        self.assertRaises(ValueError, self.qm.parse_size, -1)
        # Normal test
        self.assertEqual(self.qm.parse_size(1), 1)
        # key   -- excepted return value
        # value -- test patterns
        testcases = {
            '10K': ['10k', '10KB', '10Kb', '10kb', '10kB', '10k'],
            '10G': ['10G', '10GB', '10Gb', '10gb', '10gB', '10g'],
            '10T': ['10T', '10TB', '10Tb', '10tb', '10tB', '10t'],
            '10P': ['10P', '10PB', '10Pb', '10pb', '10pB', '10p'],
            '10E': ['10E', '10EB', '10Eb', '10eb', '10eB', '10e']
        }
        for except_return, argument_patterns in testcases.items():
            for pattern in argument_patterns:
                self.assertEqual(self.qm.parse_size(pattern), except_return)

    def test_absname(self):
        self.__check_assertRaises_number(TypeError, self.qm.absname)
        self.__check_assertRaises_data_structure(TypeError, self.qm.absname)
        self.assertEqual(self.qm.absname(self.img + 'qcow2'))

    def test_create(self):
        self.assertRaises(
            TypeError,
            self.qm.img_create(
                format='dsjf;alksdjf',
                size='10G'
            )
        )
        self.assertRaises(
            TypeError,
            self.qm.img_create(
                name=self.img,
                size='10G'
            )
        )
        self.assertRaises(
            TypeError,
            self.qm.img_create(
                name=self.img,
                format='dsjf;alksdjf'
            )
        )
        self.assertRaises(
            ValueError,
            self.qm.img_create(
                name=self.img,
                format='dsjf;alksdjf',
                size='10G'
            )
        )
        self.assertRaises(
            ValueError,
            self.qm.img_create(
                name=self.img,
                format='qcow2',
                size='fdjksl'
            )
        )
        self.assertEqual(
            self.qm.create(
                name=self.img,
                format='qcow2',
                size='10G'
            ),
            self.vm
        )
