#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import selenium.common as err
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

def format_desc(desc):
    """
    Format the raw description text by replacing specific HTML tags with corresponding text formatting.

    Parameters:
        desc (str): Raw description text with HTML tags.

    Returns:
        str: Formatted description text.
    """
    desc = desc.strip()
    replace_dic = {
        '<!---->': '',
        '<br>': '\n',  # line break
        '<p>': '',  # paragraph break (start)
        '</p>': '\n',  # paragraph break (end)
        '<strong>': "\033[1m",  # Bold text (start)
        '</strong>': "\033[0m",  # Bold text (end)
        '<em>': "\x1B[3m",  # Italic text (start)
        '</em>': "\x1B[0m",  # Italic text (end)
        '<u>': "\x1B[4m",  # Underline text (start)
        '</u>': "\x1B[0m",  # Underline text (end)
        '</ul>': "\n",  # unordered list (end)
        '<ul>': "\n",  # unordered list (start)
        '</ol>': "\n",  # ordered list (end)
        '<ol>': "\n",  # ordered list (start)
        '<li>': "  \u2022 ",  # Bullet point symbol
        '</li>': "\n",  # Bullet point (end)
        '</h1>': "\n\n",  # Header 1 (start)
        '</h2>': "\n\n",  # Header 2 (start)
        '</h3>': "\n\n",  # Header 3 (start)
        '</h4>': "\n\n",  # Header 4 (start)
        '</h5>': "\n\n",  # Header 5 (start)
        '</h6>': "\n\n",  # Header 6 (start)
        '<h1>': "\n\n\033[1m",  # Header 1 (end)
        '<h2>': "\n\n\033[1m",  # Header 2 (end)
        '<h3>': "\n\n\033[1m",  # Header 3 (end)
        '<h4>': "\n\n\033[1m",  # Header 4 (end)
        '<h5>': "\n\n\033[1m",  # Header 5 (end)
        '<h6>': "\n\n\033[1m",  # Header 6 (end)
        '</code>': "\033[0m",  # Code block (end)
        '<code>': "\033[44m\033[30m",  # Code block (start, blue background and black text)
    }
    for tag, replacement in replace_dic.items():
        desc = desc.replace(tag, replacement)
    # Define a regular expression pattern to match any <span> tag and its contents
    span_pattern = r'<span\b[^>]*>'

    # Use re.sub() to replace all occurrences of <span> tags and their contents with an empty string
    cleaned_data = re.sub(span_pattern, '', desc)
    cleaned_data = cleaned_data.replace('</span>', '')
    return cleaned_data.strip()


def clean(data):
    data = data.strip()
    pattern = r'<[^>]*>'
    cleaned_string = re.sub(pattern, '', data)
    return cleaned_string


class extractData:
    def __init__(self):
        self.keywords = config.keywords
        self.driver = webdriver.Firefox(options=self.browser_options())
        self.wait = WebDriverWait(self.driver, 10)

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

    def getinnerHTML(self, xpath):
        try:
            res = self.driver.find_element(By.XPATH, xpath).get_attribute('innerHTML')
        except err.NoSuchElementException:
            res = "not found"
        return res

    def location(self, path):
        try:
            res = self.driver.find_element(By.XPATH, path).get_attribute('innerHTML')
            html_tag_pattern = r'<[^>]*>'

            # Use re.sub() to replace all occurrences of HTML tags and their contents with an empty string
            res = re.sub(html_tag_pattern, '', res)
        except err.NoSuchElementException:
            # print(e)
            res = "not found"
        # print(res)
        return res.strip('\n')

    def get(self, input_url):
        """
        Extract job poster's name and description from the given URL and print the results.

        Parameters:
            input_url (str): URL of the job posting page.
        """
        job_data = {}

        try:
            self.driver.get(url=input_url)
            element = self.wait.until(EC.presence_of_element_located((By.XPATH, config.load_flag)))
            element.click()
            job_data['job_link'] = input_url
            job_data['job_title'] = self.getinnerHTML(config.job_title)
            job_data['company_name'] = self.getinnerHTML(config.comp_name)
            company_name = job_data['company_name']
            job_data['job_type'] = self.getinnerHTML(config.job_type)
            job_data['location'] = self.location(config.location)
            job_data['posted_by_name'] = self.getinnerHTML(config.posted_by_name)
            job_data['posted_by_designation'] = self.getinnerHTML(config.posted_by_desig)
            if job_data['posted_by_name'] == 'not found':
                job_data['job_description'] = self.getinnerHTML(config.job_desc)
            else:
                job_data['job_description'] = self.getinnerHTML(config.job_desc_alt)
            raw_job_desc = job_data['job_description']
            job_data['posting_time'] = self.getinnerHTML(config.posting_time)
            posting_time = job_data['posting_time']

            temp = job_data['location']
            temp2 = temp.strip(f"{company_name}").strip(f"{posting_time}")
            job_data['location'] = temp2

            # print(job_data)

            for k, v in job_data.items():
                # print(k,v)
                job_data[k] = clean(v)
            temp = []
            job_data['is_relevant'] = False
            for word in self.keywords:
                # print(word)
                find_ele = re.findall(word.lower(), raw_job_desc.lower(), re.IGNORECASE)
                if len(find_ele) > 0:
                    job_data['is_relevant'] = True
                    temp.append(word)
            job_data['keywords'] = ' '.join(temp)

            easy_apply = self.getinnerHTML(config.easy_apply)
            if clean(easy_apply) == "Easy Apply":
                job_data['easy_apply'] = True
            else:
                job_data['easy_apply'] = False
            try:
                element = self.wait.until(EC.presence_of_element_located((By.XPATH, config.poster_profile)))
                element.click()
                url_flag = self.wait.until(EC.url_contains('/in/'))
                if url_flag:
                    job_data['poster_url'] = self.driver.current_url
                else:
                    job_data['poster_url'] = 'not found'
            except:
                job_data['poster_url'] = 'not found'
            return job_data
        except Exception as err:
            print(err)
            return "NOT FOUND"

    def close(self):
        self.driver.close()
