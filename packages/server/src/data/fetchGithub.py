import requests
from dotenv import load_dotenv
import json
import os

load_dotenv(verbose=True)
_GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")

print(_GITHUB_ACCESS_TOKEN)

type(_GITHUB_ACCESS_TOKEN)

TOKEN = 'Bearer ' + _GITHUB_ACCESS_TOKEN
HEADERS = {"Authorization": TOKEN}
URL = 'https://api.github.com/graphql'

def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post(
        URL, 
        json={'query': query}, 
        headers=HEADERS
    )
    if request.status_code == 200:
        _request = request.json()
        return(_request["data"])
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

query = """
{{
   search(query: "{queryString}", type: REPOSITORY, first: {maxItems}) {{
     repositoryCount
     edges {{
       node {{
         ... on Repository {{
           name
           url
           stargazers {{ totalCount }}
         }}
       }}
    }}
  }}
}}
"""
variables = {
   'queryString' : 'is:public stars:>9999',
   'maxItems' : '5'
}

result = run_query(query.format(**variables))

# How many repos:
result['search']['repositoryCount']

repos = result['search']['edges']

# get values from repo results for #1
for key, value in repos[1]['node'].items():
    print(key, value)

# Get detailed output:
for i in repos:
    # print(json.dumps(i))
    print('name: ' + i['node']['name'])
    print('url: ' + i['node']['url'])
    print('stars: ' + str(i['node']['stargazers']['totalCount']) + '\n')

# more concise code:
repo_arr = [i['node']['name'] for i in repos]
repo_arr

# Convert to obj to make data easier to access:
from collections import namedtuple
def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
def json2obj(data): return json.loads(data, object_hook=_json_object_hook)
result_obj = json2obj(json.dumps(result))
# dir(result_obj.search.edges[1])

# before:
result['search']['repositoryCount']
#after:
result_obj.search.repositoryCount

result_obj.search.edges[1].node.stargazers.totalCount


# Have we gone over the query count?
query = """
{
  viewer {
    login
  }
  rateLimit {
    limit
    cost
    remaining
    resetAt
  }
}
"""
result = run_query(query) # Execute the query
# remaining_rate_limit = result["data"]["rateLimit"]["remaining"] # Drill down the dictionary
remaining_rate_limit = result["rateLimit"]["remaining"] # Drill down the dictionary
print("Remaining rate limit - {}".format(remaining_rate_limit))


# WIP: Query about charities
# see: https://developer.github.com/v4/explorer/
# queries: https://developer.github.com/v4/query/
query = """
  topic(name:"nonprofit") { 
    stargazers(first:10) {
      totalCount
      edges {
        node {
          name
          url
        }
      }
    }
  }
"""
result = run_query(query)
