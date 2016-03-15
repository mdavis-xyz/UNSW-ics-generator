from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz
# from icalendar import UTC # timezone

debug = True

def dayStrToInt(dayStr):

    d = {
        "mon":0,
        "tue":1,
        "wed":2,
        "thu":3,
        "fri":4,
        "sat":5,
        "sun":6
    }

    return d[dayStr.lower()[0:4]]

tz=pytz.timezone("Australia/Sydney")

def calcTime(semStart,breakWeeks,week,dayOfWeek,hour):
    td = timedelta(days=7*(week-1))
    d = semStart + td
    for b in breakWeeks:
        if week > b:
            d = d + timedelta(days=7)
    d = d + timedelta(days=dayStrToInt(dayOfWeek))
    d = d + timedelta(hours=hour)
    return d


def add_event(cal,code,subject,classtype,location,start,end,weeknum):
    if debug:
        print('Adding event:'
             +'\n   code: ' + code
             +'\n   subject: ' + subject
             +'\n   classtype: ' + classtype
             +'\n   location: ' + location
             +'\n   start: ' + str(start)
             +'\n   end: ' + str(end)
             +'\n   weeknum: ' + str(weeknum)
             + '\n\n'
              )

    event = Event()
    event.add('summary', code + ' ' + classtype)
    event.add('dtstamp', datetime.today()) #year,month,day
    event.add('dtstart', start) #year,month,day
    event.add('dtend',   end)
    event.add('location', location)
    event.add('uid', str(start) + '-' + code + '-UNSW-timetable')
    event.add('description',code + ' - ' + subject + '\nWeek ' + str(weeknum) + ' ' + classtype)

    cal.add_component(event)

    return cal

def blank_calendar():
    cal = Calendar()
    cal.add('prodid', '-//My calendar product//mxm.dk//')
    cal.add('version', '2.0')
    return cal

# def save_calendar(cal, filename):
#     f = open(filename, 'wb')
#     f.write(cal.to_ical())
#     f.close()

def cal_download(cal):
    icsStr = cal.to_ical()
    print('<code>' + icsStr + '</code>')


def main():
    print("Welcome to Matt's .ics timetable creator\n\n")
    print("This script generates a static .ics calendar file to be uploaded into a calendar program.")
    print("It does this based on the information you give it about when your classes are.\n")

    unsw = input('Are you a UNSW student? (y/n)\n')
    unsw = unsw[0].lower() == 'y'
    if unsw:
        weeksPerSem = 13
    else:
        print('This script is designed for UNSW students. It might work for any other student.')
        print('It it doesn\'t work, email me: matthew%smdavis%sxyz','@','.')
        weeksPerSem = int(input('How many weeks per semester/term?\n'))


    semStartYear = int(input("What year is this for?\n"))
    semStartMonth = int(input("What month does the semester start? (As an integer, e.g. \"3\" for March.)\n"))
    semStartDay = int(input("What day of the month does semester start? (As an integer, e.g. \"5\")\n"))

    semStart = datetime(semStartYear, semStartMonth, semStartDay, 0, 0, 0, tzinfo=pytz.timezone("Australia/Sydney"))

    if unsw:
        breakWeeks = [int(input("The mid sem break is after which week?\n"))]
    else:
        breakWeeks = input('When are the breaks? I\'m assuming each break is one week long.'
                           + 'So if there is a 1 week break after week 4, and 2 week beak after week 10'
                           + 'write \"4,10,10\". (Separate each week with commas, no space)')
        breakWeeks = map(int,weeks.split(','))

    cal = blank_calendar()

    code = input("what is the code of your first subject? (e.g. \"ELEC1112\")\n")
    while code != "":
        subject = input("What is the subject name? (e.g. \"Introduction to Electronics\")\n")
        classtype = input("What is the first class type? (e.g. \"lecture\")\n")
        while classtype != "":
            numOfType = int(input('How many ' + classtype.lower() + 's are there per week?\n'))
            for x in range(0,numOfType):
                dayOfWeek = input('For ' + classtype + ' number ' + str(x+1) + ', what day of the week is this class? (e.g. Mon, Tue) \n')
                startHour = int(input('What time does it start? (Use 24h time, e.g. \"9\", \"13\")\n'))
                endHour = int(input('What time does it end? (Use 24h time, e.g. \"10\", \"14\")\n'))
                weeks = input("What weeks does this " + classtype + " run?\n(list all weeks, no dashes. Separate with commas, no spaces. e.g. \"1,2,3,4,5,6,7,8,9\")\n")
                weeks = list(map(int,weeks.split(',')))
                for w in weeks:
                    if not 0 <= w <= weeksPerSem:
                        print('Warning: week %d is not within the %d week UNSW semester' % (w,weeksPerSem))
                        cont = input("Do you want to continue? (Y/N)")
                        if cont[0].lower() == 'n':
                            print('aborting')
                            return
                        else:
                            print('continuing')
                allWeeks = set(range(1,weeksPerSem+1))
                weeksOut = allWeeks - set(weeks)
                # print("Ok, so I'm excluding weeks %s" % str(weeksOut))
                location = input("Where is this " + classtype + "?\n")
                if debug:
                    print('\nweeks = ' + str(weeks) + 'type: ' + str(type(weeks)))
                for week in weeks:
                    startTime = calcTime(semStart,breakWeeks,week,dayOfWeek,startHour)
                    endTime = calcTime(semStart,breakWeeks,week,dayOfWeek,endHour)
                    cal = add_event(cal,code,subject,classtype,location,startTime,endTime,week)
            classtype = input('What is the next class type for '
                          + code + '? (Press enter if there is no more for this subject)\n')
        code = input("What is the code of your next subject? (e.g. \"ELEC1112\") (Press enter if there are no more.)\n")

    filename = input("What filename would you like the calendar saved as?\n")
    save_calendar(cal,filename)
    print("done! Saved as " + filename + '\n')
    # cal_download(cal)
    print('done!')

main()
