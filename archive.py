from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as Bs
from selenium.webdriver.common.by import By
import re
import csv

child = 1
all_matches = [('Тотал', 'ТБ', 'ТМ', 'Дата', 'Время', 'Чемпионат', 'Команда 1', 'Команда 2',
                'Счет 1', 'Счет 2', 'Тотал матча', '1Ч К1', '1Ч К2', '2Ч К1', '2Ч К2', '3Ч К1',
                '3Ч К2', '4Ч К1', '4Ч К2')]

month_day_count = {
    'дек': 31, 'ноя': 30, 'окт': 31, 'сен': 30, 'авг': 31, 'июль': 31,
    'июнь': 30, 'май': 31, 'апр': 30, 'март': 31, 'фев': 28, 'янв': 31
    }


def how_many_pages():
    global child

    soup = Bs(driver.page_source, 'lxml')
    all_pages = soup.find('div', {'class': 'pages_pag'})
    try:
        child_count = len(list(all_pages.children)) - 1
    except:
        child_count = 1

    while child <= child_count:

        soup = Bs(driver.page_source, 'lxml')
        all_match = soup.find_all('table', {'class': 'event'})

        for match in all_match:

            total_coefficient = match.find_next_sibling('table')
            match_format = []
            match_format.append(re.split(r'</td>', str(list(total_coefficient.children)[1])).pop(-36))
            match_format.append(re.split(r'</td>', str(list(total_coefficient.children)[1])).pop(-35))
            match_format.append(re.split(r'</td>', str(list(total_coefficient.children)[1])).pop(-34))
            coefficient_index = 0
            for i in match_format:
                match_format[coefficient_index] = i.replace('<td>', '')
                coefficient_index += 1
            coefficient_index = 0
            for i in match_format:
                match_format[coefficient_index] = i.replace('<td class="c1">', '')
                coefficient_index += 1
            coefficient_index = 0
            for i in match_format:
                match_format[coefficient_index] = i.replace('<td class="c2">', '')
                coefficient_index += 1

            matchs = re.sub(r'[</tablecs="vn>,odyrp\t)(]', '', str(match)).split(' ')

            match_format.append(matchs[1])
            match_format.append(matchs[2])

            match_format.append(re.findall(r"\b\d\d:\d\d[\s{1,} {1,}](.{1,}) -", str(match))[0])

            try:
                match_format.append(re.findall(r"- {1,}(.{1,});", str(match))[0])
            except:
                match_format.append(re.findall(r"- {1,}(.{1,})</td> <td>", str(match))[0])

            match_format.append(re.findall(r"Баскетбол : {1,}(.{1,}) </td> </tr>", str(match))[0])

            try:
                game_total = matchs.index('Матча:')
                game_score = matchs.index('Счет:')
                match_format.append(f"{matchs[game_score + 1].split(':')[0]}")
                match_format.append(f"{matchs[game_score + 1].split(':')[1]}")
                match_format.append(f"{matchs[game_total + 1]}")
                match_format.append(f"{matchs[game_score + 2].split(':')[0]}")
                match_format.append(f"{matchs[game_score + 2].split(':')[1]}")
                match_format.append(f"{matchs[game_score + 3].split(':')[0]}")
                match_format.append(f"{matchs[game_score + 3].split(':')[1]}")
                match_format.append(f"{matchs[game_score + 4].split(':')[0]}")
                match_format.append(f"{matchs[game_score + 4].split(':')[1]}")
                match_format.append(f"{matchs[game_score + 5].split(':')[0]}")
                match_format.append(f"{matchs[game_score + 5].split(':')[1]}")
            except:
                match_format.append('Нет результатов')

            all_matches.append(match_format)
        child += 1
        time.sleep(0.5)
        try:
            button_next_page = driver.find_element(By.ID, f'bc{child}')
            driver.execute_script('arguments[0].click();', button_next_page)
        except:
            break

    child = 1


def click_month(day):
    j = 1
    driver.find_element(By.XPATH, "//a[@class='ui-datepicker-prev ui-corner-all']"
                                  "[@data-handler='prev']"
                                  "[@data-event='click']"
                                  "[@title='Назад']").click()
    driver.find_element(By.XPATH, "//h4[@class='widget-title']").click()
    while j <= day:
        button_day = driver.find_element(By.XPATH, "//a[@class='ui-state-default'][text()="f'{j}'"]")
        driver.execute_script('arguments[0].click();', button_day)

        j += 1
        time.sleep(0.5)
        how_many_pages()


random_agent = UserAgent()
url = 'https://line4bet.ru/1x-01-01-2021-football/'
chrome_options = Options()
chrome_options.add_argument(f'user-agent={random_agent.chrome}')
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(executable_path='chromedriver')
driver.get(url)
time.sleep(0.5)

driver.find_element(By.ID, 'basket_btn').click()
time.sleep(0.5)
driver.find_element(By.XPATH, "//li[@id='tab_bc']").click()
time.sleep(0.5)

driver.find_element(By.XPATH, "//a[@class='ui-datepicker-prev ui-corner-all']"
                                  "[@data-handler='prev']"
                                  "[@data-event='click']"
                                  "[@title='Назад']").click()
driver.find_element(By.XPATH, "//h4[@class='widget-title']").click()

for month in month_day_count:
    click_month(month_day_count[month])

with open('dataNEW.csv', 'a', encoding='cp1251') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerows(all_matches)

driver.close()
