#!/usr/bin/env python
"""CLI tool for quickly generating my daily log templates.

Usage: gen_log [OPTIONS] log
Type gen_log -h for more details

"""
import subprocess
from datetime import datetime, timedelta

# Let's try using click instead of argparse
import click

# click doesn't include -h as a default help flag
# so we need to explicitliy set it and then use
# these settings in our command directory below
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

# The daily logs I maintain
DAILY_LOGS = ['personal', 'programming', 'sixpack']

INPUT_DATE_FORMAT = '%m/%d/%y'
OUTPUT_DATE_FORMAT = '%m/%d/%y (%A)'

class BaseLog(object):
    """Base object for Log generator objects.

    This class defines methods and helpers to generate
    daily logging entries using properties specified
    by subclasses which inherit from it.

    """
    DAILY_LOG_TEMPLATE = 'logs/daily_base.tmpl'

    @classmethod
    def generate_entries(cls, dates):
        """ Used by a logger to generate entries for the specified dates """
        with open(cls.LOG_OUTPUT, 'w') as f:
            content = cls._render_daily_entries(dates, cls.TAGS)
            f.write(content)

    @staticmethod
    def _get_template(tmpl):
        template_env = get_jinja_env()
        return template_env.get_template(tmpl)

    @classmethod
    def _render_daily_entries(cls, dates, tags):
        template = cls._get_template(cls.DAILY_LOG_TEMPLATE)
        return template.render(dates=dates, tags=tags)

class PersonalLog(BaseLog):
    """ Metadata for my personal log """

    TAGS = ['Social', 'Done']
    LOG_OUTPUT = 'logs/personal_log.html'

class ProgrammingLog(BaseLog):
    """ Metadata for my programming log """

    TAGS = ['Productive', 'Done']
    LOG_OUTPUT = 'logs/programming_log.html'

class SixPackLog(BaseLog):
    """ Metadata for my sixpack log """

    TAGS = ['Lift', 'Cardio', 'Diet']
    LOG_OUTPUT = 'logs/sixpack_log.html'

def date_to_string(do):
    """ Returns formatted string representation of a date from a datetime object """
    return do.strftime(OUTPUT_DATE_FORMAT)

def get_jinja_env(path=None):
    """Returns jinja2 environment object that loads templates from the specified path.

    If no path provided then uses the directory of the module that invoked this method
    """
    import os
    import jinja2

    if path is None:
        path = os.path.dirname(os.path.abspath(__name__))

    template_loader = jinja2.FileSystemLoader(path)
    return jinja2.Environment(loader=template_loader)

def to_datetime(s):
    """ Returns datetime object from a formatted string """
    return datetime.strptime(s, INPUT_DATE_FORMAT)

def today():
    """ Returns date object representing the current date """
    return datetime.now().date()

# Use this dictionary to fetch the desired log generator
LOG_DICT = {
    'personal': PersonalLog,
    'programming': ProgrammingLog,
    'sixpack': SixPackLog
}

@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('log', type=click.Choice(DAILY_LOGS))
@click.option('--date', default=today, help="Enter date as {} ex: 08/03/14".format(INPUT_DATE_FORMAT))
@click.option('--days', default=7, type=int, help="Enter number of days to generate (default 7)")
def main(log, date, days):
    """ Generates a template for one of my daily logs """

    log = LOG_DICT[log]

    # If this is true, that means a date was specified in the command-line
    # In that case it will be a string, will need to make it a datetime object to use timedelta below
    if date != today():
        date = to_datetime(date)

    dates = [date + timedelta(days=x) for x in range(days)]
    date_strings = reversed([date_to_string(d) for d in dates]  # Reversing so the latest date will be rendered at the top
    log.generate_entries(date_strings)

    # Open the file so I can copy and paste
    subprocess.call(['open', log.LOG_OUTPUT])

if __name__ == '__main__':
    main()
