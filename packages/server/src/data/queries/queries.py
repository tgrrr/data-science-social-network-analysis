query_repo = """
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

variables_repo = {
   'queryString' : 'is:public stars:>9999',
   'maxItems' : '5'
}

query_rate_limit = """
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

query_nonprofit = """
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
