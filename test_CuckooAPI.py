#
# Headers
#
import CuckooAPI
import mock
import os


def test_submitfile_directory_exception():
    """
    Test that a directory throws error
    """
    api = CuckooAPI.CuckooAPI()
    ExceptionThrown = False
    try:
        api.submitfile('.')
    except CuckooAPI.CuckooExceptions.CuckooAPIInvalidFileException:
        ExceptionThrown = True

    assert ExceptionThrown is True


@mock.patch('CuckooAPI.requests.post')
def test_submitfile_bad_status_code(mock_get):
    """
    Test that a bad status code throws error
    """
    mock_get.return_value.status_code = 404

    api = CuckooAPI.CuckooAPI()
    ExceptionThrown = False
    try:
        api.submitfile('README.md')
    except CuckooAPI.CuckooExceptions.CuckooAPIBadRequest:
        ExceptionThrown = True

    assert ExceptionThrown is True


@mock.patch('CuckooAPI.requests.post')
def test_submitfile_ok_noapipy(mock_get):
    """
    Test a pretend submission without api.py
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = ('{"url": ["http://example.tld/submit/'
                                  'status/14/"], "data": {"task_ids": [14],'
                                  ' "message": "Task ID 14 has been '
                                  'submitted"}, "error": false}')

    api = CuckooAPI.CuckooAPI()

    response = api.submitfile('README.md')

    assert response['url'][0] == "http://example.tld/submit/status/14/"
    assert response['data']['task_ids'][0] == 14


@mock.patch('CuckooAPI.requests.post')
def test_submitfile_ok_apipy(mock_get):
    """
    Test a pretend submission with api.py
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = ('{"task_ids": [14]}')

    api = CuckooAPI.CuckooAPI(port=8090, APIPY=True)

    response = api.submitfile('README.md')

    assert response['task_ids'][0] == 14


@mock.patch('CuckooAPI.requests.get')
def test_getcuckoostatus_exception(mock_get):
    """
    Test a pretend get status with an exception
    """
    mock_get.return_value.status_code = 404

    api = CuckooAPI.CuckooAPI()

    ExceptionThrown = False

    try:
        api.getcuckoostatus()
    except CuckooAPI.CuckooExceptions.CuckooAPIBadRequest:
        ExceptionThrown = True

    assert ExceptionThrown is True


@mock.patch('CuckooAPI.requests.get')
def test_getcuckoostatus_ok_noapipy(mock_get):
    """
    Test a pretend get status without api.py
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = '{}'

    api = CuckooAPI.CuckooAPI()

    response = api.getcuckoostatus()

    assert response == {}


@mock.patch('CuckooAPI.requests.get')
def test_getcuckoostatus_ok_apipy(mock_get):
    """
    Test a pretend get status with api.py
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = '{}'

    api = CuckooAPI.CuckooAPI(port=8090, APIPY=True)

    response = api.getcuckoostatus()

    assert response == {}


@mock.patch('CuckooAPI.requests.get')
def test_listmachines_exception(mock_get):
    """
    Test a pretend list machines with an exception
    """
    mock_get.return_value.status_code = 404

    api = CuckooAPI.CuckooAPI()

    ExceptionThrown = False

    try:
        api.listmachines()
    except CuckooAPI.CuckooExceptions.CuckooAPIBadRequest:
        ExceptionThrown = True

    assert ExceptionThrown is True


@mock.patch('CuckooAPI.requests.get')
def test_listmachines_ok_noapipy(mock_get):
    """
    Test a pretend list machines without api.py
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = '{}'

    api = CuckooAPI.CuckooAPI()

    response = api.listmachines()

    assert response == {}


@mock.patch('CuckooAPI.requests.get')
def test_listmachines_ok_apipy(mock_get):
    """
    Test a pretend list machines with api.py
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = '{}'

    api = CuckooAPI.CuckooAPI(port=8090, APIPY=True)

    response = api.listmachines()

    assert response == {}


