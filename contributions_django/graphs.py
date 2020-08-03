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

# This code is derived from the archived respository:
# https://github.com/alexwlchan/contributions-graph which has an MIT license

from collections import defaultdict
from contributions_django import dateutils
from contributions_django import settings

from collections import namedtuple
import datetime
import re

GridCell = namedtuple("GridCell", ["date", "contributions", "cell_class", "tooltip"])


def generate_contributors_graph(items, title="Contributions"):
    """Parse through items, and generate a GitHub styled contributions graph.
       We use the last modified date since it has a full datetime, and it represents
       the recency of the item.
    """
    counts = defaultdict(int)
    for item in items:

        # Ensure we are always using a naive datetime
        if item.date() not in counts:
            counts[item.date()] = 0
        counts[item.date()] += 1

    # For color ranges, etc.
    quartiles = dateutils.quartiles(counts.values())
    cells = gridify_contributions(counts, quartiles)

    graph = {
        "data": cells,
        "range": range(len(cells[0]) - 6),
        "longest_streak": dateutils.longest_streak(
            [key for key, val in counts.items() if val > 0]
        ),
        "current_streak": dateutils.current_streak(
            [key for key, val in counts.items() if val > 0]
        ),
        "sum": sum(counts.values()),
        "title": title,
        "start_date": dateutils.display_date(dateutils.start()),
        "today_date": dateutils.display_date(dateutils.today()),
        "last_date": ([""] + sorted([key for key, v in counts.items() if v]))[-1],
    }

    # Generate weekdays and months
    weekdays = dateutils.weekday_initials()
    for idx in [0, 2, 4, 6]:
        weekdays[idx] = ""

    months = [
        cell.date.strftime("%b") for cell in gridify_contributions(counts, quartiles)[0]
    ]
    months = filter_months(months)

    # Return the context for the template, namespaced by contributions_django
    return {
        "contributions_django": {
            "graph": graph,
            "today": dateutils.today(),
            "start": dateutils.today(),
            "weekdays": weekdays,
            "months": months,
            # Extra parameters to customize from settings
            "include_bootstrap": settings.include_bootstrap,
            "include_fontawesome": settings.include_fontawesome,
            "icon_classes": settings.icon_classes,
            "gradients": settings.gradients,
        }
    }


def gridify_contributions(contributions, quartiles):
    """
    The contributions graph has seven rows (one for each day of the week).
    It spans a year. Given a dict of date/value pairs, rearrange these results
    into seven rows of "cells", where each cell records a date and a value.
    """
    start = dateutils.start()
    today = dateutils.today()

    graph_entries = []

    # The first row is a Sunday, so go back to the last Sunday before the start
    if start.weekday() == 6:
        first_date = start
    else:
        first_date = start - datetime.timedelta(start.weekday() + 1 % 7)
    next_date = first_date

    first_row_dates = [first_date]
    while (next_date <= today) and (next_date + datetime.timedelta(7) <= today):
        next_date += datetime.timedelta(7)
        first_row_dates.append(next_date)

    # Now get contribution counts for each of these dates, and save the row
    first_row = [
        GridCell(
            date,
            contributions[date],
            _cell_class(date, contributions[date], quartiles),
            tooltip_text(date, contributions[date]),
        )
        for date in first_row_dates
    ]
    graph_entries.append(first_row)

    # For each subsequent day of the week, use the first row as a model: add
    # the appropriate number of days and count the contributions
    for i in range(1, 7):
        row_dates = [day + datetime.timedelta(i) for day in first_row_dates]
        next_row = [
            GridCell(
                date,
                contributions[date],
                _cell_class(date, contributions[date], quartiles),
                tooltip_text(date, contributions[date]),
            )
            for date in row_dates
        ]
        graph_entries.append(next_row)

    return graph_entries


def tooltip_text(date, contributions):
    """
    Returns the tooltip text for a cell.
    """
    if contributions == 0:
        count = "No %s" % settings.item_name
    elif contributions == 1:
        count = "1 %s" % re.sub("s$", "", settings.item_name, 1)
    else:
        count = "%d %s" % (contributions, settings.item_name)
    date_str = dateutils.display_date(date)
    return "%s on %s" % (count, date_str)


def _cell_class(date, contributions, quartiles):
    """
    Returns a function which determines how a cell is highlighted.
    """
    if date > dateutils.today() or date < dateutils.start():
        return "empty"
    elif contributions == 0:
        return "grad0"
    elif contributions <= quartiles[1]:
        return "grad1"
    elif contributions <= quartiles[2]:
        return "grad2"
    elif contributions <= quartiles[3]:
        return "grad3"
    return "grad4"


def filter_months(months):
    """
    We only want to print each month heading once, over the first column
    which contains days only from that month. This function filters a list of
    months so that only the first unique month heading is shown.
    """
    for idx in reversed(range(len(months))):
        if months[idx] == months[idx - 1]:
            months[idx] = ""

    # If the same month heading appears at the beginning and end of the year,
    # then only show it at the end of the year
    if months.count(months[0]) > 1:
        months[0] = ""
    if months.count(months[-1]) > 1:
        months[-1] = ""

    # Since each month takes up cells, we delete an empty space for each month
    # heading
    indices = [idx for idx, month in enumerate(months) if month]
    for idx in reversed(indices):
        if idx != len(months) - 1:
            del months[idx + 1]

    return months
