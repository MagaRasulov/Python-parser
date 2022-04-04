import requests as req
from bs4 import BeautifulSoup as Bs

url = 'https://www.kinopoisk.ru/lists/navigator/2021/?quick_filters=high_rated%2Cfilms&limit=20&tab=best'
response = req.get(url)
soup = Bs(response.text, 'lxml')
films = soup.find_all('p', class_='selection-film-item-meta__name')
i = 1
print('Лучшие фильмы 2021 года по версии Кинопоиск')
for film in films:
    print(i, film.text)
    i += 1

# url = 'https://www.cybersport.ru/base/tournaments/dota-pro-circuit-2021-2022-vostochnaia-evropa'
# response = req.get(url)
# soup = Bs(response.text, 'lxml')
# games = soup.find_all('article', class_="matche")
# for game in games:
#     print(game.text)
