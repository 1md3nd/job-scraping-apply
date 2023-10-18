import os
import time
import random
import re
import mysql
from datetime import datetime

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions as err
from tqdm import tqdm
from colorama import Fore, Style, init

import config
from database.check import CheckJob
import utils

# Initialize colorama
init(autoreset=True)


def clean(data):
    data = data.strip()
    pattern = r'<[^>]*>'
    cleaned_string = re.sub(pattern, '', data)
    return cleaned_string.strip()


class ExtractBot:
    def __init__(self):
        try:
            self.insert = CheckJob()
        except:
            print(Fore.RED+'The database is not connected and it will create further issues.\n'
                  'Make sure to turn on the server before executing this file..' + Style.RESET_ALL)
            exit()
        self.options = uc.ChromeOptions()
        # self.options.add_argument('--headless')
        self.options.add_argument("--ignore-certificate-errors")
        self.options.add_argument('--no-sandbox')
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--window-size=512,314")
        self.options.add_argument(f"--user-data-dir={config.chrome_profile}")
        self.options.add_argument(f'--profile-directory={config.profile}')
        self.driver = uc.Chrome(
            browser_executable_path=config.chrome_executable_path, use_subprocess=True, options=self.options)
        self.wait = WebDriverWait(self.driver, 15)

    def get_element_text(self, by, key):
        try:
            element = self.driver.find_element(by, key)
            return clean(element.get_attribute('innerHTML'))
        except err.NoSuchElementException:
            return "not found"

    def find_desc(self, link):
        data = {}
        self.driver.get(link)
        data['job_link'] = link
        try:
            self.wait.until(EC.presence_of_element_located(
                (By.ID, config.job_desc)))
            data['job_title'] = self.get_element_text(
                By.XPATH, config.job_title)
            data['company_name'] = self.get_element_text(
                By.XPATH, config.company_name)
            data['location'] = self.get_element_text(By.ID, config.location_)
            data['job_description'] = self.get_element_text(
                By.ID, config.job_desc)
            data['job_type'] = self.get_element_text(By.ID, config.job_type)
            complete_job = self.get_element_text(
                By.CLASS_NAME, config.job_component)
            temp = set()
            data['type_'] = ''
            for id, keyword in enumerate(config.job_type_keyowrds):
                for key in keyword:
                    if re.search(key.lower(), complete_job.lower(), re.IGNORECASE):
                        temp.add(config.job_type_labels[id])
                        break
            data['type_'] = ', '.join(temp)
            apply_btn = self.get_element_text(By.CLASS_NAME, config.apply_btn)
            data['easy_apply'] = (apply_btn == 'Apply now')
            temp = []
            data['is_relevant'] = False
            for word in config.keywords:
                if re.search(word.lower(), data['job_description'].lower(), re.IGNORECASE):
                    data['is_relevant'] = True
                    temp.append(word)
            data['keywords'] = ', '.join(temp)
        except err.TimeoutException:
            print(
                f'{Fore.RED}Timeout exception occurred while processing job link: {link}{Style.RESET_ALL}')
            return False
        except:
            print(
                f'{Fore.RED}Something went wrong while processing job link: {link}{Style.RESET_ALL}')
            return False
        return data

    def extract_desc(self):
        current_date = datetime.now()
        date_string = current_date.strftime("%Y-%m-%d")
        script_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_directory, f"jobs/links_{date_string}")

        with open(file_path, "r") as file:
            links = [line.strip() for line in file.readlines()]

        progress_link = tqdm(links, total=len(links))
        for count, link in enumerate(progress_link, start=1):
            time.sleep(random.randint(4, 8))
            data = self.find_desc(link)
            if data:
                self.insert.insert_indeed_job(data)
                print(
                    f'{Fore.GREEN}Job data inserted for link {link}{Style.RESET_ALL}')
            progress_link.set_description(
                f'{Fore.CYAN}Processing item {count}{Style.RESET_ALL}')

        self.driver.quit()


if __name__ == "__main__":
    ExtractBot().extract_desc()
