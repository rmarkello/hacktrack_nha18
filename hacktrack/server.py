import os.path as op
from flask import Flask, send_from_directory
from hacktrack import get_project_info, PROJECT_LIST

dname = op.join(op.dirname(op.dirname(op.abspath(__file__))),
                'blog/static')
app = Flask(__name__, static_folder=dname)


def get_author(x):
    if isinstance(x, dict):
        return x['login']
    return ''


@app.route('/')
def index():
    return send_from_directory(dname, 'index.html')


@app.route('/data')
def data():
    commits, issues = get_project_info(PROJECT_LIST, verbose=False)
    commits.author = commits.author.apply(get_author)
    commits = commits[['author', 'additions', 'deletions']]
    return commits.to_json()


def run_server():
    app.run()
