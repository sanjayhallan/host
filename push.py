import git
from datetime import datetime
from combine import combine_all
from dist import write_rank_high_low
from pathlib import Path
import urllib.request
import urllib.error
import os

# Define the repository path and GitHub details
repo_path = Path(__file__).parent

branch = 'main'  # Change this if you're using a different branch
commit_message = 'Auto commit on file change or addition'

RANK_ENDPOINT_URL = os.environ.get("RANK_ENDPOINT_URL")

def post_todays_ranking():
    if not RANK_ENDPOINT_URL:
        raise Exception("Missing RANK_ENDPOINT_URL")

    file_path = repo_path.joinpath("rank").joinpath(f"{datetime.today().strftime('%Y_%m_%d')}.csv")
    if not file_path.exists():
        print(f"{datetime.now()} no ranking data file {file_path.as_posix()}")
        return

    with open(file_path.as_posix(), 'r', encoding='utf-8') as f:
        csv_text = f.read().encode('utf-8')

    req = urllib.request.Request(
        url=RANK_ENDPOINT_URL,
        data=csv_text,
        headers={'Content-Type': 'text/plain'},
        method='POST'
    )

    try:
        with urllib.request.urlopen(req) as response:
            return response.status, response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')
    except urllib.error.URLError as e:
        return None, str(e.reason)

def commit_and_push():
    try:
         # Initialize the repository
        repo = git.Repo(repo_path.as_posix())

        # Check if there is anything to commit
        if repo.is_dirty(untracked_files=True):
            # Add all changes (including untracked files)
            repo.git.add(A=True)

            # Commit the changes
            repo.index.commit(commit_message)

            # Push to GitHub
            origin = repo.remotes.origin
            origin.push(branch)
            print(f'{datetime.now()} all pushed')
        else:
            print(f'{datetime.now()} no changes to push')
    except Exception as e:
        print(f'Error: {e}')

# Run the script
if __name__ == "__main__":
    combine_all()
    write_rank_high_low()
    commit_and_push()
    post_todays_ranking()
