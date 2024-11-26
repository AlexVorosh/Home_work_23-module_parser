import requests
from bs4 import BeautifulSoup

import pandas as pd

def collect_user_rates(user_login):
   page_num = 1

   data = []

   while True:
       url = f'https://www.kinopoisk.ru/user/{user_login}/votes/'

       r = requests.get(url)

       soup = BeautifulSoup(r.text, 'lxml')

       entries = soup.find_all('div', class_='item')

       if len(entries) == 0:
           break

       for entry in entries:
           nameRus = entry.find('div', class_='nameRus')
           film_name = nameRus.find('a').text

           time = entry.find('div', class_='rating')
           if time is not None:
               film_duration = time.text.split()[-2]
           else:
               film_duration = 'Нет данных о продолжительности фильма'

           kinopoisk_rating = entry.find('div', class_='rating')
           if kinopoisk_rating is not None:
               rating = kinopoisk_rating.text.split()[0]
           else:
               rating = 'Нет данных о рейтинге КиноПоиск'

           your_vote = entry.find('div', class_='vote').text

           data.append({'film_name': film_name, 'film_duration_min': film_duration, 'kinopoisk_rating': rating,
                        'your_vote': your_vote})

           page_num += 1

       return data

user_rates = collect_user_rates(user_login='29141473')

df = pd.DataFrame(user_rates)

df.to_excel('user_rates_kinopoisk.xlsx')
