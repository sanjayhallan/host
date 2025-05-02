import time
import os
import git
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

# Define the repository path and GitHub details
repo_path = r'C:\Users\PC\git\host'  # Windows path with raw string notation (r'')
watch_path = repo_path + r"\activity"

branch = 'main'  # Change this if you're using a different branch
commit_message = 'Auto commit on file change or addition'

# Event handler for file modifications and additions
class WatcherHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Ignore .git directory changes
        if '.git' in event.src_path:
            return

        # Only track modifications and additions, ignore deletions
        if not event.is_directory and event.event_type in ['created', 'modified']:
            commit_and_push(event.src_path)

def commit_and_push(src_path="all"):
    try:
        # Initialize the repository
        repo = git.Repo(repo_path)

        # Add all changes (excluding .git directory)
        repo.git.add(A=True)

        # Commit the changes
        repo.index.commit(commit_message)

        # Push to GitHub
        origin = repo.remotes.origin
        origin.push(branch)
        print(f'{datetime.now()} {src_path} pushed to Github')
    except Exception as e:
        print(f'Error: {e}')

# Initialize the observer
def start_watching():
    event_handler = WatcherHandler()
    observer = Observer()
    observer.schedule(event_handler, path=watch_path, recursive=False)  # Monitor all subdirectories
    observer.start()

    print(f'Pushing file modifications in {watch_path}')
    commit_and_push()

    print(f'Started watching for file modifications and additions in {watch_path}')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Run the script
if __name__ == "__main__":
    input("Ensure tradestation has loaded fully!!! press any key continue:")
    start_watching()
