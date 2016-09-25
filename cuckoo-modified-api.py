#
# Imports
#
import requests
import os
import CuckooExceptions


#
# The Main Function
#
def main():
    """
    Main function for this library
    """
    print("This is a library and not a script.  It cannot be run as a script.")
    pass


#
# Classes
#
class CuckooAPI(object):
    """
    Class to hold Cuckoo API data.
    """
    def __init(self, proto="https", host="127.0.0.1", port="8000"):
        """
        :param proto: http or https
        :param host: Hostname or IP address of Cuckoo server
        :param port: The port of the Cuckoo server
        """
        self.proto = proto
        self.host = host
        self.port = port

    def filecreate(self, filepath):
        """
        Function to submit a local file to Cuckoo for analysis.
        :param filepath: Path to a file to submit.
        :results : Return the task ID of the submission
        """
        # Error if the file does not exist
        if filepath is None or not os.path.exists(filepath):
            raise CuckooExceptions.CuckooFileNotFoundException

        # Build the URL
        apiurl = "{0}://{1}:{2}{3}".format(self.proto, self.host, self.port,
                                           "/api/tasks/create/file/")

#
# Call main if run as a script
#
if __name__ == '__main__':
    main()
