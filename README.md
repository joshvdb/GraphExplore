# Graph Explore

## Introduction

Graph Explore is an analytics engine that allows businesses to find potential customers using data from only a small number of accounts from similar businesses. It is written in Python (using the Flask framework), and can be deployed to a Cloud server.

## Instructions

### Overview

This tool currently relies on users to import data from a given social network into it, through copy and paste operations, or the bulk upload from a csv file. The data must be in csv format. Note that if there are, for example, no accounts following a given account, the field can be left blank.

### Execution

Run app_script.py after downloading this project directory. This will deploy a Flask server, which can then be accessed at the specified url.

### User Input

The main page can be used to enter the comma-separated-value list of accounts that are both follwers of, and following, a given sample account. The Graph that they belong to should also be specified, so that you can have multiple graph sets (e.g., different groups of users). Simply click  "Add Account" when done, and the account details will be added to the graph.


![alt text](https://github.com/polyphron-projects/Graph-Xplore/blob/main/img/main_entry_example.jpeg)


A bulk upload, through a csv file, is also possible, using the "Upload Account Data (csv format)" button. A sample file for this upload is available in the "sample_file" folder.


![alt text](https://github.com/polyphron-projects/Graph-Xplore/blob/main/img/upload_entry_example.jpeg)


### Information Retrieval

You can select an account from a given graph, and click the "Get Account Details" button to retrieve the list of followers and following accounts.


![alt text](https://github.com/polyphron-projects/Graph-Xplore/blob/main/img/main_information_example.jpeg)


### Graph Analytics

On the below page, you can specify the graph you wish to analyze (this should consist entirely of accounts similar to your own). You can also select whether the analysis should be based on follower or following accounts, and which type of graph should be used to visually represent the analysis.


![alt text](https://github.com/polyphron-projects/Graph-Xplore/blob/main/img/selection_example.jpeg)


You can then click "Analyze" and see the results on the next page.


![alt text](https://github.com/polyphron-projects/Graph-Xplore/blob/main/img/results_example.jpeg)


In this simple example, we are analyzing the graph: "graph". Accounts for which we have (following and follower) data are shown in red; accounts that are not directly in our database, and appear only in the following/follower lists of existing accounts, are shown in blue. In the Recommended Accounts section, the recommended accounts that we should follow are shown. This list can easily be copied and pasted.
