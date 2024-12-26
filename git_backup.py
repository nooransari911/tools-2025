import os
import subprocess
from datetime import datetime, timedelta
from google.cloud import bigquery
from google.cloud import storage

def backup_github_repos(request):
    """
    Performs incremental backups of GitHub repositories using Git.
    Uses BigQuery to store backup information and Cloud Storage for storage.
    """

    # Get environment variables
    github_username = os.environ['GITHUB_USERNAME']
    github_token = os.environ['GITHUB_TOKEN']
    bucket_name = os.environ['BACKUP_BUCKET']
    bigquery_project = os.environ['BIGQUERY_PROJECT']
    bigquery_dataset = os.environ['BIGQUERY_DATASET']
    bigquery_table = os.environ['BIGQUERY_TABLE']

    # Create BigQuery client
    bigquery_client = bigquery.Client()
    table_ref = bigquery_client.dataset(bigquery_dataset).table(bigquery_table)

    # Create Cloud Storage client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Get list of repositories
    # (You could fetch repos from the GitHub API, but using env variables is simpler for this example)
    repos = [
        {'name': 'your-repo-name', 'clone_url': 'https://github.com/your-username/your-repo-name.git'},
        # ... Add other repositories here ...
    ]

    for repo in repos:
        repo_name = repo['name']
        clone_url = repo['clone_url']

        # Get current timestamp
        current_backup_time = datetime.utcnow()

        # Check BigQuery for existing backup information
        query = f"""
            SELECT last_commit_sha, last_backup_timestamp
            FROM `{bigquery_project}.{bigquery_dataset}.{bigquery_table}`
            WHERE repo_name = '{repo_name}'
        """
        query_job = bigquery_client.query(query)
        results = query_job.result()

        last_commit_sha = None
        last_backup_timestamp = None
        for row in results:
            last_commit_sha = row.last_commit_sha
            last_backup_timestamp = row.last_backup_timestamp

        # Determine if a full or incremental backup is needed
        if last_commit_sha is None or (current_backup_time - last_backup_timestamp) > timedelta(days=7):
            print(f"Performing full backup for {repo_name}")
            # Full backup using `git clone --mirror`
            backup_dir = f'/tmp/{repo_name}'  # Temporary directory in Cloud Function
            os.makedirs(backup_dir, exist_ok=True)
            subprocess.run(
                ['git', 'clone', '--mirror', clone_url, backup_dir],
                cwd='/tmp',
                check=True,
            )

            # Get latest commit SHA from the cloned repository
            latest_commit_sha = subprocess.check_output(
                ['git', 'rev-parse', 'HEAD'],
                cwd=backup_dir,
            ).decode('utf-8').strip()

            # Upload to Cloud Storage
            blob = bucket.blob(f'{github_username}/{repo_name}.git')
            blob.upload_from_directory(backup_dir)

            # Update BigQuery with the latest commit SHA and backup timestamp
            row_to_insert = {
                'repo_name': repo_name,
                'last_commit_sha': latest_commit_sha,
                'last_backup_timestamp': current_backup_time
            }
            bigquery_client.insert_rows_json(table_ref, [row_to_insert])

        else:
            print(f"Performing incremental backup for {repo_name}")
            # Incremental backup using `git remote update`
            backup_dir = f'/tmp/{repo_name}'
            os.makedirs(backup_dir, exist_ok=True)

            # Clone the repository if it doesn't exist locally
            if not os.path.exists(os.path.join(backup_dir, '.git')):
                subprocess.run(
                    ['git', 'clone', '--mirror', clone_url, backup_dir],
                    cwd='/tmp',
                    check=True,
                )

            # Update the remote repository
            subprocess.run(
                ['git', 'remote', 'update'],
                cwd=backup_dir,
                check=True,
            )

            # Get latest commit SHA from the cloned repository
            latest_commit_sha = subprocess.check_output(
                ['git', 'rev-parse', 'HEAD'],
                cwd=backup_dir,
            ).decode('utf-8').strip()

            # Update BigQuery with the latest commit SHA and backup timestamp
            row_to_insert = {
                'repo_name': repo_name,
                'last_commit_sha': latest_commit_sha,
                'last_backup_timestamp': current_backup_time
            }
            bigquery_client.insert_rows_json(table_ref, [row_to_insert])

    return 'Repositories backed up successfully!'
