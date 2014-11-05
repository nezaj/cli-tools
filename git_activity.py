#!/usr/bin/env python
"""
CLI tool for seeing my git activity over the last week

v0.1: First version -- messy but it does the job!

TODO: Clean this up...
"""

from collections import defaultdict, namedtuple, OrderedDict
from datetime import datetime, timedelta
import json
import os
import subprocess

import click
import dateutil.parser
import dateutil.tz
import requests
import pytz

# Use this to make timezone aware datetime objects
pacific_tz = pytz.timezone('US/Pacific')

# Used for converting datetime objects into strings and vice versa
INPUT_DATE_FORMAT = '%m/%d/%y'
ISO8601_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
OUTPUT_DATE_FORMAT = '%m/%d/%y (%A)'

# I use this to build urls from tuples of json data
# This is easier to manage then remembering which index of the tuple
# corresponds to which piece of information
Repo = namedtuple('Repo', 'owner, name')

def date_to_iso8601_string(d):
    """
    Returns iso8601 string representation of a date from a datetime object
    Using this when dealing with github API
    """
    return d.strftime(ISO8601_DATE_FORMAT)

def date_to_ouput_string(do):
    """
    Returns formatted string representation of a date from a datetime object
    Using this to return a pretty format of the date for the file generated
    when I'm done
    """
    return do.strftime(OUTPUT_DATE_FORMAT)

def s_to_iso8601(s):
    """
    Convert a string to a ISO 8601 date-string
    Use this for dealing with github API
    """
    return dateutil.parser.parse(s)

def strip_time(d):
    """
    Remove time time component from a datetime object
    Useful for just getting the current date as a datetime object so
    it can be timezone aware
    """
    return d.replace(hour=0, minute=0, second=0, microsecond=0)

def to_datetime(s):
    """Returns timezone aware datetime object from a formatted string """
    return datetime.strptime(s, INPUT_DATE_FORMAT).replace(tzinfo=pacific_tz)

def today():
    """Returns date-string datetime object representing the current date"""
    dt = datetime.now(pacific_tz)
    return strip_time(dt)

@click.command()
@click.option('--date', default=today, help="Enter date as {} ex: 08/03/14".format(INPUT_DATE_FORMAT))
@click.option('--days', default=7, type=int, help="Enter number of days to generate (default 7)")
def main(date, days):

    # If this is true, that means a date was specified in the command-line
    # In that case it will be a string, will need to make it a datetime object to use timedelta below
    if date != today():
        date = to_datetime(date)
    start_date = date - timedelta(days + 1)  # Add one day because Github API does not include the earliest date when filtering

    # I use this to get my repos
    my_username = 'nezaj'

    # Setup headers for all requests
    api_version = 'application/vnd.github.v3'
    access_token = os.environ.get('GH_PLOG_TOKEN')
    headers = {'Accept': api_version, 'Authorization': 'token ' + access_token}

    # Get my repos
    repos_payload = {'sort': 'pushed', 'direction': 'desc'}
    my_repos_url = 'https://api.github.com/users/{}/repos'.format(my_username)
    my_repos_resp = requests.get(my_repos_url, headers=headers, params=repos_payload)
    my_repos_json = my_repos_resp.json()

    # Get the repos who have had pushes within the specified number of days
    # Github API returns ISO 8601 date strings in UTC
    start_date_utc = start_date.astimezone(pytz.utc)
    updated_repos = []
    for repo in my_repos_json:
        pushed_dt = s_to_iso8601(repo['pushed_at'])
        if pushed_dt > start_date_utc:
            repo_owner = repo['owner']['login']
            repo_name = repo['name']
            updated_repos.append(Repo(repo_owner, repo_name))

    # Add quixey repos to the updated list
    quixey_username = 'quixey'
    my_quixey_repos = [
        'apk-storage',
        'python-quixeycloud',
        'GooglePlayDownloader',
    ]
    for repo in my_quixey_repos:
        updated_repos.append(Repo(quixey_username, repo))

    # Commits endpoint supports filtering by author and date
    start_date_str = date_to_iso8601_string(start_date_utc)
    end_date_str = date_to_iso8601_string(today())
    repo_commit_payload = {'author': my_username, 'since': start_date_str, 'until': end_date_str}

    # Build activity dict from commit endpoint
    activity = defaultdict(list)

    for repo in updated_repos:
        # Get the commits for the repo
        repo_commit_url = 'https://api.github.com/repos/{}/{}/commits'.format(repo.owner, repo.name)
        repo_commit_resp = requests.get(repo_commit_url, headers=headers, params=repo_commit_payload)
        repo_commit_json = repo_commit_resp.json()

        # Store repo name and commit message by commit date
        for repo_commit in repo_commit_json:
            # Extract commit message
            commit_msg = repo_commit['commit']['message']
            if commit_msg.find('\n') > 0:
                commit_msg = commit_msg[:commit_msg.find('\n')]  # Only want first line

            # Some commits may be earlier since they were pushed upstream later
            # I don't want to include these for logging purposes
            commit_dt = repo_commit['commit']['author']['date']
            if commit_dt >= start_date_str:
                # Convert commit_dt to output format and add to activity dict
                commit_dt_utc = strip_time(s_to_iso8601(commit_dt))
                commit_dt_str = date_to_ouput_string(commit_dt_utc)
                activity[commit_dt_str].append((repo.name, commit_msg))

    # Write activity to file in reverse chronological order
    filename = 'tmp/git-activity.html'
    activity = OrderedDict(sorted(activity.items(), reverse=True))
    with open(filename, 'w+') as f:
        for date, commit in activity.iteritems():
            f.write("<h2>{}:</h2>".format(date))
            f.write('<ul>')
            for repo_name, msg in commit:
                f.write('<li>')
                f.write('<b>{}:</b> {}'.format(repo_name, msg))
                f.write('</li>'.format(msg))
            f.write('</ul>')

    # Open the file so I can copy and paste
    subprocess.call(['open', filename])

if __name__ == '__main__':
    main()
