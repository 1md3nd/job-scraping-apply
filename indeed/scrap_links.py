import os
import time
import random
import urllib
import ssl
from urllib.parse import urlparse, parse_qs
from datetime import datetime

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions as err
from tqdm import tqdm
import config  # Assuming config.py contains your configuration values
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class IndeedJobScraper:
    def __init__(self):
        self.options = uc.ChromeOptions()
        # self.options.add_argument('--headless')
        # self.options.add_argument("--ignore-certificate-errors")
        self.options.add_argument('--no-sandbox')
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--window-size=512,314") 
        self.options.add_argument(f"--user-data-dir={config.chrome_profile}")
        self.options.add_argument(f'--profile-directory={config.profile}')
        self.driver = uc.Chrome(browser_executable_path=config.chrome_executable_path, use_subprocess=True,options=self.options)
        self.wait = WebDriverWait(self.driver, 15)

    def login(self):
        try:
            self.driver.get(config.signin_page)
            time.sleep(4)
            if self.driver.current_url == config.singin_flag:
                print(Fore.YELLOW + 'Already logged in.' + Style.RESET_ALL)
                return
            self.enter_text_and_click(By.NAME, config.email_input, config.EMAIL)
            self.enter_text_and_click(By.XPATH, config.contiune_btn)
            time.sleep(3)
            self.enter_text_and_click(By.NAME, config.password_input, config.PASS)
            self.enter_text_and_click(By.XPATH, config.login_btn)
            print(Fore.GREEN + 'Logged in successfully.' + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Login failed: {e}" + Style.RESET_ALL)

    def enter_text_and_click(self, by, locator, text=None):
        element = self.driver.find_element(by, locator)
        if text:
            element.send_keys(text)
        element.click()
        time.sleep(2)

    def load_search_urls(self):
        search_urls = []
        for countries,domain in config.countries_domain.items():
            for location in config.countries_states[countries]:
                for keyword in config.query_keywords:
                        for age in config.fromage:
                            search_urls.append(
                                self.load_indeed_url(
                                keyword=keyword,
                                start_url=domain,
                                age=age,
                                location=location
                                ))
        print(Fore.CYAN + f'Total {len(search_urls)} search URLs generated.' + Style.RESET_ALL)
        
        return search_urls

    def load_indeed_url(self, keyword,start_url, sort=config.sort, age=1, location=''):
        get_vars = {'q': keyword, 'sort': sort, 'fromage': age, 'l': location}
        url = start_url + urllib.parse.urlencode(get_vars)
        return url

    def extract_job_links(self):
        search_urls = self.load_search_urls()
        print(Fore.CYAN + f'Extracting job links from {len(search_urls)} search URLs.' + Style.RESET_ALL)

        job_links = set()
        progress_bar = tqdm(search_urls, total=len(search_urls))

        for cnt, url in enumerate(progress_bar, start=1):
            time.sleep(random.randint(4, 7))
            self.driver.get(url)
            # time.sleep(500)
            try:
                self.driver.find_element(By.CLASS_NAME, config.no_job_flag)
                print(Fore.YELLOW + f"No jobs found for URL {url}" + Style.RESET_ALL)
            except:
                job_links = self.extract_links_from_page(job_links)
        
        print(Fore.GREEN + f'Total {len(job_links)} unique job links found.' + Style.RESET_ALL)
        self.save_jobs(job_links)

    def extract_links_from_page(self, job_links):
        try:
            try:
                self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, config.job_list_ele)))
                jobs = self.driver.find_elements(By.CLASS_NAME, config.job_list_ele)
            except (err.NoSuchElementException, err.TimeoutException):
                self.driver.execute_script("window.stop();")
                return job_links
            
            for job in jobs:
                link = job.get_attribute('href')
                job_links.add(link)
            
            try:
                time.sleep(random.randint(4, 7))
                self.driver.find_element(By.XPATH, config.next_page).click()
            except (err.NoSuchElementException,err.ElementClickInterceptedException):
                pass
        except Exception as e:
            # return job_links/////////////////////
            pass
        return job_links

    def save_jobs(self, job_links):
        current_date = datetime.now()
        date_string = current_date.strftime("%Y-%m-%d")
        script_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_directory, f"jobs/links_{date_string}")

        with open(file_path, "w") as file:
            for link in job_links:
                file.write(link + "\n")

        print(Fore.GREEN + f'{len(job_links)} job links saved.' + Style.RESET_ALL)
        self.driver.quit()

if __name__ == "__main__":
    scraper = IndeedJobScraper()
    # scraper.login()
    scraper.extract_job_links()

