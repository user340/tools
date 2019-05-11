#!/usr/bin/env python

import time
import re
import unittest
import yaml
from lib import api
from lib import exceptions


class TestConoHaAPI(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.conoha = api.ConoHaAPI()
        with open('./tests/conf/server_id.conf',
                  encoding='utf-8', mode='r') as server_id_conf:
            self.__server_id = yaml.safe_load(server_id_conf)['server_id']

    @classmethod
    def tearDownClass(self):
        vm, vm_status_code = \
            self.conoha.get_vm_detail_specified(self.__server_id)
        if vm['server']['status'] == 'ACTIVE':
            self.conoha.stop_cleanly_vm(self.__server_id)
        if vm['server']['flavor']['id'] != self.conoha.get_flavor_id('g-1gb'):
            self.conoha.change_flavor(
                self.__server_id,
                self.conoha.get_flavor_id('g-1gb')
            )
            while True:
                after_change_flavor, _ = \
                    self.conoha.get_vm_detail_specified(self.__server_id)
                if after_change_flavor['server']['status'] == 'VERIFY_RESIZE':
                    break
                else:
                    time.sleep(10)
            self.conoha.confirm_flavor(self.__server_id)

    def check_keys_in_dict(self, keys, dictionary):
        """Check given dictionary contains given keys or not.

        Args:
            keys (list): Keys you want to check
            dictionary (dict): Dictionary that test target
        """
        [self.assertTrue(key in dictionary) for key in keys]

    def check_response_values(self, body, status_code, excepted_status_code):
        """Check given response body and status_code are valid.

        Args:
            body (dict): API response body
            status_code (int): HTTP status_code
            excepted_status_code (int): HTTP status_code that you excepted
        """
        self.assertEqual(status_code, excepted_status_code)
        self.assertIsNotNone(body)
        self.assertTrue(isinstance(body, dict))

    def test_get_identity(self):
        """Test that necessary keys are contained in token information.
        """
        token = self.conoha.return_token()
        keys = ['issued_at', 'expires', 'id']
        self.check_keys_in_dict(keys, token)
        self.assertRegex(token['issued_at'], '\\S*')
        self.assertRegex(token['expires'], '\\S*')
        self.assertRegex(token['id'], '\\S*')

    def test_get_billing_invoices(self):
        """Check required keys are contained in billing informations.
        """
        """ Abnormal test """
        self.assertRaises(TypeError, self.conoha.get_billing_invoices, 'xx')
        self.assertRaises(TypeError, self.conoha.get_billing_invoices, None)
        """ Normal test"""
        body, status_code = self.conoha.get_billing_invoices()
        self.check_response_values(body, status_code, 200)
        self.assertTrue('billing_invoices' in body)
        for i in body['billing_invoices']:
            self.assertTrue(isinstance(i, dict))
            keys = [
                'invoice_id',
                'payment_method_type',
                'invoice_date',
                'bill_plus_tax',
                'due_date'
            ]
            self.check_keys_in_dict(keys, i)

    def test_get_vms_list(self):
        """Check required keys are contained in VMs list.
        """
        body, status_code = self.conoha.get_vms_list()
        self.check_response_values(body, status_code, 200)
        self.assertTrue('servers' in body)
        for i in body['servers']:
            self.assertTrue(isinstance(i, dict))
            keys = ['id', 'links', 'name']
            self.check_keys_in_dict(keys, i)

    def test_get_vms_detail(self):
        """Check required keys are contained in vm details.

        We want to test we can access to these informations:
            - Server Name
            - Server Status
            - IP Address
            - Flavor (Billing Plan)
        """
        """ Abnormal test """
        self.assertRaises(TypeError, self.conoha.get_vm_detail_specified, None)
        self.assertRaises(TypeError, self.conoha.get_vm_detail_specified, 1)
        self.assertRaises(
            exceptions.ServerNotFoundError,
            self.conoha.get_vm_detail_specified,
            'xxxx'
        )
        """ Normal test """
        body, status_code = self.conoha.get_vm_detail_specified(
            self.__server_id
        )
        self.check_response_values(body, status_code, 200)
        keys = [
            'OS-EXT-IPS-MAC:mac_addr',
            'OS-EXT-IPS:type',
            'addr',
            'version'
        ]
        addr_data = body['server']['addresses']
        for interface in addr_data:
            for nwinfo in addr_data[interface]:
                self.check_keys_in_dict(keys, nwinfo)
        self.assertTrue('id' in body['server']['flavor'])
        self.assertTrue('status' in body['server'])
        self.assertTrue('name' in body['server'])

    def test_get_all_vm_details(self):
        """ Get all virtual machine details
        """
        """ Normal test """
        body, status_code = self.conoha.get_all_vm_details()
        self.check_response_values(body, status_code, 200)
        self.assertTrue(isinstance(body['servers'], list))

    def test_power_on_vm(self):
        """Power on specified VM.
        """
        """ Abnormal test """
        self.assertRaises(TypeError, self.conoha.power_on_vm, None)
        self.assertRaises(TypeError, self.conoha.power_on_vm, -1)
        self.assertRaises(
            exceptions.ServerNotFoundError,
            self.conoha.power_on_vm,
            'jkfljklruin'
        )
        """ Normal test """
        while True:
            vm, vm_status_code = self.conoha.get_vm_detail_specified(
                self.__server_id
            )
            self.check_response_values(vm, vm_status_code, 200)
            if vm['server']['status'] == 'SHUTOFF':
                self.assertEqual(
                    self.conoha.power_on_vm(self.__server_id),
                    202
                )
                break
            elif vm['server']['status'] == 'ACTIVE':
                """ Power off if test virtual machine is active """
                self.assertEqual(
                    self.conoha.stop_cleanly_vm(self.__server_id),
                    202
                )
        """ Cleanup: Shutoff test virtual machine"""
        self.assertEqual(self.conoha.stop_cleanly_vm(self.__server_id), 202)

    def test_stop_cleanly_vm(self):
        """Stop specified VM.
        """
        """ Abnormal test """
        self.assertRaises(TypeError, self.conoha.stop_cleanly_vm, None)
        self.assertRaises(TypeError, self.conoha.stop_cleanly_vm, -3)
        self.assertRaises(
            exceptions.ServerNotFoundError,
            self.conoha.stop_cleanly_vm,
            'jkfljklruin'
        )
        """ Normal test """
        while True:
            vm, vm_status_code = \
                self.conoha.get_vm_detail_specified(self.__server_id)
            self.check_response_values(vm, vm_status_code, 200)
            if vm['server']['status'] == 'ACTIVE':
                self.assertEqual(
                    self.conoha.stop_cleanly_vm(self.__server_id),
                    202
                )
                break
            elif vm['server']['status'] == 'SHUTOFF':
                self.assertEqual(
                    self.conoha.power_on_vm(self.__server_id),
                    202
                )
        """ Nothing cleanup phase because virtual machine is stopped """

    def test_reboot_vm(self):
        """Reboot specified VM.
        """
        """ Abnormal test """
        self.assertRaises(TypeError, self.conoha.reboot_vm, None)
        self.assertRaises(TypeError, self.conoha.reboot_vm, 9)
        self.assertRaises(
            exceptions.ServerNotFoundError,
            self.conoha.reboot_vm,
            'fjadksfjrueiwl'
        )
        """ Normal test """
        while True:
            vm, vm_status_code = self.conoha.get_vm_detail_specified(
                self.__server_id
            )
            self.check_response_values(vm, vm_status_code, 200)
            if vm['server']['status'] == 'ACTIVE':
                self.assertEqual(self.conoha.reboot_vm(self.__server_id), 202)
                break
            elif vm['server']['status'] == 'SHUTOFF':
                self.assertEqual(
                    self.conoha.power_on_vm(self.__server_id),
                    202
                )
            else:
                print(f'server status is {vm["server"]["status"]}')
                time.sleep(10)
        """ Cleanup: Shutoff test virtual machine"""
        self.assertEqual(self.conoha.stop_cleanly_vm(self.__server_id), 202)

    def test_get_flavors_list(self):
        """Check required keys are conrained in flavors dictionary.
        """
        body, status_code = self.conoha.get_flavors_list()
        self.check_response_values(body, status_code, 200)
        keys = ['id', 'name']
        for flavor in body['flavors']:
            self.check_keys_in_dict(keys, flavor)

    def test_get_flavor_name(self):
        """Get flavor name from billing UUID.
        """
        """ Abnormal test """
        self.assertRaises(TypeError, self.conoha.get_flavor_name, None)
        self.assertRaises(TypeError, self.conoha.get_flavor_name, 3)
        self.assertIsNone(self.conoha.get_flavor_name('x'))
        """ Normal test """
        self.assertEqual(
            self.conoha.get_flavor_name(
                '7eea7469-0d85-4f82-8050-6ae742394681'
            ),
            'g-1gb'
        )

    def test_get_flavor_id(self):
        """Get UUID by specified billing plan.
        """
        plans = [
            'g-512mb',
            'g-1gb',
            'g-2gb',
            'g-4gb',
            'g-8gb',
            'g-16gb',
            'g-32gb',
            'g-64gb'
        ]
        """
        Abnormal test
        The "g-512mb" plan is not allowed by get_flavor_id() method.
        """
        self.assertRaises(TypeError, self.conoha.get_flavor_id, None)
        self.assertRaises(TypeError, self.conoha.get_flavor_id, 0)
        self.assertRaises(
            exceptions.InvalidArgumentError,
            self.conoha.get_flavor_id,
            plans[0]
        )
        self.assertRaises(
            exceptions.InvalidArgumentError,
            self.conoha.get_flavor_id,
            'aaa'
        )
        """ Normal test """
        for plan in plans[1:]:
            self.assertIsNotNone(
                re.match(
                    r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}',
                    self.conoha.get_flavor_id(plan)
                )
            )

    def test_change_flavor(self):
        """Change flavor of target server to g-1gb or g-2gb plan.
        """
        vm, vm_status_code = \
            self.conoha.get_vm_detail_specified(self.__server_id)
        self.check_response_values(vm, vm_status_code, 200)
        current_flavor = vm['server']['flavor']['id']

        """ Abnormal test """
        self.assertRaises(
            TypeError,
            self.conoha.change_flavor,
            None,
            None
        )
        self.assertRaises(
            TypeError,
            self.conoha.change_flavor,
            4,
            0
        )
        self.assertRaises(
            TypeError,
            self.conoha.change_flavor,
            None,
            current_flavor
        )
        self.assertRaises(
            TypeError,
            self.conoha.change_flavor,
            1,
            current_flavor
        )
        self.assertRaises(
            TypeError,
            self.conoha.change_flavor,
            self.__server_id,
            None
        )
        self.assertRaises(
            TypeError,
            self.conoha.change_flavor,
            self.__server_id,
            -4
        )
        """ Normal test """
        if current_flavor == self.conoha.get_flavor_id('g-1gb'):
            res = self.conoha.change_flavor(
                self.__server_id,
                self.conoha.get_flavor_id('g-2gb')
            )
        else:
            res = self.conoha.change_flavor(
                self.__server_id,
                self.conoha.get_flavor_id('g-1gb')
            )
        self.assertIsNotNone(res)
        self.assertEqual(res.status_code, 202)
        while True:
            """ Sleep until server status be VERIFY_RESIZE """
            vm, vm_status_code = \
                self.conoha.get_vm_detail_specified(self.__server_id)
            self.assertEqual(vm_status_code, 200)
            if vm['server']['status'] == 'VERIFY_RESIZE':
                break
            else:
                time.sleep(10)
        confirm = self.conoha.confirm_flavor(self.__server_id)
        self.assertEqual(confirm.status_code, 204)
        while True:
            """ Sleep until server status be SHUTOFF """
            vm, vm_status_code = \
                self.conoha.get_vm_detail_specified(self.__server_id)
            self.check_response_values(vm, vm_status_code, 200)
            if vm['server']['status'] == 'SHUTOFF':
                break
            else:
                time.sleep(10)

    # @unittest.skip('Do manualy (For debugging test)')
    def test_confirm_flavor(self):
        confirm = self.conoha.confirm_flavor(self.__server_id)
        self.assertEqual(confirm.status_code, 204)

    def test_init(self):
        """Abnormal test for `api.__init__()` method.
        """
        self.assertRaises(OSError, api.ConoHaAPI, confname='asdffdrafdsaez')


if __name__ == '__main__':
    unittest.main()
