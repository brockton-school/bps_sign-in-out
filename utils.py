import subprocess
import os

def format_time(datetime_obj):
    """Formats a datetime object into a 12-hour time string."""
    return datetime_obj.strftime('%I:%M %p')

def get_git_info():
    # Get commit hash and version tag from environment variables
    commit_hash = os.getenv('COMMIT_HASH', 'Unknown')
    # version_tag = os.getenv('VERSION_TAG', 'Unknown')
    version_tag = "v0.1.1b Initial Testing Release"
    return commit_hash, version_tag
