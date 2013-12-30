def vm_file(args):
    pass


def make(parser):
    """
    Process files in guest image.
    """
    parser.set_defaults(
        func=vm_file,
        )
