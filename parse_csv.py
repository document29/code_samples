#!/usr/bin/python

import csv
import glob
import os
import sys
import syslog

syslog.openlog('csv_parser', syslog.LOG_PID, syslog.LOG_LOCAL0)
def load_csv(fh):
    if not isinstance(fh, file):
        syslog.syslog(syslog.LOG_ERR, 'load_csv called with a bad parameter')
        raise TypeError('load_csv requires a file like object')
    reader = csv.reader(fh, delimiter=',', quotechar='"')
    headers = reader.next() 
    for header in headers:
        if header.count('course') and not header.count('user'):
            file_type = 'course'
        elif header.count('user') and not header.count('course'):
            file_type = 'user'
        elif header.count('user') and header.count('course'):
            file_type = 'enrollment'
    csv_data = []
    for line in reader:
        csv_data.append(zip(headers, line))
    data = {file_type:csv_data}
    return data
    

if not os.path.exists('csvs'):
    syslog.syslog(syslog.LOG_WARNING, 'Could not locate directory csvs')
    sys.exit(1)
files = glob.glob('csvs/*.csv')
course_data = []
user_data = []
enrollment_data = []
for f in files:
    fh = open(f, 'r')
    data = load_csv(fh)
    fh.close()
    if not data:
        syslog.syslog(syslog.LOG_ERR, 'Failed to load csv (%s)' % (f))
        continue 
    if data.keys()[0] == 'course':
        course_data.extend(data.values()[0])
    elif data.keys()[0] == 'user':
        user_data.extend(data.values()[0])
    elif data.keys()[0] == 'enrollment':
        enrollment_data.extend(data.values()[0])

