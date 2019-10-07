# %%
import requests
import os

# FIXME:
PATH = '/Users/phil/code/data-science-next/uni/social-media/ass02_datascience_social_network_analysis/packages/server'
os.chdir(PATH)

from src.data.auth import auth # fetch_github_query, Auth.HEADERS
from src.config import * # Constants, including URL, PATH
from src.data.queries import queries

HEADERS = auth.Auth.HEADERS
URL = Constants.URL

def fetch_github_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post(
        URL, 
        json={'query': query}, 
        headers=HEADERS
    )
    if request.status_code == 200:
        _request = request.json()
        return(_request)
        # return(_request["data"])
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

from src.data.queries import queries

query_nonprofit = """
  topic(name:"nonprofit") { 
    stargazers(first:10) {
      totalCount
    }
  }
"""

import src.data.queries.graphql_query.graphql

result_nonprofit = fetch_github_query(query_nonprofit)


def do_fetch_github_query(query, variable):
    result_charity = fetch_github_query(query.format(**variable))
    return(result_charity)
