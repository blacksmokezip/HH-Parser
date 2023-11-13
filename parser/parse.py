from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup as bs
import time
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from pathlib import Path
from progress.bar import IncrementalBar


def parse_vacancies(query, file):

    bar = IncrementalBar('Parsing', max=5)

    url = "https://hh.ru/"

    useragent = UserAgent()

    service = Service(
        executable_path="/home/blacksmoke/projects/HH-Parser/driver/driver"
    )
    options = Options()
    options.add_argument("headless")
    options.add_argument(f"user-agent={useragent.chrome}")
    driver = wd.Chrome(service=service, options=options)

    bar.next()

    try:
        driver.get(url=url)

        search = driver.find_element(By.XPATH, '//*[@id="a11y-search-input"]')
        search.send_keys(query)

        bar.next()

        button = driver.find_element(
            By.XPATH,
            '//*[@id="supernova_search_form"]/div/div[2]/button'
        )
        button.click()

        bar.next()

        time.sleep(2)

        soup = bs(driver.page_source, 'lxml')
        vacancies = soup.find_all('a', class_="serp-item__title")

        bar.next()

        fle = Path(file)
        fle.touch(exist_ok=True)

        with open(fle, 'w') as f:
            for a in vacancies:
                f.write(f"{a.text} - {a['href']}\n")

        bar.next()
        bar.finish()
        print('Vacancies were successfully parsed!')

    except Exception as e:
        print(e)

    finally:
        driver.close()
        driver.quit()
