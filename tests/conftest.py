import pytest
from base64 import b64encode


@pytest.fixture(params=["username", "password"])
def auth(credential):
    headers = {'Authorization': 'Basic %s' % b64encode(
        bytes(credential["username"] + ':' + password, "utf-8")).decode("ascii")}
    yield headers
