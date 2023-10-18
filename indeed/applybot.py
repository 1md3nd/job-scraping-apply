import re
from datetime import datetime
import random
import mysql
from colorama import Fore, Style, init
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

# Initialize colorama
init(autoreset=True)


def clean(data):
    data = data.strip()
    pattern = r'<[^>]*>'
    cleaned_string = re.sub(pattern, '', data)
    return cleaned_string.strip()


COLORS = {
    "INFO": "\033[94m",    # Blue
    "SUCCESS": "\033[92m",  # Green
    "WARNING": "\033[93m",  # Yellow
    "ERROR": "\033[91m",   # Red
    "ENDC": "\033[0m"      # Reset color
}


def printc(text, color):
    """
    Print colored text to the console.
    """
    print(f"{color}{text}{COLORS['ENDC']}")


class ApplyBot:
    def __init__(self):
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
        window_width = 400
        window_height = 800

        self.driver.set_window_size(window_width, window_height)
        try:
            self.insert = CheckJob()
        except mysql.connector.errors.DatabaseError:
            printc('The database is not connected and it will create further issues.\n'
                   'Make sure to turn on the server before executing this file..', 'ERROR')
            exit()

    def fix_alert(self):
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
            return True
        except err.NoAlertPresentException:
            return False

    def find_and_apply(self):
        getJobUrlData = self.insert.find_non_applied_jobs(
            table_name=config.TABLE_NAME)
        if not getJobUrlData:
            printc('No jobs found', COLORS['INFO'])
            exit()
        printc(f'{len(getJobUrlData)} job found..', 'INFO')
        progress_links = tqdm.tqdm(getJobUrlData, total=len(getJobUrlData))

        for count, link in enumerate(progress_links, start=1):
            time.sleep(random.randint(4, 8))
            success = self.apply_job(link=link)

            if success:
                apply_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                self.insert.update_job_applied(
                    table_name=config.TABLE_NAME, job_link=link, applied_date=apply_date)
                print(
                    f'{Fore.GREEN}Applied successfully for job link {link}{Style.RESET_ALL}')
            else:
                self.insert.update_job_cant_apply(
                    table_name=config.TABLE_NAME, job_link=link)
                print(
                    f'{Fore.RED}Failed to apply for job link {link}{Style.RESET_ALL}')

            progress_links.set_description(
                f'{Fore.CYAN}Processing item {count}{Style.RESET_ALL}')

    def apply_job(self, link):
        try:
            self.driver.get(link)

            if self.fix_alert():
                self.driver.get(link)

            time.sleep(random.randint(4, 8))

            try:
                apply_btn = self.driver.find_element(
                    By.CLASS_NAME, config.apply_btn)
                apply_btn.click()
            except:
                print(f'{Fore.YELLOW}Job Problem{Style.RESET_ALL}')
                return False

            time.sleep(random.randint(4, 8))
            progress_bar = self.driver.find_element(
                By.CSS_SELECTOR, config.prog_bar)
            prev_prog = progress_bar.get_attribute(config.prog_att)

            while prev_prog != '100':
                self.fill_page()
                cont_btn = self.driver.find_element(
                    By.CLASS_NAME, config.cont_btn)
                cont_btn.click()
                time.sleep(random.randint(4, 8))
                progress_bar = self.driver.find_element(
                    By.CSS_SELECTOR, config.prog_bar)
                curr_prog = progress_bar.get_attribute(config.prog_att)

                if curr_prog == prev_prog:
                    print(
                        f'{Fore.YELLOW}Some fields are required !!{Style.RESET_ALL}')
                    return False

                prev_prog = curr_prog

            cont_btn = self.driver.find_element(By.CLASS_NAME, config.cont_btn)
            cont_btn.click()
            time.sleep(random.randint(4, 8))

            self.wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, config.post_apply_flag)))

            if self.driver.current_url == config.post_apply_url:
                return True
            else:
                return False

        except Exception as e:
            print(e)
            self.insert.update_job_cant_apply(
                table_name=config.TABLE_NAME, job_link=link)
            return False

    def fill_page(self):
        try:
            header = self.driver.find_element(
                By.CLASS_NAME, config.header_cname).get_attribute('innerHTML')

            match header:
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

        except err.NoSuchElementException:
            print(f'{Fore.YELLOW}Page structure not found{Style.RESET_ALL}')

    def review_application(self):
        # used for checking the application not edit required
        return

    def enter_experience(self):
        return
        try:
            for input_field, input_value in config.exp_values.items():
                try:
                    input_element = self.driver.find_element(
                        By.NAME, input_field)
                    input_element.send_keys(Keys.CONTROL, 'a')
                    input_element.send_keys(Keys.DELETE)
                    input_element.send_keys(input_value)
                except err.NoSuchElementException:
                    print(input_field, ' not found !')
                    pass
        except Exception as e:
            print(e)
        return

    def find_question_type(self, question):
        try:
            content = question.find_element(By.TAG_NAME, config.type_radio)
            return content, 'radio'
        except err.NoSuchElementException:
            try:
                content = question.find_element(By.TAG_NAME, config.type_input)
                try:
                    question.find_element(By.TAG_NAME, config.type_drop_down)
                    return content, 'drop_down'
                except err.NoSuchElementException:
                    return content, 'input'
            except err.NoSuchElementException:
                return None

    def find_radio_questions(self, question):
        try:
            question_text = question.find_element(
                By.TAG_NAME, config.radio_ques_text).get_attribute('innerHTML')
            question_text = clean(question_text)
            options = question.find_elements(By.TAG_NAME, config.radio_options)

            print(f"{Fore.YELLOW}Question: {question_text}{Style.RESET_ALL}")

            answer = self.insert.find_question(question_text)
            print()

            if answer is None:
                return
            try:
                print(f'{Fore.GREEN}Stored answer: {answer}{Style.RESET_ALL}')
                for option in options:
                    if option.text == answer:
                        option.click()
                        return True
            except Exception as e:
                print(
                    f"{Fore.RED}Not suitable question. Please apply manually.{Style.RESET_ALL}")

        except:
            return False

    def find_input_questions(self, question):
        try:

            question_element = question.find_element(
                By.TAG_NAME, config.input_ques_text)
            question_text = question_element.get_attribute('innerHTML')
            question_text = clean(question_text)
            # question_id = question_element.get_attribute('for')
            print(f"{Fore.YELLOW}Question: {question_text}{Style.RESET_ALL}")

            answer = self.insert.find_question(question_text)
            print()
            print("stored answer", answer)

            if answer is None:

                return
            print(f"{Fore.YELLOW}Stored answer: {answer}{Style.RESET_ALL}")

            try:
                text_area = question.find_element(
                    By.TAG_NAME, config.input_text_area)
                text_area.click()
                text_area.send_keys(Keys.CONTROL, 'a')
                text_area.send_keys(Keys.DELETE)
                text_area.send_keys(answer)
            except err.NoSuchElementException:
                input_area = question.find_element(
                    By.TAG_NAME, config.input_area)
                input_area.click()
                input_area.send_keys(Keys.CONTROL, 'a')
                input_area.send_keys(Keys.DELETE)
                input_area.send_keys(answer)
        except:
            return False

    def find_drop_down_questions(self, question):
        try:
            question_element = question.find_element(
                By.TAG_NAME, config.drop_ques_text)
            question_text = question_element.get_attribute('innerHTML')
            question_id = question_element.get_attribute('for')
            question_text = clean(question_text)
            print(f"{Fore.YELLOW}Question: {question_text}{Style.RESET_ALL}")

            options = question.find_elements(By.TAG_NAME, config.drop_options)
            answer = self.insert.find_question(question_text)
            print()

            if answer is None:
                return
            try:
                print(f"{Fore.YELLOW}Stored answer: {answer}{Style.RESET_ALL}")

                drop_down_element = question.find_element(By.ID, question_id)
                drop_down_element.click()
                options = drop_down_element.find_elements(
                    By.TAG_NAME, config.drop_options)
                for option in options:
                    if option.text == answer:
                        option.click()
                        return
            except Exception as e:
                print(
                    f"{Fore.RED}Not suitable question. Please apply manually.{Style.RESET_ALL}")

        except:
            print(
                f"{Fore.RED}Not suitable question. Please apply manually.{Style.RESET_ALL}")

            return False

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
        try:
            questions = self.driver.find_elements(
                By.CLASS_NAME, config.question_tag)
            for question in questions:
                content, q_type = self.find_question_type(question)
                if q_type == 'radio':
                    self.find_radio_questions(question)
                if q_type == 'input':
                    self.find_input_questions(question)
                if q_type == 'drop_down':
                    self.find_drop_down_questions(question)
            return
        except Exception as e:
            print(e)

    def resume(self):
        # if the resume it already uploaded then it will process the last used resume
        current_resume = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, config.resume_selector)))
        current_resume.click()
        return

    def add_contact(self):
        # replace the necessary fields
        try:

            for input_field, input_value in config.contact_values.items():
                try:
                    input_element = self.driver.find_element(
                        By.NAME, input_field)
                    # Send key combination (CTRL+A) to select all and then send DELETE to clear
                    input_element.send_keys(Keys.CONTROL, 'a')
                    input_element.send_keys(Keys.DELETE)
                    # input_element.send_keys(u'\ue009' + u'\ue003')
                    input_element.send_keys(input_value)
                except err.NoSuchElementException:
                    print(input_field, ' not found !')
                    pass
        except Exception as e:
            print(
                f"{Fore.RED}Not suitable question. Please apply manually.{Style.RESET_ALL}")

        return

    # ... (rest of the methods)


if __name__ == "__main__":
    apply_bot = ApplyBot()
    apply_bot.find_and_apply()
