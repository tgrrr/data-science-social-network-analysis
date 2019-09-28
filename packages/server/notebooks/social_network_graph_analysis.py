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

