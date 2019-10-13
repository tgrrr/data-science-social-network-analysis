import os
import json

PATH = '/Users/phil/code/data-science-next/uni/social-media/ass02_datascience_social_network_analysis/packages/server'
os.chdir(PATH)

from src.data import *
from src.data.queries import queries


# Have we gone over the query count?

# TODO: move to utils file
def get_rate_limit():
    result_rate_limit = fetch_github_query(queries.query_rate_limit) # Execute the query
    remaining_rate_limit = result_rate_limit['data']["rateLimit"]["remaining"] # Drill down the dictionary
    # print("Remaining rate limit - {}".format(remaining_rate_limit))
    return(remaining_rate_limit)

# get_rate_limit()

def do_and_save_query_with_variables_to_file(
    FILENAME = 'data.json',
    query = None,
    variables = None,
    indent = 4,
    ):

    repos_to_query = [
        # ['torvalds', 'linux'], # no issues enabled on github
        # ['apache', 'spark'], # no issues enabled on github
        # ['django', 'django'], # no issues enabled on github
        
        ['ipython', 'ipython'],
        ['nodejs', 'node'],
        ['keras-team', 'keras'], # GOT IT
        ['tensorflow', 'tensorflow'], # GOT IT
        ['pandas-dev', 'pandas'],
        ['scikit-learn', 'scikit-learn'],
        ['tidyverse', 'ggplot2'],
        ['tidyverse', 'tidyverse'],
    ]

    data = {}

    for author,repo in repos_to_query:

        rate_limit = get_rate_limit()
        
        if (rate_limit > 100):

            variables.update(repo_owner=author, repo_name=repo)

            if (variables):
                results = do_fetch_github_query(query, variables)
            else:
                results = fetch_github_query(query)
            
            with open(FILENAME) as data_file:
                print('open file')
                is_file_empty = (os.stat(FILENAME).st_size == 0)
                os.stat(FILENAME).st_size

                try:
                    # Check if file not empty
                    if is_file_empty: 
                        old_data = json.load(data_file)
                        # Merge old_data with new results:
                        print('appending to data') 
                        data[repo].update(results)
                    
                except:
                    print('file is empty')
                    data[repo]=results
                    
            data_file.close()

        else:
            print('rate limit exceeded')

    with open(FILENAME, 'w') as outfile:
        print('saving...')
        # print(data)
        json.dump(
        data, 
        outfile,
        indent=indent
        )
        
def do_and_save_query_to_file(
    FILENAME = 'data.json',
    query = None,
    indent = 4,
    ):

    data = {}

    rate_limit = get_rate_limit()
    
    if (rate_limit > 100):

        results = fetch_github_query(query)
        
        with open(FILENAME) as data_file:
            print('open file')
            is_file_empty = (os.stat(FILENAME).st_size == 0)
            os.stat(FILENAME).st_size

            try:
                # Check if file not empty
                if is_file_empty: 
                    old_data = json.load(data_file)
                    # Merge old_data with new results:
                    print('appending to data') 
                    data[repo].update(results)
                
            except:
                print('file is empty')
                data[repo]=results
                                
        data_file.close()

    else:
        print('rate limit exceeded')

    with open(FILENAME, 'w') as outfile:
        print('saving...')
        # print(data)
        json.dump(
        data, 
        outfile,
        indent=indent
        )