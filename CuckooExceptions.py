#
# Includes
#


#
# Classes
#
class CuckooInvalidFileException(Exception):
    """
    Exception for when a file is not found.
    """
    def __init__(self, filepath):
        Exception.__init__(self, "Cuckoo: Invalid File {0}".format(filepath))
