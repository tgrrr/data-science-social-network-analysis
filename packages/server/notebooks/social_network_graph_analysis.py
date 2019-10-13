# %% markdown
#
# # COSC2671 Social Media and Network Analytics
# ## Assignment 2
# ### @author Phil Steinke, student: s3725547 github: tgrrr
# ### @author Oliver Eaton, student: s3641518 github: shaggycamel
# ### @author FIXME Aidan Cowie, student: s3429481 github: aidancowie
# ### Due FIXME
# 
# ----------------------------------------------------------------------------

# %% markdown
#
# # Introduction
# ## Describe what/who is your selected entity
# ## Describe why it is interesting to find the sentiment and topics (answer questions) of this entity
#
# #### RUBRIC: Problem Formulation (15%)
# - [ ] The proposed problem/question is interesting, well-motivated and non-trivial. 
# - [ ] Problem and success criteria are well designed and thought out, 
#   - [ ] and scope is realistic.
#
# ## Problem or Question Construction
#
# - [ ] Must include at least one source of social media and networks.
# - [ ] Must include a graph or network and its analysis/processing to solve a problem.
# - [ ] Must include some element of analysis using social media and networks, and something we learnt in class. It cannot be all machine learning for example.
# - [ ] Your analyst or solution is in Python (no R, including visualisation), but parts of it could be done in other languages, e.g., Javascript if you decide to prototype a front end on website.
# - [ ] All code should be your own, you can leverage packages such as `networkx` etc., but it shouldn’t be copied from an existing solution.

# %% markdown
#
# # Data Collection
# ## Describe how you collected the data, and briefly why you chose that approach (restful vs stream)
# ## Report some statistics of your collected data

# %%
import os
import json

PATH = '/Users/phil/code/data-science-next/uni/social-media/ass02_datascience_social_network_analysis/packages/server'
os.chdir(PATH)

from src.data import * # fetch_github_query, Auth.HEADERS
from src.data.auth import * # fetch_github_query, Auth.HEADERS
from src.config import * # Constants, including URL, PATH
from src.data.queries import queries

# %% markdown
#
# What it includes:
#
# - github api v4 
# - graphql queries
# - python 3.7

# %%

# fetch top repositories from github
# AND remove first part of json:

repos_results = do_fetch_github_query(queries.query_repo, queries.variables_repo)['data']['search']

# %% markdown
#
# How many repos:

# %%
print(repos_results['repositoryCount'])

# %% markdown
#
# What are the top 5 repos by stars?

# %%

top_repos = repos_results['edges']
for repo in top_repos:
    _name = repo['node']['name']
    _url = repo['node']['url']
    _stars = str(repo['node']['stargazers']['totalCount'])
    print(
        "Name: %(n)s \nstars: %(s)s \nurl: %(u)s\n" 
        % {'n': _name, 'u': _url, 's': _stars}
        )

# %% markdown
#
# # TODO: Pre-processing and Data Cleaning
# ## TODO: Show examples of noisy data, plot some graphs, etc to show why you decided to do those pre-processing

# ## Describe  what pre-processing you performed
#
# - By switching to a graphql API call, we only get the results we want back
# from the server. Which leaves less json to clean
# - cleaned `node` and `edges` from the json results
#
# ### Convert to obj to make data easier to access:

# %%

# functions to convert json to objects:
from collections import namedtuple
def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
def json2obj(data): return json.loads(data, object_hook=_json_object_hook)

result_obj = json2obj(json.dumps(repos_results))

# before:
repos_results
result_obj.repositoryCount

# total stars for each package:
result_obj.edges[3].node.name
result_obj.edges[3].node.stargazers.totalCount

# %%
# WIP: Query about charities
# see: https://developer.github.com/v4/explorer/
# queries: https://developer.github.com/v4/query/

# FIXME: KeyError: data
# result_nonprofit = fetch_github_query(queries.query_nonprofit)

issues_results = fetch_github_query(queries.query_issues)
# Kill the first few json objects:
issues_results = issues_results['data']['repository']['issues']['edges']

# Output from first issue:
first_issues_title = issues_results[1]['node']['title']
first_issues_comment = issues_results[1]['node']['comments']['edges'][1]['node']['body']
first_issues_author = issues_results[1]['node']['comments']['edges'][1]['node']['author']['login']

print("Title:   %s \nAuthor:  %s\nComment: %s" 
    % (first_issues_title, first_issues_author, first_issues_comment))

# Expensive query:
do_and_save_query_with_variables_to_file(
    FILENAME = 'data.json',
    query = queries.query_issues_dynamic,
    variables = queries.variables_issues,
    indent = 4,
    )

