#
# Headers
#
import CuckooAPI


def test_submitfile_directory_exception():
    api = CuckooAPI.CuckooAPI()
    ExceptionThrown = False
    try:
        api.submitfile('.')
    except CuckooAPI.CuckooExceptions.CuckooInvalidFileException:
        ExceptionThrown = True

    assert ExceptionThrown is True
