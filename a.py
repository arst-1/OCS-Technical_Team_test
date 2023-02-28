import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def get_repositories():
    org_name = request.form['org_name']
    n = int(request.form['n'])
    m = int(request.form['m'])

    # Get a list of repositories for the given organization
    response = requests.get(f'https://api.github.com/orgs/{org_name}/repos')
    repositories = response.json()

    # Sort the repositories based on the number of forks and select the top n repositories
    sorted_repositories = sorted(repositories, key=lambda r: r['forks_count'], reverse=True)[:n]

    # For each selected repository, get a list of forkers sorted by creation date and select the oldest m forkers
    for repository in sorted_repositories:
        response = requests.get(f'https://api.github.com/repos/{org_name}/{repository["name"]}/forks')
        forkers = response.json()

        sorted_forkers = sorted(forkers, key=lambda f: f['created_at'])[:m]

        # Add the oldest m forkers to the repository
        repository['forkers'] = sorted_forkers

    # Render the template with the selected repositories and their oldest m forkers
    return render_template('repositories.html', repositories=sorted_repositories)

if __name__ == '__main__':
    app.run(debug=True)
