# UNSW-ics-generator
Generate ics calendar files for your UNSW timetable


When you run this python script, you will be asked what subjects you do, what classes you have for each subject, what weeks they are, etc. The output of the script is a `.ics` calendar file, which can be uploaded to any calendar program which supports direct `.ics` importing. (e.g. Owncloud, Thunderbird, Google Calendars etc. Many calendar programs only accept dynamic caldav links.) 

This calendar asks for manual input of each type of class. It does not automatically scrape that info from myUNSW (because I can't be bothered implementing that, and the weeks for each class in myUNSW often don't match the weeks listed in the course outline).

You may be thinking

> What? It's not fully automatic? I could just enter a few weekly events myself. What does this script give me?

Good question. The problem with just adding repeating events is that you need to specify the start and end date for each weekly event (e.g. does it end in week 12 or week 13?), and fortnightly events get messed up by the mid sem break.
