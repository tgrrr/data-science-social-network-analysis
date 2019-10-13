query_issues = """
{
  repository(owner:"keras-team", name:"keras") {
    issues(last:100, states:CLOSED) {
      edges {
        node {
          title
          url
          comments(first:100) {
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
}
"""

issues_results = fetch_github_query(query_issues)
# ['data']['repository']['issues']['edges']

with open('data.json', 'w') as outfile:
    json.dump(issues_results, outfile, indent=4)