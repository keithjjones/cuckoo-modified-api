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
def buildapiurl(proto="http", host="127.0.0.1", port=8000,
                action=None, APIPY=False):
    """
    Create a URL for the Cuckoo API
    :param proto: http or https
    :param host: Hostname or IP address
    :param port: The port of the Cuckoo API server
    :param action: The action to perform with the API
    """
    if action is None:
        return None
    else:
        if APIPY is True:
            return "{0}://{1}:{2}{3}".format(proto, host, port, action)
        else:
            return "{0}://{1}:{2}/api{3}/".format(proto, host, port, action)


#
# Classes
#
class CuckooAPI(object):
    """
    Class to hold Cuckoo API data.
    """
    def __init__(self, host="127.0.0.1", port=8000, proto="http",
                 APIPY=False):
        """
        :param host: Hostname or IP address of Cuckoo server
        :param port: The port of the Cuckoo server
        :param proto: http or https
        :param APIPY: Set to true to submit to api.py on the server
        """
        self.proto = proto
        self.host = host
        self.port = port
        self.APIPY = APIPY

    def submitfile(self, filepath, data=None):
        """
        Function to submit a local file to Cuckoo for analysis.
        :param filepath: Path to a file to submit.
        :param data: This is data containing any other options for the
        submission form.  This is a dict of values accepted by the
        create file options in the cuckoo-modified API.  More form information
        can be found int the following link:
        https://github.com/spender-sandbox/cuckoo-modified/blob/master/docs/book/src/usage/api.rst
        :results : Returns the json results of the submission
        """
        # Error if the file does not exist
        if (filepath is None or not os.path.exists(filepath) or
                not os.path.isfile(filepath)):
            raise CuckooExceptions.CuckooAPIInvalidFileException(filepath)

        # Build the URL
        apiurl = buildapiurl(self.proto, self.host, self.port,
                             "/tasks/create/file", self.APIPY)

        with open(filepath, "rb") as sample:
            multipart_file = {"file": ("temp_file_name", sample)}
            request = requests.post(apiurl, files=multipart_file, data=data)

        # ERROR CHECK request.status_code!
        if request.status_code == 200:
            jsonreply = json.loads(request.text)
            return jsonreply
        else:
            raise CuckooExceptions.CuckooAPIBadRequest(apiurl)

    def getcuckoostatus(self):
        """
        Function to get the status of the Cuckoo instance.
        :results : Returns the status as a dictionary.
        """
        # Build the URL
        apiurl = buildapiurl(self.proto, self.host, self.port,
                             "/cuckoo/status", self.APIPY)

        request = requests.get(apiurl)

        # ERROR CHECK request.status_code!
        if request.status_code == 200:
            jsonreply = json.loads(request.text)
            return jsonreply
        else:
            raise CuckooExceptions.CuckooAPIBadRequest(apiurl)

    def listmachines(self):
        """
        Lists the machines available for analysis.
        :results : Returns the list of machines as a list.
        """
        # Build the URL
        apiurl = buildapiurl(self.proto, self.host, self.port,
                             "/machines/list", self.APIPY)
        request = requests.get(apiurl)

        # ERROR CHECK request.status_code!
        if request.status_code == 200:
            jsonreply = json.loads(request.text)
            return jsonreply
        else:
            raise CuckooExceptions.CuckooAPIBadRequest(apiurl)

    def viewmachine(self, vmname=None):
        """
        Lists the details about an analysis machine.
        :param vmname: The vm name for the machine to be listed
        :results : Returns the dictionary of the machine specifics
        """
        # Build the URL
        if vmname is None:
            raise CuckooExceptions.CuckooAPINoVM(vmname)

        apiurl = buildapiurl(self.proto, self.host, self.port,
                             "/machines/view/"+vmname, self.APIPY)
        request = requests.get(apiurl)

        # ERROR CHECK request.status_code!
        if request.status_code == 200:
            jsonreply = json.loads(request.text)
            return jsonreply
        else:
            raise CuckooExceptions.CuckooAPIBadRequest(apiurl)

#
# Call main if run as a script
#
if __name__ == '__main__':
    main()
