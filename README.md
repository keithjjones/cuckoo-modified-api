# Build Status

| Master | Devel |
|--------|-------|
| [![Build Status](https://travis-ci.org/keithjjones/cuckoo-modified-api.svg?branch=master)](https://travis-ci.org/keithjjones/cuckoo-modified-api) | [![Build Status](https://travis-ci.org/keithjjones/cuckoo-modified-api.svg?branch=devel)](https://travis-ci.org/keithjjones/cuckoo-modified-api) |


# cuckoo-modified-api
A Python library to interface with a cuckoo-modified instance

This library interfaces with the Cuckoo malware sandbox at:

https://github.com/spender-sandbox/cuckoo-modified

This library can be used either with the Django web front end
or the api.py script in utils.

# Installation:

```
pip install git+https://github.com/keithjjones/cuckoo-modified-api.git
```
...or...
```
pip install cuckoo-modified-api
```

# Usage:
You can load this module like any other module.  As an example to submit a sample to Cuckoo:
```
Python 2.7.12 (v2.7.12:d33e0cf91556, Jun 27 2016, 15:24:40) [MSC v.1500 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import CuckooAPI
>>> api = CuckooAPI.CuckooAPI("10.0.0.144")
>>> api.submitfile("malware.exe")
{u'url': [u'http://example.tld/submit/status/3/'], u'data': {u'task_ids': [3], u'message': u'Task ID 3 has been submitted'}, u'error': False}
>>>
```

More information about each function call is below.  This is the standard Django web interface API.

You can also interface with the api.py script, if you don't have Django running for example, 
from Cuckoo by setting the following API characteristics:
```
Python 2.7.12 (v2.7.12:d33e0cf91556, Jun 27 2016, 15:24:40) [MSC v.1500 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import CuckooAPI
>>> api = CuckooAPI.CuckooAPI("10.0.0.144", APIPY=True, port=8090)
```

# Documentation
```
Help on module CuckooAPI:

NAME
    CuckooAPI

FILE
    c:\source\cuckoo-modified-api\cuckooapi.py

DESCRIPTION
    # Imports
    #

CLASSES
    __builtin__.object
        CuckooAPI

    class CuckooAPI(__builtin__.object)
     |  Class to hold Cuckoo API data.
     |
     |  Methods defined here:
     |
     |  __init__(self, host='127.0.0.1', port=8000, proto='http', APIPY=False)
     |      :param host: Hostname or IP address of Cuckoo server
     |      :param port: The port of the Cuckoo server
     |      :param proto: http or https
     |      :param APIPY: Set to true to submit to api.py on the server
     |
     |  droppeddownload(self, taskid=None, filepath=None)
     |      Download files dropped by sample identified by task ID.
     |      :param taskid: The task ID of the sample.
     |      :param filepath: The file path of the file to create/download.
     |      :returns : Nothing
     |
     |  fileview(self, hashid=None, hashtype=None)
     |      View the details for the file given the hash.
     |      :param hashid: The hash or task ID to search.
     |      :param hashtype: The following types of hash:
     |      'taskid', 'md5', 'sha256'.  Any other values will cause
     |      an error!
     |      :returns : Returns the results of the file in a dict.
     |
     |  fullmemdownload(self, taskid=None, filepath=None)
     |      Download SuriFiles for the sample identified by task ID.
     |      :param taskid: The task ID of the sample.
     |      :param filepath: The file path of the file to create/download.
     |      :returns : Nothing
     |
     |  getcuckoostatus(self)
     |      Function to get the status of the Cuckoo instance.
     |      :returns : Returns the status as a dictionary.
     |
     |  listmachines(self)
     |      Lists the machines available for analysis.
     |      :returns : Returns the list of machines as a list.
     |
     |  pcapdownload(self, taskid=None, filepath=None)
     |      Download a pcap by task ID.
     |      :param taskid: The task ID to download the pcap.
     |      :returns : Nothing
     |
     |  procmemdownload(self, taskid=None, filepath=None, pid=None)
     |      Download SuriFiles for the sample identified by task ID.
     |      :param taskid: The task ID of the sample.
     |      :param filepath: The file path of the file to create/download.
     |      :param pid: Process ID to download
     |      :returns : Nothing
     |
     |  sampledownload(self, hashid=None, hashtype=None, filepath=None)
     |      Download a file by hash.
     |      :param hashid: The hash used to download the sample.
     |      :param hashtype: The hash type, can be "task", "md5", sha1",
     |      or "sha256".  "task" means the task ID.
     |      :returns : Nothing
     |
     |  submitfile(self, filepath, data=None)
     |      Function to submit a local file to Cuckoo for analysis.
     |      :param filepath: Path to a file to submit.
     |      :param data: This is data containing any other options for the
     |      submission form.  This is a dict of values accepted by the
     |      create file options in the cuckoo-modified API.  More form information
     |      can be found in the following link:
     |      https://github.com/spender-sandbox/cuckoo-modified/blob/master/docs/book/src/usage/api.rst
     |      :returns : Returns the json results of the submission
     |
     |  submiturl(self, url, data=None)
     |      Function to submit a URL to Cuckoo for analysis.
     |      :param url: URL to submit.
     |      :param data: This is data containing any other options for the
     |      submission form.  This is a dict of values accepted by the
     |      create file options in the cuckoo-modified API.  More form information
     |      can be found in the following link:
     |      https://github.com/spender-sandbox/cuckoo-modified/blob/master/docs/book/src/usage/api.rst
     |      :returns : Returns the json results of the submission
     |
     |  surifilesdownload(self, taskid=None, filepath=None)
     |      Download SuriFiles for the sample identified by task ID.
     |      :param taskid: The task ID of the sample.
     |      :param filepath: The file path of the file to create/download.
     |      :returns : Nothing
     |
     |  taskdelete(self, taskid=None)
     |      Delete a task.
     |      :param taskid: The task ID to delete.
     |      :returns : Status
     |
     |  taskiocs(self, taskid=None, detailed=False)
     |      View the task IOCs for the task ID.
     |      :param taskid: The ID of the task to view.
     |      :param detailed: Set to true for detailed IOCs.
     |      :returns : Returns a dict of task details.
     |
     |  taskreport(self, taskid=None, reportformat='json')
     |      View the report for the task ID.
     |      :param taskid: The ID of the task to report.
     |      :param reportformat: Right now only json is supported.
     |      :returns : Returns a dict report for the task.
     |
     |  taskscreenshots(self, taskid=None, filepath=None, screenshot=None)
     |      Download screenshot(s).
     |      :param taskid: The task ID for the screenshot(s).
     |      :param filepath: Where to save the screenshot(s).
     |      If you are using the Django web api the screenshots
     |      are saved as .tar.bz!
     |      If you are using the api.py script the screenshots are in .zip
     |      format.
     |      This function adds the apppropriate file extensions to the
     |      filepath variable.
     |      :param screenshot: The screenshot number to download.
     |      :returns : Nothing
     |
     |  tasksearch(self, hashid=None, hashtype=None)
     |      View information about a specific task by hash.
     |      :param hashid: MD5, SHA1, or SHA256 hash to search.
     |      :param hashtype: 'md5', 'sha1', or 'sha256'
     |      :returns : Returns a dict with results.
     |
     |  taskslist(self, limit=None, offset=None)
     |      Lists the tasks in the Cuckoo DB.
     |      :param limit: Limit to this many results (Optional)
     |      :param offset: Offset the output to offset in the total task list
     |      and requires limit above. (Optional)
     |      :returns : Returns a list of task details.
     |
     |  taskstatus(self, taskid=None)
     |      View the task status for the task ID.
     |      :param taskid: The ID of the task to view.
     |      :returns : Returns a dict of task details.
     |
     |  taskview(self, taskid=None)
     |      View the task for the task ID.
     |      :param taskid: The ID of the task to view.
     |      :returns : Returns a dict of task details.
     |
     |  viewmachine(self, vmname=None)
     |      Lists the details about an analysis machine.
     |      :param vmname: The vm name for the machine to be listed
     |      :returns : Returns the dictionary of the machine specifics
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables (if defined)
     |
     |  __weakref__
     |      list of weak references to the object (if defined)

FUNCTIONS
    buildapiurl(proto='http', host='127.0.0.1', port=8000, action=None, APIPY=False)
        Create a URL for the Cuckoo API
        :param proto: http or https
        :param host: Hostname or IP address
        :param port: The port of the Cuckoo API server
        :param action: The action to perform with the API

    main()
        Main function for this library
```

# Resources:

Documentation can be found at the following links:

  - Api.py:
  	- https://github.com/spender-sandbox/cuckoo-modified/blob/master/docs/book/src/usage/api.rst
  - Django Web Front End:
  	- Navigate to a running cuckoo-modified instance and click on "API" in the upper menu bar.
  - Mock testing library:
  	- http://mock.readthedocs.io/en/latest/
  	- https://realpython.com/blog/python/testing-third-party-apis-with-mocks/
  - Nose2 testing library:
  	- http://nose2.readthedocs.io/en/latest/
  - Setup information:
  	- http://stackoverflow.com/questions/14399534/how-can-i-reference-requirements-txt-for-the-install-requires-kwarg-in-setuptool
  	- http://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/creation.html

# License:

This application is covered by the Creative Commons BY-SA license.

- https://creativecommons.org/licenses/by-sa/4.0/
- https://creativecommons.org/licenses/by-sa/4.0/legalcode

# Contributing:

If you would like to contribute you can fork this repository, make your changes, and
then send me a pull request to my "devel" branch.

# To Do:
  - Extended Task Search
  - Reschedule Task