# ###################################

do_and_save_query_to_file(
    FILENAME = 'data.json',
    query = queries.query_repos_tensorflow,
    )

# %% markdown
#
# **Goal:**  Show a network of developers that are contributing to open source projects
#
# - ggplot2
# - spark
# - tidyverse
# - linux
# - django
# - keras
# - pandas
# - ipython
# - scikit-learn
# - node
# - tensorflow
# - TODO: FreeCodeCamp https://github.com/freeCodeCamp/freeCodeCamp
# - TODO: Linux


# %%
import json
import os
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import matplotlib
from collections import Counter
import pandas as pd
import numpy as np
import sys
import altair as alt

# %% markdown
#
# Get list of json files in directory

# %%
PATH = '/Users/phil/code/data-science-next/uni/social-media/ass02_datascience_social_network_analysis/packages/server/data/raw'
FIGURES_PATH = '/Users/phil/code/data-science-next/uni/social-media/ass02_datascience_social_network_analysis/packages/server/notebooks/figures/'

os.chdir(PATH)

# Set default figure size for plots:
matplotlib.rc('figure', figsize=(10, 10))

# From Oli's Jupyter notebook:
# Get list of json files in directory
files_in_drive = os.listdir(PATH)
json_files = []
for ix, file in enumerate(files_in_drive):
    if('.json' in file):
        json_files.append(file)
   
# Remove files if wanted
rm = []
# rm.append(['linux', 'ipython', 'spark', 'node']) # cosc
# rm.append(['django', 'keras', 'tensorflow', 'pandas', 'scikit-learn']) # Python
# rm.append(['ggplot2', 'tidyverse']) # R
for layer in rm:
    for f in layer:
        json_files.remove(f+".json")
json_files

# Prepare keys for dictionary

# %%
# Prepare keys for dictionary
file_names = []
for file in json_files:
    start = file.find('.')
    file_names.append(file[0:start])

# %% markdown
#
# Put all json data into dictionary

# %%
data = {}
for ix, file in enumerate(json_files):
    tmp = json.loads(open(file, encoding="utf-8").read())
    data[file_names[ix]] = tmp['data']['repository']['ref']['target']['history']['edges']

data.keys()

# %% markdown
# ## Graph with weight

# %%
# Data Helpers
repo_user_list = {}
repo_weight = {}

for repo in data:
    ix = 0
    user_list = []
    weight = []
    while ix < len(data[repo]):
        try:
            user = data[repo][ix]['node']['author']['user']['login']
            weight.append(user)
            user_list.append(user)
        except:
            pass
        ix += 1
    repo_user_list[repo] = list(set(user_list))
    repo_weight[repo] = Counter(weight)
# %%
print("Top contributors for each repo\n")
for repo in repo_weight:
    print(repo + ": " + str(repo_weight[repo].most_common(5)))
    # TODO: pretty print
# %%
print("Number of unique contributors for each Repo\n")
for repo in repo_weight:
    print(repo + ": " + str(len(repo_weight[repo])))
# %%
user_contributions = {}

for repo in repo_user_list:
    for user in repo_user_list[repo]:
        if (user not in user_contributions):
            user_contributions[user] = str(repo)
        else:
            tmp = str(user_contributions[user] + " " + repo).split(" ")
            user_contributions[user] = tmp

print("Coders who contribute to more than one repo\n")
for user in user_contributions:
    if type(user_contributions[user]) != str:
        print(user + ": " + str(user_contributions[user]))
# %%
number_of_contributions = Counter()
for repo in repo_weight:
    for user in repo_weight[repo]:
        number_of_contributions[user] += repo_weight[repo][user]
# %%
network_weight = nx.Graph()

for repo in repo_weight:
    size = sum(repo_weight[repo].values())
    network_weight.add_node(repo, repo=repo, size=size, l=repo)

for user in user_contributions:
    repo = user_contributions[user]
    if type(repo) == str:
#         size = number_of_contributions[user]
        weight = repo_weight[repo][user]
        network_weight.add_node(user, repo=repo)
        network_weight.add_edge(repo, user, weight=weight)
    else:
#         size = number_of_contributions[user]
        network_weight.add_node(user, repo='multiple', size = 20, l=user)
        for contribution in repo:              
            weight = repo_weight[contribution][user]
            network_weight.add_edge(contribution, user, weight=weight)
# %%
network_weight = nx.Graph()

