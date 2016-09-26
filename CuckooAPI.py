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
        :returns : Returns the json results of the submission
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
        :returns : Returns the status as a dictionary.
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
        :returns : Returns the list of machines as a list.
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
        :returns : Returns the dictionary of the machine specifics
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

    def taskslist(self, limit=None, offset=None):
        """
        Lists the tasks in the Cuckoo DB.
        :param limit: Limit to this many results (Optional)
        :param offset: Offset the output to offset in the total task list
        and requires limit above. (Optional)
        :returns : Returns a list of task details.
        """
        # Build the URL
        baseurl = "/tasks/list"
        if limit is not None:
            baseurl = baseurl+"/"+str(limit)
            if offset is not None:
                baseurl = baseurl+"/"+str(offset)

        apiurl = buildapiurl(self.proto, self.host, self.port,
                             baseurl, self.APIPY)
        request = requests.get(apiurl)

        # ERROR CHECK request.status_code!
        if request.status_code == 200:
            jsonreply = json.loads(request.text)
            return jsonreply
        else:
            raise CuckooExceptions.CuckooAPIBadRequest(apiurl)

    def taskview(self, taskid=None):
        """
        View the task for the task ID.
        :param taskid: The ID of the task to view.
        :returns : Returns a dict of task details.
        """
        # Build the URL
        if taskid is None or taskid < 1:
            raise CuckooExceptions.CuckooAPINoTaskID(taskid)

        apiurl = buildapiurl(self.proto, self.host, self.port,
                             "/tasks/view/"+str(taskid), self.APIPY)

        request = requests.get(apiurl)

        # ERROR CHECK request.status_code!
        if request.status_code == 200:
            jsonreply = json.loads(request.text)
            return jsonreply
        else:
            raise CuckooExceptions.CuckooAPIBadRequest(apiurl)

    def taskreport(self, taskid=None, reportformat="json"):
        """
        View the report for the task ID.
        :param taskid: The ID of the task to report.
        :param reportformat: Right now only json is supported.
        :returns : Returns a dict report for the task.
        """
        # Build the URL
        if taskid is None or taskid < 1:
            raise CuckooExceptions.CuckooAPINoTaskID(taskid)

        if self.APIPY is True:
            apiurl = buildapiurl(self.proto, self.host, self.port,
                                 "/tasks/report/"+str(taskid)+"/"+reportformat,
                                 self.APIPY)
        else:
            apiurl = buildapiurl(self.proto, self.host, self.port,
                                 "/tasks/get/report/"+str(taskid)+"/" +
                                 reportformat, self.APIPY)

        # Error on any other format for now...
        if reportformat != "json":
            raise CuckooExceptions.CuckooAPINotImplemented(apiurl)

        request = requests.get(apiurl)

        # ERROR CHECK request.status_code!
        if request.status_code == 200:
            jsonreply = json.loads(request.text)
            return jsonreply
        else:
            raise CuckooExceptions.CuckooAPIBadRequest(apiurl)

    def fileview(self, hashid=None, hashtype=None):
        """
        View the details for the file given the hash.
        :param hashid: The hash or task ID to search.
        :param hashtype: The following types of hash:
        'taskid', 'md5', 'sha256'.  Any other values will cause
        an error!
        :returns : Returns the results of the file in a dict.
        """
        # Build the URL
        if hashid is None:
            raise CuckooExceptions.CuckooAPINoHash(hashid, hashtype)

        apiurl = buildapiurl(self.proto, self.host, self.port,
                             "/files/view/"+str(hashtype)+"/"+hashid,
                             self.APIPY)

        # This appears to be unavailable in the documentation...
        if self.APIPY is True and hashtype == "sha1":
            raise CuckooExceptions.CuckooAPINotAvailable(apiurl)

        # This appears to be unavailable in the documentation...
        if hashtype != "md5" and hashtype != "sha1" and hashtype != "sha256":
            raise CuckooExceptions.CuckooAPINotAvailable(apiurl)

        request = requests.get(apiurl)

        # ERROR CHECK request.status_code!
        if request.status_code == 200:
            jsonreply = json.loads(request.text)
            return jsonreply
        else:
            raise CuckooExceptions.CuckooAPIBadRequest(apiurl)

    def taskdelete(self, taskid=None):
        """
        Delete a task.
        :param taskid: The task ID to delete.
        :returns : Status
        """
        if taskid is None or taskid < 1:
            raise CuckooExceptions.CuckooAPINoTaskID(taskid)

        apiurl = buildapiurl(self.proto, self.host, self.port,
                             "/tasks/delete/"+str(taskid),
                             self.APIPY)

        request = requests.get(apiurl)

        # ERROR CHECK request.status_code!
        if request.status_code == 200:
            jsonreply = json.loads(request.text)
            return jsonreply
        elif request.status_code == 404:
            raise CuckooExceptions.CuckooAPINoTaskID(taskid)
        elif request.status_code == 500:
            raise CuckooExceptions.CuckooAPITaskNoDelete(taskid)
        else:
            raise CuckooExceptions.CuckooAPIBadRequest(apiurl)

    def taskscreenshots(self, taskid=None, filepath=None, screenshot=None):
        """
        Download screenshot(s).
        :param taskid: The task ID for the screenshot(s).
        :param filepath: Where to save the screenshot(s).
        If you are using the Django web api the screenshots
        are saved as .tar.bz!
        If you are using the api.py script the screenshots are in .zip
        format.
        This function adds the apppropriate file extensions to the
        filepath variable.
        :param screenshot: The screenshot number to download.
        :returns : Nothing
        """
        if taskid is None or taskid < 1:
            raise CuckooExceptions.CuckooAPINoTaskID(taskid)

        if filepath is None or os.path.exists(filepath):
            raise CuckooExceptions.CuckooAPIFileExists(filepath)

        if self.APIPY is True:
            filepath = filepath+".zip"
        else:
            filepath = filepath+".tar.bz"

        if self.APIPY is True:
            baseurl = "/tasks/screenshots/"+str(taskid)
            if screenshot is not None:
                baseurl = baseurl+"/"+str(screenshot)
        else:
            baseurl = "/tasks/get/screenshot/"+str(taskid)
            if screenshot is not None:
                baseurl = baseurl+"/"+str(screenshot)

        apiurl = buildapiurl(self.proto, self.host, self.port,
                             baseurl,
                             self.APIPY)

        # Turn on stream to download files
        request = requests.get(apiurl, stream=True)

        # ERROR CHECK request.status_code!
        if request.status_code == 200:
            with open(filepath, 'wb') as f:
                # Read and write in chunks
                for chunk in request.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        else:
            raise CuckooExceptions.CuckooAPIBadRequest(apiurl)


#
# Call main if run as a script
#
if __name__ == '__main__':
    main()
