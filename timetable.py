# -*- coding: utf-8 -*-

from controller import *
import imgkit

def clean_weekday(weekday_list):
    clean_weekdays = []
    for each in weekday_list:
        split_str = each.split(" ")
        split_str.pop(0)
        clean_weekdays.append(''.join(str(elem) for elem in split_str))
    return clean_weekdays


def get_table(group_name):
    template = bs(open("templates/shedule.html"), "html.parser")
    rows = template.find_all("tr")
    td_list = []
    for weekday in range(0, 6):
	weekday_list = get_week(group_name)
	clean_weekdays = clean_weekday(weekday_list)
	for each in range(1, len(rows)):
	    td = template.new_tag("td")
	    td.string = clean_weekdays[each-1]
	    rows[each].append(td)
    imgkit.from_string(template.prettify(), output_path = "screenshots/timetable.jpg", options = {"xvfb": ""})

