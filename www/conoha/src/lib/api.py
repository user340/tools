#!/usr/bin/env python

import collections
import datetime
import json
import os
import requests
import tempfile
import time
import yaml
from lib import exceptions


class ConoHaAPI:
    """Collection of methods that GET/POST from/to ConoHa API.

    It is collection of HTTP request wrapper for ConoHa API
    (https://www.conoha.jp/docs/). This is OpenStack-compliant API.

    I don't/can't implement large collection of methods for all provided API.
    Basic policy is: Just least APIs that I want to use.

    Attributes:
        confname (str): Path to config file
    """
    def __init__(self, confname='./conf/conohactl.conf'):
        try:
            with open(os.path.abspath(confname),
                      encoding='utf-8', mode='r') as f:
                self.__conf = yaml.safe_load(f)
        except OSError:
            raise
        p = collections.namedtuple('URI', ['billing', 'compute', 'flavors'])
        self.__api = p(
            billing=f'https://account.{self.__conf["region"]}/v1'
                    f'/{self.__conf["tenantid"]}/billing-invoices',
            compute=f'https://compute.{self.__conf["region"]}/v2'
                    f'/{self.__conf["tenantid"]}/servers',
            flavors=f'https://compute.{self.__conf["region"]}/v2'
                    f'/{self.__conf["tenantid"]}/flavors'
        )
        self.__token = self.__get_token()
        self.__headers = {
            'Accept': 'application/json', 'X-Auth-Token': self.__token['id']
        }

    """
    ==========================================================================
    API authentication methods
    ==========================================================================
    """

    def __get_token(self):
        """Return access token from existing temporary file or API.

        If temporary token file is existing and this token is not expired, The
        function returns the token. Else, it calls `self.__do_auth()` method
        then return it.

        Returns:
            dict: It contains "issued_at", "expires" and "id" keys.
        """
        tokenfiles = []
        tempdir = tempfile.gettempdir()
        for root, dirs, files in os.walk(tempdir):
            for file in files:
                if file.endswith('_conohavps.info'):
                    tokenfiles.append(os.path.join(tempdir, file))
        # Is token file exists?
        if tokenfiles == []:
            return self.__do_auth()
        else:
            # Use latest token file
            tokenfile = tokenfiles[0]
            for i in tokenfiles[1:]:
                if os.path.getctime(tokenfile) < os.path.getctime(i):
                    tokenfile = i
            with open(tokenfile, encoding='utf-8', mode='r') as fp:
                token_from_tmp = json.load(fp)['access']['token']
            # Was token expired?
            expires = datetime.datetime.strptime(
                token_from_tmp['expires'],
                '%Y-%m-%dT%H:%M:%SZ'
            )
            if datetime.datetime.now() >= expires:
                return self.__do_auth()
            else:
                return token_from_tmp

    def __do_auth(self):
        """Return access token.

        It calls `self.__get_identity()` method to get new API access token for
        access to ConoHa VPS API. After called, it creates new temporary file
        for records access token information as JSON format. The access token
        will be expired after 24 hours.

        Returns:
            dict: It contains "issued_at", "expires" and "id" keys. If error
                  has occured, It returns None.
        """
        res = self.__get_identity()
        handle, _ = tempfile.mkstemp(suffix='_conohavps.info', text=True)
        with open(handle, encoding='utf-8', mode='w') as fp:
            fp.write(json.dumps(res.json()))
        return res.json()['access']['token']

    def __get_identity(self):
        """Post usename, password and tenantid into identity API v2.0.

        Documentation:
            https://www.conoha.jp/docs/identity-post_tokens.html

        Returns:
            dict: Full response text from identity API v2.0. If error has
                  occured, It returns None.
        """
        payload = {
                    'auth': {
                        'passwordCredentials': {
                            'username': self.__conf['username'],
                            'password': self.__conf['password']
                        },
                        'tenantId': self.__conf['tenantid']
                    }
                  }
        res = requests.post(
            f'https://identity.{self.__conf["region"]}/v2.0/tokens',
            data=json.dumps(payload)
        )
        if res.status_code != 200:
            raise exceptions.BadStatusCodeError(
                f'HTTP status code is {res.status_code} but we excepted 200.'
            )
        return res

    def return_token(self):
        """Getter of `self.__token` which is private variable.

        Maybe, common user has no chance of call it.

        Returns:
            dict: It contains "issued_at", "expires" and "id" keys.
        """
        return self.__token

    """
    ==========================================================================
    Blling methods
    ==========================================================================
    """

    def get_billing_invoices(self, limit=1):
        """Get billing invoices from billing API v1.

        Documentation:
            https://www.conoha.jp/docs/account-billing-invoices-list.html

        Args:
            limit (int): Number of gettings

        Returns:
            dict: Full respose body from billing API v1
            int: HTTP status code
        """
        if type(limit) is not int:
            raise TypeError
        res = requests.get(
            self.__api.billing + f'?limit={limit}',
            headers=self.__headers
        )
        if res.status_code != 200:
            raise exceptions.BadStatusCodeError(
                f'HTTP status code is {res.status_code} but we excepted 200.'
            )
        body = res.json()
        if body is None:
            raise exceptions.JsonDecodeError
        return body, res.status_code

    """
    ==========================================================================
    Compute methods -- Get virtual machine informations
    ==========================================================================
    """

    def get_vms_list(self):
        """Get list of virtual machines that you deployed.

        Documentation:
            https://www.conoha.jp/docs/compute-get_vms_list.html

        Returns:
            dict: Full response from compute API v2.0
            int: HTTP status code
        """
        res = requests.get(self.__api.compute, headers=self.__headers)
        if res.status_code != 200:
            raise exceptions.BadStatusCodeError(
                f'HTTP status code is {res.status_code} but we excepted 200.'
            )
        body = res.json()
        if body is None:
            raise exceptions.JsonDecodeError
        return body, res.status_code

    def get_vm_detail_specified(self, server_id):
        """Get details by given server id.

        We can see "server id" in ConoHa control panel. Move to
        "詳細設定->VPS設定" on VM you want to check.
        Here, "UUID" is "server id".

        Documentation:
            https://www.conoha.jp/docs/compute-get_vms_detail_specified.html

        Args:
            server_id (str): UUID of virtual machine

        Returns:
            dict: Full response body
            int: HTTP status code
        """
        if type(server_id) is not str:
            raise TypeError
        res = requests.get(self.__api.compute + f'/{server_id}',
                           headers=self.__headers)
        if res.status_code != 200:
            if res.status_code == 404:
                raise exceptions.ServerNotFoundError(
                    f'Given UUID\'s server not found: {server_id}'
                )
            else:
                raise exceptions.BadStatusCodeError(
                    f'HTTP status code is {res.status_code}'
                    ' but we excepted 200.'
                )
        body = res.json()
        if body is None:
            raise exceptions.JsonDecodeError
        return body, res.status_code

    def get_all_vm_details(self):
        """ Get all virtual machines details

        Documentation:
            https://www.conoha.jp/docs/compute-get_vms_detail.html

        Returns:
            dict: Full response body
            int: HTTP status code
        """
        res = requests.get(
            self.__api.compute + '/detail',
            headers=self.__headers
        )
        if res.status_code != 200:
            raise exceptions.BadStatusCodeError(
                f'HTTP status code is {res.status_code}'
                ' but we excepted 200.'
            )
        body = res.json()
        if body is None:
            raise exceptions.JsonDecodeError
        return body, res.status_code

    """
    ==========================================================================
    Compute methods -- Power on/Shut off/Reboot virtual machine
    ==========================================================================
    """

    def wait_status(self, server_id, status):
        """Wait until specified virtual machine status be given status

        Args:
            server_id (str): Virtual machine UUID
            status (str): Server status
        """
        if type(server_id) is not str:
            raise TypeError
        supported_status = ['ACTIVE', 'SHUTOFF']
        if status not in supported_status:
            raise ValueError
        max_loop_count = 12  # Max wait time is 60 seconds
        while True:
            if max_loop_count == 0:
                raise TimeoutError
            vm, vm_status_code = self.get_vm_detail_specified(server_id)
            if vm['server']['status'] == status:
                break
            else:
                time.sleep(5)
                max_loop_count = max_loop_count - 1

    def power_on_vm(self, server_id):
        """Power on given server id's VM.

        Documentation:
            https://www.conoha.jp/docs/compute-power_on_vm.html

        Args:
            server_id (str): UUID of virtual machine

        Returns:
            int: HTTP status code
        """
        if type(server_id) is not str:
            raise TypeError
        data = {'os-start': 'null'}
        res = requests.post(
            self.__api.compute + f'/{server_id}/action',
            headers=self.__headers,
            data=json.dumps(data)
        )
        if res.status_code != 202:
            if res.status_code == 404:
                raise exceptions.ServerNotFoundError(
                    'Given server_id\'s server not found.'
                )
            elif res.status_code == 409:
                raise exceptions.ConflictingRequestError(
                    res.json()['conflictingRequest']['message']
                )
            else:
                raise exceptions.BadStatusCodeError(
                    f'HTTP status code is {res.status_code}'
                    ' but we excepted 202.'
                )
        self.wait_status(server_id, 'ACTIVE')
        return res.status_code

    def stop_cleanly_vm(self, server_id):
        """Stop given server id's VM.

        Documentation:
            https://www.conoha.jp/docs/compute-stop_cleanly_vm.html

        Args:
            server_id (str): UUID of virtual machine

        Returns:
            int: HTTP status code
        """
        if type(server_id) is not str:
            raise TypeError
        data = {'os-stop': 'null'}
        res = requests.post(
            self.__api.compute + f'/{server_id}/action',
            headers=self.__headers,
            data=json.dumps(data)
        )
        if res.status_code != 202:
            if res.status_code == 404:
                raise exceptions.ServerNotFoundError(
                    'Given server_id\'s server not found.'
                )
            elif res.status_code == 409:
                raise exceptions.ConflictingRequestError(
                    res.json()['conflictingRequest']['message']
                )
            else:
                raise exceptions.BadStatusCodeError(
                    f'HTTP status code is {res.status_code}'
                    ' but we excepted 202.'
                )
        self.wait_status(server_id, 'SHUTOFF')
        return res.status_code

    def reboot_vm(self, server_id):
        """Reboot given server id's VM.

        Documentation:
            https://www.conoha.jp/docs/compute-reboot_vm.html

        Args:
            server_id (str): UUID of virtual machine

        Returns:
            int: HTTP status code
        """
        if type(server_id) is not str:
            raise TypeError
        data = {'reboot': {'type': 'SOFT'}}
        res = requests.post(
            self.__api.compute + f'/{server_id}/action',
            headers=self.__headers,
            data=json.dumps(data)
        )
        if res.status_code != 202:
            if res.status_code == 404:
                raise exceptions.ServerNotFoundError(
                    'Given server_id\'s server not found.'
                )
            elif res.status_code == 409:
                raise exceptions.ConflictingRequestError(
                    res.json()['conflictingRequest']['message']
                )
            else:
                raise exceptions.BadStatusCodeError(
                    f'HTTP status code is {res.status_code}'
                    ' but we excepted 202.'
                )
        self.wait_status(server_id, 'ACTIVE')
        return res.status_code

    """
    ==========================================================================
    Compute methods -- Get/Change virtual machine flavor
    ==========================================================================
    """

    def get_flavors_list(self):
        """Return flavors list

        Documentation:
            https://www.conoha.jp/docs/compute-get_flavors_list.html

        Returns:
            dict: Full response from compute API v2.0
            int: HTTP status code
        """
        res = requests.get(self.__api.flavors, headers=self.__headers)
        if res.status_code != 200:
            raise exceptions.BadStatusCodeError(
                f'HTTP status code is {res.status_code} but we excepted 200.'
            )
        body = res.json()
        if body is None:
            raise exceptions.JsonDecodeError
        return body, res.status_code

    def get_flavor_name(self, flavor_id):
        """Return flavor name by given flavor_id

        Args:
            flavor_id (str): flavor_id which can get from `get_flavors_list()`

        Returns:
            If given flavor_id is found, return flavor's name.
            Otherwise, return None.
        """
        if type(flavor_id) is not str:
            raise TypeError
        flavors, _ = self.get_flavors_list()
        for flavor in flavors['flavors']:
            if flavor['id'] == flavor_id:
                return flavor['name']
        return None

    def get_flavor_id(self, plan):
        """Return given plan's flavor_id (UUID)

        Args:
            plan (str): Billing plan
                            - g-1gb
                            - g-2gb
                            - g-4gb
                            - g-8gb
                            - g-16gb
                            - g-32gb
                            - g-64gb
        Memo:
            g-512mb (1 Core, 512MB RAM) plan is not included in test case
            because the plan can not change to other plans.

        Returns:
            str: flavor_id
        """
        if type(plan) is not str:
            raise TypeError
        if plan not in ['g-1gb', 'g-2gb', 'g-4gb',
                        'g-8gb', 'g-16gb', 'g-32gb', 'g-64gb']:
            raise exceptions.InvalidArgumentError(f'Invalid argument: {plan}')
        body, _ = self.get_flavors_list()
        for flavor in body['flavors']:
            if flavor['name'] == plan:
                return flavor['id']

    def change_flavor(self, server_id, flavor_id):
        """Change flavor of given server_id's virtual machine to given flavor.

        Memo:
            We can't switch to g-512mb plan from other plan.

        Args:
            server_id (str): UUID of virtual machine
            flavor_id (str): id of flavor (take from `self.get_flavors()`)

        Returns:
            dict: Full response body from compute API v2.0. If server status is
                  not "SHUTOFF", return None.
        """
        if type(server_id) is not str:
            raise TypeError
        if type(flavor_id) is not str:
            raise TypeError
        vm, _ = self.get_vm_detail_specified(server_id)
        if vm['server']['flavor']['id'] == flavor_id:
            print('Given flavor_id is same as current flavor. Skip.')
            return None
        if vm['server']['status'] == 'SHUTOFF':
            data = {'resize': {'flavorRef': flavor_id}}
            res = requests.post(
                self.__api.compute + f'/{server_id}/action',
                headers=self.__headers,
                data=json.dumps(data)
            )
            if res.status_code != 202:
                if res.status_code == 400:
                    raise exceptions.BadRequestError(
                        res.json()['badRequest']['message']
                    )
                else:
                    raise exceptions.BadStatusCodeError(
                        f'HTTP status code is {res.status_code} '
                        'but we excepted 202.'
                    )
            return res
        else:
            print(
                'Change flavor operation allowed until server stopped.\n'
                f'Current server status: {vm["server"]["status"]}'
            )
            return None

    def confirm_flavor(self, server_id):
        """Confirm given server id's VM flavor.

        Args:
            server_id (str): UUID of virtual machine

        Returns:
            dict: Full response from compute API v2.0. If server status is
                  not "VERIFY_RESIZE", return empty dictionary.
        """
        if type(server_id) is not str:
            raise TypeError
        while True:
            vm, vm_status_code = self.get_vm_detail_specified(server_id)
            if vm['server']['status'] == 'RESIZE':
                time.sleep(20)  # XXX: Magic Number
            elif vm['server']['status'] == 'VERIFY_RESIZE':
                break
            else:
                raise exceptions.UnexceptedServerStatusError(
                    'Here, we excepted RESIZE or VERIFY_RESIZE server status'
                    f' but current server status: {vm["server"]["status"]}'
                )

        data = {'confirmResize': 'null'}
        res = requests.post(
            self.__api.compute + f'/{server_id}/action',
            headers=self.__headers,
            data=json.dumps(data)
        )
        if res.status_code != 204:
            raise exceptions.BadStatusCodeError(
                f'HTTP status code is {res.status_code}'
                ' but we excepted 204.'
            )
        return res