@mock.patch('CuckooAPI.requests.get')
def test_viewmachine_exception(mock_get):
    """
    Test a pretend view machine with exceptions
    """
    mock_get.return_value.status_code = 404

    api = CuckooAPI.CuckooAPI()

    ExceptionThrown = False

    try:
        api.viewmachine()
    except CuckooAPI.CuckooExceptions.CuckooAPINoVM:
        ExceptionThrown = True

    assert ExceptionThrown is True

    ExceptionThrown = False

    try:
        api.viewmachine("cuckoo1")
    except CuckooAPI.CuckooExceptions.CuckooAPIBadRequest:
        ExceptionThrown = True

    assert ExceptionThrown is True


@mock.patch('CuckooAPI.requests.get')
def test_viewmachine_ok_noapipy(mock_get):
    """
    Test a pretend view machine without api.py
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = '{}'

    api = CuckooAPI.CuckooAPI()

    response = api.viewmachine('cuckoo1')

    assert response == {}


@mock.patch('CuckooAPI.requests.get')
def test_viewmachine_ok_apipy(mock_get):
    """
    Test a pretend view machine with api.py
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = '{}'

    api = CuckooAPI.CuckooAPI(port=8090, APIPY=True)

    response = api.viewmachine('cuckoo1')

    assert response == {}


@mock.patch('CuckooAPI.requests.get')
def test_taskslist_exception(mock_get):
    """
    Test a pretend tasks list with exception
    """
    mock_get.return_value.status_code = 404

    api = CuckooAPI.CuckooAPI()

    ExceptionThrown = False

    try:
        api.taskslist()
    except CuckooAPI.CuckooExceptions.CuckooAPIBadRequest:
        ExceptionThrown = True

    assert ExceptionThrown is True


@mock.patch('CuckooAPI.requests.get')
def test_taskslist_ok_noapipy(mock_get):
    """
    Test a pretend tasks list without api.py
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = '{}'

    api = CuckooAPI.CuckooAPI()

    response = api.taskslist('cuckoo1')

    assert response == {}


@mock.patch('CuckooAPI.requests.get')
def test_taskslist_ok_apipy(mock_get):
    """
    Test a pretend tasks list with api.py
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = '{}'

    api = CuckooAPI.CuckooAPI(port=8090, APIPY=True)

    response = api.taskslist('cuckoo1')

    assert response == {}


@mock.patch('CuckooAPI.requests.get')
def test_taskview_exception(mock_get):
    """
    Test a pretend task view with exception
    """
    mock_get.return_value.status_code = 404

    api = CuckooAPI.CuckooAPI()

    ExceptionThrown = False

    try:
        api.taskview()
    except CuckooAPI.CuckooExceptions.CuckooAPINoTaskID:
        ExceptionThrown = True

    assert ExceptionThrown is True

    ExceptionThrown = False

    try:
        api.taskview(1)
    except CuckooAPI.CuckooExceptions.CuckooAPIBadRequest:
        ExceptionThrown = True

    assert ExceptionThrown is True


@mock.patch('CuckooAPI.requests.get')
def test_taskview_ok_noapipy(mock_get):
    """
    Test a pretend task view without api.py
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = '{}'

    api = CuckooAPI.CuckooAPI()

    response = api.taskview(1)

    assert response == {}


@mock.patch('CuckooAPI.requests.get')
def test_taskview_ok_apipy(mock_get):
    """
    Test a pretend task view with api.py
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = '{}'

    api = CuckooAPI.CuckooAPI(port=8090, APIPY=True)

    response = api.taskview(1)

    assert response == {}


