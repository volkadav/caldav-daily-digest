#!/usr/bin/python3

"""calendar digest cron script

this logs into a caldav server and tries to get a digest of all of the
events scheduled for that day. naive and hacky but seems to mostly
work? easiest way to run this is from cron.

author: michael.o.jackson@gmail.com

license: apache 2.0"""

from datetime import datetime, timedelta
from os import environ
from urllib.parse import quote_plus
from icalendar import Calendar
import caldav
import pytz
import sys

# you'll probably want to change these:
USERNAME = 'foobar@bazquux.com'
PASSWORD = 'ChAng3M3!'
BASE_URL = 'stbeehive.blahblahblah.foo/caldav/st/principals/individuals/'

# below here you probably will not need to make changes
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)
URL = 'https://' + quote_plus(USERNAME) + ":" + quote_plus(PASSWORD) \
        + '@' + BASE_URL + quote_plus(USERNAME) + '/'
NOW = datetime.now()
DAY_START = datetime(NOW.year, NOW.month, NOW.day)
DAY_END = DAY_START + timedelta(hours=24)

if "TZ" in environ:
    LOCAL_TZ = pytz.timezone(environ["TZ"])
else:
    LOCAL_TZ = pytz.timezone("US/Pacific")

def pretty_print_time(date_time):
    """takes a datetime and normalizes it to local time, prints nicely"""
    local_dt = date_time.replace(tzinfo=pytz.utc).astimezone(LOCAL_TZ)
    return local_dt.strftime("%I:%M %p")

print("pulling events for %d-%d-%d" % (NOW.year, NOW.month, NOW.day))

CLIENT = caldav.DAVClient(URL)
PRINCIPAL = CLIENT.principal()
CALENDARS = PRINCIPAL.calendars()

if not CALENDARS:
    print("No calendars defined for " + USERNAME)
else:
    CALENDAR = CALENDARS[0]
    EVENTS = CALENDAR.date_search(DAY_START, DAY_END)

    if not EVENTS:
        print("Nothing on your calendar for today!")
    else:
        FILTERED_EVENTS = []
        for ev in EVENTS:
            components = Calendar.from_ical(ev.data).walk('vevent')
            if not components:
                continue
            FILTERED_EVENTS.append(components[0])

        FILTERED_EVENTS.sort(key=lambda e: e.decoded('dtstart'))
        for event in FILTERED_EVENTS:
            summary = event.decoded('summary').decode('utf-8')
            description = ""
            if event.decoded('description') != b'':
                description = event.decoded('description').decode('utf-8')
            start = event.decoded('dtstart')
            end = event.decoded('dtend')

            print(u"%s - %s %s\n%s\n\n" % (pretty_print_time(start),
                                           pretty_print_time(end),
                                           summary,
                                           description))
