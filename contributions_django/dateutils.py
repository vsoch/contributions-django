"""

Copyright (c) 2020, Vanessa Sochat

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import datetime


def today():
    """
    Gets the current date. Wrapper function to make it easier to stub out in
    tests.
    """
    return datetime.date.today()


def start():
    """
    Gets the date from one year ago, which is the start of the contributions
    graph.
    """
    return datetime.date(today().year - 1, today().month, today().day)


def display_date(date):
    """
    Returns a long date string. Example output: "May 24, 2015".
    """
    return date.strftime("%B %d, %Y").replace(" 0", " ")


def previous_day(date):
    """
    Returns the previous day as a datetime.date object.
    """
    return date - datetime.timedelta(1)


def next_day(date):
    """
    Returns the next day as a datetime.date object.
    """
    return date + datetime.timedelta(1)


def elapsed_time(date):
    """
    Given a date in the past, return a human-readable string explaining how
    long ago it was.
    """
    if date > today():
        raise ValueError("Date {} is in the future, not the past".format(date))

    difference = (today() - date).days

    # I'm treating a month as ~30 days. This may be a little inaccurate in some
    # months, but it's good enough for our purposes.
    if difference == 1:
        return "a day ago"
    elif difference < 30:
        return "%d days ago" % difference
    elif difference < 30 * 2:
        return "a month ago"
    elif difference < 366:
        return "%d months ago" % (difference / 30)
    else:
        return "more than a year ago"


def weekday_initials():
    """
    Returns a list of abbreviations for the days of the week, starting with
    Sunday.
    """
    # Get a week's worth of date objects
    week = [today() + datetime.timedelta(i) for i in range(7)]

    # Sort them so that Sunday is first
    week = sorted(week, key=lambda day: (day.weekday() + 1) % 7)

    # Get the abbreviated names of the weekdays
    day_names = [day.strftime("%a") for day in week]

    # Now reduce the names to minimal unique abbreviations (in practice, this
    # means one or two-letter abbreviations).
    short_names = []

    # For each day of the week, start with the first letter, and keep adateing
    # letters until we have a unique abbreviation.
    for idx in range(7):
        day_name = day_names[idx]
        length = 1

        # This list comprehension finds collisions: other day names which match
        # the first (length) characters of this day.
        while [
            day
            for day in day_names
            if day[:length] == day_name[:length] and day != day_name
        ]:
            length += 1

        short_names.append(day_name[:length])

    return short_names


def quartiles(values):
    """
    Returns the (rough) quintlines of a series of values. This is not intended
    to be statistically correct - it's not a quick 'n' dirty measure.
    """
    if not values:
        return [0 for i in range(5)]
    return [i * max(values) / 4 for i in range(5)]


def longest_streak(dates):
    """
    Given a list of datetime.date objects, return the longest sublist of
    consecutive dates. If there are multiple longest sublists of the same
    length, then the first such sublist is returned.
    """
    if not dates:
        return []
    dates = sorted(dates)

    streaks = []
    current_streak = [dates[0]]

    # For each date, check to see whether it extends the current streak
    for idx in range(1, len(dates)):
        date = dates[idx]
        if previous_day(date) == current_streak[-1]:
            current_streak.append(date)
        else:
            streaks.append(current_streak)
            current_streak = [date]

    # When we've gone through all the dates, save the last streak
    streaks.append(current_streak)

    return max(streaks, key=len)


def current_streak(dates):
    """
    Given a list of datetime.date objects, return today's date (if present)
    and all/any preceding consecutive dates.
    """
    streak = []
    current_date = today()

    while current_date in dates:
        streak.append(current_date)
        current_date = previous_day(current_date)

    return sorted(streak)
