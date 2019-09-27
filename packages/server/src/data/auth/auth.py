import os
from dotenv import load_dotenv

load_dotenv(verbose=False)

class Auth:
    def get_headers():
        _GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
        TOKEN = 'Bearer ' + _GITHUB_ACCESS_TOKEN
        _HEADERS = {"Authorization": TOKEN}
        
        return(_HEADERS)

    HEADERS = get_headers()
