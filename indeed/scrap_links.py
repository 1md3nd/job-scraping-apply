import datetime
import itertools
import re
import random
import os

import selenium.common
from selenium.webdriver.common.by import By
from tqdm import tqdm

import config

import urllib
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import undetected_chromedriver as uc
import time
from urllib.parse import urlparse, parse_qs


def clean(data):
    data = data.strip()
    pattern = r'<[^>]*>'
    cleaned_string = re.sub(pattern, '', data)
    return cleaned_string


class ScrapLink:
    def __init__(self):
        # load_dotenv()

        self.options = uc.ChromeOptions()
        # options.add_argument('--headless')
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--ignore-certificate-errors")
        self.options.add_argument('--no-sandbox')
        self.options.add_argument("--disable-extensions")
        self.options.add_argument(f"--user-data-dir={config.chrome_profile}")

    def create_drive(self):
        self.driver = uc.Chrome(use_subprocess=True, options=self.options)
        # self.driver = webdriver.Firefox(options=self.browser_options())
        self.wait = WebDriverWait(self.driver, 15)

    def login(self):
        try:
            self.driver.get(config.signin_page)
            time.sleep(4)
            if self.driver.current_url == config.singin_flag:
                print('already login..')
                return
            # self.driver.get_screenshot_as_file("login.png")
            email = self.driver.find_element(By.NAME, config.email_input)
            email.send_keys(config.EMAIL)
            time.sleep(2)
            continue_btn = self.driver.find_element(By.XPATH, config.contiune_btn)
            continue_btn.click()
            # self.driver.get_screenshot_as_file("login_.png")
            time.sleep(3)
            pswd = self.driver.find_element(By.NAME, config.password_input)
            pswd.send_keys(config.PASS)
            time.sleep(2)
            login_btn = self.driver.find_element(By.XPATH, config.login_btn)
            login_btn.click()
            # self.driver.get_screenshot_as_file("login__.png")
            print('login success..')
        except Exception as e:
            print(e)
            print('login failed..')

    def load_indeed(self, keyword, sort=config.sort, age=config.fromage, location=''):
        getVars = {'q': keyword, 'sort': sort, 'fromage': age, 'l': location}
        url = config.start_url + urllib.parse.urlencode(getVars)
        return url

    def extract_job_links(self):
        # self.login()
        self.create_drive()
        search_url = []
        for keyword, location, age in itertools.product(config.query_keyword, config.locations, config.fromage):
            url = self.load_indeed(keyword=keyword, location=location, age=age)
            search_url.append(url)
        print(f'total {len(search_url)} search available.')
        job_links = set()
        job_ids = set()
        progress_bar = tqdm(search_url, total=len(search_url))
        self.create_drive()
        for cnt, url in enumerate(progress_bar):
            time.sleep(random.randint(4, 7))
            self.driver.get(url)
            try:
                is_available = self.driver.find_element(By.CLASS_NAME, config.no_job_flag)
                if is_available:
                    print(clean(is_available.get_attribute('innerHTML')))
                    continue
            except selenium.common.NoSuchElementException:
                while True:
                    try:
                        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, config.job_list_ele)))
                        jobs = self.driver.find_elements(By.CLASS_NAME, config.job_list_ele)
                    except selenium.common.NoSuchElementException or selenium.common.TimeoutException:
                        self.driver.execute_script("window.stop();")
                        break
                    for job in jobs:
                        link = job.get_attribute('href')
                        job_links.add(link)
                        parsed_url = urlparse(link.encode('utf-8'))
                        query_params = parse_qs(parsed_url.query)
                        job_id = query_params.get('jk', [None])[0]
                        job_ids.add(job_id)
                    try:
                        time.sleep(random.randint(4, 7))
                        next_btn = self.driver.find_element(By.XPATH, config.next_page)
                        next_btn.click()
                    except selenium.common.NoSuchElementException:
                        break

            progress_bar.set_description(f'Processing item {cnt + 1}')
        job_links = list(job_links)
        job_ids = list(job_ids)
        print(f'{len(job_links)} jobs found.')
        self.save_jobs(job_links=job_links)
        self.driver.quit()


    def save_jobs(self,job_links):
        current_date = datetime.date.today()

        # Format the current date and month strings
        date_string = current_date.strftime("%Y-%m-%d")
        script_path = os.path.abspath(__file__)

        # Get the directory containing the script
        script_directory = os.path.dirname(script_path)
        file_path = os.path.join(script_directory,f"jobs/links_{date_string}")
        with open(file_path, "w") as file:
            for link in job_links:
                file.write(link + "\n")


obj = ScrapLink()
obj.extract_job_links()
