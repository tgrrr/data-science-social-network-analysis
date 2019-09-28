#
# TODO:
# Make nodes bigger/another colour

# ----------------------------------------------------------------------------

# %% markdown
#
# # COSC2671 Social Media and Network Analytics
# ## Assignment 2
# ### @author Phil Steinke, student: s3725547 github: tgrrr
# ### @author Oli FIXME, student: FIXME github: shaggycamel
# ### @author FIXME Aidan Cowie, student: s3429481 github: aidancowie
# ### Due FIXME

# ----------------------------------------------------------------------------

# %%
import os

PATH = '/Users/phil/code/data-science-next/uni/social-media/ass02_datascience_social_network_analysis/packages/server'
os.chdir(PATH)

from src.data import * # fetch_github_query, Auth.HEADERS
from src.config import * # Constants, including URL, PATH
from src.data.queries import queries

# %% markdown
#
# How many repos:

# %%

result_charity = do_fetch_github_query(queries.query_repo, queries.variables_repo)

# %% markdown
#
# How many repos:

# %%

repos_charity_count = result_charity['search']['repositoryCount']
print(repos_charity_count)


# %% markdown
#
# What are the top repos?

# %%

repos_charity = result_charity['search']['edges']

# import json
for i in repos_charity:
    _name = i['node']['name']
    _url = i['node']['url']
    _stars = str(i['node']['stargazers']['totalCount'])
    print("Name: %(n)s \nstars: %(s)s \nurl: %(u)s\n" 
        % {'n': _name, 'u': _url, 's': _stars})
    # print(json.dumps(i))

# get values from repo results for #1
# for key, value in repos_charity[1]['node'].items():
#     print(key, value)

# more concise code:
# repo_arr = [i['node']['name'] for i in repos_charity]
# repo_arr

# Convert to obj to make data easier to access:
from collections import namedtuple
def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
def json2obj(data): return json.loads(data, object_hook=_json_object_hook)
result_charity_obj = json2obj(json.dumps(result_charity))
# dir(result_charity_obj.search.edges[1])

# before:
result_charity['search']['repositoryCount']
#after:
result_charity_obj.search.repositoryCount

result_charity_obj.search.edges[1].node.stargazers.totalCount

# Have we gone over the query count?

result_rate_limit = fetch_github_query(queries.query_rate_limit, Constants.URL, Auth.HEADERS) # Execute the query
remaining_rate_limit = result_rate_limit["rateLimit"]["remaining"] # Drill down the dictionary
print("Remaining rate limit - {}".format(remaining_rate_limit))

# WIP: Query about charities
# see: https://developer.github.com/v4/explorer/
# queries: https://developer.github.com/v4/query/
result_nonprofit = fetch_github_query(query_nonprofit)



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
from os import listdir
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd

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
files_in_drive = listdir(PATH)
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

# %% markdown
# ## Graph with weight

# %%
repo_weight = []
user_list = []
repo_user_list = {}
network_weight = nx.Graph()

for repo in data:
    ix = 0
    network_weight.add_node(repo)
    while ix < len(data[repo]):
        try:
            user = data[repo][ix]['node']['author']['user']['login']
            network_weight.add_node(user)
            repo_weight.append(repo + " " + user)
            user_list.append(user)
        except:
            pass
        ix += 1
    repo_user_list[repo] = list(set(user_list))

repo_weight = Counter(repo_weight)
# %%
for weight in repo_weight:
    space = weight.find(' ')
    r = weight[0:space].strip()
    u = weight[space+1:len(weight)].strip()
    w = repo_weight[weight]
    network_weight.add_edge(r, u, weight=w)
# %%
nx.draw(network_weight, with_labels=True, pos=nx.kamada_kawai_layout(network_weight, scale=10))
plt.axis('off')
plt.rcParams["figure.figsize"] = (10,10) # new
plt.savefig(FIGURES_PATH + 'network_with_weight.png', bbox_inches='tight') # new

plt.show()

# %% markdown
# ## Graph without weight

# %%
network_no_weight = nx.Graph()

for repo in data:
    network_no_weight.add_node(repo)
    ix = 0
    while ix < len(data[repo]):
        try:
            user = data[repo][ix]['node']['author']['user']['login']
            network_no_weight.add_node(user)
            network_no_weight.add_edge(repo, user)
        except:
            pass
        ix += 1
# %%
nx.draw(network_no_weight, pos=nx.kamada_kawai_layout(network_no_weight, scale=10), with_labels=False)
plt.axis('off')
plt.rcParams["figure.figsize"] = (20,20) # new
plt.savefig(FIGURES_PATH + 'network_no_weight.png', bbox_inches='tight')
plt.show()

# %% markdown