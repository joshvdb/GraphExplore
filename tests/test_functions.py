import sys
import os

cwd = os.getcwd()

# Add the parent directory to sys.path
sys.path.append(cwd)

import unittest
from unittest.mock import Mock, patch
from lib.functions import (
    construct_account_graph,
    reduce_graph,
    return_account_page,
    get_network_graph,
    get_similar_accounts,
    get_edge_weights
)
import sqlite3 as _sql

import networkx as nx
from lib.account import Account

class TestConstructAccountGraph(unittest.TestCase):
    def test_construct_account_graph_followers(self):
        # Test construct_account_graph with 'followers' type
        account_list = [Account("A", "Description", ["B", "C"], ["B", "C"]), Account("B", "Description", ["A", "C"], ["A", "C"]), Account("C", "Description", ["B", "A"], ["B", "A"])]
        expected_result = [('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'B'), ('C', 'A')]
        self.assertEqual(construct_account_graph(account_list), expected_result)

    def test_construct_account_graph_following(self):
        # Test construct_account_graph with 'following' type
        account_list = [Account("A", "Description", ["B", "C"], ["B", "C"]), Account("B", "Description", ["A", "C"], ["A", "C"]), Account("C", "Description", ["B", "A"], ["B", "A"])]
        expected_result = [('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'B'), ('C', 'A')]
        self.assertEqual(construct_account_graph(account_list, type='following'), expected_result)

class TestReduceGraph(unittest.TestCase):
    def test_reduce_graph_common(self):
        # Test reduce_graph with mode='common'
        graph = [("A", 1), ("B", 2), ("C", 2), ("D", 3)]
        major_accounts = ["A"]
        expected_result = [('A', 1), ('D', 3)]
        self.assertEqual(reduce_graph(graph, major_accounts), expected_result)

    def test_reduce_graph_unique(self):
        # Test reduce_graph with mode='unique'
        graph = [("A", 1), ("B", 2), ("C", 2), ("D", 3)]
        major_accounts = ["A"]
        expected_result = [("A", 1), ("D", 3)]
        self.assertEqual(reduce_graph(graph, major_accounts, mode='unique'), expected_result)

class TestReturnAccountPage(unittest.TestCase):
    def test_return_account_page_empty(self):
        # Test return_account_page when database is empty
        mock_app = Mock()
        mock_app.config = {'DATABASE': ':memory:'}
        self.assertEqual(return_account_page(mock_app), ('Empty', [], 'Empty', []))

    def test_return_account_page_non_empty(self):
        # Test return_account_page when database has data
        mock_app = Mock()
        mock_app.config = {'DATABASE': ':memory:'}
        conn = _sql.connect(':memory:')
        conn.execute("CREATE TABLE connections (graph text, user text, followers text, following text)")
        conn.execute("INSERT INTO connections VALUES ('graph1', 'user1', 'follower1', 'following1')")
        conn.execute("INSERT INTO connections VALUES ('graph2', 'user2', 'follower2', 'following2')")
        conn.commit()
        self.assertEqual(return_account_page(mock_app), ('graph1', ['graph1', 'graph2'], 'user1', ['user1', 'user2']))

class TestGetNetworkGraph(unittest.TestCase):
    def test_get_network_graph(self):
        # Test get_network_graph with different layout types
        graph = nx.Graph()
        graph.add_nodes_from(["A", "B", "C"])
        graph.add_edges_from([("A", "B"), ("B", "C")])
        major_accounts = ["A"]
        
        # Test with layout='1'
        plot = get_network_graph(graph, major_accounts, layout='1')
        self.assertIsNotNone(plot)
        # Add more tests for other layouts if needed

class TestGetSimilarAccounts(unittest.TestCase):
    def test_get_similar_accounts(self):
        # Test get_similar_accounts function
        following_graph = nx.Graph()
        following_graph.add_nodes_from(["A", "B", "C"])
        following_graph.add_edges_from([("A", "B"), ("B", "C")])
        
        follower_graph = nx.Graph()
        follower_graph.add_nodes_from(["A", "D", "E"])
        follower_graph.add_edges_from([("A", "D"), ("D", "E")])
        
        major_accounts = ["A"]
        following_follower_ratio = 0.5
        
        expected_result = [('D', 2.0), ('B', 1.0), ('E', 1.0), ('C', 0.5)]
        self.assertEqual(get_similar_accounts(following_graph, follower_graph, major_accounts, following_follower_ratio), expected_result)

class TestGetEdgeWeights(unittest.TestCase):
    def test_get_edge_weights(self):
        # Test get_edge_weights function
        graph = nx.Graph()
        graph.add_nodes_from(["A", "B", "C"])
        graph.add_edges_from([("A", "B"), ("B", "C")])
        major_accounts = ["A"]
        expected_result = [('B', 2), ('C', 1)]
        self.assertEqual(get_edge_weights(graph, major_accounts), expected_result)

import unittest
from unittest.mock import Mock, patch

class TestReturnAccountPage(unittest.TestCase):
    @patch('lib.functions._sql.connect')
    def test_return_account_page(self, mock_connect):
        # Set the return value of the mock connect method to the mock cursor
        mock_connect.return_value.execute.return_value = [("graph1", "account1", "followers1", "following1")]

        # Mock the Flask app object
        mock_app = Mock()
        mock_app.config = {'DATABASE': 'mock_db'}

        # Call the function with the mock app
        graph_list_first, graph_list, account_list_first, account_list = return_account_page(mock_app)

        # Check the returned values
        self.assertEqual(graph_list_first, "graph1")
        self.assertEqual(graph_list, ["graph1"])
        self.assertEqual(account_list_first, "account1")
        self.assertEqual(account_list, ["account1"])

if __name__ == '__main__':
    unittest.main()
