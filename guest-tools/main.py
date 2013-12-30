#!/usr/bin/python

"""
A script for handling files in virtual machine image, e.g.

guest-tool img open file.img
guest-tool img ls
guest-tool img rootfs /dev/nbd0p5 --is-lvm true
guest-tool img close
guest-tool file cat /home/vm/foo.txt
guest-tool file rm /home/vm/foo.txt
guest-tool config network static --ip 192.168.1.25
guest-tool config network dhcp
guest-tool config network mac 00:15:65:45:23:45
guest-tool config hostname foo
guest-tool config ls

"""

import sys
import argparse
import pkg_resources


def create_parser():
    parser = argparse.ArgumentParser(
        prog='guest-tools',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Convenient tools for qemu guest image\n\n',
        )
    sub = parser.add_subparsers(
        title='Commands',
        metavar='COMMAND',
        help='description',
        )
    entry_points = [
        (e.name, e.load()) for e in pkg_resources.iter_entry_points('command')
    ]
    for (name, fn) in entry_points:
        p = sub.add_parser(
            name,
            description=fn.__doc__,
            help=fn.__doc__,
        )
        fn(p)
    return parser


def main():
    parser = create_parser()
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit()
    else:
        args = parser.parse_args()

    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
