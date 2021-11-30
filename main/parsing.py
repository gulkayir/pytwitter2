# import requests
# from bs4 import BeautifulSoup as BS

# import csv


# def get_html(url):
#     headers = {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
#     response = requests.get(url, headers=headers)
#     return response.text


# def get_data(html):
#     soup = BS(html, 'lxml')
#     catalog = soup.find('div', class_='_2lzCpzHH0OvyFsvuESLurr')
#     news = catalog.find_all('h3', class_="EmAI60CZ6hqtjh7kIC2SS")
#     h = []
#     for new in news:
#         try:
#             title = new.find('h3', class_="_eYtD2XCVieq6emjKBH3m").text.strip()
#         except:
#             title = 'Health'

#         # try:
#         #     description = health.find('div', class_="amw-card-list__description amw-editor-text").text.strip()
#         # except:
#         #     description = 'https://thumbor.forbes.com/thumbor/fit-in/1200x0/filters%3Aformat%28jpg%29/https%3A%2F%2Fspecials-images.forbesimg.com%2Fimageserve%2F5d35eacaf1176b0008974b54%2F0x0.jpg%3FcropX1%3D790%26cropX2%3D5350%26cropY1%3D784%26cropY2%3D3349'

#         data = {
#             'title': title,
#             # 'description': description,

#         }

#         h.append(data)
#     return h


# def main():
#     url = 'https://www.reddit.com/r/news/search/?q=twitter&restrict_sr=1&sr_nsfw='
#     print(url)
#     html = get_html(url)
#     print(html)
#     r = get_data(html)
#     return r
# print(main())


import json
import requests


def main():
    url = 'https://www.reddit.com/r/news/search/.json?q=twitter/'
    responce = requests.get(url,headers={'User-agent':"your bot 0.1"})
    json_object = responce.text
    python_object = json.loads(json_object)
    news = python_object['data']['children']
    data = []
    number = 1
    for new in news:
        news_dictionary = {
                'title': new['data']['title'],
                'author':new['data']['author']

        }
        number +=1
        data.append(news_dictionary)
    return data    

# print(main())