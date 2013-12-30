def config(args):
    pass


def make(parser):
    """
    config guest, e.g. hostname, network
    """
    parser.set_defaults(
        func=config,
        )
