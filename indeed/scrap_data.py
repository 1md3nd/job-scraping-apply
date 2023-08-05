import datetime
import re
import random

import mysql.connector.errors
import selenium.common as err
from selenium.webdriver.common.by import By
from tqdm import tqdm

import config

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import undetected_chromedriver as uc
import time

from database.check import CheckJob
from linkedin import utils


def clean(data):
    data = data.strip()
    pattern = r'<[^>]*>'
    cleaned_string = re.sub(pattern, '', data)
    return cleaned_string.strip()


class ExtractBot:
    def __init__(self):
        # load_dotenv()

        options = uc.ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument("--start-maximized")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-extensions")
        options.add_argument(f"--user-data-dir={config.chrome_profile}")
        self.driver = uc.Chrome(use_subprocess=True, options=options)
        # self.driver = webdriver.Firefox(options=self.browser_options())
        self.wait = WebDriverWait(self.driver, 15)
        try:
            self.insert = CheckJob()
        except mysql.connector.errors.DatabaseError:
            utils.prRed('The database is not connected and it will create further issue \n'
                        'Make sure to turn on the server before executing this file..')
            exit()

    def getinnerHTML(self, xpath):
        try:
            res = self.driver.find_element(By.XPATH, xpath).get_attribute('innerHTML')
            res = clean(res)
        except:
            # print(e)
            res = "not found"
        # print(res)
        return res

    def find_desc(self, link):
        data = {}
        self.driver.get(link)
        data['job_link'] = link
        try:
            self.wait.until(EC.presence_of_element_located((By.ID, config.job_desc)))
            data['job_title'] = self.getinnerHTML(config.job_title)
            data['company_name'] = self.getinnerHTML(config.company_name)
            data['location'] = self.getinnerHTML(config.location_)
            desc = self.driver.find_element(By.ID, config.job_desc).get_attribute('innerHTML')
            data['job_description'] = clean(desc)
            raw_job_desc = data['job_description']

            data['job_type'] = self.getinnerHTML(config.job_type)
            try:
                apply_btn = clean(self.driver.find_element(By.CLASS_NAME, config.apply_btn).get_attribute('innerHTML'))
            except err.NoSuchElementException:
                try:
                    apply_btn = clean(self.driver.find_element(By.ID, config.apply_btn_).get_attribute('innerHTML'))
                except err.NoSuchElementException:
                    apply_btn = ''
            if apply_btn == 'Apply now':
                data['easy_apply'] = True
            else:
                data['easy_apply'] = False
            temp = []
            data['is_relevant'] = False
            for word in config.keywords:
                find_ele = re.findall(word.lower(), raw_job_desc.lower(), re.IGNORECASE)
                if len(find_ele) > 0:
                    data['is_relevant'] = True
                    temp.append(word)
            data['keywords'] = ' '.join(temp)
        except:
            return 'something went wrong'
        return data

    def extract_desc(self):
        current_date = datetime.date.today()

        # Format the current date and month strings
        date_string = current_date.strftime("%Y-%m-%d")
        with open(f"jobs/links_{date_string}", "r") as file:
            # Read the lines of the file
            lines = file.readlines()

        # Extract the links from the lines
        links = [line.strip() for line in lines]
        progress_link = tqdm(links, total=len(links))
        for count, link in enumerate(progress_link):
            time.sleep(random.randint(4, 8))
            data = self.find_desc(link)
            if data == 'something went wrong':
                self.driver.get_screenshot_as_file(f'problem{count + 1}.png')
                continue
            else:
                self.insert.insert_indeed_job(data)
            progress_link.set_description(f'Processing item {count + 1}')
        self.driver.close()


ExtractBot().extract_desc()
