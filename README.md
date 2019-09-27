# Data Science Scoial Network Analysis

github api v4 graphql python3

## Getting Started

To set a project directory:
Navigate to:
`packages/server/src/config/constants.py`

You might need to set it here as well:
`packages/server/notebooks/social_network_graph_analysis.py`

Make a copy of:

`cp packages/server/template.env packages/server/.env`

And update the file to include your [Personal Access Token from Github](https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line)

## Howto guides:

- [Python requests guide](https://www.twilio.com/blog/2016/12/http-requests-in-python-3.html)
- [Using the github api](https://developer.github.com/apps/quickstart-guides/using-the-github-api-in-your-app/)
- [Authentication](https://developer.github.com/v4/guides/forming-calls/#authenticating-with-graphql)

### Github docs

- [Github Dev API](https://developer.github.com/v4/)
- [Auth](https://developer.github.com/v4/guides/forming-calls/#authenticating-with-graphql)
- [Github developer queries](https://developer.github.com/v4/query/)
- [API explorer](https://developer.github.com/v4/explorer/)

### Project Organisation

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── TODO: docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── TODO: requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── TODO: setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── TODO: features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── TODO: models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.testrun.org


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
