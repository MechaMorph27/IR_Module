import json
import os

FILE = "issues.json"

def load_issues():

    if not os.path.exists(FILE):

        save_issues([])

        return []

    try:

        with open(FILE, "r") as f:

            data = json.load(f)

            return data.get("issues", [])

    except:

        return []

def save_issues(data):

    with open(FILE, "w") as f:

        json.dump(
            {
                "issues": data
            },
            f,
            indent=4
        )
def add_issue(issue):

    issue = issue.strip()

    if not issue:
        return

    issues = load_issues()


    if issue not in issues:

        issues.append(issue)

        save_issues(issues)

def delete_issue(issue):

    issues = load_issues()


    if issue in issues:

        issues.remove(issue)

        save_issues(issues)