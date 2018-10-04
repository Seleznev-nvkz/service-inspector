from utils.common import InspectorAbstract
from utils.sessions import Session

TEST_URL = 'https://example.con'
session = Session(TEST_URL)


class TestClass(InspectorAbstract):
    name = 'testClass'
    interval = 100

    def check(self):
        response = session.get(TEST_URL)
        self.set_details_from_response(response)
        return response.ok


class TestClass2(TestClass):
    name = 'TestClass2'
