# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup as bs
from settings import login,password
from views import resultsView
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
    bsObj = bs( examData.text, "html" )
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
    #results = []
    #results.append( exams )
    #results.append( credit )
    #results.append( course )
    
    return resultsView( exams, credit, course )
