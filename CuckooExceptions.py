#
# Includes
#


#
# Classes
#
class CuckooAPIInvalidFileException(Exception):
    """
    Exception for when a file is not found.
    """
    def __init__(self, filepath):
        Exception.__init__(self, "CuckooAPI: Invalid File {0}".format(
                           filepath))


class CuckooAPINotImplemented(Exception):
    """
    Exception for when a call is not implemented, but is available.
    """
    def __init__(self, apicall):
        Exception.__init__(self,
                           "CuckooAPI: Not Implemented {}".format(apicall))


class CuckooAPINotAvailable(Exception):
    """
    Exception for when a call is not available on the remote server.
    This signifies you may have used an API call meant for the Django
    interface and sent it to the api.py interface, or vice versa.
    """
    def __init__(self, apicall):
        Exception.__init__(self, "CuckooAPI: This API is not available for "
                           "your target Cuckoo server.  Are you mixing "
                           "calls from Django web interface with the "
                           "api.py interface?  Or the other way around?")


class CuckooAPIBadRequest(Exception):
    """
    Exception for when a Cuckoo machine is not found.
    """
    def __init__(self, apiurl):
        Exception.__init__(self, "CuckooAPI:  Unable to connect "
                           "with URL {0}  Are you mixing "
                           "calls from Django web interface with the "
                           "api.py interface?  Or the other way "
                           "around?".format(apiurl))


class CuckooAPINoVM(Exception):
    """
    Exception for when a vm is not found.
    """
    def __init__(self, vmname):
        Exception.__init__(self, "CuckooAPI:  VM {0} not available or valid!"
                           .format(vmname))


class CuckooAPINoTaskID(Exception):
    """
    Exception for when an invalid task ID is used.
    """
    def __init__(self, taskid):
        Exception.__init__(self, "CuckooAPI:  Task ID {0} not avilable or "
                           "valid!".format(taskid))


class CuckooAPINoHash(Exception):
    """
    Exception for when an invalid file hash is used.
    """
    def __init__(self, hashid, hashtype):
        Exception.__init__(self, "CuckooAPI:  Hash {0} of type {1} not "
                           "available or valid!".format(hashid, hashtype))
