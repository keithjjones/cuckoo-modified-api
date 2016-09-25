#
# Includes
#


#
# Classes
#
class CuckooFileNotFoundException(Exception):
    """
    Exception for when a file is not found.
    """
    def __init__(self, filepath):
        Exception.__init__(self, "Cuckoo: File Not Found {0}".format(filepath))
