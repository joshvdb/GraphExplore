import sys
import os

cwd = os.getcwd()

# Add the parent directory to sys.path
sys.path.append(cwd)

import unittest
from lib.constants import AccountAttributes, LinkTypes, GraphLayoutTypes

class TestEnums(unittest.TestCase):

    def test_account_attributes(self):
        self.assertEqual(AccountAttributes.followers.value, 'followers')
        self.assertEqual(AccountAttributes.following.value, 'following')

    def test_link_types(self):
        self.assertEqual(LinkTypes.common.value, 'common')
        self.assertEqual(LinkTypes.uncommon.value, 'uncommon')

    def test_graph_layout_types(self):
        self.assertEqual(GraphLayoutTypes.circular_layout.value, 'circular_layout')
        self.assertEqual(GraphLayoutTypes.spring_layout.value, 'spring_layout')
        self.assertEqual(GraphLayoutTypes.spectral_layout.value, 'spectral_layout')

if __name__ == '__main__':
    unittest.main()