#!/usr/bin/env python
"""
Creates pre-filled templates for my daily logs

TODO: Write tests so you can refactor
TODO: Use a class-based approach for generating different logs
"""
import click
from datetime import datetime, timedelta

# Used for generating and outputting dates
INPUT_DATE_FORMAT = '%m/%d/%y'
OUTPUT_DATE_FORMAT = '%m/%d/%y (%A)'

# These are the daily logs I maintain
DAILY_LOGS = ['personal', 'programming', 'sixpack']

# The base template for generating my daily logs
DAILY_LOG_TEMPLATE = 'logs/daily_base.tmpl'

# Output files for generated templates
PERSONAL_LOG_OUTPUT = 'logs/personal_log.html'
PROGRAMMING_LOG_OUTPUT = 'logs/programming_log.html'
SIXPACK_LOG_OUTPUT = 'logs/sixpack_log.html'

def _get_template(tmpl):
    """ Returns an unrendered jinja2 template object"""
    template_env = get_jinja_env()
    return template_env.get_template(tmpl)

def date_to_string(do):
    """ Returns formatted string based on OUTPUT_DATE_FORMAT from datetime object """
    return do.strftime(OUTPUT_DATE_FORMAT)

def generate_personal_entries(dates):
    tags = ['Social', 'Felt', 'Done']
    with open(PERSONAL_LOG_OUTPUT, 'w') as f:
        content = render_daily_entries(dates, tags)
        f.write(content)

def generate_programming_entries(dates):
    tags = ['Productive', 'Done']
    with open(PROGRAMMING_LOG_OUTPUT, 'w') as f:
        content = render_daily_entries(dates, tags)
        f.write(content)

def generate_sixpack_entries(dates):
    tags = ['Exercise', 'Sugar', 'Diet']
    with open(SIXPACK_LOG_OUTPUT, 'w') as f:
        content = render_daily_entries(dates, tags)
        f.write(content)

def get_jinja_env(path=None):
    """
    Returns jinja2 environment object that loads templates from the specified path.

    If no path provided then uses the invoked modules directory by default
    """
    import os
    import jinja2

    if path is None:
        path = os.path.dirname(os.path.abspath(__name__))

    template_loader = jinja2.FileSystemLoader(path)
    return jinja2.Environment(loader=template_loader)

def render_daily_entries(dates, tags):
    template = _get_template(DAILY_LOG_TEMPLATE)
    return template.render(dates=dates, tags=tags)

def to_datetime(s):
    """ Returns datetime object from string with INPUT_DATE_FORMAT """
    return datetime.strptime(s, INPUT_DATE_FORMAT)

def today():
    return datetime.now().date()

# I like using -h for help as well
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('log', type=click.Choice(DAILY_LOGS))
@click.option('--date', default=today, help="Enter date as {} ex: 08/03/14".format(INPUT_DATE_FORMAT))
@click.option('--days', default=7, type=int, help="Enter number of days to generate")
def main(log, date, days):
    """
    Generates a template for one of my daily log files.

    By default I expect to generate a week worth of entries. The generated
    templates are saved in the logs folder
    """

    # If a date is provied it will be a string -- want to convert it to a datetime object
    if date != today():
        date = to_datetime(date)

    # Ultimately I do want a string representation of all the dates I'm interested in. It's
    # easier however to start with a datetime object and generate a list of dates and
    # then convert them into strings
    dates = [date + timedelta(days=x) for x in range(days)]
    date_strings = reversed([date_to_string(d) for d in dates])

    generate_log = generator_dict[log]
    generate_log(date_strings)

generator_dict = {
    'personal': generate_personal_entries,
    'programming': generate_programming_entries,
    'sixpack': generate_sixpack_entries
}

if __name__ == '__main__':
    main()
