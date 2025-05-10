# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pandas",
#     "requests",
#     "rich",
# ]
# ///

import sys
import requests
from rich.pretty import pprint
import pandas

print(f"Python version: {sys.version}")
print(f"Python executable path: {sys.executable}")

resp = requests.get("https://peps.python.org/api/peps.json")
data = resp.json()
pprint([(k, v["title"]) for k, v in data.items()][:10])
