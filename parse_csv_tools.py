#!/usr/bin/python

import csv
import syslog

def get_file_type(mask):
    if mask == 0:
        raise ValueError('Invalid value for mask in get_file_type')
    if mask == 1:
        return 'course'
    if mask == 2:
        return 'user'
    if mask == 3:
        return 'enrollment'

def load_csv(fh):
    if not isinstance(fh, file):
        syslog.syslog(syslog.LOG_ERR, 'load_csv called with a bad parameter')
        raise TypeError('load_csv requires a file like object')
    reader = csv.reader(fh, delimiter=',', quotechar='"')
    headers = reader.next() 
    ccount = 0
    ucount = 0
    for header in headers:
        if header.count('course'):
            ccount = 1
        if header.count('user'):
            ucount = 2
    file_type = get_file_type(ccount+ucount)
    if file_type == 'enrollment':
        csv_data = load_enrollment_csv(reader, headers)
    else:
        csv_data = load_course_user_csv(reader, headers, file_type) 
    return csv_data

def load_enrollment_csv(reader, headers):
    csv_data = []
    for line in reader:
        zip_data = dict(zip(headers, line))
        csv_data.append(zip_data)
    data = {'enrollment':csv_data}
    return data

def load_course_user_csv(reader, headers, file_type):
    csv_data = {}
    for line in reader:
        zip_data = dict(zip(headers, line))
        idx = zip_data.get(file_type+'_id')
        csv_data[idx] = zip_data
    data = {file_type:csv_data}
    return data

def get_active_course_schedule(courses, users, enrollment):
    course_enrollment = {}
    for item in enrollment:
        if item.get('state') == 'deleted':
            continue
        elif item.get('state') == 'active':
            user = users.get(item.get('user_id'))
            course = courses.get(item.get('course_id'))
            if course and course.get('state') == 'active':
                if not course_enrollment.has_key(course.get('course_id')):
                    course_enrollment[course.get('course_id')] = []
                if user and user.get('state') == 'active':
                    course_enrollment[course.get('course_id')].append(user.get('user_name')+'['+user.get('user_id')+']')
    return course_enrollment

def print_course_schedule(course_enrollment, course_data):
    for k,v in course_enrollment.iteritems():
        print course_data.get(k).get('course_name')+'['+k+']'
        for item in v:
                print '\t'+item
    return