for repo in repo_weight:
    network_weight.add_node(repo, repo=repo)
    for user in repo_weight[repo]:
        if (network_weight.has_node(user)) == False:
            network_weight.add_node(user, repo='multiple')
            network_weight.add_edge(repo, user, weight=repo_weight[repo][user])
        else:
            network_weight.add_node(user, repo=repo)
            network_weight.add_edge(repo, user, weight=repo_weight[repo][user])
# %%
# degree centrality
lDegCentrality = nx.degree_centrality(network_weight)
for nodeId, cent in lDegCentrality.items():
    network_weight.node[nodeId]['degree'] = float(cent)
    
# eigenvector centrality
# eigen vector centrality make sno sense on bi-partite graphs
# https://stackoverflow.com/questions/43208737/using-networkx-to-calculate-eigenvector-centrality?rq=1
lEigenVectorCentrality = nx.eigenvector_centrality_numpy(network_weight)
for nodeId, cent in lEigenVectorCentrality.items():
    network_weight.node[nodeId]['eigen'] = float(cent)
    
# katz centrality
lKatzCentrality = nx.katz_centrality(network_weight)    
for nodeId, cent in lKatzCentrality.items():
    network_weight.node[nodeId]['katz'] = float(cent)

# Betweeness centrality
lBetCentrality = nx.betweenness_centrality(network_weight)
for nodeId, cent in lBetCentrality.items():
    network_weight.node[nodeId]['betweenness'] = float(cent)
# %%
for g in nx.local_bridges(network_weight, with_span=True, weight=None):
    if g[2] < 100:
        print(g)
# %%
import altair as alt
alt.renderers.enable('notebook')
# %%
# Generating Data
source = pd.DataFrame({
    'Degree Centrality': list(lDegCentrality.values()),
#     'Eigenvector Centrality': list(lEigenVectorCentrality.values()),
    'Betweenness Centrality': list(lBetCentrality.values()),
    'Katz Centrality': list(lKatzCentrality.values())
})

chart = alt.Chart(source).transform_fold(
    ['Degree Centrality', 'Betweenness Centrality', 'Katz Centrality'],
    as_=['Centrality', 'Measurement']
).mark_area(
    opacity=0.7,
    interpolate='step'
).encode(
    alt.X('Measurement:Q', bin=alt.Bin(maxbins=50)),
    alt.Y('count()', stack=None),
    alt.Color('Centrality:N')
)

chart.configure_legend(
    strokeColor='gray',
    fillColor='#EEEEEE',
    padding=10,
    cornerRadius=10,
    orient='top-right'
)
# %%
# export graphml file
weight_graphFile='weight_repo.graphml'
with open(weight_graphFile, 'wb') as fOut:
    nx.write_graphml(network_weight, fOut)
# %% markdown
#
#  # TODO: Analysis Approach
# ### RUBRIC: Approach (20%)
#
#  - [ ] The approach is an appropriate method to take to solve the problem or answer the analytical question. 
#  - [ ] Approach taken goes beyond using the tools provided in class. 
#  - [ ] Team justifies and explains their approach well. Approach includes data collected and techniques used.
#
#  ## TODO: Describe what analysis you performed to answer the questions
#  ## TODO: What type of sentiment analysis did you do?  Briefly explain your rationale for doing it as such.
#  ## TODO: What type of topic modelling did you do?  Again, briefly explain your rationale for your approach.

# %% markdown
#
# ### RUBRIC: Analysis/result & Discussion (20%)
#
#  - [ ] Problem solving: The solution solves the problem well and all the success criteria are satisfied. 
#  - [ ] Team is able to provide analytical and/or empirical evidence of this.
#  - [ ] Answering analytical question & Analysis component: 
#    - [ ] Excellent discussion of results that answers the question proposed 
#      - [ ] or contributes towards solving the problem. 
#    - [ ] Conclusions are supported by analytical and/or empirical evidence. 
#    - [ ] All success criteria are answered.
# 
#  # TODO: Analysis & Insights
#  ## TODO: Present your analysis, to answer the questions 
#  ## TODO: Present and discuss your insights
#  ## TODO: Use plots, tables, example of prints, visualisation, word clouds etc that supports your analysis and insights

# %% markdown
#
# #  Conclusion
# ##  Provide a short conclusion about your entity, analysis and what you found

# %% markdown
#
# ### Team Management & Mentoring
#
# - [ ] Use timesheets
# - [ ] Set up regular meetings within your team
# - [ ] We've setup a slack channel
# - [ ] [Github repo](https://github.com/tgrrr/data-science-social-network-analysis)
# - [ ] Meet lecturers 3 times before assignment due
