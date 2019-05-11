#!/usr/bin/env python

import texttable
import time
import re
from lib import api
from lib import exceptions


class ConoHaCmd:
    def __init__(self, confname='conf/conohactl.conf'):
        self.__api = api.ConoHaAPI(confname=confname)

    def check_id_or_tag(self, string):
        """ If given string is UUID, return it. If not UUID, It may Tag

        Args:
            string (str): UUID or Tag

        Returns:
            str: UUID
        """
        if re.match(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}', string):
            return string
        else:
            return self.get_server_id_from_tag(string)

    def return_table(self, colums=None):
        if type(colums) is not int:
            raise TypeError
        elif colums < 1:
            raise ValueError('Given argument less than 1')
        table = texttable.Texttable()
        table.set_cols_align(['l' for _ in range(colums)])
        table.set_cols_valign(['m' for _ in range(colums)])
        table.set_deco(texttable.Texttable.HEADER)
        return table

    def return_vm_status_table(self, before, after):
        """Return table that shows changes virtual machine status

        Args:
            before (dict): machine status before operation
            after (dict): machine status after operation

        Returns:
            texttable.Texttable
        """
        table = self.return_table(4)
        table.header(['Tag', 'Previous', '->', 'Now'])
        table.add_row([
            after['server']['metadata']['instance_name_tag'],
            before['server']['status'],
            '->',
            after['server']['status']
        ])
        return table

    def get_vm_list(self):
        """Get all virtual machine list

        Returns:
            texttable.Texttable: It contains server ID and name
        """
        body, _ = self.__api.get_vms_list()
        table = self.return_table(2)
        table.header(['Name', 'UUID'])
        for server in body['servers']:
            table.add_row([server['name'], server['id']])
        return table

    def get_vm_detail(self, server_id):
        """Return VM informations.

        This is `lib.api.get_vm_detail_specified` wrapper method

        Args:
            server_id (str): UUID of virtual machine

        Returns:
            dict: API response body
        """
        body, _ = self.__api.get_vm_detail_specified(server_id)
        return body

    def get_server_id_from_tag(self, tag):
        """ Return VM UUID by given Tag

        Args:
            tag (str): VM Tag

        Returns:
            str: UUID if found. Otherwise empty.
        """
        if type(tag) is not str:
            raise TypeError
        body, _ = self.__api.get_all_vm_details()
        for vm in body['servers']:
            if vm['metadata']['instance_name_tag'] == tag:
                return vm['id']
        raise ValueError

    def show_vm_detail(self, server_id, ipv4=True, ipv6=False):
        """Show specified VM informations

        Args:
            server_id (str): UUID of virtual machine
            ipv4 (bool): Flag that show IPv4 address or not
            ipv6 (bool): Flag that show IPv6 address or not

        Returns:
            texttable.Texttable: Server name, Tag and UUID
            texttable.Texttable: IPv4/IPv6 address, server status and plan
        """
        if type(server_id) is not str:
            raise TypeError
        try:
            res = self.get_vm_detail(self.check_id_or_tag(server_id))
        except exceptions.ServerNotFoundError:
            raise
        except exceptions.NothingServerIDError:
            raise
        except Exception:
            raise
        address = {'ipv4': None, 'ipv6': None}
        for interface in res['server']['addresses']:
            for nwinfo in res['server']['addresses'][interface]:
                if nwinfo['version'] == 4 and ipv4:
                    address['ipv4'] = nwinfo['addr']
                elif nwinfo['version'] == 6 and ipv6:
                    address['ipv6'] = nwinfo['addr']
        first_table = self.return_table(3)
        second_table = self.return_table(4)
        first_table.header(['Name', 'Tag', 'UUID'])
        first_table.add_row(
            [
                res['server']['name'],
                res['server']['metadata']['instance_name_tag'],
                res['server']['id']
            ]
        )
        second_table.header(['IPv4', 'IPv6', 'Status', 'Plan'])
        second_table.add_row(
            [
                address['ipv4'],
                address['ipv6'],
                res['server']['status'],
                self.__api.get_flavor_name(res['server']['flavor']['id'])
            ]
        )
        return first_table, second_table

    def show_billing(self, limit=1):
        """Show billing invoices

        Args:
            limit (int): number of billing information

        Returns:
            texttable.Texttable:
                It contains invoice ID, payment method, bill, and due date.
        """
        if type(limit) is not int:
            raise TypeError
        if limit < 0:
            raise ValueError
        body, _ = self.__api.get_billing_invoices(limit=limit)
        table = self.return_table(4)
        table.header(['Invoice ID', 'Type', 'Yen (include tax)', 'Due'])
        for i in range(len(body['billing_invoices'])):
            table.add_row(
                [
                    body['billing_invoices'][i]['invoice_id'],
                    body['billing_invoices'][i]['payment_method_type'],
                    body['billing_invoices'][i]['bill_plus_tax'],
                    body['billing_invoices'][i]['due_date']
                ]
            )
        return table

    def power_on_vm(self, server_id):
        """Power on to specified virtual machine

        Args:
            server_id (str): virtual machine UUID

        Returns:
            texttable.Texttable:
                It contains Tag, before status and current status
        """
        if type(server_id) is not str:
            raise TypeError
        uuid = self.check_id_or_tag(server_id)
        before_power_on = self.get_vm_detail(uuid)
        if before_power_on['server']['status'] == 'SHUTOFF':
            self.__api.power_on_vm(uuid)
        after_power_on = self.get_vm_detail(uuid)
        return self.return_vm_status_table(before_power_on, after_power_on)

    def shutoff_vm(self, server_id):
        """Shut off to specified virtual machine

        Args:
            server_id (str): virtual machine UUID

        Returns:
            texttable.Texttable:
                It contains Tag, before status and current status
        """
        if type(server_id) is not str:
            raise TypeError
        uuid = self.check_id_or_tag(server_id)
        before_shutoff = self.get_vm_detail(uuid)
        if before_shutoff['server']['status'] == 'ACTIVE':
            self.__api.stop_cleanly_vm(uuid)
        after_shutoff = self.get_vm_detail(uuid)
        return self.return_vm_status_table(before_shutoff, after_shutoff)

    def reboot_vm(self, server_id):
        """Reboot specified virtual machine

        Args:
            server_id (str): virtual machine UUID

        Returns:
            texttable.Texttable:
                It contains Tag, before status and current status
        """
        if type(server_id) is not str:
            raise TypeError
        uuid = self.check_id_or_tag(server_id)
        before_reboot = self.get_vm_detail(uuid)
        if before_reboot['server']['status'] == 'ACTIVE':
            self.__api.reboot_vm(uuid)
        after_reboot = self.get_vm_detail(uuid)
        return self.return_vm_status_table(before_reboot, after_reboot)

    def get_flavor_id_from_name(self, flavor_name):
        """Return flavor ID by given flavor name

        Args:
            flavor_name (str): flavor name

        Return:
            str: flavor ID
        """
        flavors = [
            'g-512mb',
            'g-1gb',
            'g-2gb',
            'g-4gb',
            'g-8gb',
            'g-16gb',
            'g-32gb',
            'g-64gb'
        ]
        if type(flavor_name) is not str:
            raise TypeError
        if flavor_name not in flavors:
            raise ValueError
        return self.__api.get_flavor_id(flavor_name)

    def get_flavor_name_from_id(self, flavor_id):
        """Return flavor name by given flavor ID

        Args:
            flavor_id (str): flavor ID

        Returns:
            str: flavor name
        """
        if type(flavor_id) is not str:
            raise TypeError
        return self.__api.get_flavor_name(flavor_id)

    def change_flavor(self, server_id, flavor_name):
        """Change given server's flavor to given flavor_name

        Args:
            server_id (str): virtual machine UUID
            flavor_name (str): flavor name

        Returns:
            texttable.Texttable:
                It contains Tag, flavor before operation
                and flavor after operation
        """
        uuid = self.check_id_or_tag(server_id)
        pre = self.get_vm_detail(uuid)
        if pre['server']['status'] != 'SHUTOFF':
            print('Current VM status is ' + pre['server']['status'])
            return None
        flavor_id = self.__api.get_flavor_id(flavor_name)
        self.__api.change_flavor(uuid, flavor_id)
        while True:
            vm = self.get_vm_detail(uuid)
            if vm['server']['status'] == 'VERIFY_RESIZE':
                self.__api.confirm_flavor(uuid)
                break
            else:
                time.sleep(10)
        while True:
            vm = self.get_vm_detail(uuid)
            if vm['server']['status'] == 'SHUTOFF':
                break
            else:
                time.sleep(5)
        table = self.return_table(4)
        table.header(['Tag', 'Previous', '->', 'Now'])
        table.add_row(
            [
                vm['server']['metadata']['instance_name_tag'],
                self.get_flavor_name_from_id(pre['server']['flavor']['id']),
                '->',
                self.get_flavor_name_from_id(vm['server']['flavor']['id']),
            ]
        )
        return table
