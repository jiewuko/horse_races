from selenium import webdriver
import csv
import os
from lxml import etree
from config import *

FILE_NAME = os.getcwd() + '/punters{}_{}.csv'.format(TIME_PERIOD_FROM, TIME_PERIOD_TO)

START_URL = 'https://www.sportsbet.com.au/racing-schedule/Horse/today'


class ParseSportsBet(object):
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=os.getcwd() + '/chromedriver')
        self.start_request()
        self.driver.close()

    def start_request(self):
        self.driver.get(START_URL)
        page_data = etree.HTML(self.driver.page_source)
        for items in page_data.xpath("//div[contains(@data-automation-id, 'horse-racing-section-content')]//"
                                     "tr[contains(@class, 'firstRow_f185foic lastRowDesktop_f1xvifhw')]"):
            if 'Australia' in (items.xpath("td[1]//div[2]//span//text()")):
                for url in items.xpath("td[contains(@class, 'notResultedEventCell_f1kqmput')]//a//@href"):
                    self.driver.get('https://www.sportsbet.com.au' + url)
                    page_with_race = etree.HTML(self.driver.page_source)

                    name_race = ''.join(page_with_race.xpath(
                        "//h2[contains(@data-automation-id, 'racecard-header-title')]//text()")).replace(
                        ' ', '_').replace('/', '_')
                    with open(name_race + '.csv', 'a') as race:
                        writer = csv.writer(race)
                        writer.writerow(['Horses', '1st', '2nd', '3rd', 'starts', 'win', 'place', 'roi'])
                    for horses in page_with_race.xpath(
                            "//div[contains(@data-automation-id, 'racecard-outcome-name')]/span[1]//text()"):
                        with open(FILE_NAME, 'r') as allData, open(name_race + '.csv', 'a') as race:
                            reader = csv.reader(allData)
                            next(reader, None)
                            writer = csv.writer(race)
                            horse = ''.join(filter(str.isalpha, horses))
                            horses_for_write_file = []
                            for row in reader:
                                if horse.lower() in row[0].lower():
                                    horses_for_write_file.append(row)
                            if horses_for_write_file:
                                for horse_ in horses_for_write_file:
                                    writer.writerow(horse_)
                                    print(horse_)
                            else:
                                writer.writerow([horse.lower() + 'does not exist in the main file'])


if __name__ == '__main__':
    ParseSportsBet()
