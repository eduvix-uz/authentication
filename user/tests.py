from user.services.Clients.Tests.TestLogin import TestLoginUser
from user.services.Clients.Tests.TestRegister import TestRegisterUser
import unittest
from rabbitmq_messages.test_rabbitmq import main


# Tests
class AllTests:
    def test_all(self):
        test = unittest.TestSuite()
        test.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestLoginUser))
        test.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestRegisterUser))
        test.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(main))
        return test