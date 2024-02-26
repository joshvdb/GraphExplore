import unittest
from unittest.mock import MagicMock, patch, Mock
from flask import Flask
from app_script import app, get_account_details, delete_graph, delete_account, analyze, add_account, homepage, home, upload
from werkzeug.datastructures import ImmutableMultiDict

class TestIndexRoute(unittest.TestCase):
    def setUp(self):
        # Create a test client using Flask's test_client method
        self.app = app.test_client()

    @patch('app_script.os.path.isfile')
    @patch('app_script.sqlite3.connect')
    @patch('app_script.return_account_page')
    @patch('app_script.render_template')
    def test_index_route(self, mock_render_template, mock_return_account_page, mock_sqlite_connect, mock_os_path_isfile):
        with self.app as a:
            # Set up mocks
            mock_os_path_isfile.return_value = False
            mock_sqlite_connect.return_value = MagicMock()
            mock_return_account_page.return_value = ("graph1", ["graph1"], "account1", ["account1"])
            mock_render_template.return_value = "test"

            # Make a GET request to the '/' route
            response = a.get('/')

            # Check if the response status code is 200 (OK)
            self.assertEqual(response.status_code, 200)

            # Check if render_template is called with the expected arguments
            mock_render_template.assert_called_once_with('add.html', graph_list_first='graph1', graph_list=['graph1'], account_list_first='account1', account_list=['account1'])

class TestGetAccountDetails(unittest.TestCase):
    @patch('app_script.sqlite3.connect')
    @patch('app_script.render_template')
    @patch('app_script.return_account_page')
    def test_get_account_details(self, return_account_page_mock, mock_render_template, mock_connect):
        # Create a mock cursor
        mock_cursor = Mock()
        mock_cursor.execute.return_value = [("graph1", "account1", "followers1", "following1")]
        return_account_page_mock.return_value = ('graph1', ['graph1', 'graph2'], 'user1', ['user1', 'user2'])

        # Set the return value of the mock connect method to the mock cursor
        mock_connect.return_value.__enter__.return_value = mock_cursor

        # Create a mock Flask app
        app.config = {'DATABASE': 'mock_db', 'APPLICATION_ROOT': '/', 'PREFERRED_URL_SCHEME': 'http', 'SERVER_NAME': 'localhost:5000'
                           , 'SECRET_KEY': '', 'PRESERVE_CONTEXT_ON_EXCEPTION': '', 'DEBUG': ''}

        with app.test_request_context('/'):
            # Create a new ImmutableMultiDict with updated form data
            form_data = ImmutableMultiDict({'graph_name': 'graph1', 'account_name_1': 'account1'})
            # Mock request form data
            with patch('app_script.request.form', form_data):
                get_account_details()

        # Check if the render_template function was called with the expected arguments
        mock_render_template.assert_called_once_with(
            'add.html', graph_list_first='graph1', graph_list=['graph1', 'graph2'], account_list_first='account1', account_list=['user1', 'user2'], followers='Empty', following='Empty'
        )

class TestDeleteGraph(unittest.TestCase):
    @patch('app_script.sqlite3.connect')
    @patch('app_script.return_account_page')
    @patch('app_script.render_template')
    def test_delete_graph(self, mock_render_template, mock_return_account_page, mock_connect):
        # Mock the request form data
        mock_request = Mock()
        mock_request.form = {'graph_name': 'test_graph'}

        # Mock the Flask app configuration
        app.config = {'DATABASE': 'mock_db', 'APPLICATION_ROOT': '/', 'PREFERRED_URL_SCHEME': 'http', 'SERVER_NAME': 'localhost:5000'
                           , 'SECRET_KEY': '', 'PRESERVE_CONTEXT_ON_EXCEPTION': '', 'DEBUG':''}

        # Mock the cursor and connection
        mock_cursor = Mock()
        mock_conn = Mock()
        mock_conn.execute.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        # Mock the return values of return_account_page function
        mock_return_account_page.return_value = ('graph_list_first', ['graph_list'], 'account_list_first', ['account_list'])

        with app.test_request_context('/'):
            # Create a new ImmutableMultiDict with updated form data
            form_data = ImmutableMultiDict({'graph_name': 'test_graph'})
            # Mock request form data
            with patch('app_script.request.form', form_data):
                # Call delete_graph function
                response = delete_graph()

        # Check if the render_template function is called with the correct arguments
        mock_render_template.assert_called_with('add.html', graph_list_first='graph_list_first', graph_list=['graph_list'], account_list_first='account_list_first', account_list=['account_list'])

        # Check if the connection.execute method is called with the correct SQL query
        mock_conn.execute.assert_called_with("DELETE from connections where graph='test_graph'")

        # Check if the connection.commit method is called
        mock_conn.commit.assert_called()

