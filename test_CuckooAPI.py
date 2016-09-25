#
# Headers
#
import CuckooAPI
import mock


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
