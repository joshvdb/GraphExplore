from flask import Flask, render_template, request
from bokeh.plotting import output_file
import csv
import os
import sqlite3
import networkx as nx
import sqlite3
from lib.account import Account
from lib.functions import construct_account_graph, reduce_graph, return_account_page, get_network_graph, get_edge_weights
from bokeh.io import save


app = Flask(__name__, static_folder='static')


@app.route('/', methods=['GET', 'POST'])
def index():
    # get user IP address
    user_ip = request.remote_addr
    db_file = 'database/' + user_ip + 'database.db'

    # check if database file exists: if not, create it
    if os.path.isfile(db_file) != True:
        conn = sqlite3.connect(db_file)
        conn.execute("""CREATE TABLE connections (
            graph text,
            user text,
            followers text,
            following text
        );""")

        # insert standard values as initial graph entry
        values = ('graph', 'test', 'test', 'test')
        conn.execute("INSERT INTO connections (graph, user, followers, following) VALUES " + str(values) + ";")

        # save the database to file
        conn.commit()

    app.config['DATABASE'] = db_file

    graph_list_first, graph_list, account_list_first, account_list = return_account_page(app)

    return render_template('add.html', graph_list_first=graph_list_first, graph_list=graph_list, account_list_first=account_list_first, account_list=account_list)

@app.route('/get_account_details', methods=['GET', 'POST'])
def get_account_details():
    graph_name = request.form['graph_name']
    account_name = request.form['account_name_1']

    try:
        conn = sqlite3.connect(app.config['DATABASE'])
        cursor = conn.execute("""SELECT * from connections where graph='""" + graph_name + """' and user='""" + account_name + """'""")
        results = [row for row in cursor]
        followers = results[0][2]
        following = results[0][3]
    except:
        followers = 'Empty'
        following = 'Empty'
    
    _, graph_list, _, account_list = return_account_page(app)

    return render_template('add.html', graph_list_first=graph_name, graph_list=graph_list, account_list_first=account_name, account_list=account_list, followers=followers, following=following)

@app.route('/delete_graph', methods=['GET', 'POST'])
def delete_graph():
    graph_name = request.form['graph_name']

    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.execute("""DELETE from connections where graph='""" + graph_name + """'""")

    # save the database to file
    conn.commit()

    graph_list_first, graph_list, account_list_first, account_list = return_account_page(app)

    return render_template('add.html', graph_list_first=graph_list_first, graph_list=graph_list, account_list_first=account_list_first, account_list=account_list)

@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    account_name = request.form['account_name_1']

    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.execute("""DELETE from connections where user='""" + account_name + """'""")

    # save the database to file
    conn.commit()

    graph_list_first, graph_list, account_list_first, account_list = return_account_page(app)

    return render_template('add.html', graph_list_first=graph_list_first, graph_list=graph_list, account_list_first=account_list_first, account_list=account_list)

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    graph_name = request.form['graphs']
    connection_type = request.form['connection_type']
    analysis_type = request.form['analysis_type']
    graph_type = request.form['graph_type']

    conn = sqlite3.connect(app.config['DATABASE'])

    cursor = conn.execute("SELECT * from connections where graph='""" + graph_name + """'""")

    results = [row for row in cursor]

    account_list = [Account(row[1], '', row[2].split(', '), row[3].split(', ')) for row in results]

    major_accounts = [v.account_name for v in account_list]

    graph_edges = construct_account_graph(account_list, type=connection_type)

    graph_edges = reduce_graph(graph_edges, major_accounts, mode=analysis_type)

    g = nx.Graph()
    g.add_edges_from(graph_edges)

    #Create a plot — set dimensions, toolbar, and title
    plot = get_network_graph(g, major_accounts, layout=graph_type)

    output_file('templates/bokeh_plot.html')

    save(plot)

    recommended_accounts = get_edge_weights(g, major_accounts)
    recommended_accounts = ', '.join([v[0] for v in recommended_accounts])

    rendered_template_html = render_template('result.html', graph=graph_name, recommended_accounts=recommended_accounts)

    return rendered_template_html


@app.route('/add_account', methods=['GET', 'POST'])
def add_account():
    graph_name = request.form["graph_name_2"]

    account_name = request.form['account_name_2']
    followers = request.form['follower_accounts']
    following = request.form['following_accounts']

    conn = sqlite3.connect(app.config['DATABASE'])

    values = (graph_name, account_name, followers, following)
    conn.execute("INSERT INTO connections (graph, user, followers, following) VALUES " + str(values) + ";")

    # save the database to file
    conn.commit()

    graph_list_first, graph_list, account_list_first, account_list = return_account_page(app)

    return render_template('add.html', graph_list_first=graph_list_first, graph_list=graph_list, account_list_first=account_list_first, account_list=account_list)

@app.route('/explore', methods=['POST'])
def homepage():
    graph_list_first, graph_list, account_list_first, account_list = return_account_page(app)

    return render_template('explore.html', graph_list_first=graph_list_first, graph_list=graph_list, account_list_first=account_list_first, account_list=account_list)

@app.route('/home', methods=['GET', 'POST'])
def home():
    graph_list_first, graph_list, account_list_first, account_list = return_account_page(app)

    return render_template('add.html', graph_list_first=graph_list_first, graph_list=graph_list, account_list_first=account_list_first, account_list=account_list)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
      # upload file flask
    f = request.files.get('file')

    data = []

    with open(f.filename) as file:
        csv_file = csv.reader(file)
        for row in csv_file:
            data.append(row)

    # get user IP address
    user_ip = request.remote_addr
    db_file = 'database/' + user_ip + 'database.db'

    conn = sqlite3.connect(db_file)

    for values in data:
        conn.execute("INSERT INTO connections (graph, user, followers, following) VALUES " + str(tuple(values)) + ";")

    # save the database to file
    conn.commit()

    graph_list_first, graph_list, account_list_first, account_list = return_account_page(app)

    return render_template('add.html', graph_list_first=graph_list_first, graph_list=graph_list, account_list_first=account_list_first, account_list=account_list)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
