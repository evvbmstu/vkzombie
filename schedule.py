
# coding: utf-8

# In[116]:

import requests
from bs4 import BeautifulSoup
from datetime import time, date, datetime, timedelta
#from selenium import webdriver
# -*- coding: utf-8 -*- 




url = 'http://www.bmstu.ru/mstu/undergraduate/schedule/table-view/'


def site(url):
    response = requests.get(url).content
    return response
    

def checkCourse(mes):
    if mes.find(u'М') != -1 or mes.find(u'Б') != -1 :
        mes = mes[:-1]
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

#ищем ссылку на нужное расписание    
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
 
#ищем пару, которая идет в данный момент времени
def timeShedule(mes, period):   
    schedule_url = findSchedule(site(url), mes)
    #schedule_url = "http://www.bmstu.ru/mstu/undergraduate/schedule/table-view/?id=186&action=view"
    if schedule_url == 'nothing':
        return 'Расписания нет'
    #понделеьник первой недели первого семестра
    #print schedule_url
    d = date(2017, 9, 1) #1 september
    def_weekday = d.isoweekday() - 1  #what is it weekday?
    d = d - timedelta(days=def_weekday) #find monday of the first week
    
    #необходимые данные по входной дате
    d2 = date(2017, 10, 1)    
    week_counter = ((d2 - d).days / 7) % 2 #find is current week 'чс' == 0 or 'зн' == 1
    t = time(12, 10)
    dt = datetime.combine(d2, t)
    weekday = dt.isoweekday()
    print weekday
    
    #парсим расписание
    soup = BeautifulSoup(site(schedule_url), 'lxml')
    text = soup.get_text()
    lines = takingData(text)


#     for each in lines:
#         print each 
    lines[0] = lines[0][1:-1]
    groups = lines[0].split('","')
    #print lines[0]  
    
    # вычисляем номер столбца, который принадлежит нужной группе
    col = 0
    for each in groups:
        if each == mes + ' ':
            break
        else:
            col+=1
    #print col
    #теперь еще и стили оказывается надо найти
    styles = takingStyles(text)

#     for each in styles:
#         print each       
            
    #наконец-то начинаем поиск нужной пары
    cur_row = rowFinding(weekday, week_counter, t)
    if period == 'next' and cur_row != -1:
        cur_row += 2
    return whatLesson(lines, cur_row, col, styles)
       
   






  
def takingData(text):
    beg = text.find('data: [[')  #вычисляем начало и конец data[] с необходимыми данными, 
    beg2 = text.find(']]', beg)  #которые хранятся построчно
    data_text = text[beg+8:beg2]
    #print text
    lines = data_text.split('],[')
    return lines

def takingStyles(text):
    sty1 = text.find('mergeCells: [{')  #вычисляем начало и конец data[] с необходимыми данными, 
    sty2 = text.find('}]', sty1)  #которые хранятся построчно
    style_text = text[sty1+14:sty2]
    styles = style_text.split('},{')
    return styles

def rowFinding(weekday, week_counter, t):
    if weekday == 7:
        cur_row = -1
        return cur_row
    cur_row = (weekday - 1) * 14 + 1
    #print cur_row
    if t > time(8, 30) and t < time(10, 5):
        cur_row += week_counter
    elif t > time(10, 15) and t < time(11, 50):
        cur_row += week_counter + 2
    elif t > time(12, 0) and t < time(13, 35):
        cur_row += week_counter + 4
    elif t > time(13, 50) and t < time(15, 25):
        cur_row += week_counter + 6
    elif t > time(15, 40) and t < time(17, 15):
        cur_row += week_counter + 8
    elif t > time(17, 25) and t < time(19, 0):
        cur_row += week_counter + 10
    elif t > time(19, 10) and t < time(20, 45):
        cur_row += week_counter + 12 
    else:
        cur_row = -1; 
    return cur_row

def whatLesson (lines, cur_row, col, styles):
    lines[cur_row] = lines[cur_row][1:-1]
    lessons = lines[cur_row].split('","')
#     for each in lessons:
#          print each 
    #print col
    #print groups
    
    if (lessons[col] != ''):
        return lessons[col]
    else:
        cell = checkStyles(cur_row, col, styles)
        #print cell
        if cell[0] == -1:
            return "пар нет"
        elif cur_row == cell [0]:
            return lessons[cell[1]]
        else:
            lines[cell[0]] = lines[cell[0]][1:-1]
            lessons = lines[cell[0]].split('","')
            return lessons[cell[1]]
    return "пар нет"

def checkStyles(cur_row, cur_col, styles):
    for each in styles:
        #Ищем объединения по горионтали (colspan)
        if each.find('"row":' + str(cur_row) + ',') >= 0:
            col = each[each.find('"col":') + 6 : each.find('"col":') + 8]
            if col[1] == ',':
                col = col[0]
            if int(col) < cur_col:
                colspan = each[each.find('"colspan":') + 10 : each.find('"colspan":') + 11]
                if int(cur_col) - int(col) < int(colspan):
                    cell = [cur_row, int(col)]
                    return cell
                
        elif cur_row % 2 == 0:
            
            row = cur_row - 1
            if each.find('"row":' + str(row) + ',') >= 0:
                
                col = each[each.find('"col":') + 6 : each.find('"col":') + 8]
                if col[1] == ',':
                    col = col[0]
                if int(col) <= cur_col:
                    rowspan = each[each.find('"rowspan":') + 10 : each.find('"rowspan":') + 11]
                    if int(rowspan) == 2:                        
                        if (cur_col == int(col)):
                            cell = [row, int(col)]
                            return cell
                        else:
                            if len(each[each.find('"colspan":')]) == 11:
                                colspan = each[each.find('"colspan":') + 10 : each.find('"colspan":') + 11]
                            else:
                                colspan = each[each.find('"colspan":') + 10 : each.find('"colspan":') + 12]
                            if int(cur_col) - int(col) < int(colspan):
                                cell = [row, int(col)]
                                return cell
    
    return [-1]


def weekSchedule(mes):
   
    schedule_url = findSchedule(site(url), mes)  
    if schedule_url == 'nothing':
        return 'Расписания нет' 
    d = date(2017, 9, 1) #1 september
    def_weekday = d.isoweekday() - 1  #what is it weekday?
    d = d - timedelta(days = def_weekday) 
    d2 = date(2017, 10, 1)
    weeknumber = ((d2 - d).days / 7) + 1 #'чс' == 1 or 'зн' == 0
    print weeknumber 
    week_counter = weeknumber % 2
    print week_counter
    soup = BeautifulSoup(site(schedule_url), 'lxml')
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

            if week_counter == 1:
                if row % 2 == 1:
                    schedule_row.append(getting_line[1] + "   " + getting_line[col])
            else:
                if row % 2 == 0:
                    schedule_row.append(getting_line[1] + "   " + getting_line[col])
                
            if (row - 1) % 14 == 0:
                schedule_row.append('---------------------------------------------------')
                #schedule_row.append('---------------------------------------------------') 

            
    
    for each in schedule_row:
        print each















print timeShedule(u'ИУ9-12Б', 'now')    
print weekSchedule(u'ИУ9-11Б')   #тут пока трабл с 12 группой почему-то, остальные вроде все работают  
   
#дни недели - изображения day-1:day-6


# In[ ]:



