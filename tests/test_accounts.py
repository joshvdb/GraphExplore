import sys
import os

cwd = os.getcwd()

# Add the parent directory to sys.path
sys.path.append(cwd)

import unittest
from lib.account import Account

class TestAccount(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        self.account_name = "test_user"
        self.account_description = "Test account"
        self.follower_accounts = ["follower1", "follower2"]
        self.following_accounts = ["following1", "following2"]

    def test_account_initialization(self):
        # Test initialization of Account class
        account = Account(self.account_name, self.account_description, self.follower_accounts, self.following_accounts)
        self.assertEqual(account.account_name, self.account_name)
        self.assertEqual(account.account_description, self.account_description)
        self.assertEqual(account.follower_accounts, self.follower_accounts)
        self.assertEqual(account.following_accounts, self.following_accounts)

    def test_attribute_access(self):
        # Test attribute access
        account = Account(self.account_name, self.account_description, self.follower_accounts, self.following_accounts)
        self.assertEqual(account.account_name, self.account_name)
        self.assertEqual(account.account_description, self.account_description)
        self.assertEqual(account.follower_accounts, self.follower_accounts)
        self.assertEqual(account.following_accounts, self.following_accounts)

if __name__ == '__main__': 
    unittest.main() 
