from pkgutil import iter_modules
from unittest import TestCase, mock

from keeper import MainKeeper
from utils.common import InspectorBuilder
from utils.tests import MockResponse
from tests import inspectors


class TestInspectors(TestCase):

    def setUp(self):
        # replace modules_info to testing module
        self.keeper = MainKeeper()
        modules_info = list(iter_modules(inspectors.__path__))
        self.keeper.projects = [InspectorBuilder(module_info) for module_info in modules_info]

    @mock.patch('utils.sessions.Session.get')
    def test_keeper_result_all_failed(self, get_mock):
        params = (('first request', 400), ('second request', 500))
        fake_responses = [MockResponse(*params[0]), MockResponse(*params[1])]
        get_mock.side_effect = fake_responses
        self.keeper.run()
        self.assertFalse(self.keeper.ok)
        response_data = str(self.keeper.data)
        for param in params[0] + params[1]:
            self.assertIn(str(param), response_data)
        self.keeper.stop()

    # one failed
    @mock.patch('utils.sessions.Session.get')
    def test_keeper_result_one_failed(self, get_mock):
        params = (('first request', 200), ('second request', 500))
        fake_responses = [MockResponse(*params[0]), MockResponse(*params[1])]
        get_mock.side_effect = fake_responses
        self.keeper.run()
        self.assertFalse(self.keeper.ok)
        response_data = str(self.keeper.data)
        for param in params[0] + params[1]:
            self.assertIn(str(param), response_data)
        self.keeper.stop()

    @mock.patch('utils.sessions.Session.get')
    def test_keeper_result_all_ok(self, get_mock):
        params = (('first request', 200), ('second request', 201))
        fake_responses = [MockResponse(*params[0]), MockResponse(*params[1])]
        get_mock.side_effect = fake_responses
        self.keeper.run()
        self.assertTrue(self.keeper.ok)
        response_data = str(self.keeper.data)
        for param in params[0] + params[1]:
            self.assertIn(str(param), response_data)
        self.keeper.stop()

    @mock.patch('utils.sessions.Session.get')
    def test_keeper_status_check(self, get_mock):
        params = (('first request', 400), ('second request', 500))
        fake_responses = [MockResponse(*params[0]), MockResponse(*params[1])]
        get_mock.side_effect = fake_responses
        with mock.patch('keeper.MainKeeper.status_check') as mocked_status_check:
            keeper = MainKeeper()
            keeper.run()
            self.assertFalse(keeper.ok)
            self.assertTrue(mocked_status_check.called)
            self.assertEqual(mocked_status_check.call_count, 1)
            keeper.stop()
