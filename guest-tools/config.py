import logging

LOG = logging.getLogger(__name__)
MNT = '/mnt/guest-tools.mnt'


class DebianFamily(object):
    host_file = MNT + '/etc/hostname'
    ip_file = MNT + '/etc/network/interfaces'
    mac_file = MNT + '/etc/udev/rules.d/70-persistent-net.rules'

    def get_hostname(self):
        try:
            with open(self.host_file) as f:
                return f.read().strip('\n')
        except IOError:
            LOG.warn('%s not found' % (self.host_file))
            return ''

    def get_ip(self):
        """ Not implement"""
        return ''

    def get_mac(self):
        """Not implement"""
        return ''


def network(args):
    print args


def hostname(args):
    print args


def ls(args):
    # TODO: donot hard code os type
    g = DebianFamily()
    if args.subcommand == 'all':
        print "Hostname: %s\nIP address: %s\nMAC address: %s\n" \
            % (g.get_hostname(), g.get_ip(), g.get_mac())
    elif args.subcommand == 'network':
        print "IP address: %s\nMAC address: %s\n" % (g.get_ip(), g.get_mac())
    elif args.subcommand == 'hostname':
        print "Hostname: %s\n" % (g.get_hostname())


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
