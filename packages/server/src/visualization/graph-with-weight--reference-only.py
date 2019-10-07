Original Graph with weight 
- For reference

# %% markdown
# ## Graph with weight

# %%
# Data Helpers
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