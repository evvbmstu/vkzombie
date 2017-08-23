
# -*- coding: utf-8 -*-
import json
import requests
from bs4 import BeautifulSoup as bs
import re
import sys
from inner import pfInner
from outter import pfOutter
from settings import login, password
reload(sys)
sys.setdefaultencoding('utf8')
def perfomanse( inputStr ):
    #Списки которые отдадим обратно
    session = requests.Session()
    exams = {} # Словарь вида <наименование экзамена> : <оценка> <str><str>
    credit = {} # Словарь вида <наименование > : <оценка> <str><str>
    course = {} # Словарь вида <наименование курсовых> : <оценка> <str><str>
    count = 0
    # Смотрим на входный текст с предварительным форматированием.
    try:
        groups,surname = pfInner( inputStr )
    except TypeError:
        return "Неправильно введена команда"
        #return errorMsg
    # Вернет NULL если строчка не подходит.
    
    #Базовая ссылка для конкантенации
    baseUrl = "https://webvpn.bmstu.ru"
    # Ссылка куда на самом деле идет POST на webvpn.
    url = "https://webvpn.bmstu.ru/+webvpn+/index.html"
    # Ссылка на последнюю сессию
    examUrl = "https://webvpn.bmstu.ru/+CSCO+0h75676763663A2F2F72682E6F7A6667682E6568++/modules/session/"
    # Логин и пароль для авторизации.
    
    # Формируем POST запрос для авторизации.
    params = { 'tgroup':"", 'next':"", 'tgcoockieset': "", 'username':login, 'password':password, 'Login':"Login"}
    # Притворяемся браузером на всякий случай.
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
    
    #Получаем куки от сайта:
    try:
        loginPost = session.post( url, params )
    except ConnectionError:
        errorMsg = "Проблемы с доступом к электронному университету.Уже разбираюсь."
        return errorMsg
    # Либо получили куки, либо словили ConnectionError и отослали пользователю.
    
    if( len( loginPost.cookies.get_dict().keys() ) ) == 1:
        loginPost = session.post( url, params )
        
    #Начинаем веселый парсинг полный приключений.
    examData = session.get( examUrl, cookies = loginPost.cookies, headers = headers )
    bsObj = bs( examData.text, "html" )
    tryList = []
    groupsList = bsObj.findAll("a",{"name":"sdlk"})
    groupsFound = False
    surnameFound = False
    
    for each in groupsList:
        #print(each.get_text().encode("latin-1"))
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
        errorMsg = " Не удалось найти такую группу. "
        return errorMsg
    elif not surnameFound:
        errorMsg = " Не смог найти такого студента, проверь фамилию. "
        return errorMsg
    
    return pfOutter(exams,credit,course)

if __name__ == "__main__":
	exams, credit, course = perfomanse("ИУ361 Елфимов")
	#print(json.dumps(exams).decode("unicode_escape"))
	#print( sys.getdefaultencoding() )
