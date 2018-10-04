from unittest import TestCase, mock

from utils.common import InspectorAbstract
from utils.tests import MockResponse
from tests.inspectors.test_examples import TestClass


class TestInspectors(TestCase):

    def test_init(self):
        """ On required init params (name, interval & check) """
        EmptyClass = InspectorAbstract
        with self.assertRaises(AssertionError):
            EmptyClass()

        EmptyClass.name = 'testClass'
        EmptyClass.interval = 'testClass'
        with self.assertRaises(ValueError):
            EmptyClass()

        EmptyClass.interval = 100
        with self.assertRaises(NotImplementedError):
            EmptyClass().check()

    def test_details(self):
        """ Check to storing result and details """
        test_sets = [{'result': True, 'details': {'ok': True}},
                     {'result': False, 'details': {'error': 'msg'}}]

        for test_set in test_sets:
            def check(this):
                this.details = test_set['details']
                return test_set['result']

            NewTestClass = type('TestClass', (TestClass, ), {})
            NewTestClass.check = check
            instance = NewTestClass()
            instance.run()
            self.assertEqual(instance.result, test_set['result'])
            self.assertEqual(bool(instance), test_set['result'])
            self.assertEqual(instance.details, test_set['details'])
            instance.stop()

    @mock.patch('utils.sessions.Session.get')
    def test_requests(self, get_mock):
        test_sets = [{'status': 404, 'body': "{'error': 'not found'}", 'bool': False},
                     {'status': 500, 'body': "Server error", 'bool': False},
                     {'status': 200, 'body': "Text", 'bool': True}]
        for test_set in test_sets:
            fake_responses = [MockResponse(test_set['body'], test_set['status'])]
            get_mock.side_effect = fake_responses
            instance = TestClass()
            instance._run()
            self.assertEqual(bool(instance), test_set['bool'], repr(test_set))
            self.assertEqual(instance.details['status'], test_set['status'], repr(test_set))
            self.assertEqual(instance.details['body'], test_set['body'], repr(test_set))
