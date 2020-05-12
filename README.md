# caldav-daily-digest
a little python script to put together a daily digest of events, e.g. to 
be run from cron to email to a user

# dependencies
  - python 3.x
  - caldav
  - icalendar

(pip install works for both, but as a note, if you have caldav <= 0.5, 
and your system's usernames include an "@", you will need to patch one file 
by hand in line with this bug report:
https://github.com/python-caldav/caldav/issues/11
for convenience, a patch file has been included that can be applied by
running patch -p0 < objects.py.patch wherever you have objects.py
installed on your system)

optional but likely: a functioning cron setup to run this
(e.g.: "30  6 * * 1-5 /path/to/caldav-daily-digest.py" to get a list of
the day's meetings at 6:30am every workday)

# tested on
linux (debian, python 3.4, x86)
