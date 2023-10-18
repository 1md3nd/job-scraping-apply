import re
from datetime import datetime
import random

import selenium.common as err
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from colorama import Fore, Style, init
import undetected_chromedriver as uc
import time
import config
from database.check import CheckJob
import tqdm
import sys


def clean(data):
    data = data.strip()
    pattern = r'<[^>]*>'
    cleaned_string = re.sub(pattern, '', data)
    return cleaned_string.strip()


class ReApplyBot:
    def __init__(self):
        # load_dotenv()

        self.options = uc.ChromeOptions()
        # options.add_argument('--headless')
        # options.add_argument("--start-maximized")
        self.options.add_argument("--ignore-certificate-errors")
        self.options.add_argument('--no-sandbox')
        self.options.add_argument("--disable-extensions")
        self.options.add_argument(f"--user-data-dir={config.chrome_profile}")
        self.options.add_argument(f'--profile-directory={config.profile}')
        self.driver = uc.Chrome(
            browser_executable_path=config.chrome_executable_path, use_subprocess=True, options=self.options)
        window_width = 400
        window_height = 800

        self.driver.set_window_size(window_width, window_height)
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
        try:
            print(
                f"{Fore.YELLOW}Please review the application details carefully.{Style.RESET_ALL}")
            print(
                f"{Fore.YELLOW}If everything looks good, press Enter to continue.{Style.RESET_ALL}")
            input()
        except KeyboardInterrupt:
            print(
                f"{Fore.RED}Application review interrupted. Exiting...{Style.RESET_ALL}")
            sys.exit(1)
        except Exception as e:
            print(f"{Fore.RED}Error during application review:{Style.RESET_ALL}")
            # sys.exit(1)
        return

    def enter_experience(self):
        # try:
        #     for input_field, input_value in config.exp_values.items():
        #         try:
        #             input_element = self.driver.find_element(By.NAME, input_field)
        #             input_element.send_keys(Keys.CONTROL, 'a')
        #             input_element.send_keys(Keys.DELETE)
        #             input_element.send_keys(input_value)
        #         except err.NoSuchElementException:
        #             print(input_field, ' not found !')
        #             pass
        # except Exception as e:
        #     print(e)
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
            question_text_element = question.find_element(
                By.TAG_NAME, config.radio_ques_text)
            question_text = clean(
                question_text_element.get_attribute('innerHTML'))

            options = question.find_elements(By.TAG_NAME, config.radio_options)
            options_dic = {}
            for o_no, option in enumerate(options):
                options_dic[o_no] = option.text

            print(f"{Fore.YELLOW}Question: {question_text}{Style.RESET_ALL}")
            answer = self.cursor.find_question(question_text)

            if answer is None:
                print()
                for k, v in options_dic.items():
                    print(f"{k+1}: {v}")

                while True:
                    try:
                        select_option = int(input("Select an option: "))
                        if 1 <= select_option <= len(options_dic):
                            answer = options_dic[select_option-1]
                            self.cursor.insert_question(question_text, answer)
                            break
                        else:
                            print(
                                f"{Fore.RED}Invalid option. Please select a valid option.{Style.RESET_ALL}")
                    except ValueError:
                        print(
                            f"{Fore.RED}Invalid input. Please enter a valid number.{Style.RESET_ALL}")

            print()
            print(f"{Fore.YELLOW}Stored answer: {answer}{Style.RESET_ALL}")

            try:
                for option in options:
                    if option.text == answer:
                        option.click()
                        return True
                # radio_label = question.find_element(By.XPATH, config.select_radio_answer(answer))
                # radio_label.click()
            except Exception as e:
                print(
                    f"{Fore.RED}Not suitable question. Please apply manually.{Style.RESET_ALL}")
                return False
        except KeyboardInterrupt:
            print(
                f"{Fore.RED}Radio question handling interrupted. Exiting...{Style.RESET_ALL}")
            sys.exit(1)
        except Exception as e:
            print(
                f"{Fore.RED}Not suitable question. Please apply manually.{Style.RESET_ALL}")
            return False

    def find_input_questions(self, question):
        try:
            question_element = question.find_element(
                By.TAG_NAME, config.input_ques_text)
            question_text = clean(question_element.get_attribute('innerHTML'))
            print(f"{Fore.YELLOW}Question: {question_text}{Style.RESET_ALL}")

            answer = self.cursor.find_question(question_text)

            if answer is None:
                while True:
                    print(f"{Fore.YELLOW}Type your answer:{Style.RESET_ALL}")
                    answer = input()
                    if answer:
                        break
                    else:
                        print(
                            f"{Fore.RED}Answer cannot be empty. Please provide an answer.{Style.RESET_ALL}")

                self.cursor.insert_question(question_text, answer)
            else:
                print()
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

        except KeyboardInterrupt:
            print(
                f"{Fore.RED}Input question handling interrupted. Exiting...{Style.RESET_ALL}")
            sys.exit(1)
        except Exception as e:
            print(
                f"{Fore.RED}Not suitable question. Please apply manually.{Style.RESET_ALL}")
            return False

    def find_drop_down_questions(self, question):
        try:
            question_element = question.find_element(
                By.TAG_NAME, config.drop_ques_text)
            question_text = clean(question_element.get_attribute('innerHTML'))
            question_id = question_element.get_attribute('for')
            print(f"{Fore.YELLOW}Question: {question_text}{Style.RESET_ALL}")

            options = question.find_elements(By.TAG_NAME, config.drop_options)
            options_dic = {}
            for o_no, option in enumerate(options):
                option_text = option.text
                options_dic[o_no] = option_text

            answer = self.cursor.find_question(question_text)

            if answer is None:
                print()
                for k, v in options_dic.items():
                    print(f"{k+1}: {v}")

                while True:
                    try:
                        select_option = int(input("Select an option: "))
                        if 1 <= select_option <= len(options_dic):
                            answer = options_dic[select_option-1]
                            self.cursor.insert_question(question_text, answer)
                            break
                        else:
                            print(
                                f"{Fore.RED}Invalid option. Please select a valid option.{Style.RESET_ALL}")
                    except ValueError:
                        print(
                            f"{Fore.RED}Invalid input. Please enter a valid number.{Style.RESET_ALL}")

            print()
            print(f"{Fore.YELLOW}Stored answer: {answer}{Style.RESET_ALL}")

            try:
                drop_down_element = question.find_element(By.ID, question_id)
                drop_down_element.click()
                for option in options:
                    if option.text == answer:
                        option.click()
                        return True
            except Exception as e:
                print(
                    f"{Fore.RED}Not suitable question. Please apply manually.{Style.RESET_ALL}")
                return False
        except KeyboardInterrupt:
            print(
                f"{Fore.RED}Drop-down question handling interrupted. Exiting...{Style.RESET_ALL}")
            sys.exit(1)
        except Exception as e:
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
            print(
                f"{Fore.RED}Not suitable question. Please apply manually.{Style.RESET_ALL}")

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

    def fill_page(self):
        try:
            header = self.driver.find_element(
                By.CLASS_NAME, config.header_cname).text
            print(f"{Fore.GREEN}{header}{Style.RESET_ALL}")
            match clean(header):
                case config.review_page:
                    return self.review_application()
                case config.experience_page:
                    return self.enter_experience()
                case config.em_question_page:
                    return self.employer_ques()
                case config.em_question_page1:
                    return self.employer_ques()
                case config.resume_page:
                    return self.resume()
                case config.contact_page:
                    return self.add_contact()
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
            try:
                apply_btn = self.driver.find_element(
                    By.CLASS_NAME, config.apply_btn)
                apply_btn.click()
            except:
                print(
                    f"{Fore.RED}Job Application Error: Unable to find the apply button.{Style.RESET_ALL}")
                self.cursor.make_as_manual(
                    table_name=config.TABLE_NAME, job_link=link)
                return False

            time.sleep(random.randint(4, 8))
            try:
                progress_bar = self.driver.find_element(
                    By.CSS_SELECTOR, config.prog_bar)
                prev_prog = progress_bar.get_attribute(config.prog_att)
            except:
                print(f"{Fore.GREEN}Already applied.{Style.RESET_ALL}")
                self.cursor.make_as_manual(
                    table_name=config.TABLE_NAME, job_link=link)
                return False
            while prev_prog != '100':
                self.fill_page()
                cont_btn = self.driver.find_element(
                    By.CLASS_NAME, config.cont_btn)
                cont_btn.click()
                time.sleep(random.randint(4, 8))
                progress_bar = self.driver.find_element(
                    By.CSS_SELECTOR, config.prog_bar)
                curr_prog = progress_bar.get_attribute(config.prog_att)
                if prev_prog == curr_prog:
                    is_skip = input(
                        f"{Fore.YELLOW}Select 'y'/'yes' to exit the job or fill the job manually, and 'n'/'no' to continue: {Style.RESET_ALL}")
                    if is_skip in ('y', 'yes'):
                        print(
                            f"{Fore.YELLOW}Exiting the current job...{Style.RESET_ALL}")
                        return False

                prev_prog = curr_prog
            self.fill_page()

            cont_btn = self.driver.find_element(By.CLASS_NAME, config.cont_btn)
            cont_btn.click()
            time.sleep(random.randint(4, 8))

            if EC.presence_of_element_located((By.CLASS_NAME, config.post_apply_flag)):
                apply_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if self.driver.current_url == config.post_apply_url:
                    print(f"{Fore.GREEN}Job Applied Successfully!{Style.RESET_ALL}")
                    self.cursor.update_job_applied(
                        table_name=config.TABLE_NAME, job_link=link, applied_date=apply_date)
                    return True
                else:
                    print(
                        f"{Fore.RED}Job Application Error: Unable to confirm application.{Style.RESET_ALL}")
                    self.cursor.update_job_cant_apply(
                        table_name=config.TABLE_NAME, job_link=link)
            else:
                print(
                    f"{Fore.RED}Job Application Error: Unable to confirm application.{Style.RESET_ALL}")
                self.cursor.update_job_cant_apply(
                    table_name=config.TABLE_NAME, job_link=link)

        except KeyboardInterrupt:
            print(
                f"{Fore.RED}Job application process interrupted. Exiting...{Style.RESET_ALL}")
            sys.exit(1)
        except Exception as e:
            print(f"{Fore.RED}Job Application Error: {str(e)}{Style.RESET_ALL}")
            self.cursor.update_job_cant_apply(
                table_name=config.TABLE_NAME, job_link=link)

        return False

    def find_and_apply(self):
        get_job_url_data = self.cursor.find_manual_jobs(
            table_name=config.TABLE_NAME)
        total_jobs = len(get_job_url_data)

        if total_jobs == 0:
            print(f"{Fore.GREEN}No manual jobs found to apply.{Style.RESET_ALL}")
            return

        progress_links = tqdm.tqdm(get_job_url_data, total=total_jobs)

        for count, link in enumerate(progress_links, start=1):
            print(
                f"{Fore.YELLOW}Processing job {count}/{total_jobs}:{Style.RESET_ALL}")
            result = self.apply_job(link=link)
            if result is False:
                print(
                    f"{Fore.YELLOW}Job application skipped for job {count}/{total_jobs}. Moving to the next job...{Style.RESET_ALL}")
            else:
                print(
                    f"{Fore.GREEN}Job {count}/{total_jobs} successfully applied!{Style.RESET_ALL}")

        print(f"{Fore.GREEN}All manual jobs have been processed.{Style.RESET_ALL}")


if __name__ == "__main__":
    print(f"{Fore.GREEN}LinkedIn Semi-Auto Job Application Bot{Style.RESET_ALL}")
    start = time.time()
    try:
        bot = ReApplyBot()
        bot.find_and_apply()
        end = time.time()
        print(
            f"{Fore.GREEN}---Took: {str(round((end - start) / 60))} minute(s).{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
