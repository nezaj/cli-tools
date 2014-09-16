#!/usr/bin/env python
"""
CLI tool for quickly generating my daily log templates.

TODO: Write tests!
"""
import subprocess
from datetime import datetime, timedelta

# Let's try using click instead of argparse
import click

class BaseLog(object):
    """
    Base object for Log generator objects.

    This class defines methods and helpers to generate
    daily logging entries using properties specified
    by subclasses which inherit from it.
    """

    # The base template for generating my daily logs
    DAILY_LOG_TEMPLATE = 'logs/daily_base.tmpl'

    @classmethod
    def generate_entries(cls, dates):
        with open(cls.LOG_OUTPUT, 'w') as f:
            content = cls._render_daily_entries(dates, cls.TAGS)
            f.write(content)

    @staticmethod
    def _get_template(tmpl):
        """ Returns an unrendered jinja2 template object """
        template_env = get_jinja_env()
        return template_env.get_template(tmpl)

    @classmethod
    def _render_daily_entries(cls, dates, tags):
        template = cls._get_template(cls.DAILY_LOG_TEMPLATE)
        return template.render(dates=dates, tags=tags)

class PersonalLog(BaseLog):

    TAGS = ['Social', 'Done']
    LOG_OUTPUT = 'logs/personal_log.html'

class ProgrammingLog(BaseLog):

    TAGS = ['Productive', 'Done']
    LOG_OUTPUT = 'logs/programming_log.html'

class SixPackLog(BaseLog):

    TAGS = ['Exercise', 'Sugar', 'Diet']
    LOG_OUTPUT = 'logs/sixpack_log.html'

def date_to_string(do):
    """ Returns formatted string representation of a date from a datetime object """
    return do.strftime(OUTPUT_DATE_FORMAT)

def get_jinja_env(path=None):
    """
    Returns jinja2 environment object that loads templates from the specified path.

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

# I like using -h for help as well
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

# These are the daily logs I maintain
DAILY_LOGS = ['personal', 'programming', 'sixpack']

# Used for generating and outputting dates
INPUT_DATE_FORMAT = '%m/%d/%y'
OUTPUT_DATE_FORMAT = '%m/%d/%y (%A)'

# Use this dictionary to fetch the desired log generator -- much cleaner than using a bunch of if/else statements
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
    """ Generates a template for one of my daily log files.  """

    # If a date is specified on the command-line it will be a string -- want to convert it to a datetime object
    if date != today():
        date = to_datetime(date)

    # Ultimately I do want a string representation of all the dates I'm interested in. It's
    # easier however to start with a datetime object and generate a list of dates and
    # then convert them into strings
    dates = [date + timedelta(days=x) for x in range(days)]
    date_strings = reversed([date_to_string(d) for d in dates])

    log = LOG_DICT[log]
    log.generate_entries(date_strings)

    # It's convenient to open the file once it's generated so I can copy and paste
    subprocess.call(['open', log.LOG_OUTPUT])

if __name__ == '__main__':
    main()