class TestDeleteAccount(unittest.TestCase):
    @patch('app_script.sqlite3.connect')
    @patch('app_script.return_account_page')
    @patch('app_script.render_template')
    def test_delete_account(self, mock_render_template, mock_return_account_page, mock_connect):
        # Mock the request form data
        mock_request = Mock()
        mock_request.form = {'graph_name': 'test_graph'}

        # Mock the Flask app configuration
        app.config = {'DATABASE': 'mock_db', 'APPLICATION_ROOT': '/', 'PREFERRED_URL_SCHEME': 'http', 'SERVER_NAME': 'localhost:5000'
                           , 'SECRET_KEY': '', 'PRESERVE_CONTEXT_ON_EXCEPTION': '', 'DEBUG':''}

        # Mock the cursor and connection
        mock_cursor = Mock()
        mock_conn = Mock()
        mock_conn.execute.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        # Mock the return values of return_account_page function
        mock_return_account_page.return_value = ('graph_list_first', ['graph_list'], 'account_list_first', ['account_list'])

        with app.test_request_context('/'):
            # Create a new ImmutableMultiDict with updated form data
            form_data = ImmutableMultiDict({'account_name_1': 'test_account'})
            # Mock request form data
            with patch('app_script.request.form', form_data):
                # Call delete_account function
                response = delete_account()

        # Check if the render_template function is called with the correct arguments
        mock_render_template.assert_called_with('add.html', graph_list_first='graph_list_first', graph_list=['graph_list'], account_list_first='account_list_first', account_list=['account_list'])

        # Check if the connection.execute method is called with the correct SQL query
        mock_conn.execute.assert_called_with("DELETE from connections where user='test_account'")

        # Check if the connection.commit method is called
        mock_conn.commit.assert_called()

class TestAddAccount(unittest.TestCase):
    @patch('app_script.sqlite3.connect')
    @patch('app_script.return_account_page')
    @patch('app_script.render_template')
    def test_add_account(self, mock_render_template, mock_return_account_page, mock_connect):
        # Mock the request form data
        mock_request = Mock()
        mock_request.form = {'graph_name': 'test_graph'}

        # Mock the Flask app configuration
        app.config = {'DATABASE': 'mock_db', 'APPLICATION_ROOT': '/', 'PREFERRED_URL_SCHEME': 'http', 'SERVER_NAME': 'localhost:5000'
                           , 'SECRET_KEY': '', 'PRESERVE_CONTEXT_ON_EXCEPTION': '', 'DEBUG':''}

        # Mock the cursor and connection
        mock_cursor = Mock()
        mock_conn = Mock()
        mock_conn.execute.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        # Mock the return values of return_account_page function
        mock_return_account_page.return_value = ('graph_list_first', ['graph_list'], 'account_list_first', ['account_list'])

        with app.test_request_context('/'):
            # Create a new ImmutableMultiDict with updated form data
            form_data = ImmutableMultiDict({'graph_name_2': 'test_graph', 'account_name_2': 'test_account', 'follower_accounts': 'test_account_1', 'following_accounts': 'test_account_2'})
            # Mock request form data
            with patch('app_script.request.form', form_data):
                # Call add_account function
                add_account()

        # Check if the render_template function is called with the correct arguments
        mock_render_template.assert_called_with('add.html', graph_list_first='graph_list_first', graph_list=['graph_list'], account_list_first='account_list_first', account_list=['account_list'])

        # Check if the connection.execute method is called with the correct SQL query
        mock_conn.execute.assert_called_with("INSERT INTO connections (graph, user, followers, following) VALUES ('test_graph', 'test_account', 'test_account_1', 'test_account_2');")

        # Check if the connection.commit method is called
        mock_conn.commit.assert_called()

