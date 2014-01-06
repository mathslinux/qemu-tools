#!/usr/bin/python

"""
A script for handling files in virtual machine image, e.g.

guest-tool img open file.img
guest-tool img ls
guest-tool img rootfs /dev/nbd0p5 --is-lvm true
guest-tool img close
guest-tool file cat /home/vm/foo.txt
guest-tool file rm /home/vm/foo.txt
guest-tool config network --static --ip 192.168.1.25 --mac 00:15:65:45:23:45
guest-tool config hostname foo
guest-tool list network

"""

import sys
import argparse
import pkg_resources
import logging
from functools import wraps
import exc

LOG = logging.getLogger(__name__)


def catches(catch=None, handler=None, exit=True):
    catch = catch or Exception
    logger = logging.getLogger('gtools')

    def decorate(f):
        @wraps(f)
        def newfunc(*a, **kw):
            try:
                return f(*a, **kw)
            except catch as e:
                if handler:
                    return handler(e)
                else:
                    logger.error(make_exception_message(e))
                    if exit:
                        sys.exit(1)
        return newfunc

    return decorate


def make_exception_message(exc):
    """
    An exception is passed in and this function
    returns the proper string depending on the result
    so it is readable enough.
    """
    if str(exc):
        return '%s: %s\n' % (exc.__class__.__name__, exc)
    else:
        return '%s\n' % (exc.__class__.__name__)


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


def set_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(name)s] [%(levelname)s] %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

@catches((KeyboardInterrupt, RuntimeError, exc.GToolsError,))
def main():
    parser = create_parser()
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit()
    else:
        args = parser.parse_args()

    set_logger()

    return args.func(args)

if __name__ == '__main__':
    sys.exit(main())
