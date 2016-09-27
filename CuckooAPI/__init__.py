#
# Imports
#
import requests
import json
import os


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

    def getcuckoostatus(self):
        """
        Function to get the status of the Cuckoo instance.
        :return: Returns the status as a dictionary.
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
            raise CuckooAPIBadRequest(apiurl)

    def listmachines(self):
        """
        Lists the machines available for analysis.
        :return: Returns the list of machines as a list.
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
            raise CuckooAPIBadRequest(apiurl)

    def viewmachine(self, vmname=None):
        """
        Lists the details about an analysis machine.
        :param vmname: The vm name for the machine to be listed
        :return: Returns the dictionary of the machine specifics
        """
        # Build the URL
        if vmname is None:
            raise CuckooAPINoVM(vmname)

        apiurl = buildapiurl(self.proto, self.host, self.port,
                             "/machines/view/"+vmname, self.APIPY)
        request = requests.get(apiurl)

        # ERROR CHECK request.status_code!
        if request.status_code == 200:
            jsonreply = json.loads(request.text)
            return jsonreply
        else:
            raise CuckooAPIBadRequest(apiurl)

    def taskslist(self, limit=None, offset=None):
        """
        Lists the tasks in the Cuckoo DB.
        :param limit: Limit to this many results (Optional)
        :param offset: Offset the output to offset in the total task list
        and requires limit above. (Optional)
        :return: Returns a list of task details.
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
            raise CuckooAPIBadRequest(apiurl)

    def taskview(self, taskid=None):
        """
        View the task for the task ID.
        :param taskid: The ID of the task to view.
        :return: Returns a dict of task details.
        """
        # Build the URL
        if taskid is None or taskid < 1:
            raise CuckooAPINoTaskID(taskid)

        apiurl = buildapiurl(self.proto, self.host, self.port,
                             "/tasks/view/"+str(taskid), self.APIPY)

        request = requests.get(apiurl)

        # ERROR CHECK request.status_code!
        if request.status_code == 200:
            jsonreply = json.loads(request.text)
            return jsonreply
        else:
            raise CuckooAPIBadRequest(apiurl)

    def taskstatus(self, taskid=None):
        """
        View the task status for the task ID.
        :param taskid: The ID of the task to view.
        :return: Returns a dict of task details.
        """
        # Build the URL
        if taskid is None or taskid < 1:
            raise CuckooAPINoTaskID(taskid)

        apiurl = buildapiurl(self.proto, self.host, self.port,
                             "/tasks/status/"+str(taskid), self.APIPY)

        # Not available with APIPY
        if self.APIPY is True:
            raise CuckooAPINotAvailable(apiurl)

        request = requests.get(apiurl)

        # ERROR CHECK request.status_code!
        if request.status_code == 200:
            jsonreply = json.loads(request.text)
            return jsonreply
        else:
            raise CuckooAPIBadRequest(apiurl)

    def taskiocs(self, taskid=None, detailed=False):
        """
        View the task IOCs for the task ID.
        :param taskid: The ID of the task to view.
        :param detailed: Set to true for detailed IOCs.
        :return: Returns a dict of task details.
        """
        # Build the URL
        if taskid is None or taskid < 1:
            raise CuckooAPINoTaskID(taskid)

        baseurl = "/tasks/get/iocs/"+str(taskid)
        if detailed is True:
            baseurl = baseurl + "/detailed"

        apiurl = buildapiurl(self.proto, self.host, self.port,
                             baseurl, self.APIPY)

        # Not available with APIPY
        if self.APIPY is True:
            raise CuckooAPINotAvailable(apiurl)

        request = requests.get(apiurl)

        # ERROR CHECK request.status_code!
        if request.status_code == 200:
            jsonreply = json.loads(request.text)
            return jsonreply
        else:
            raise CuckooAPIBadRequest(apiurl)

    def taskreport(self, taskid=None, reportformat="json"):
        """
        View the report for the task ID.
        :param taskid: The ID of the task to report.
        :param reportformat: Right now only json is supported.
        :return: Returns a dict report for the task.
        """
        # Build the URL
        if taskid is None or taskid < 1:
            raise CuckooAPINoTaskID(taskid)

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
            raise CuckooAPINotImplemented(apiurl)

        request = requests.get(apiurl)

        # ERROR CHECK request.status_code!
        if request.status_code == 200:
            jsonreply = json.loads(request.text)
            return jsonreply
        else:
            raise CuckooAPIBadRequest(apiurl)

    def taskdelete(self, taskid=None):
        """
        Delete a task.
        :param taskid: The task ID to delete.
        :return: Status
        """
        if taskid is None or taskid < 1:
            raise CuckooAPINoTaskID(taskid)

        apiurl = buildapiurl(self.proto, self.host, self.port,
                             "/tasks/delete/"+str(taskid),
                             self.APIPY)

        request = requests.get(apiurl)

        # ERROR CHECK request.status_code!
        if request.status_code == 200:
            jsonreply = json.loads(request.text)
            return jsonreply
        elif request.status_code == 404:
            raise CuckooAPINoTaskID(taskid)
        elif request.status_code == 500:
            raise CuckooAPITaskNoDelete(taskid)
        else:
            raise CuckooAPIBadRequest(apiurl)

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
        :return: Nothing
        """
        if taskid is None or taskid < 1:
            raise CuckooAPINoTaskID(taskid)

        if filepath is None or os.path.exists(filepath):
            raise CuckooAPIFileExists(filepath)

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
            raise CuckooAPIBadRequest(apiurl)

    def submitfile(self, filepath, data=None):
        """
        Function to submit a local file to Cuckoo for analysis.
        :param filepath: Path to a file to submit.
        :param data: This is data containing any other options for the
        submission form.  This is a dict of values accepted by the
        create file options in the cuckoo-modified API.  More form information
        can be found in the following link:
        https://github.com/spender-sandbox/cuckoo-modified/blob/master/docs/book/src/usage/api.rst
        :return: Returns the json results of the submission
        """
        # Error if the file does not exist
        if (filepath is None or not os.path.exists(filepath) or
                not os.path.isfile(filepath)):
            raise CuckooAPIInvalidFileException(filepath)

        # Build the URL
        apiurl = buildapiurl(self.proto, self.host, self.port,
                             "/tasks/create/file", self.APIPY)

        with open(filepath, "rb") as sample:
            # multipart_file = {"file": ("temp_file_name", sample)}
            multipart_file = {"file": (os.path.basename(filepath), sample)}
            request = requests.post(apiurl, files=multipart_file, data=data)

        # ERROR CHECK request.status_code!
        if request.status_code == 200:
            jsonreply = json.loads(request.text)
            return jsonreply
        else:
            raise CuckooAPIBadRequest(apiurl)

    def submiturl(self, url, data=None):
        """
        Function to submit a URL to Cuckoo for analysis.
        :param url: URL to submit.
        :param data: This is data containing any other options for the
        submission form.  This is a dict of values accepted by the
        create file options in the cuckoo-modified API.  More form information
        can be found in the following link:
        https://github.com/spender-sandbox/cuckoo-modified/blob/master/docs/book/src/usage/api.rst
        :return: Returns the json results of the submission
        """
        # Build the URL
        apiurl = buildapiurl(self.proto, self.host, self.port,
                             "/tasks/create/url", self.APIPY)

        multipart_url = {"url": ("", url)}
        request = requests.post(apiurl, files=multipart_url, data=data)

        # ERROR CHECK request.status_code!
        if request.status_code == 200:
            jsonreply = json.loads(request.text)
            return jsonreply
        else:
            raise CuckooAPIBadRequest(apiurl)

    def tasksearch(self, hashid=None, hashtype=None):
        """
        View information about a specific task by hash.
        :param hashid: MD5, SHA1, or SHA256 hash to search.
        :param hashtype: 'md5', 'sha1', or 'sha256'
        :return: Returns a dict with results.
        """
        if hashid is None:
            raise CuckooAPINoHash(hashid, hashtype)

        # Build the URL
        apiurl = buildapiurl(self.proto, self.host, self.port,
                             "/files/view/"+hashtype+"/"+hashid,
                             self.APIPY)

        # This appears to be unavailable in the documentation...
        if self.APIPY is True:
            raise CuckooAPINotAvailable(apiurl)

        request = requests.get(apiurl)

        # ERROR CHECK request.status_code!
        if request.status_code == 200:
            jsonreply = json.loads(request.text)
            return jsonreply
        else:
            raise CuckooAPIBadRequest(apiurl)

    def fileview(self, hashid=None, hashtype=None):
        """
        View the details for the file given the hash.
        :param hashid: The hash or task ID to search.
        :param hashtype: The following types of hash:
        'taskid', 'md5', 'sha256'.  Any other values will cause
        an error!
        :return: Returns the results of the file in a dict.
        """
        if hashid is None:
            raise CuckooAPINoHash(hashid, hashtype)

        # Get rid of ints
        hashid = str(hashid)

        # Build the URL
        apiurl = buildapiurl(self.proto, self.host, self.port,
                             "/files/view/"+hashtype+"/"+hashid,
                             self.APIPY)

        # This appears to be unavailable in the documentation...
        if self.APIPY is True and hashtype == "sha1":
            raise CuckooAPINotAvailable(apiurl)

        if hashtype != "md5" and hashtype != "sha1" and hashtype != "sha256":
            raise CuckooAPINotAvailable(apiurl)

        request = requests.get(apiurl)

        # ERROR CHECK request.status_code!
        if request.status_code == 200:
            jsonreply = json.loads(request.text)
            return jsonreply
        else:
            raise CuckooAPIBadRequest(apiurl)

    def sampledownload(self, hashid=None, hashtype=None,
                       filepath=None):
        """
        Download a file by hash.
        :param hashid: The hash used to download the sample.
        :param hashtype: The hash type, can be "task", "md5", sha1",
        or "sha256".  "task" means the task ID.
        :return: Nothing
        """
        # Get rid of ints
        hashid = str(hashid)

        if hashid is None or hashtype is None:
            raise CuckooAPINoHash(hashid, hashtype)

        if filepath is None or os.path.exists(filepath):
            raise CuckooAPIFileExists(filepath)

        if self.APIPY is True:
            baseurl = "/files/get/"+hashid
        else:
            baseurl = "/files/get/"+hashtype+"/"+hashid

        apiurl = buildapiurl(self.proto, self.host, self.port,
                             baseurl,
                             self.APIPY)

        if hashtype != "sha256" and self.APIPY is True:
            raise CuckooAPINotAvailable(apiurl)

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
            raise CuckooAPIBadRequest(apiurl)

    def pcapdownload(self, taskid=None, filepath=None):
        """
        Download a pcap by task ID.
        :param taskid: The task ID to download the pcap.
        :return: Nothing
        """
        if taskid is None or taskid < 1:
            raise CuckooAPINoTaskID(taskid)

        if filepath is None or os.path.exists(filepath):
            raise CuckooAPIFileExists(filepath)

        if self.APIPY is True:
            baseurl = "/pcap/get/"+str(taskid)
        else:
            baseurl = "/tasks/get/pcap/"+str(taskid)

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
            raise CuckooAPIBadRequest(apiurl)

    def droppeddownload(self, taskid=None, filepath=None):
        """
        Download files dropped by sample identified by task ID.
        :param taskid: The task ID of the sample.
        :param filepath: The file path of the file to create/download.
        :return: Nothing
        """
        if taskid is None or taskid < 1:
            raise CuckooAPINoTaskID(taskid)

        if filepath is None or os.path.exists(filepath):
            raise CuckooAPIFileExists(filepath)

        baseurl = "/tasks/get/dropped/"+str(taskid)

        apiurl = buildapiurl(self.proto, self.host, self.port,
                             baseurl,
                             self.APIPY)

        if self.APIPY is True:
            raise CuckooAPINotAvailable(apiurl)

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
            raise CuckooAPIBadRequest(apiurl)

    def surifilesdownload(self, taskid=None, filepath=None):
        """
        Download SuriFiles for the sample identified by task ID.
        :param taskid: The task ID of the sample.
        :param filepath: The file path of the file to create/download.
        :return: Nothing
        """
        if taskid is None or taskid < 1:
            raise CuckooAPINoTaskID(taskid)

        if filepath is None or os.path.exists(filepath):
            raise CuckooAPIFileExists(filepath)

        baseurl = "/tasks/get/surifile/"+str(taskid)

        apiurl = buildapiurl(self.proto, self.host, self.port,
                             baseurl,
                             self.APIPY)

        if self.APIPY is True:
            raise CuckooAPINotAvailable(apiurl)

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
            raise CuckooAPIBadRequest(apiurl)

    def fullmemdownload(self, taskid=None, filepath=None):
        """
        Download SuriFiles for the sample identified by task ID.
        :param taskid: The task ID of the sample.
        :param filepath: The file path of the file to create/download.
        :return: Nothing
        """
        if taskid is None or taskid < 1:
            raise CuckooAPINoTaskID(taskid)

        if filepath is None or os.path.exists(filepath):
            raise CuckooAPIFileExists(filepath)

        baseurl = "/tasks/get/fullmemory/"+str(taskid)

        apiurl = buildapiurl(self.proto, self.host, self.port,
                             baseurl,
                             self.APIPY)

        if self.APIPY is True:
            raise CuckooAPINotAvailable(apiurl)

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
            raise CuckooAPIBadRequest(apiurl)

    def procmemdownload(self, taskid=None, filepath=None, pid=None):
        """
        Download SuriFiles for the sample identified by task ID.
        :param taskid: The task ID of the sample.
        :param filepath: The file path of the file to create/download.
        :param pid: Process ID to download
        :return: Nothing
        """
        if taskid is None or taskid < 1:
            raise CuckooAPINoTaskID(taskid)

        if filepath is None or os.path.exists(filepath):
            raise CuckooAPIFileExists(filepath)

        baseurl = "/tasks/get/procmemory/"+str(taskid)
        if pid is not None:
            baseurl = baseurl+"/"+str(pid)

        apiurl = buildapiurl(self.proto, self.host, self.port,
                             baseurl,
                             self.APIPY)

        if self.APIPY is True:
            raise CuckooAPINotAvailable(apiurl)

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
            raise CuckooAPIBadRequest(apiurl)


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
        Exception.__init__(self, "CuckooAPI:  VM {0} not available or invalid!"
                           .format(vmname))


class CuckooAPINoTaskID(Exception):
    """
    Exception for when an invalid task ID is used.
    """
    def __init__(self, taskid):
        Exception.__init__(self, "CuckooAPI:  Task ID {0} not avilable or "
                           "invalid!".format(taskid))


class CuckooAPITaskNoDelete(Exception):
    """
    Exception for when a task cannot be deleted.
    """
    def __init__(self, taskid):
        Exception.__init__(self, "CuckooAPI: Task ID {0} cannot be "
                           "deleted!".format(taskid))


class CuckooAPINoHash(Exception):
    """
    Exception for when an invalid file hash is used.
    """
    def __init__(self, hashid, hashtype):
        Exception.__init__(self, "CuckooAPI:  Hash {0} of type {1} not "
                           "available or invalid!".format(hashid, hashtype))


class CuckooAPIFileExists(Exception):
    """
    Exception for when a file is about to be saved over an existing file
    or the file name is invalid.
    """
    def __init__(self, filepath):
        Exception.__init__(self, "CuckooAPI: {0} already exists or "
                           "is invalid!".format(filepath))

#
# Call main if run as a script
#
if __name__ == '__main__':
    main()
