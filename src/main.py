import requests

"""

An system that automates voting on Urban Dictionary.
plz no spam >:(

"""

class terminal:
    def __init__(self):
        from pystyle import System
import os
        System.Clear()

class functions:
    def request():
        response = requests.post(
            "https://api.urbandictionary.com/v0/vote",
            json={"defid": 5010758, "direction": "up"},
            headers={"Content-Type": "application/json"}
        )


if __name__ == "__main__":
    print("Starting..")