class TestHomepage(unittest.TestCase):
    @patch('app_script.sqlite3.connect')
    @patch('app_script.return_account_page')
    @patch('app_script.render_template')
    def test_homepage(self, mock_render_template, mock_return_account_page, mock_connect):
        # Mock the request form data
        mock_request = Mock()
        mock_request.form = {'graph_name': 'test_graph'}

        # Mock the Flask app configuration
        app.config = {'DATABASE': 'mock_db', 'APPLICATION_ROOT': '/', 'PREFERRED_URL_SCHEME': 'http', 'SERVER_NAME': 'localhost:5000'
                           , 'SECRET_KEY': '', 'PRESERVE_CONTEXT_ON_EXCEPTION': '', 'DEBUG':''}

        # Mock the cursor and connection
        mock_cursor = Mock()
        mock_conn = Mock()
        mock_conn.execute.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        # Mock the return values of return_account_page function
        mock_return_account_page.return_value = ('graph_list_first', ['graph_list'], 'account_list_first', ['account_list'])

        with app.test_request_context('/'):
            # Create a new ImmutableMultiDict with updated form data
            form_data = ImmutableMultiDict({'graph_name_2': 'test_graph', 'account_name_2': 'test_account', 'follower_accounts': 'test_account_1', 'following_accounts': 'test_account_2'})
            # Mock request form data
            with patch('app_script.request.form', form_data):
                # Call homepage function
                homepage()

        # Check if the render_template function is called with the correct arguments
        mock_render_template.assert_called_with('explore.html', graph_list_first='graph_list_first', graph_list=['graph_list'], account_list_first='account_list_first', account_list=['account_list'])

class TestHome(unittest.TestCase):
    @patch('app_script.sqlite3.connect')
    @patch('app_script.return_account_page')
    @patch('app_script.render_template')
    def test_home(self, mock_render_template, mock_return_account_page, mock_connect):
        # Mock the request form data
        mock_request = Mock()
        mock_request.form = {'graph_name': 'test_graph'}

        # Mock the Flask app configuration
        app.config = {'DATABASE': 'mock_db', 'APPLICATION_ROOT': '/', 'PREFERRED_URL_SCHEME': 'http', 'SERVER_NAME': 'localhost:5000'
                           , 'SECRET_KEY': '', 'PRESERVE_CONTEXT_ON_EXCEPTION': '', 'DEBUG':''}

        # Mock the cursor and connection
        mock_cursor = Mock()
        mock_conn = Mock()
        mock_conn.execute.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        # Mock the return values of return_account_page function
        mock_return_account_page.return_value = ('graph_list_first', ['graph_list'], 'account_list_first', ['account_list'])

        with app.test_request_context('/'):
            # Create a new ImmutableMultiDict with updated form data
            form_data = ImmutableMultiDict({'graph_name_2': 'test_graph', 'account_name_2': 'test_account', 'follower_accounts': 'test_account_1', 'following_accounts': 'test_account_2'})
            # Mock request form data
            with patch('app_script.request.form', form_data):
                # Call home function
                home()

        # Check if the render_template function is called with the correct arguments
        mock_render_template.assert_called_with('add.html', graph_list_first='graph_list_first', graph_list=['graph_list'], account_list_first='account_list_first', account_list=['account_list'])

