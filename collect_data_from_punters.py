from selenium import webdriver
from time import sleep
import csv
import os
from lxml import etree
from config import *

FILE_NAME = os.getcwd() + '/punters{}_{}.csv'.format(TIME_PERIOD_FROM, TIME_PERIOD_TO)


class ParsePunters(object):
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=os.getcwd() + '/chromedriver')
        self.create_file()
        self.open_source_page()
        self.driver.close()

    @staticmethod
    def create_file():
        if not os.path.isfile(os.getcwd() + FILE_NAME):
            with open(FILE_NAME, 'w') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(['Horses', '1st', '2nd', '3rd', 'starts', 'win', 'place', 'roi'])

    def open_source_page(self):
        self.driver.get('https://www.punters.com.au/stats/horses/#dateRange={}-08-01:{}-07-31'.format(
            TIME_PERIOD_FROM, TIME_PERIOD_TO))
        self.collect_data_from_page(self.driver.page_source)

    def collect_data_from_page(self, page_source):
        page_data = etree.HTML(page_source)
        with open(FILE_NAME, 'a') as csvFile:
            writer = csv.writer(csvFile)
            data_for_write = []
            for data in page_data.xpath("//table[contains(@class, 'stat-table')]/tbody//tr"):
                name = ''.join(data.xpath('td[2]/a/@data-name'))
                first = ''.join(data.xpath("td[3]/text()"))
                second = ''.join(data.xpath("td[4]/text()"))
                third = ''.join(data.xpath("td[5]/text()"))
                starts = ''.join(data.xpath("td[6]/text()"))
                win = ''.join(data.xpath("td[7]/text()")).replace('%', '')
                place = ''.join(data.xpath("td[8]/text()")).replace('%', '')
                roi = ''.join(data.xpath("td[9]/text()")).replace('%', '')
                collected_data = [name, first, second, third, starts, win, place, roi]
                data_for_write.append(collected_data)
                print(collected_data)
            writer.writerows(data_for_write)

        try:
            next_page = self.driver.find_element_by_xpath("//div[contains(@id, 'pagerWrapper')]//ul//li[last()]")
            if 'next' in next_page.text.lower():
                self.driver.execute_script("arguments[0].scrollIntoView();", next_page)
                sleep(2)
                next_page.click()
                sleep(6)
                next_page_source = self.driver.page_source
                self.collect_data_from_page(next_page_source)
        except Exception as e:
            print('Finish with exception: Bad internet connection')


if __name__ == '__main__':
    ParsePunters()
