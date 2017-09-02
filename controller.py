# -*- coding: utf-8 -*-

import requests
import re
import MySQLdb
from bs4 import BeautifulSoup as bs
from settings import *
from views import resultsView, schedulePrint
from datetime import time, date, datetime, timedelta
from schedule import site, findSchedule, takingData, takingStyles, rowFinding, whatLesson, checkStyles


url = 'http://www.bmstu.ru/mstu/undergraduate/schedule/table-view/'

# Return results of the last exams.
def getResults( groups, surname ):
    # List that we return after web parsing.
    session = requests.Session()
    exams  = {}
    credit = {}
    course = {}

    # Base url for concatenation.
    baseUrl = "https://webvpn.bmstu.ru"
    # Url for post request.
    url = "https://webvpn.bmstu.ru/+webvpn+/index.html"
    # Link to the last session
    examUrl = "https://webvpn.bmstu.ru/+CSCO+0h75676763663A2F2F72682E6F7A6667682E6568++/modules/session/"
    
    # Prepare for POST request to auth.
    params  = { 'tgroup':"", 'next':"", 'tgcoockieset': "", 'username':login, 'password':password, 'Login':"Login"}
    # Pretend we're not a replicant ( blade runner style )
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
    
    #Get some cookies from website
    try:
        loginPost = session.post( url, params )
    except ConnectionError:
        return  "Проблемы с доступом к электронному университету.Уже разбираюсь."

    if( len( loginPost.cookies.get_dict().keys() ) ) == 1:
        loginPost = session.post( url, params )

    #Start to crawl.
    examData = session.get( examUrl, cookies = loginPost.cookies, headers = headers )
    bsObj = bs( examData.text, "lxml" )
    tryList = []
    groupsList = bsObj.findAll("a",{"name":"sdlk"})
    groupsFound = False
    surnameFound = False

    for each in groupsList:
        if groups in each.get_text().encode("latin-1"):
            groupsFound = True
            examTableUrl = each['href']
            examTableData = requests.get( baseUrl + examTableUrl,  cookies = loginPost.cookies, headers = headers )
            bsExamObj = bs( examTableData.text, "html")
            for each in bsExamObj.find("table").tbody.findAll("div",{"class":"student-fio"}):
                if surname in each.get_text().encode("latin-1"):
                    surnameFound = True
                    for exam in each.find_parents('tr')[0].findAll('td',{"test-type":re.compile("[0-9]")}):
                        if exam['test-type'] == "1":
                            if type(exam.span) != None.__class__:
                                exams[exam['title'].encode('latin-1').split('—')[1]] = exam.span.get_text().encode("latin-1")
                        if exam['test-type'] == "2":
                            if type(exam.span) != None.__class__:
                                credit[exam['title'].encode('latin-1').split('—')[1]] = exam.span.get_text().encode("latin-1")
                        if exam['test-type'] == "3":
                            if type(exam.span) != None.__class__:
                                course[exam['title'].encode('latin-1').split('—')[1]] = exam.span.get_text().encode("latin-1")
    if not groupsFound:
        return  " Не удалось найти такую группу. "
    elif not surnameFound:
        return  " Не смог найти такого студента, проверь фамилию. "
    
    return resultsView( exams, credit, course )

def checkIn ( vkId, surname, uid, name = None ):
    # Create connection to MySQL db
    conn = MySQLdb.connect( MYSQL_HOST, MYSQL_USER, MYSQL_PASSWD, MYSQL_DB, charset = 'utf8', use_unicode = True )
    cursor = conn.cursor()
    # Arguments for stored procedure createUser()
    args = [ vkId, surname, name, uid ]
    # Call procedure
    cursor.callproc( "createUser", args )
    # Retrieve call result
    result = cursor.fetchone()
    if result is None:
    	conn.commit()
	cursor.close()
    	conn.close()
	return " Студент успешно зарегистрирован "
    else:
	cursor.close()
	conn.close()
	return " Вы уже зарегистрированы "

