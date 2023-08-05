import math
import random
import re
import time
from datetime import datetime

import selenium.common as err
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

import config
import constants
import utils
from database.check import CheckJob
from utils import prRed, prYellow


def displayWriteResults(lineToWrite: str):
    try:
        print(lineToWrite)
        utils.writeResults(lineToWrite)
    except Exception as e:
        prRed("Error in DisplayWriteResults: " + str(e))


class Linkedin:
    def __init__(self):
        load_dotenv()
        self.driver = webdriver.Firefox(options=self.browser_options())

    def browser_options(self):
        options = Options()
        firefoxProfileRootDir = config.firefox_profile
        options.add_argument("--start-maximized")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-extensions")
        options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'

        options.add_argument("--disable-blink-features")
        options.add_argument("-profile")
        options.add_argument(firefoxProfileRootDir)

        return options

    def Link_job_apply(self):
        countApplied = 0
        countJobs = 0
        cursor = CheckJob()
        getJobUrlData = cursor.find_non_applied_jobs(table_name=config.TABLE_NAME)
        lineToWrite = "Total Jobs = " + str(len(getJobUrlData))
        displayWriteResults(lineToWrite)
        for url in getJobUrlData:
            self.driver.get(url)
            time.sleep(random.uniform(1, constants.botSpeed))
            time.sleep(random.uniform(1, constants.botSpeed))

            countJobs += 1

            button = self.easyApplyButton()

            if button is not False:
                button.click()
                time.sleep(random.uniform(1, constants.botSpeed))
                try:
                    self.driver.find_element(By.CSS_SELECTOR, config.submit_btn).click()
                    time.sleep(random.uniform(1, constants.botSpeed))
                    apply_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    cursor.update_job_applied(table_name=config.TABLE_NAME, job_link=url, applied_date=apply_date)
                    countApplied += 1
                    lineToWrite = "* 🥳 Just Applied to this job: " + str(url)
                    displayWriteResults(lineToWrite)

                except err.NoSuchElementException:
                    try:
                        self.driver.find_element(By.CSS_SELECTOR, config.next_btn).click()
                        time.sleep(random.uniform(1, constants.botSpeed))
                        time.sleep(random.uniform(1, constants.botSpeed))
                        comPercentage = self.driver.find_element(By.XPATH, config.com_percent).text
                        percenNumber = int(comPercentage[0:comPercentage.index("%")])
                        result = self.applyProcess(percenNumber, url)
                        if re.search("couldn't apply", result):
                            cursor.update_job_cant_apply(table_name=config.TABLE_NAME, job_link=url)
                        else:
                            apply_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            cursor.update_job_applied(table_name=config.TABLE_NAME, job_link=url,
                                                      applied_date=apply_date)
                            countApplied += 1
                        lineToWrite = result
                        displayWriteResults(lineToWrite)

                    except err.NoSuchElementException:
                        lineToWrite = "* 🥵 Cannot apply to this Job! " + str(url)
                        cursor.update_job_cant_apply(table_name=config.TABLE_NAME, job_link=url)
                        displayWriteResults(lineToWrite)
            else:
                lineToWrite = "* 🥳 Already applied! Job: " + str(url)
                displayWriteResults(lineToWrite)

            prYellow("applied: " + str(countApplied) +
                     " jobs out of " + str(countJobs) + ".")
        self.driver.close()
        cursor.cursor.close()
        cursor.connection.close()

    def easyApplyButton(self):
        try:
            button = self.driver.find_element(By.XPATH, config.apply_btn)
            EasyApplyButton = button
        except err.NoSuchElementException:
            EasyApplyButton = False
        return EasyApplyButton

    def applyProcess(self, percentage, offerPage):
        applyPages = math.floor(100 / percentage)
        try:
            for pages in range(applyPages - 2):
                try:
                    self.driver.find_element(By.XPATH, config.choose_btn).click()
                    time.sleep(random.uniform(1, constants.botSpeed))
                except err.NoSuchElementException:
                    prRed("Can't Fill")
                self.driver.find_element(By.CSS_SELECTOR, config.next_btn).click()
                time.sleep(random.uniform(1, constants.botSpeed))
                time.sleep(random.uniform(1, constants.botSpeed))

            self.driver.find_element(By.CSS_SELECTOR, config.review_btn).click()
            time.sleep(random.uniform(1, constants.botSpeed))

            self.driver.find_element(By.CSS_SELECTOR, config.submit_btn).click()
            time.sleep(random.uniform(1, constants.botSpeed))

            result = "* 🥳 Just Applied to this job: " + str(offerPage)
        except err.NoSuchElementException:
            result = "* 🥵 " + str(applyPages) + " Pages, couldn't apply to this job! Extra info needed. Link: " + str(
                offerPage)

        return result


start = time.time()
Linkedin().Link_job_apply()
end = time.time()
prYellow("---Took: " + str(round((time.time() - start) / 60)) + " minute(s).")
