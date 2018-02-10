import requests
from bs4 import BeautifulSoup as bs

url = 'https://students.bmstu.ru/schedule/list'

def get_urls():
    response = requests.get(url).content
    html_page = bs(response, 'html.parser')
    url_dict = {}
    for tag in html_page.find_all('a', {'class': 'btn btn-sm btn-default text-nowrap'}):
        url_dict[tag.get_text().replace(' ', '').replace('\n', '').replace('(М)', '').replace('(Б)', '')] = url[:-14] + tag.get('href')
    return url_dict

parser():
    urls = get_urls()
    schedule = {}
    for each in urls:
        print(each)
        response = requests.get(urls[each]).content
        html_page = bs(response, 'html.parser')
        schedule_string = ''
        for table in html_page.find_all('div', {'class': 'col-md-6 hidden-xs'}):
            i = 0
            for row in table.find_all('tr'):
                if i < 2:
                    i += 1
                    continue
                if row.find('td',{"colspan":"2"}) != None:
                    schedule_string += "$" + row.find('td',{"colspan":"2"}).get_text().replace("\xa0", " ")
                    schedule_string += "$" + row.find('td',{"colspan":"2"}).get_text().replace("\xa0", " ")
                else:
                    if row.find('td',{"class":"text-success"}) != None:
                        schedule_string += "$" + row.find('td',{"class":"text-success"}).get_text().replace("\xa0", " ")
                    else:
                        schedule_string += "$ - "
                    if row.find('td',{"class":"text-info"}) != None:
                        schedule_string += "$" + row.find('td',{"class":"text-info"}).get_text().replace("\xa0", " ")
                    else:
                        schedule_string += "$ - "
        schedule[each] = [urls[each], schedule_string]
    return schedule