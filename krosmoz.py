import csv
import json
import re
import logging
import sys
from datetime import timedelta, date
from typing import Dict, List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

DRIVER_PATH = './chromedriver'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    stream=sys.stdout
)

logger = logging.getLogger(__name__)


def daterange(start_date, end_date):
    """
    Date iterator
    """
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


class KrosmozBot:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=chrome_options)
        self.bonus = r'Bonus : (.*)'
        self.offering = r'Récupérer ([0-9]+) (.+) et rapporter .*'
        self.description = r'\n(.*)\nQuête.*'
        self.url = 'http://www.krosmoz.com/fr/almanax/%s?game=dofustouch'

    def get_offering(self, date: date):
        self.driver.get(self.url % date)
        content = self.driver.find_element_by_xpath('//*[@id="achievement_dofus"]/div[2]').text
        img = None
        try:
            img: str = self.driver.find_element_by_xpath(
                '//*[@id="achievement_dofus"]/div[2]/div/div/div[1]/img').get_attribute('src')
        except Exception:
            logger.info(Exception)
        offering = {}

        offering['date'] = date.strftime('%d/%m/%Y')
        m = re.search(self.bonus, content)
        offering['bonus'] = m.group(1) if m is not None else None
        m = re.search(self.offering, content)
        offering['quantity'] = m.group(1) if m is not None else None
        m = re.search(self.offering, content)
        offering['offering'] = m.group(2) if m is not None else None
        m = re.search(self.description, content)
        offering['description'] = m.group(1) if m is not None else None
        offering['img'] = img

        logger.debug(offering)

        return offering

    def __del__(self):
        self.driver.close()


if __name__ == '__main__':
    import time

    start_time = time.time()

    start_date = date(2020, 2, 23)
    end_date = date(2021, 1, 1)

    bot = KrosmozBot()

    offerings: List[Dict] = []

    for date in daterange(start_date, end_date):
        offerings.append(bot.get_offering(date))

    with open('krosmoz.json', 'w', encoding='utf-8', newline='') as f:
        json.dump(offerings, f)

    with open('krosmoz2020.csv', 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, offerings[0].keys())
        w.writeheader()
        for offering in offerings:
            w.writerow(offering)

    del bot
    print("--- Fetched data in %s seconds ---" % (time.time() - start_time))
