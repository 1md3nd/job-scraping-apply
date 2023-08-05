import time, random
import utils, constants

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from utils import prRed, prYellow

from dotenv import load_dotenv

from linkedin.py import extractData
from database.insert import InsertJob
from tqdm import tqdm
import config


def remove_duplicates(offerIds):
    # Create an empty result list
    result = []

    # Iterate through the input list
    for row in offerIds:
        # If the row is not in the result list, append it
        if row not in result:
            result.append(row)

    # Return the resulting list
    return result


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
        # driver = webdriver.Firefox(executable_path=r'C:\WebDrivers\geckodriver.exe', options=options)

        options.add_argument("--disable-blink-features")
        # options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("-profile")
        options.add_argument(firefoxProfileRootDir)

        return options

    def Link_job_apply(self):
        offerIds = []
        urlData = utils.getUrlDataFile()
        for url in urlData:
            self.driver.get(url)
            try:
                totalJobs = self.driver.find_element(By.XPATH, config.total_jobs).text
            except Exception as e:
                prRed("No Jobs Found " + str(e))
                continue
            totalPages = utils.jobsToPages(totalJobs)

            for page in range(totalPages):
                currentPageJobs = constants.jobsPerPage * page
                url = url + "&start=" + str(currentPageJobs)
                self.driver.get(url)
                time.sleep(random.uniform(1, constants.botSpeed))

                offersPerPage = self.driver.find_elements(By.XPATH, config.per_job)
                for offer in offersPerPage:
                    try:
                        offerId = offer.get_attribute(config.offer_id)
                    except Exception as e:
                        prRed("No Offers Found " + str(e))
                        continue

                    offerIds.append(int(offerId.split(":")[-1]))
                    prYellow("Offer Found - " + offerId)
        uniqueJobIds = remove_duplicates(offerIds)
        # writing links to txt
        self.driver.close()
        extract = extractData()
        insert = InsertJob()
        progress_bar = tqdm(uniqueJobIds, total=len(uniqueJobIds))
        for jobID in progress_bar:
            offerPage = config.linkedin_start_url + str(jobID)
            utils.writeResultsJobList(offerPage)
            # print(offerPage)
            time.sleep(random.uniform(1, constants.botSpeed))
            job_data = extract.get(offerPage)
            if job_data != 'NOT FOUND':
                insert.insert(job_data)
            progress_bar.set_description(f"Processing item {jobID}")

        extract.close()
        insert.close()

    def displayWriteResults(self, lineToWrite: str):
        try:
            print(lineToWrite)
            utils.writeResults(lineToWrite)
        except Exception as e:
            prRed("Error in DisplayWriteResults: " + str(e))


start = time.time()
Linkedin().Link_job_apply()
end = time.time()
prYellow("---Took: " + str(round((time.time() - start) / 60)) + " minute(s).")
