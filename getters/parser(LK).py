import requests
from bs4 import BeautifulSoup as bs

url = 'https://students.bmstu.ru/schedule/list'


""" Получение ссылок на расписания групп МГТУ
    Args:
        ---
    Returns:
        dict: Словарь с названием группы и ссылкой на расписание.
"""
def get_urls():
    response = requests.get(url).content
    html_page = bs(response, 'html.parser')
    url_dict = {}

    for tag in html_page.find_all('a', {'class': 'btn btn-sm btn-default text-nowrap'}):
        url_dict[tag.get_text().replace(' ', '').replace('\n', '').replace('(М)', '').replace('(Б)', '')] = url[:-14] + tag.get('href')
    return url_dict


""" Получение расписания групп МГТУ
    Args:
        ---
    Returns:
        dict: Словарь с названием группы и ссылкой на расписание
        и расписанием, сохраненном в виде строки с разделителем '$'.
"""
def parser():
    urls = get_urls()
    schedule = {}

    for each in urls:
        print(each)
        response = requests.get(urls[each]).content
        html_page = bs(response, 'html.parser')
        schedule_string = ''

        #Находим div с нужной таблицей
        #В нынешнем расписании хранится почему-то две версии расписаний на каждый день \_0_/
        for table in html_page.find_all('div', {'class': 'col-md-6 hidden-xs'}):
            i = 0
            for row in table.find_all('tr'):

                #Пропускаем первые две строки таблицы, так как они не хранит нужной дл янас информации
                if i < 2:
                    i += 1
                    continue

                if i == 3:
                    schedule_string += '$8:30-10:05 '
                elif i == 4:
                    schedule_string += '$10:15-11:50 '
                elif i == 5:
                    schedule_string += '$12:00-13:35 '
                elif i == 6:
                    schedule_string += '$13:50-15:25 '
                elif i == 7:
                    schedule_string += '$15:40-17:15 '
                elif i == 8:
                    schedule_string += '$17:25-19:00 '
                elif i == 9:
                    schedule_string += '$19:10-20:45 '
                            
                #Сначала ищем пары, которые есть и в ЧС и в ЗН
                if row.find('td',{"colspan":"2"}) != None:
                    schedule_string += row.find('td',{"colspan":"2"}).get_text().replace("\xa0", " ")
                    schedule_string += row.find('td',{"colspan":"2"}).get_text().replace("\xa0", " ")

                #Далее ищем пары, которые есть только или в ЧС или в ЗН, иначе записываем в строк прочерк
                else:
                    if row.find('td',{"class":"text-success"}) != None:
                        schedule_string += row.find('td',{"class":"text-success"}).get_text().replace("\xa0", " ")
                    else:
                        schedule_string += " - "
                    if row.find('td',{"class":"text-info"}) != None:
                        schedule_string += row.find('td',{"class":"text-info"}).get_text().replace("\xa0", " ")
                    else:
                        schedule_string += " - "

        schedule[each] = [urls[each], schedule_string]
    return schedule