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


def clean(data):
    data = data.strip()
    pattern = r'<[^>]*>'
    cleaned_string = re.sub(pattern, '', data)
    return cleaned_string.strip()


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
    
    def contact_info(self):
        return 
    
    def resume_page(self):
        return
    
    def additional_ques(self):
        return
    
    def fill_page(self):
        try:
            header = self.driver.find_element(By.XPATH, config.header_cname).get_attribute('innerHTML').text
            match clean(header):
                case config.contact_info:
                    return self.contact_info()
                case config.resume_page:
                    return self.resume()
                case config.additional_ques:
                    return self.additional_ques()
                case config.work:
                    return self.work()
                case config.review_application:
                    return self.review_application()
                case _:
                    return False
        except err.NoSuchElementException:
            # print('not found')
            return False

    def hit_btn(self):
        try:
            bttn = self.driver.find_element(By.XPATH,config.next_btn)
        except err.NoSuchAttributeException:
            try:
                bttn = self.driver.find_element(By.XPATH,config.review_btn)
            except err.NoSuchAttributeException:
                return False
        bttn.click()
        return True               

    def apply_until_done(self,):
        progress_bar = self.driver.find_element(By.XPATH, config.com_percent)
        prev_prog = progress_bar.get_attribute('innerHTML').text
        while prev_prog != '100':
            # self.fill_page()
            if not self.hit_btn():
                return False
            time.sleep(random.randint(4, 8))
            progress_bar = self.driver.find_element(By.XPATH, config.com_percent)
            curr_prog = progress_bar.get_attribute('innerHTML').text
            while curr_prog == prev_prog:
                utils.prGreen('Manual Input Require!! \n Press Enter Onto Done..')
                input()
                self.hit_btn()
                time.sleep(random.randint(3, 5))
                progress_bar = self.driver.find_element(By.XPATH, config.com_percent)
                curr_prog = progress_bar.get_attribute('innerHTML').text

            prev_prog = curr_prog
        submit_bttn = self.driver.find_element(By.XPATH, config.submit_btn)
        submit_bttn.click()
        return True


    def manual_jobs_apply(self):
        
        cursor = CheckJob()
        job_list = cursor.find_manual_jobs(table_name=config.TABLE_NAME)
        lineToWrite = "Total Manual Jobs = " + str(len(job_list))
        print(lineToWrite)
        for url in job_list:
            self.driver.get(url)
            time.sleep(random.randint(4, 7))
            button = self.easyApplyButton()

            if not button:
                continue
            button.click()
            time.sleep(random.randint(4, 7))
            if self.apply_until_done():
                apply_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.update_job_applied(table_name=config.TABLE_NAME, job_link=url,
                                            applied_date=apply_date)

                
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

    

start = time.time()
Linkedin().manual_jobs_apply()
end = time.time()
prYellow("---Took: " + str(round((time.time() - start) / 60)) + " minute(s).")