#ищем пару, которая идет в данный момент времени
def timeSchedule(mes, period):
    schedule_url = findSchedule(site(url), mes)
    if schedule_url == 'nothing':
        print 'Расписания нет'
        return 'Расписания нет'
    #понделеьник первой недели первого семестра
    d = date(2017, 9, 1) #1 september
    def_weekday = d.isoweekday() - 1  #what is it weekday?
    d = d - timedelta(days=def_weekday) #find monday of the first week
    
    #необходимые данные по входной дате
    #d2 = date(2017, 10, 18)  
    d2 = datetime.now().date()
    week_counter = ((d2 - d).days / 7) % 2 #find is current week 'чс' == 0 or 'зн' == 1
    #t = time(13, 10)
    t = datetime.now().time()
    dt = datetime.combine(d2, t)
    weekday = dt.isoweekday()
    
    #парсим расписание
    soup = bs(site(schedule_url), 'lxml')
    text = soup.get_text()
    lines = takingData(text)
    lines[0] = lines[0][1:-1]
    groups = lines[0].split('","')
    
    # вычисляем номер столбца, который принадлежит нужной группе
    col = 0
    for each in groups:
        if each == mes + ' ':
            break
        else:
            col+=1
    #теперь еще и стили оказывается надо найти
    styles = takingStyles(text)

    #наконец-то начинаем поиск нужной пары
    cur_row = rowFinding(weekday, week_counter, t)
    if period == 'next' and cur_row != -1:
        cur_row += 2    
    print whatLesson(lines, cur_row, col, styles)
    #return whatLesson(lines, cur_row, col, styles)

def weekSchedule(mes): 
    schedule_url = findSchedule(site(url), mes)  
    if schedule_url == 'nothing':
        return 'Расписания нет' 
    d = date(2017, 9, 1) #1 september
    def_weekday = d.isoweekday() - 1  #what is it weekday?
    d = d - timedelta(days = def_weekday) 
    #d2 = date(2017, 10, 1)
    d2 = datetime.now().date()
    weeknumber = ((d2 - d).days / 7) + 1  
    week_counter = weeknumber % 2 #'чс' == 1 or 'зн' == 0
    soup = bs(site(schedule_url), 'lxml')
    text = soup.get_text()
    lines = takingData(text)
    lines[0] = lines[0][1:-1]
    groups = lines[0].split('","')
    col = 0
    row = 0
    tmp_row=''
    
    for each in groups:
        if each == mes + ' ':
            break
        else:
            col+=1
    styles = takingStyles(text)
    schedule_row = []
    if week_counter == 1:
        tmp_row = 'Числитель'
    else :
        tmp_row = 'Знаменатель'
    schedule_row.append('Неделя №' + str(weeknumber) + '   ' + tmp_row)
   
    for each in lines:
            each = each[1:-1]
            row += 1   
            getting_line = each.split('","')
            if getting_line[col] == '':
                cell = checkStyles(row - 1, col, styles)
                if cell[0] == -1:
                    getting_line[col] = '    ---'
                else:
                     tmp = lines[cell[0]].split('","')
                     getting_line[col] = tmp[cell[1]]
            elif getting_line[col].find('---') != -1 :
                 getting_line[col] = '    ---'
            
            if getting_line[1] != '' : 
                tmp_row = getting_line[1]
            else:
                getting_line[1] = tmp_row

            if week_counter == 0:
                if row % 2 == 1:
                    schedule_row.append(getting_line[1] + "   " + getting_line[col])
            else:
                if row % 2 == 0:
                    schedule_row.append(getting_line[1] + "   " + getting_line[col])
                
            if (row - 1) % 14 == 0:
                schedule_row.append('---------------------------------------------------')
    return schedule_row

def daySchedule(mes):
    weekday = datetime.now().date().isoweekday()
    #weekday = 7
    if weekday == 7:
        print "Сегодня выходной, отдыхай)"
        print "Вот тебе пары на завтра:"
        print ''
        return tomorrowSchedule(mes)
    else:
        lessons_list = weekSchedule(mes)
        first_el = (weekday - 1) * 8 + 2
        last_el = first_el + 7
        day_lessons = lessons_list[first_el : last_el]
        schedulePrint(day_lessons)
        return day_lessons

def tomorrowSchedule(mes):
    cur_weekday = datetime.now().date().isoweekday()
    #cur_weekday = 7
    if cur_weekday == 7:
        weekday = 1
    else:
        weekday = cur_weekday + 1
    #weekday = 7
    if weekday == 7:
        print "Завтра выходной, отдыхай)"
        return "Завтра выходной, отдыхай)"
    else:
        lessons_list = weekSchedule(mes)
        first_el = (weekday - 1) * 8 + 2
        last_el = first_el + 7
        day_lessons = lessons_list[first_el : last_el]
        schedulePrint(day_lessons)
        return day_lessons

