import random
from bs4 import BeautifulSoup
from selenium import webdriver
import lxml
import time


# Первым проходом собираем все ссылки на бары
def first_scan():
    # Тут хранятся ссылки на все бары
    fin_list = []
    # Кол-во страниц всего
    count_p = 0
    # Короткие описания
    short_about = []
    # Ссылка на главную страницу
    link = f'https://www.restoclub.ru/spb/search/bary-sankt-peterburga'
    res = open_and_save(link)
    soup = BeautifulSoup(res, "lxml")
    num_pages = soup.find_all(class_="pagination__item _page")
    c = 0
    for p in num_pages:
        if c == 2:
            count_p = int(p.get('data-page'))
        c += 1

    all_bars_links = soup.find_all(class_="search-place-title__link")
    for i in all_bars_links:
        print(f'{i.text}')
        fin_list.append(i.get('href'))

    all_short_about = soup.find_all(class_="search-place-card__about")
    for j in all_short_about:
        print(f'{j.text}')
        short_about.append(j.text)

    soup.clear()
    for j in range(2, count_p + 1):
        res = open_and_save(f'https://www.restoclub.ru/spb/search/bary-sankt-peterburga/{j}')
        soup = BeautifulSoup(res, "lxml")
        all_bars_links = soup.find_all(class_="search-place-title__link")
        for i in all_bars_links:
            print(f'{i.text}')
            fin_list.append(i.get('href'))

        all_short_about = soup.find_all(class_="search-place-card__about")
        for j in all_short_about:
            print(f'{j.text}')
            short_about.append(j.text)

        soup.clear()



    with open("links.py", "w") as file:
        file.write(f"all_links = {fin_list}")

    with open("short_about.py", "w") as file:
        file.write(f"all_about = {short_about}")

    print('[INFO] Success')


def open_and_save(link, key_name):
    # driver = webdriver.Chrome()

    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir=C:\\Users\\daria\\AppData\\Local\\Google\\Chrome\\User Data")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)

    driver.get(link)
    res = None
    try:
        bar_page = driver.page_source
        res = bar_page

        # Сохранение страницы
        # with open(f"pages/{key_name}.html", "w") as file:
        #     file.write(res)

    except Exception as e:
        print(e)

    finally:
        time.sleep(random.randint(5, 8))
        driver.quit()
        return res


if __name__ == "__main__":
    first_scan()
