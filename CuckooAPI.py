#
# Imports
#
import requests
import json
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
# Static Functions
#
def buildapiurl(proto="https", host="127.0.0.1", port="8000",
                action="/tasks/create/file"):
    """
    Create a URL for the Cuckoo API
    :param proto: http or https
    :param host: Hostname or IP address
    :param port: The port of the Cuckoo API server
    :param action: The action to perform with the API
    """
    return "{0}://{1}:{2}/api/{3}".format(proto, host, port, action)


#
# Classes
#
class CuckooAPI(object):
    """
    Class to hold Cuckoo API data.
    """
    def __init__(self, proto="https", host="127.0.0.1", port="8000"):
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
        :results : Returns the json results of the submission
        """
        # Error if the file does not exist
        if (filepath is None or not os.path.exists(filepath) or
                not os.path.isfile(filepath)):
            raise CuckooExceptions.CuckooInvalidFileException(filepath)

        # Build the URL
        apiurl = buildapiurl(self.proto, self.host, self.port,
                             "/tasks/create/file/")

        with open(filepath, "rb") as sample:
            multipart_file = {"file": ("temp_file_name", sample)}
            request = requests.post(apiurl, files=multipart_file)

        # ERROR CHECK request.status_code!

        jsonreply = json.loads(request.text)
        return jsonreply


#
# Call main if run as a script
#
if __name__ == '__main__':
    main()
