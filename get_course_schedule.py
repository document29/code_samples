#!/usr/bin/python

import os
import sys
import parse_csv_tools as pct
import glob
import syslog
if not os.path.exists('csvs'):
    syslog.syslog(syslog.LOG_WARNING, 'Could not locate directory csvs')
    sys.exit(1)

file_list = glob.glob('csvs/*.csv')
course_data = {}
user_data = {}
enrollment_data = []
for f in file_list:
    fh = open(f, 'r')
    data = pct.load_csv(fh)
    fh.close()
    if not data:
        syslog.syslog(syslog.LOG_ERR, 'Failed to load csv (%s)' % (f))
        continue
    if data.keys()[0] == 'course':
        course_data.update(data.values()[0])
    elif data.keys()[0] == 'user':
        user_data.update(data.values()[0])
    elif data.keys()[0] == 'enrollment':
        enrollment_data.extend(data.values()[0])

course_enrollment = pct.get_active_course_schedule(course_data, user_data, enrollment_data)
if not course_enrollment:
    print "No active courses available"
    sys.exit(0)
pct.print_course_schedule(course_enrollment, course_data)
sys.exit(0)
