#
# Headers
#
import CuckooAPI
import mock


def test_submitfile_directory_exception():
    api = CuckooAPI.CuckooAPI()
    ExceptionThrown = False
    try:
        api.submitfile('.')
    except CuckooAPI.CuckooExceptions.CuckooInvalidFileException:
        ExceptionThrown = True

    assert ExceptionThrown is True


@mock.patch('CuckooAPI.requests.post')
def test_submitfile_ok_noapipy(mock_get):
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
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = ('{"task_ids": [14]}')

    api = CuckooAPI.CuckooAPI(port=8090, APIPY=True)

    response = api.submitfile('README.md')

    assert response['task_ids'][0] == 14
