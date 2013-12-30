from ConfigParser import ConfigParser
import os


def network(args):
    print args


def hostname(args):
    print args


def ls(args):
    # TODO: 1. only show what user want to, not all
    # get the mount point from temporary config file, not hard code
    def get_ip(f):
        return '192.168.176.151'

    def get_mac(f):
        return '00:15:65:12:34:56'
    mnt = '/mnt/guest-tools.mnt'
    hostname = ''
    ip = ''
    mac = ''
    # TODO: centos and other OS support
    with open(mnt + '/etc/hostname') as f:
        hostname = f.read().strip('\n')
    with open(mnt + '/etc/network/interfaces') as f:
        ip = get_ip(f)
    with open(mnt + '/etc/udev/rules.d/70-persistent-net.rules') as f:
        mac = get_mac(f)
    out = """
IP address: %s
MAC address: %s
Hostname: %s""" % (ip, mac, hostname)
    print out


def make_network(parser):
    """
    config network:
    guest-tools network --static --ip 192.168.1.25 --mac 00:15:65:45:23:45
    """
    mode = parser.add_mutually_exclusive_group(required=False)
    mode.add_argument(
        '--static',
        action='store_true',
        default=True,
        help='config static IP Address',
    )
    mode.add_argument(
        '--dhcp',
        action='store_true',
        default=False,
        help='config DHCP mode',
    )
    parser.add_argument(
        '--ip',
        metavar='IPAddress',
        help='IP address',
    )
    parser.add_argument(
        '--if',
        metavar='InterfaceType',
        default='eth0',
        help='config interface type, default is "eth0"',
    )
    parser.add_argument(
        '--mac',
        metavar='MacAddress',
        help='config Macaddress',
    )
    parser.set_defaults(func=network)


def make_hostname(parser):
    """
    config hostname:
    guest-tools hostname foo
    """
    parser.add_argument(
        'hostname',
        metavar='HOSTNAME',
        help='config hostname',
    )
    parser.set_defaults(func=hostname)


def make_ls(parser):
    """
    list configuration:
    guest-tools ls network
    """
    parser.add_argument(
        'subcommand',
        metavar='SUBCOMMAND',
        choices=[
            'all',
            'network',
            'hostname',
        ],
        help='all, network, hostname',
        )
    parser.set_defaults(func=ls)
