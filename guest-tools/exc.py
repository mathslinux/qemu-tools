class GToolsError(Exception):
    """
    Unknown gtools error
    """

    def __str__(self):
        doc = self.__doc__.strip()
        return ': '.join([doc] + [str(a) for a in self.args])


class ArgumentError(Exception):
    """Argument error"""


class OpenError(Exception):
    """Open error"""
