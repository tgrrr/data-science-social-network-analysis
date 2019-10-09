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

# @focus NEW!
query_issues = """
  repository(owner:"tensorflow", name:"tensorflow") {
    issues(last:20, states:CLOSED) {
      edges {
        node {
          title
          url
          comments(first:10) {
            edges {
              node {
                author {
                  login
                }
                body
              }
            }
          }
          labels(first:5) {
            edges {
              node {
                name
              }
            }
          }
        }
      }
    }
  }
"""

# https://developer.github.com/v4/explorer/
# Only latest 100 commits are returned

# Repo ideas
# name: "tensorflow", owner: "tensorflow"
# name: "keras", owner: "keras-team"
# name: "scikit-learn", owner: "scikit-learn"
# name: "ipython", owner: "ipython"
# name: "spark", owner: "apache"
# name: "django", owner: :django"
# name: "tidyverse", owner: "tidyverse"
# name: "linux", owner: "torvalds"
# name: "node", owner: "nodejs"
# name: "ggplot2", owner: "tidyverse"
# name: "pandas", owner: "pandas-dev" 

 # Define repo
 
query_repos = """
  repository(name: "tensorflow", owner: "tensorflow") {
    ref(qualifiedName: "master") {
      target {
        ... on Commit {
        
         # Commits since X. Only 100 latest commits are returned
          history(since:"2019-01-01T00:00:00Z") {
            edges {
            
             # Commit info returned
              node {
                messageHeadline
                message
                
                # Author of Commit info
                author {
                  user {
                    id
                    login
                  }
                  name
                  email
                  date
                }
                
                # Comments associated with Commit
                comments(first: 10) {
                  edges {
                    node {
                      bodyText
                      createdAt
                      
                      # Reactions of comment
                      reactions(first:10) {
                        edges {
                          node {
                            content
                            createdAt
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
"""