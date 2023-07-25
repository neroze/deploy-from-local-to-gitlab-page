import requests
import os
import subprocess


GITLAB_TOKEN = os.environ.get("GITLAB_ACCESS_TOKEN")
GITLAB_PROJECT_ID = os.environ.get("GITLAB_ACCESS_TOKEN")

# Path to the static files to deploy
# STATIC_FILES_PATH = "/Users/nirajmaharjan/python-sandbox/bitbucket-to-Gitlab/dist/"  # dynamic
STATIC_FILES_PATH = "[path to your build]/dist/"  # dynamic
REMOTE_URL = f"https://oauth2:{GITLAB_TOKEN}@gitlab.com/[project]/[Repo].git"

# GitLab Pages configuration
PAGES_BRANCH = "feature/storybook"  # TODO : story book deploy branch
PAGES_DIR = "public"

# Function to deploy static files to GitLab Pages


def deploy_static_files():
    # Clone the GitLab repository to the public directory
    clone_repository()

    # # Move static files to the public directory
    move_files()

    # # Change to the public directory
    os.chdir(PAGES_DIR)

    # # Check if the branch exists, create it if necessary
    if not branch_exists():
        create_branch()

    # # # Configure Git
    configure_git()

    # # # Add and commit the changes
    add_and_commit()

    # # # Push the changes to GitLab Pages
    push_to_pages()
    exit()

# Clone the GitLab repository to the public directory


def clone_repository():
    if not os.path.exists(PAGES_DIR):
        repository_url = REMOTE_URL
        subprocess.run(["git", "clone", repository_url, PAGES_DIR], check=True)
    else:
        print(f"Destination folder '{PAGES_DIR}' already exists.")

# Move static files to the public directory


def move_files():
    subprocess.run(
        ["ls", os.path.join(STATIC_FILES_PATH)])
    subprocess.run(
        ["cp", "-rf", os.path.join(STATIC_FILES_PATH), PAGES_DIR])


# Check if the branch exists
def branch_exists():
    url = f"https://gitlab.com/api/v4/projects/{GITLAB_PROJECT_ID}/repository/branches/{PAGES_BRANCH}"
    headers = {
        "PRIVATE-TOKEN": GITLAB_TOKEN
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False
    else:
        print(
            f"Failed to check branch '{PAGES_BRANCH}'. Error: {response.text}")
        return False

# # Create a new branch for GitLab Pages


def create_branch():
    url = f"https://gitlab.com/api/v4/projects/{GITLAB_PROJECT_ID}/repository/branches"
    headers = {
        "PRIVATE-TOKEN": GITLAB_TOKEN
    }
    data = {
        "branch": PAGES_BRANCH,
        "ref": "main"
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print(f"Branch '{PAGES_BRANCH}' created successfully.")
    else:
        print(
            f"Failed to create branch '{PAGES_BRANCH}'. Error: {response.text}")

# Configure Git


def configure_git():
    subprocess.run(["git", "config", "--global",
                   "user.email", "[email]"])
    subprocess.run(["git", "config", "--global",
                   "user.name", "[name]"])
    subprocess.run(["git", "config", "pull.rebase", "false"])

# Add and commit the changes


def add_and_commit():
    subprocess.run(["git", "add", "."])
    # Commit message
    subprocess.run(["git", "commit", "-m", "Deploy to GitLab Pages"])

# Push the changes to GitLab Pages


def push_to_pages():
    subprocess.run(["git", "remote", "set-url", "origin",
                   REMOTE_URL], check=True)
    subprocess.run(["git", "push", "origin", "--delete", PAGES_BRANCH])

    # subprocess.run(["git", "pull", "origin", PAGES_BRANCH,
    #                "--allow-unrelated-histories"], check=True)

    # subprocess.run(["git", "merge", "origin/{}".format(PAGES_BRANCH),
    #                "--no-edit", "-m", "''"], check=True)
    subprocess.run(["git", "push", "-u", "origin",
                   "HEAD:{}".format(PAGES_BRANCH)], check=True)


# Run the deployment
deploy_static_files()
