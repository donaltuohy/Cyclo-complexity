import flask, requests, git
from flask import Flask


app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisShouldBeSecret'


if __name__ == "__main__":

    response = requests.get("https://api.github.com/repos/donaltuohy/CS4400---Internet-Applications/commits")
    jsonResponse = response.json()
    listOfCommits = []
    for commit in jsonResponse:
        listOfCommits.append(commit['sha'])

    print(listOfCommits)
