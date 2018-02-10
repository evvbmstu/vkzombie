
# coding: utf-8

# In[87]:


import requests
from bs4 import BeautifulSoup as bs
from schedule import takingData, takingStyles, checkStyles

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
    while i < 8:
        try:
            table = soup.find('div', {'id': 'vt-list-' + str(i)})
            i += 1
            table1 = table.find('div', {'class': 'col-md-12'})
        except AttributeError:
            return 'nothing'
    
        for row in table1.find_all('tr'): 
            for col in row.find_all('td', {'class':'groupname'}):
                schedule_link = row.find('a',{'class':'j-bold'}).get('href')
                links.append(schedule_link)         
                groupsFind(schedule_link, result_list)
    return result_list

            

def groupsFind(schedule_link, result_list):
    soup = bs(site(url+schedule_link), 'lxml')
    text = soup.get_text()
    lines = takingData(text)
    
    lines[0] = lines[0][1:-1]
    groups = lines[0].split('","')
    counter = 3
    while (counter < len(groups)):
        if groups[counter] != " " and groups[counter] != "":
            result_list[groups[counter]] =  schedule_link                   
            col = 0
            row = 0
            tmp_row=''
            for each in groups:
                if each == groups[counter]:
                    break
                else:
                    col+=1
            styles = takingStyles(text)
            schedule_row = []
            schedule_string = ''
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

                    schedule_string += "$"
                    schedule_string += getting_line[1] + "   " + getting_line[col]
                    #schedule_row.append(getting_line[1] + "   " + getting_line[col])                
            result_list[groups[counter]] =  [schedule_link, schedule_string]

#         print groups[counter]
#         for each in result_list[groups[counter]]:
#             print each
        counter += 1

dataList()


