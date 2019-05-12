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

    def test_parse_size(self):
        self.assertRaises(TypeError, self.qm.parse_size, {'size': '10GB'})
        self.assertRaises(TypeError, self.qm.parse_size, {'size', '10GB'})
        self.assertRaises(TypeError, self.qm.parse_size, ['size', '10GB'])
        self.assertRaises(TypeError, self.qm.parse_size)
        self.assertRaises(TypeError, self.qm.parse_size, 0.1)
        self.assertRaises(ValueError, self.qm.parse_size, 0)
        self.assertRaises(ValueError, self.qm.parse_size, -1)
        self.assertRaises(ValueError, self.qm.parse_size, '10UB')
        #  key   -- excepted return value
        #  value -- test patterns
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
