# BookCampground
Python script, which checks for availability of campgrounds for selected dates.
It writes available campgrounds and dates to a file or/and sounds alarm if something is found.
Search is for a specific date, which must be provided as

`campgrounds.py --start_day [1-31] --start_month [1-12]`(current year).
To explore available ranges one can provide

`--flexibility_weeks [0, 2, 4]` to search for exact date, within
2 or 4 weeks after given date respectively.

To silent alarm `--silent True`

If site's interface is changed, script needs to be adjusted for a new page layout.
Any missing libraries can be downloaded using pip.

Mikhail Rogozhin 2016.
<p>License: http://unlicense.org/</p>
Python 3.4
selenium 2.53.2