class TestUpload(unittest.TestCase):
    @patch('app_script.return_account_page')
    @patch('app_script.sqlite3.connect')
    @patch('builtins.open', create=True)
    @patch('csv.reader')
    @patch('app_script.render_template')
    def test_upload(self, mock_render_template, mock_csv_reader, mock_open, mock_connect, mock_return_account_page):

        # Mocking return value for return_account_page
        mock_return_account_page.return_value = ('graph_list_first', ['graph1', 'graph2'], 'account_list_first', ['account1', 'account2'])

        # Mocking csv reader
        mock_csv_reader.return_value = [['graph1', 'user1', 'followers1', 'following1']]

        # Mock the cursor and connection
        mock_cursor = Mock()
        mock_conn = Mock()
        mock_conn.execute.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        # Mock the Flask app configuration
        app.config = {'DATABASE': 'mock_db', 'APPLICATION_ROOT': '/', 'PREFERRED_URL_SCHEME': 'http', 'SERVER_NAME': 'localhost:5000'
                           , 'SECRET_KEY': '', 'PRESERVE_CONTEXT_ON_EXCEPTION': '', 'DEBUG':''}
        
        with app.test_request_context('/upload', method='POST'):
            with patch('app_script.request.files.get'):
                with patch('app_script.request.remote_addr'):
                    upload()
        
        # Check if the connection.execute method is called with the correct SQL query
        mock_conn.execute.assert_called_with("INSERT INTO connections (graph, user, followers, following) VALUES ('graph1', 'user1', 'followers1', 'following1');")

class TestAnalyze(unittest.TestCase):
    @patch('app_script.sqlite3.connect')
    @patch('app_script.nx.Graph')
    @patch('app_script.construct_account_graph')
    @patch('app_script.reduce_graph')
    @patch('app_script.output_file')
    @patch('app_script.save')
    @patch('app_script.get_edge_weights')
    @patch('app_script.render_template')
    @patch('app_script.get_network_graph')
    def test_analyze(self, get_network_graph_mock, mock_render_template, mock_get_edge_weights, mock_save, mock_output_file, mock_reduce_graph, mock_construct_account_graph, mock_nx_graph, mock_sqlite_connect):

        # Mock nx.Graph
        mock_g = MagicMock()
        mock_nx_graph.return_value = mock_g

        # Mock construct_account_graph
        mock_graph_edges = [('user1', 'user2')]
        mock_construct_account_graph.return_value = mock_graph_edges

        # Mock reduce_graph
        mock_reduced_graph_edges = [('user1', 'user2')]
        mock_reduce_graph.return_value = mock_reduced_graph_edges

        # Mock get_edge_weights
        mock_edge_weights = [('user2', 0.5), ('user3', 0.3)]
        mock_get_edge_weights.return_value = mock_edge_weights

        # Mock render_template
        mock_render_template.return_value = 'rendered_template_html'

        # mock the graph return function
        get_network_graph_mock.return_value = None

        # Mock the Flask app configuration
        app.config = {'DATABASE': 'mock_db', 'APPLICATION_ROOT': '/', 'PREFERRED_URL_SCHEME': 'http', 'SERVER_NAME': 'localhost:5000'
                           , 'SECRET_KEY': '', 'PRESERVE_CONTEXT_ON_EXCEPTION': '', 'DEBUG':''}

        with app.test_request_context('/'):
            # Create a new ImmutableMultiDict with updated form data
            form_data = ImmutableMultiDict({'graphs': 'graph1', 'connection_type': 'following', 'analysis_type': 'common', 'graph_type': 'test_account_2'})
            # Mock request form data
            with patch('app_script.request.form', form_data):
                # Call the analyze function
                result = analyze()

        # Assertions
        mock_render_template.assert_called_with('result.html', graph='graph1', recommended_accounts='user2, user3')
        self.assertEqual(result, 'rendered_template_html')

if __name__ == '__main__':
    unittest.main()
