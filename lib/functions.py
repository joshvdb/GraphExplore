from bokeh.models import Range1d, Circle, MultiLine
from bokeh.plotting import figure
from bokeh.plotting import from_networkx
import numpy as np
import networkx as nx
import sqlite3 as _sql

def construct_account_graph(account_list, type='followers'):
    """
    Function to construct a list of account pairs that indicate a link between two accounts.

    :param account_list: list
    :param account_list: str
    :return: list
    """
    if type=='followers':
        return [(account.account_name, account_i) for account in account_list for account_i in account.follower_accounts]
    else:
        return [(account.account_name, account_i) for account in account_list for account_i in account.following_accounts]


def reduce_graph(graph, major_accounts, mode='common', threshold=1):
    """
    Function to remove accounts from the graph if their degree is higher/lower than a given threshold.

    :param graph: nx.Graph
    :param major_accounts: list
    :param mode: str (either common or unique - greater than or less than/equal to)
    :param threshold: int
    :return: list
    """
    all_names = [v for k, v in graph if v not in major_accounts]
    all_names = np.unique(all_names, return_counts=True)
    frequency_count = list(zip(all_names[0], all_names[1]))
    
    if mode=='common':
        common_accounts = [k for k, v in frequency_count if v > threshold]
    else:
        common_accounts = [k for k, v in frequency_count if v <= threshold]
    
    return [(k, v) for k, v in graph if v in common_accounts]

def return_account_page(app):
    """
    Function to read graph information from the database, and return it in function-readable format (lists).

    :param app: Flask object
    :return: (list, list, list, list)
    """
    conn = _sql.connect(app.config['DATABASE'])

    cursor = conn.execute("SELECT * from connections")

    results = [row for row in cursor]
    graph_list = np.unique([row[0] for row in results])
    account_list = [row[1] for row in results]

    if len(graph_list) > 0:
        graph_list_first = graph_list[0]
    else:
        graph_list_first = 'Empty'

    if len(account_list) > 0:
        account_list_first = account_list[0]
    else:
        account_list_first = 'Empty'

    return graph_list_first, graph_list, account_list_first, account_list

def get_network_graph(graph, major_accounts, layout='1'):
    """
    Function to read graph information from the database, and return it in function-readable format (lists).

    :param graph: nx.Graph
    :param major_accounts: list
    :param layout: str
    :return: plot
    """
    if layout == '1':
        layout_variable = nx.circular_layout
    elif layout == '2':
        layout_variable = nx.spring_layout
    elif layout == '3':
        layout_variable = nx.spectral_layout
    
    color_scheme = ['red' if a in major_accounts else 'blue' for a in list(graph.nodes)]

    edge_attrs = {}

    for start_node, end_node, _ in graph.edges(data=True):
        edge_attrs[(start_node, end_node)] = 'red' if start_node in major_accounts and end_node in major_accounts else 'black'

    nx.set_edge_attributes(graph, edge_attrs, "edge_color")

    #Create a plot — set dimensions, toolbar, and title
    plot = figure(tooltips = "account: @account",
                  tools="pan,wheel_zoom,save,reset", active_scroll='wheel_zoom',
                x_range=Range1d(-10.1, 10.1), y_range=Range1d(-10.1, 10.1), title='Title')

    plot.sizing_mode = 'scale_width'

    #Create a network graph object with spring layout
    # https://networkx.github.io/documentation/networkx-1.9/reference/generated/networkx.drawing.layout.spring_layout.html
    network_graph = from_networkx(graph, layout_variable, scale=10, center=(0, 0))

    network_graph.node_renderer.data_source.data['color_scheme'] = color_scheme

    #Set node size and color
    network_graph.node_renderer.glyph = Circle(size=15, fill_color='color_scheme')

    #Set edge opacity and width
    network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.5, line_width=1)
    network_graph.node_renderer.data_source.data['account']= list(graph.nodes)
    network_graph.edge_renderer.glyph = MultiLine(line_color="edge_color", line_alpha=0.8, line_width=1)

    #Add network graph to the plot
    plot.renderers.append(network_graph)
    
    return plot

def get_similar_accounts(following_graph, follower_graph, major_accounts, following_follower_ratio):
    """
    Function to read graph information from the database, and return it in function-readable format (lists).

    :param following_graph: nx.Graph
    :param follower_graph: nx.Graph
    :param major_accounts: list
    :param following_follower_ratio: float (the relative weigthing of follower vs following)
    :return: list
    """
    following_values = dict(get_edge_weights(following_graph, major_accounts))
    follower_values = dict(get_edge_weights(follower_graph, major_accounts))
    all_accounts = list(following_values.keys()) + list(follower_values.keys())
    values = [(k, following_values.get(k, 0)*following_follower_ratio + follower_values.get(k, 0)) for k in all_accounts if k not in major_accounts]
    
    return sorted(values, key=lambda v: v[1], reverse=True)

def get_edge_weights(graph, major_accounts):
    """
    Function that returns a sorted list of (account, degree) pairs for use in graph analysis and similar account recommendation.

    :param graph: nx.Graph
    :param major_accounts: list
    :return: list
    """
    edge_values = dict(graph.degree)
    values = [(k, v) for k, v in edge_values.items() if (k not in major_accounts) and (v > 0)]
    
    return sorted(list(values), key=lambda v: v[1], reverse=True)
