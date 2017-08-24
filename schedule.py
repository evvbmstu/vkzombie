
# coding: utf-8

# In[194]:

import requests
from bs4 import BeautifulSoup
#from selenium import webdriver
# -*- coding: utf-8 -*- 

url = 'http://www.bmstu.ru/mstu/undergraduate/schedule/table-view/'


def site(url):
    response = requests.get(url).content
    return response
    

def checkCourse(mes):
    mas = mes.split('-')
    if int(mas[1]) < 30:
        course = 1
    elif int(mas[1]) < 50:
        course = 2
    elif int(mas[1]) < 70:
        course = 3
    elif int(mas[1]) < 90:
        course = 4
    elif int(mas[1]) < 110:
        course = 5
    elif int(mas[1]) < 120:
        course = 6
    elif int(mas[1]) < 130:
        course = 7
    else :
        course = 0
    return str(course)



'''def findSchedule1(response):
    soup = BeautifulSoup(response, 'lxml')
    table = soup.find('div', {'id': 'vt-list-5'})
    table1 = table.find('div', {'class': 'col-md-12'})
    for row in table1.find_all('tr'):
        group_list = row.find(text='МТ1-101; МТ2-101; МТ3-101; МТ6-101; Э5-101')
        if group_list != None:
            schedule_link = row.find('a',{'class':'j-bold'}).get('href')
            break
    return schedule_link '''
    
    
def findSchedule(response, mes):
    schedule_link = 'nothing'
    soup = BeautifulSoup(response, 'lxml')
    course = checkCourse(mes)
    parts = mes.split("-") #разделяем входное сообщение на номер кафедры и группу
    table = soup.find('div', {'id': 'vt-list-' + course})
    table1 = table.find('div', {'class': 'col-md-12'})
    for row in table1.find_all('tr'):
        for col in row.find_all('td', {'class':'groupname'}):
            mega_line = col.get_text() #все группы из найденного тега
            line = mega_line.split('; ') #разбили на отдельные кафедры
            for each in line:
                small_line = each.split('-') #список, в котором по очереди хранятся номера кафедр и группы
                x = 0
                while len(small_line) > x:
                    if small_line[x] == parts[0]:
                        groups = small_line[x+1].split(',')
                        for y in groups:
                            if y == parts[1]:
                                schedule_link = row.find('a',{'class':'j-bold'}).get('href')
                                break
                        x+=2
                    else:
                        x+=2
                        
    if schedule_link == 'nothing':
        return schedule_link
    else:
        return url + schedule_link       
 

print findSchedule(site(url), u'СМ122-81')
    
    
    
#дни недели - изображения day-1:day-6


# In[ ]:



