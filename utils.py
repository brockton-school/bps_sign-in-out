import subprocess

def format_time(datetime_obj):
    """Formats a datetime object into a 12-hour time string."""
    return datetime_obj.strftime('%I:%M %p')

def get_git_info():
    # try:
    #     # Get the latest short commit hash
    #     commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('utf-8').strip()
    #     # Get the latest version tag (if any)
    #     version_tag = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0']).decode('utf-8').strip()
    # except subprocess.CalledProcessError:
    #     # Handle the case when the git command fails (e.g., no tags)
    commit_hash = ""
    version_tag = "0.0.1 beta"
    
    return commit_hash, version_tag
