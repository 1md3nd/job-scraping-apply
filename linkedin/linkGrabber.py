import time
import random
from colorama import Fore, Style, init
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from tqdm import tqdm

import config
import constants
from py import extractData
from database.insert import InsertJob
from utils import prRed, prYellow, getUrlDataFile, jobsToPages

# Initialize colorama for colored output
init(autoreset=True)


class Linkedin:
    def __init__(self):
        load_dotenv()
        self.driver = webdriver.Firefox(options=self.browser_options())
        self.wait = WebDriverWait(self.driver, 10)
        window_width = 400
        window_height = 800

        self.driver.set_window_size(window_width, window_height)

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

    def link_job_apply(self):
        offerIds = []
        urlData = getUrlDataFile()

        progress_bar = tqdm(urlData, desc="Scanning Jobs", ncols=100)

        for (exp, url) in progress_bar:
            self.driver.get(url)
            try:
                self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, config.total_jobs)))
                totalJobs = self.driver.find_element(
                    By.XPATH, config.total_jobs).text
            except Exception as e:
                prRed(f"No Jobs Found! ")
                continue

            totalPages = jobsToPages(totalJobs)

            for page in range(totalPages):
                currentPageJobs = constants.jobsPerPage * page
                url = url + "&start=" + str(currentPageJobs)
                self.driver.get(url)
                time.sleep(random.uniform(1, constants.botSpeed))
                self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, config.per_job)))

                offersPerPage = self.driver.find_elements(
                    By.XPATH, config.per_job)
                for offer in offersPerPage:
                    try:
                        offerId = offer.get_attribute(config.offer_id)
                    except Exception as e:
                        prRed(f"No Offers Found: ")
                        continue

                    offerIds.append((exp, int(offerId.split(":")[-1])))
                    prYellow(f"Offer Found - {offerId}")

        self.driver.quit()
        extract = extractData()
        insert = InsertJob()

        progress_bar = tqdm(offerIds, total=len(offerIds),
                            desc="Processing Jobs", ncols=100)

        for (exp, jobID) in progress_bar:
            offerPage = config.linkedin_start_url + str(jobID)
            time.sleep(random.uniform(1, constants.botSpeed))
            job_data = extract.get(offerPage)
            job_data['experience'] = exp

            if job_data != 'NOT FOUND':
                insert.insert(job_data)
            progress_bar.set_description(f"Processing item {jobID}")

        extract.close()
        insert.close()


if __name__ == "__main__":
    print(f"{Fore.GREEN}LinkedIn Job Scraper{Style.RESET_ALL}")
    start = time.time()
    try:
        Linkedin().link_job_apply()
        end = time.time()
        print(
            f"{Fore.GREEN}---Took: {str(round((end - start) / 60))} minute(s).{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
