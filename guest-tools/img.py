import exc
import commands
from ConfigParser import ConfigParser
import os


def img_open(args):
    # TODO: check nbd module and arguments
    if len(args.values) != 1:
        raise exc.ArgumentError('missing image file')
    else:
        img_file = args.values[0]

    # TODO: do not hardcode, do not use print directly
    cmd = 'qemu-nbd -c /dev/nbd0 %s' % img_file
    (status, out) = commands.getstatusoutput(cmd)
    if status != 0:
        raise exc.OpenError(out)
    else:
        p = ConfigParser()
        p.add_section('global')
        p.set('global', 'file', img_file)
        p.set('global', 'device', '/dev/nbd0')
        p.write(open('/tmp/guest-tools.tmp', 'w'))
        img_ls(None)


def img_ls(args):
    cmd = 'parted -s /dev/nbd0 print'
    (status, out) = commands.getstatusoutput(cmd)
    print out


def img_rootfs(args):
    if len(args.values) != 1:
        raise exc.ArgumentError('missing image file')
    else:
        rootfs = args.values[0]
    p = ConfigParser()
    p.read('/tmp/guest-tools.tmp')
    p.set('global', 'rootfs', rootfs)
    if args.lvm:
        p.set('global', 'lvm', args.lvm)
    p.write(open('/tmp/guest-tools.tmp', 'w'))

    # mount it, TODO: remove hard code
    if not os.path.exists('/mnt/guest-tools.mnt'):
        os.mkdir('/mnt/guest-tools.mnt')
    if args.lvm:
        # update lvm metadata
        os.system('vgchange -ay %s' % args.lvm)
        os.system('mount /dev/%s/root /mnt/guest-tools.mnt' % args.lvm)
    else:
        os.system('mount %s /mnt/guest-tools.mnt' % (rootfs))


def img_close(args):
    # TODO: remove hard code
    if os.path.exists('/tmp/guest-tools.tmp'):
        os.system('umount /mnt/guest-tools.mnt')
        p = ConfigParser()
        p.read('/tmp/guest-tools.tmp')
        if p.has_option('global', 'lvm'):
            vg = p.get('global', 'lvm')
            os.system('vgchange -an %s' % vg)
        os.system('qemu-nbd -d /dev/nbd0')
        os.remove('/tmp/guest-tools.tmp')


def img(args):
    """
    guest-tool img open --file file.img
    guest-tool img ls
    guest-tool img rootfs --root /dev/nbd0p5 --lvm true
    guest-tool img close
    """
    if args.subcommand == 'open':
        img_open(args)
    elif args.subcommand == 'ls':
        img_ls(args)
    elif args.subcommand == 'rootfs':
        img_rootfs(args)
    elif args.subcommand == 'close':
        img_close(args)


def make(parser):
    """
    open/close guest image
    """
    parser.add_argument(
        'subcommand',
        metavar='SUBCOMMAND',
        choices=[
            'open',
            'ls',
            'rootfs',
            'close'
            ],
        help='open, ls, rootfs, close',
        )
    parser.add_argument(
        '--lvm',
        help='if rootfs is type of lvm, give the vgname',
        )
    parser.add_argument(
        'values',
        nargs='*',
        help='argument passed to subcommand',
        )
    parser.set_defaults(
        func=img,
        )
