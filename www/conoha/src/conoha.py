#!/usr/bin/env python

import argparse
from lib import cmd


def vm_info(args):
    first_row, second_row = cmd.show_vm_detail(args.server_id)
    print(first_row.draw() + '\n\n' + second_row.draw())


def vm_list(args):
    print(cmd.get_vm_list().draw())


def show_billing(args):
    print(cmd.show_billing(limit=args.limit).draw())


def power_on(args):
    print(cmd.power_on_vm(args.server_id).draw())


def shut_off(args):
    print(cmd.shutoff_vm(args.server_id).draw())


def reboot(args):
    print(cmd.reboot_vm(args.server_id).draw())


def change_plan(args):
    print(cmd.change_flavor(args.server_id, args.flavor).draw())


def getargs():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()
    """ info """
    info = subparser.add_parser(
        'info',
        aliases=['st'],
        help='Show information of specified virtual machine'
    )
    info.add_argument(
        'server_id',
        type=str,
        help='UUID of virtual machine. You can specify VM tag instead.'
    )
    info.set_defaults(func=vm_info)
    """ list """
    vmlist = subparser.add_parser(
        'list',
        aliases=['ls'],
        help='Show list of all vm'
    )
    vmlist.set_defaults(func=vm_list)
    """ billing """
    billing = subparser.add_parser(
        'bill',
        aliases=['bl'],
        help='Show billing invoices'
    )
    billing.add_argument(
        '-l', '--limit',
        type=int,
        default=10,
        help='Number of display invoices'
    )
    billing.set_defaults(func=show_billing)
    """ power on """
    poweron = subparser.add_parser(
        'start',
        aliases=['on'],
        help='Power on target vm'
    )
    poweron.add_argument(
        'server_id',
        type=str,
        help='UUID of virtual machine. You can specify VM tag instead.'
    )
    poweron.set_defaults(func=power_on)
    """ shutoff """
    shutoff = subparser.add_parser(
        'stop',
        aliases=['off'],
        help='Shut off target vm'
    )
    shutoff.add_argument(
        'server_id',
        type=str,
        help='UUID of virtual machine. You can specify VM tag instead.'
    )
    shutoff.set_defaults(func=shut_off)
    """ reboot """
    reboot = subparser.add_parser(
        'reboot',
        aliases=['rb'],
        help='Reboot target vm'
    )
    reboot.add_argument(
        'server_id',
        type=str,
        help='UUID of virtual machine. You can specify VM tag instead.'
    )
    reboot.set_defaults(func=reboot)
    """ chnage flavor """
    chplan = subparser.add_parser(
        'change',
        aliases=['pl'],
        help='Change billing plan'
    )
    chplan.add_argument(
        'server_id',
        type=str,
        help='UUID of virtual machine. You can specify VM tag instead.'
    )
    chplan.add_argument(
        'flavor',
        type=str,
        help='Flavor name. You can specify... '
             'g-1gb, g-2gb, g-4gb, g-8gb, g-16gb, g-32gb, g-64gb'
    )
    chplan.set_defaults(func=change_plan)
    return parser.parse_args(), parser.print_help


if __name__ == '__main__':
    cmd = cmd.ConoHaCmd(confname='./src/conf/conohactl.conf')
    args, print_help = getargs()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        print_help()
    exit(0)
