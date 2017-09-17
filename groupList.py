
# coding: utf-8

# In[87]:


import requests
from bs4 import BeautifulSoup as bs
from datetime import time
from schedule import takingData

url = 'http://www.bmstu.ru/mstu/undergraduate/schedule/table-view/'

def site(url):
    response = requests.get(url).content
    return response

def dataList():
    response = site(url)
    soup = bs(response, 'html.parser')
    result_list = dict()
    i = 1
    links = []
    while i < 2:
        try:
            table = soup.find('div', {'id': 'vt-list-' + str(i)})
            i += 1
            table1 = table.find('div', {'class': 'col-md-12'})
        except AttributeError:
            return 'nothing'
    
        for row in table1.find_all('tr'): 
            for col in row.find_all('td', {'class':'groupname'}):
                schedule_link = url + row.find('a',{'class':'j-bold'}).get('href')
                links.append(schedule_link)
#     for each in links:
#                     print each             
                groupsFind(schedule_link, result_list)
    for each in result_list:
        print each + "  " + result_list[each]
            

def groupsFind(schedule_link, result_list):
    soup = bs(site(schedule_link), 'lxml')
    text = soup.get_text()
    lines = takingData(text)
    lines[0] = lines[0][1:-1]
    groups = lines[0].split('","')
    counter = 3
    while (counter < len(groups)):
        result_list[groups[counter]] =  schedule_link   
        counter += 1
            
            
            
            
#             for col in row.find_all('td', {'class':'groupname'}):
#                 mega_line = col.get_text() #все группы из найденного тега
# #                 print mega_line
# #                 print " "
#                 schedule_link = url + row.find('a',{'class':'j-bold'}).get('href')
#                 line = mega_line.split('; ') #разбили на отдельные кафедры
#                 scheduleFind(line, schedule_link, result_list)  
#     for each in result_list:
#         print each + "  " + result_list[each]
         
        
        
# def scheduleFind(line, schedule_link, result_list):
#     for each in line:
# #         print each
# #         print " "
#         small_line = each.split('-') #список, в котором по очереди хранятся номера кафедр и группы
  
#         if len(small_line) == 2:
#             if small_line[0].find(",") == -1:
#                 if small_line[1].find(",") == -1:
#                     result_list[small_line[0] + "-" + small_line[1]] =  schedule_link
#                 else:
#                     groups = small_line[1].split(",")
#                     for each in groups:
#                         result_list[small_line[0] + "-" + each] =  schedule_link
#             else:
#                 faculties = small_line[0].split(",")
#                 for each in faculties:
#                     if small_line[1].find(",") == -1:
#                         result_list[each + "-" + small_line[1]] =  schedule_link
#                     else:
#                         groups = small_line[1].split(",")
#                         for k in groups:
#                             result_list[each + "-" + k] =  schedule_link
#         else:  
#             if small_line[0].find(",") == -1:
#                 faculty = small_line[0]
#                 difFindSit(small_line, schedule_link, result_list, faculty)                
#             else:
#                 faculties = small_line[0].split(",")
#                 for each in faculties:
#                     difFindSit(small_line, schedule_link, result_list, each)
                    
                
                
                    
# def difFindSit(small_line, schedule_link, result_list, faculty): 
#     counter1 = 1
#     while (counter1 < len(small_line)):
#         gr_list = small_line[counter1].split(",")
#         counter2 = 0;
#         while (counter2 < len(gr_list) - 1):
#             result_list[faculty + "-" + gr_list[counter2]] =  schedule_link
#             counter2 += 1

#         if counter1 == len(small_line) - 1:
#             result_list[faculty + "-" + gr_list[-1]] =  schedule_link
#         else:
#             faculty = gr_list[-1]                            
#         counter1 += 1
 
         

dataList()