@mock.patch('CuckooAPI.requests.get')
def test_taskreport_exception(mock_get):
    """
    Test a pretend task report with exception
    """
    mock_get.return_value.status_code = 404

    api = CuckooAPI.CuckooAPI()

    ExceptionThrown = False

    try:
        api.taskreport()
    except CuckooAPI.CuckooExceptions.CuckooAPINoTaskID:
        ExceptionThrown = True

    assert ExceptionThrown is True

    ExceptionThrown = False

    try:
        api.taskreport(1, 'html')
    except CuckooAPI.CuckooExceptions.CuckooAPINotImplemented:
        ExceptionThrown = True

    assert ExceptionThrown is True

    ExceptionThrown = False

    try:
        api.taskreport(1)
    except CuckooAPI.CuckooExceptions.CuckooAPIBadRequest:
        ExceptionThrown = True

    assert ExceptionThrown is True


@mock.patch('CuckooAPI.requests.get')
def test_taskreport_ok_noapipy(mock_get):
    """
    Test a pretend task report without api.py
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = '{}'

    api = CuckooAPI.CuckooAPI()

    response = api.taskreport(1)

    assert response == {}


@mock.patch('CuckooAPI.requests.get')
def test_taskreport_ok_apipy(mock_get):
    """
    Test a pretend task report with api.py
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = '{}'

    api = CuckooAPI.CuckooAPI(port=8090, APIPY=True)

    response = api.taskreport(1)

    assert response == {}


@mock.patch('CuckooAPI.requests.get')
def test_fileview_exception(mock_get):
    """
    Test a pretend file view with exception
    """
    mock_get.return_value.status_code = 404

    api = CuckooAPI.CuckooAPI()

    ExceptionThrown = False

    try:
        api.fileview()
    except CuckooAPI.CuckooExceptions.CuckooAPINoHash:
        ExceptionThrown = True

    assert ExceptionThrown is True

    ExceptionThrown = False

    try:
        api.fileview('1', 'sha255')
    except CuckooAPI.CuckooExceptions.CuckooAPINotAvailable:
        ExceptionThrown = True

    assert ExceptionThrown is True

    ExceptionThrown = False

    try:
        api.fileview('1', 'sha256')
    except CuckooAPI.CuckooExceptions.CuckooAPIBadRequest:
        ExceptionThrown = True

    assert ExceptionThrown is True


@mock.patch('CuckooAPI.requests.get')
def test_fileview_ok_noapipy(mock_get):
    """
    Test a pretend file view without api.py
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = '{}'

    api = CuckooAPI.CuckooAPI()

    response = api.fileview('1', 'sha256')

    assert response == {}


@mock.patch('CuckooAPI.requests.get')
def test_fileview_ok_apipy(mock_get):
    """
    Test a pretend file view with api.py
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = '{}'

    api = CuckooAPI.CuckooAPI(port=8090, APIPY=True)

    response = api.fileview('1', 'sha256')

    assert response == {}


@mock.patch('CuckooAPI.requests.get')
def test_taskdelete_exception(mock_get):
    """
    Test a pretend task delete with exception
    """
    mock_get.return_value.status_code = 404

    api = CuckooAPI.CuckooAPI()

    ExceptionThrown = False

    try:
        api.taskdelete()
    except CuckooAPI.CuckooExceptions.CuckooAPINoTaskID:
        ExceptionThrown = True

    assert ExceptionThrown is True

    ExceptionThrown = False

    try:
        api.taskdelete(1)
    except CuckooAPI.CuckooExceptions.CuckooAPINoTaskID:
        ExceptionThrown = True

    assert ExceptionThrown is True

    ExceptionThrown = False

    mock_get.return_value.status_code = 500

    try:
        api.taskdelete(1)
    except CuckooAPI.CuckooExceptions.CuckooAPITaskNoDelete:
        ExceptionThrown = True

    assert ExceptionThrown is True

    mock_get.return_value.status_code = 400

    try:
        api.taskdelete(1)
    except CuckooAPI.CuckooExceptions.CuckooAPIBadRequest:
        ExceptionThrown = True

    assert ExceptionThrown is True


@mock.patch('CuckooAPI.requests.get')
def test_taskdelete_ok_noapipy(mock_get):
    """
    Test a pretend task delete without api.py
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = '{}'

    api = CuckooAPI.CuckooAPI()

    response = api.taskdelete(1)

    assert response == {}


@mock.patch('CuckooAPI.requests.get')
def test_taskdelete_ok_apipy(mock_get):
    """
    Test a pretend task delete with api.py
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = '{}'

    api = CuckooAPI.CuckooAPI(port=8090, APIPY=True)

    response = api.taskdelete(1)

    assert response == {}


@mock.patch('CuckooAPI.requests.get')
def test_taskscreenshots_exception(mock_get):
    """
    Test a pretend task screenshots with exception
    """
    mock_get.return_value.status_code = 404

    api = CuckooAPI.CuckooAPI()

    ExceptionThrown = False

    try:
        api.taskscreenshots()
    except CuckooAPI.CuckooExceptions.CuckooAPINoTaskID:
        ExceptionThrown = True

    assert ExceptionThrown is True

    ExceptionThrown = False

    try:
        api.taskscreenshots(1)
    except CuckooAPI.CuckooExceptions.CuckooAPIFileExists:
        ExceptionThrown = True

    assert ExceptionThrown is True

    ExceptionThrown = False

    try:
        api.taskscreenshots(1, 'Readme.md')
    except CuckooAPI.CuckooExceptions.CuckooAPIFileExists:
        ExceptionThrown = True

    assert ExceptionThrown is True

    ExceptionThrown = False

    try:
        api.taskscreenshots(1, '1.tar.bz', 1)
    except CuckooAPI.CuckooExceptions.CuckooAPIBadRequest:
        ExceptionThrown = True

    assert ExceptionThrown is True


@mock.patch('CuckooAPI.requests.get')
def test_sampledownload_exception(mock_get):
    """
    Test a pretend sample download with exception
    """
    mock_get.return_value.status_code = 404

    api = CuckooAPI.CuckooAPI()

    ExceptionThrown = False

    try:
        api.sampledownload()
    except CuckooAPI.CuckooExceptions.CuckooAPINoHash:
        ExceptionThrown = True

    assert ExceptionThrown is True

    ExceptionThrown = False

    try:
        api.sampledownload('1', 'task', 'README.md')
    except CuckooAPI.CuckooExceptions.CuckooAPIFileExists:
        ExceptionThrown = True

    assert ExceptionThrown is True

    ExceptionThrown = False

    try:
        os.remove('test1.bin')
    except:
        pass

    try:
        api.sampledownload(1, 'task', 'test1.bin')
    except CuckooAPI.CuckooExceptions.CuckooAPIBadRequest:
        ExceptionThrown = True

    assert ExceptionThrown is True

    try:
        os.remove('test1.bin')
    except:
        pass


@mock.patch('CuckooAPI.requests.get')
def test_pcapdownload_exception(mock_get):
    """
    Test a pretend pcap download with exception
    """
    mock_get.return_value.status_code = 404

    api = CuckooAPI.CuckooAPI()

    ExceptionThrown = False

    try:
        api.pcapdownload()
    except CuckooAPI.CuckooExceptions.CuckooAPINoTaskID:
        ExceptionThrown = True

    assert ExceptionThrown is True

    ExceptionThrown = False

    try:
        api.pcapdownload(1, 'README.md')
    except CuckooAPI.CuckooExceptions.CuckooAPIFileExists:
        ExceptionThrown = True

    assert ExceptionThrown is True

    ExceptionThrown = False

    try:
        os.remove('test1.bin')
    except:
        pass

    try:
        api.pcapdownload(1, 'test1.bin')
    except CuckooAPI.CuckooExceptions.CuckooAPIBadRequest:
        ExceptionThrown = True

    assert ExceptionThrown is True

    try:
        os.remove('test1.bin')
    except:
        pass
