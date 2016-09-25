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
    except CuckooAPI.CuckooExceptions.CuckooAPIMachineNotFound:
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
    except CuckooAPI.CuckooExceptions.CuckooAPIMachineNotFound:
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
    except CuckooAPI.CuckooExceptions.CuckooAPIMachineNotFound:
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
