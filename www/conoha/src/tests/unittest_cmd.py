#!/usr/bin/env python

import texttable
import unittest
import yaml
from lib import cmd
from lib import exceptions


class TestConoHaCmd(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.cmd = cmd.ConoHaCmd()
        with open('./tests/conf/server_id.conf',
                  encoding='utf-8', mode='r') as server_id_conf:
            self.__server_id = yaml.safe_load(server_id_conf)['server_id']

    @classmethod
    def tearDownClass(self):
        self.cmd.shutoff_vm(self.__server_id)
        vm = self.cmd.get_vm_detail(self.__server_id)
        current_flavor = \
            self.cmd.get_flavor_name_from_id(vm['server']['flavor']['id'])
        if current_flavor == 'g-2gb':
            self.cmd.change_flavor(self.__server_id, 'g-1gb')

    def test_return_table(self):
        """Give valid/invalid arg to `return_table()`
        """
        """ Abnormal test. Invalid argument. """
        self.assertRaises(TypeError, self.cmd.return_table)
        self.assertRaises(TypeError, self.cmd.return_table, 'jklf;dutil;aker')
        self.assertRaises(TypeError, self.cmd.return_table, ['test', 'fail'])
        self.assertRaises(TypeError, self.cmd.return_table, {'test': 'fail'})
        self.assertRaises(TypeError, self.cmd.return_table, {'test', 'fail'})
        self.assertRaises(TypeError, self.cmd.return_table, True)
        self.assertRaises(TypeError, self.cmd.return_table, False)
        self.assertRaises(ValueError, self.cmd.return_table, 0)
        self.assertRaises(ValueError, self.cmd.return_table, -3)
        """ Normal test. Correct argument. """
        self.assertTrue(isinstance(self.cmd.return_table(4),
                                   texttable.Texttable))

    def test_show_vm_detail(self):
        """Give valid/invalid arg to `show_vm_detail()`
        """
        """ Abnormal test. Invalid argument. """
        self.assertRaises(TypeError, self.cmd.show_vm_detail, None)
        self.assertRaises(TypeError, self.cmd.show_vm_detail, 8)
        self.assertRaises(TypeError, self.cmd.show_vm_detail, 0)
        self.assertRaises(TypeError, self.cmd.show_vm_detail, -5)
        self.assertRaises(TypeError, self.cmd.show_vm_detail, ['test', 'fail'])
        self.assertRaises(TypeError, self.cmd.show_vm_detail, {'test': 'fail'})
        self.assertRaises(TypeError, self.cmd.show_vm_detail, {'test', 'fail'})
        self.assertRaises(TypeError, self.cmd.show_vm_detail, True)
        self.assertRaises(TypeError, self.cmd.show_vm_detail, False)
        self.assertRaises(ValueError, self.cmd.show_vm_detail, 'xxxxx')
        """ Normal test. Correct argument. """
        first, second = self.cmd.show_vm_detail(self.__server_id)
        self.assertTrue(isinstance(first, texttable.Texttable))
        self.assertTrue(isinstance(second, texttable.Texttable))
        print('\n' + first.draw() + '\n\n' + second.draw())

        first, second = self.cmd.show_vm_detail('NetBSD')
        self.assertTrue(isinstance(first, texttable.Texttable))
        self.assertTrue(isinstance(second, texttable.Texttable))
        print('\n' + first.draw() + '\n\n' + second.draw())

    def test_get_server_id_from_tag(self):
        """Get UUID from Tag
        """
        """ Abnormal test """
        self.assertRaises(TypeError, self.cmd.get_server_id_from_tag, None)
        self.assertRaises(TypeError, self.cmd.get_server_id_from_tag, 39)
        self.assertRaises(TypeError, self.cmd.get_server_id_from_tag, 0)
        self.assertRaises(TypeError, self.cmd.get_server_id_from_tag, -100)
        self.assertRaises(
            TypeError,
            self.cmd.get_server_id_from_tag,
            ['test', 'fail']
        )
        self.assertRaises(
            TypeError,
            self.cmd.get_server_id_from_tag,
            {'test': 'fail'}
        )
        self.assertRaises(
            TypeError,
            self.cmd.get_server_id_from_tag,
            {'test', 'fail'}
        )
        self.assertRaises(TypeError, self.cmd.get_server_id_from_tag, True)
        self.assertRaises(TypeError, self.cmd.get_server_id_from_tag, False)
        self.assertRaises(
            ValueError,
            self.cmd.get_server_id_from_tag,
            'jfkdlsajfkdl'
        )
        """ Normal test """
        uuid = self.cmd.get_server_id_from_tag('NetBSD')
        self.assertEqual(self.__server_id, uuid)

    def test_show_billing(self):
        """Give valid/invalid arg to `get_billing()`
        """
        """ Abnormal test. Invalid argument. """
        self.assertRaises(TypeError, self.cmd.show_billing, limit=None)
        self.assertRaises(TypeError, self.cmd.show_billing, limit='dfasd')
        self.assertRaises(TypeError, self.cmd.show_billing, limit=True)
        self.assertRaises(TypeError, self.cmd.show_billing, limit=False)
        self.assertRaises(
            TypeError,
            self.cmd.show_billing,
            limit=['test', 'fail']
        )
        self.assertRaises(
            TypeError,
            self.cmd.show_billing,
            limit={'test': 'fail'}
        )
        self.assertRaises(
            TypeError,
            self.cmd.show_billing,
            limit={'test', 'fail'}
        )
        self.assertRaises(ValueError, self.cmd.show_billing, limit=-100)
        """ Normal test. Correct argument """
        table = self.cmd.show_billing(limit=1)
        self.assertTrue(isinstance(table, texttable.Texttable))
        print('\n' + table.draw() + '\n')
        table = self.cmd.show_billing(limit=100)
        self.assertTrue(isinstance(table, texttable.Texttable))
        print('\n' + table.draw() + '\n')

    def check_arguments(self, method):
        self.assertRaises(TypeError, method)
        self.assertRaises(TypeError, method, None)
        self.assertRaises(TypeError, method, 0)
        self.assertRaises(TypeError, method, -8)
        self.assertRaises(TypeError, method, 54)
        self.assertRaises(TypeError, method, True)
        self.assertRaises(TypeError, method, False)
        self.assertRaises(TypeError, method, ['test', 'fail'])
        self.assertRaises(TypeError, method, {'test': 'fail'})
        self.assertRaises(TypeError, method, {'test', 'fail'})
        self.assertRaises(ValueError, method, 'jkl;dsbjnk')

    def test_power_on_vm(self):
        """Power on virtual machine
        """
        """ Abnormal test """
        self.check_arguments(self.cmd.power_on_vm)
        """ Normal test """
        table = self.cmd.power_on_vm(self.__server_id)
        self.assertTrue(isinstance(table, texttable.Texttable))
        print('\n' + table.draw() + '\n')

    def test_shutoff_vm(self):
        """Shutoff virtual machine
        """
        """ Abnormal test """
        self.check_arguments(self.cmd.shutoff_vm)
        """ Normal test """
        table = self.cmd.shutoff_vm(self.__server_id)
        self.assertTrue(isinstance(table, texttable.Texttable))
        print('\n' + table.draw() + '\n')

    def test_reboot_vm(self):
        """Reboot virtual machine
        """
        """ Abnormal test """
        self.check_arguments(self.cmd.reboot_vm)
        """ Normal test """
        table = self.cmd.reboot_vm(self.__server_id)
        self.assertTrue(isinstance(table, texttable.Texttable))
        print('\n' + table.draw() + '\n')

    def test_change_flavor(self):
        """Change flavor to g-2gb
        """
        """ Abnormal test """
        arguments = [
            None,
            0,
            87,
            -997,
            ['test', 98],
            {'test', 'fail'},
            {'test': 'fail'}
        ]
        for first_argument in arguments:
            for second_argument in arguments:
                self.assertRaises(
                    TypeError,
                    self.cmd.change_flavor,
                    first_argument,
                    second_argument
                )
        self.assertRaises(
            exceptions.ServerNotFoundError,
            self.cmd.change_flavor,
            'fjkla;nvslei',
            'sldkjf934w57jfksla'
        )
        self.assertRaises(
            exceptions.InvalidArgumentError,
            self.cmd.change_flavor,
            self.__server_id,
            'sldkjf934w57jfksla'
        )
        self.assertRaises(
            exceptions.ServerNotFoundError,
            self.cmd.change_flavor,
            'fjkla;nvslei',
            'g-2gb'
        )
        """ Normal test """
        table = self.cmd.change_flavor(self.__server_id, 'g-2gb')
        self.assertTrue(isinstance(table, texttable.Texttable))
        print('\n' + table.draw() + '\n')

    def test_check_id_or_tag(self):
        """Check given argument is UUID or Tag
        """
        self.assertEqual(
            self.cmd.check_id_or_tag(self.__server_id),
            self.__server_id
        )
        self.assertEqual(
            self.cmd.check_id_or_tag('NetBSD'),
            self.__server_id
        )


if __name__ == '__main__':
    unittest.main()
