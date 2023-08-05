import re
from datetime import datetime
import random

import selenium.common as err
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import undetected_chromedriver as uc
import time
import config
from database.check import CheckJob
import tqdm


def clean(data):
    data = data.strip()
    pattern = r'<[^>]*>'
    cleaned_string = re.sub(pattern, '', data)
    return cleaned_string.strip()


class ApplyBot:
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
        self.wait = WebDriverWait(self.driver, 10)
        self.cursor = CheckJob()

    def fix_alert(self):
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
            return True
        except err.NoAlertPresentException:
            return False

    def review_application(self):
        # used for checking the application not edit required
        return

    def enter_experience(self):
        try:
            for input_field, input_value in config.exp_values.items():
                try:
                    input_element = self.driver.find_element(By.NAME, input_field)
                    input_element.send_keys(Keys.CONTROL, 'a')
                    input_element.send_keys(Keys.DELETE)
                    input_element.send_keys(input_value)
                except err.NoSuchElementException:
                    print(input_field, ' not found !')
                    pass
        except Exception as e:
            print(e)
        return

    def employer_ques(self):
        """
        here there are question asked by the employer and the questions can be anything
        like - total experience, experience in specific tool or domain, wanted to relocate, etc.

        to solve this there is 2 methods
        1. static method:   pre-defined questions, but it can't be fully used because some questions are different.
        2. dynamic method:
            A. Either we can use someone to manually fill the data which are asked or use a LLM to get the answer by
            training it on personal data

        STRUCTURE OF THE PAGE
            - class = 'ia-BasePage-heading' contains heading of the page
                    which is  "Questions from the employer"

            - when there is an element "<fieldset" it starts with a question
                to get the question text element "<legend" contain asked questions
                followed by "<label" which has options, its "for" attribute contains the "id" for the "<input"

            - whee there is an element "<label" it asks a question with "<input" with 'id'
        """

        return

    def resume(self):
        # if the resume it already uploaded then it will process the last used resume
        return

    def add_contact(self):
        # replace the necessary fields
        try:

            for input_field, input_value in config.exp_values.items():
                try:
                    input_element = self.driver.find_element(By.NAME, input_field)
                    # Send key combination (CTRL+A) to select all and then send DELETE to clear
                    input_element.send_keys(Keys.CONTROL, 'a')
                    input_element.send_keys(Keys.DELETE)
                    # input_element.send_keys(u'\ue009' + u'\ue003')
                    input_element.send_keys(input_value)
                except err.NoSuchElementException:
                    print(input_field, ' not found !')
                    pass
        except Exception as e:
            print(e)
        return

    def fill_page(self):
        try:
            header = self.driver.find_element(By.CLASS_NAME, config.header_cname).get_attribute('innerHTML')
            match clean(header):
                case config.review_page:
                    self.review_application()
                case config.experience_page:
                    self.enter_experience()
                case config.em_question_page:
                    self.employer_ques()
                case config.resume_page:
                    self.resume()
                case config.contact_page:
                    self.add_contact()
            return
        except err.NoSuchElementException:
            print('not found')
            return

    def apply_job(self, link):
        try:
            self.driver.get(link)
            if self.fix_alert():
                self.driver.get(link)
            time.sleep(random.randint(4, 8))
            apply_btn = self.driver.find_element(By.CLASS_NAME, config.apply_btn)
            apply_btn.click()
            time.sleep(random.randint(4, 8))
            progress_bar = self.driver.find_element(By.CSS_SELECTOR, config.prog_bar)
            prev_prog = progress_bar.get_attribute(config.prog_att)
            while prev_prog != '100':
                self.fill_page()
                cont_btn = self.driver.find_element(By.CLASS_NAME, config.cont_btn)
                cont_btn.click()
                time.sleep(random.randint(4, 8))
                # self.driver.get_screenshot_as_file(f"apply{prev_prog}.png")
                progress_bar = self.driver.find_element(By.CSS_SELECTOR, config.prog_bar)
                curr_prog = progress_bar.get_attribute(config.prog_att)
                if curr_prog == prev_prog:
                    print('some fields are required !!')
                    self.cursor.update_job_cant_apply(table_name=config.TABLE_NAME, job_link=link)
                    return
                prev_prog = curr_prog
            cont_btn = self.driver.find_element(By.CLASS_NAME, config.cont_btn)
            cont_btn.click()
            time.sleep(random.randint(4, 8))
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, config.post_apply_flag)))
            apply_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # print(self.driver.current_url)
            if self.driver.current_url == config.post_apply_url:
                print('applied')
                self.cursor.update_job_applied(table_name=config.TABLE_NAME, job_link=link, applied_date=apply_date)
                return
            else:
                self.cursor.update_job_cant_apply(table_name=config.TABLE_NAME, job_link=link)
                return
        except Exception as e:
            print(e)
            self.cursor.update_job_cant_apply(table_name=config.TABLE_NAME, job_link=link)
            return

    def find_and_apply(self):
        getJobUrlData = self.cursor.find_non_applied_jobs(table_name=config.TABLE_NAME)
        progress_links = tqdm.tqdm(getJobUrlData, total=len(getJobUrlData))
        for count, link in enumerate(progress_links):
            self.apply_job(link=link)
            progress_links.set_description(f'Progressing item {count + 1} :')


ApplyBot().find_and_apply()