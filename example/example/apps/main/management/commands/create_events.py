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

from django.core.management.base import BaseCommand
from example.apps.main.models import Event
from .event_namer import RobotNamer
import random

from datetime import timedelta
from django.utils import timezone
import pytz


def generate_random_date(start, end):
    """Generate a random datetime between a starting date and an ending date.
    """
    return start + timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())),
    )


class Command(BaseCommand):
    """Create centers based on name"""

    help = "Create original set of events"

    def handle(self, *args, **options):
        print("Creating 1000 events:\n")
        namer = RobotNamer()

        # get today and one year earlier
        today = timezone.now()
        last_year = today - timedelta(days=365)

        for _ in range(1000):
            timestamp = generate_random_date(last_year, today)
            name = namer.generate()
            print("Creating Event %s at %s" % (name, timestamp))
            Event.objects.create(date=timestamp, name=name)
