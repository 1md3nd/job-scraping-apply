TABLE_NAME = 'tbl_joblist'
keywords = ['CISSP', 'Information Security', 'Network Security', 'cyber']
firefox_profile = r"C:\Users\Sushant\AppData\Roaming\Mozilla\Firefox\Profiles\6d0vlbd8.default-release"
# Link_job_apply
total_jobs = '//small'
per_job = '//li[@data-occludable-job-id]'
offer_id = "data-occludable-job-id"

linkedin_start_url = 'https://www.linkedin.com/jobs/view/'

apply_btn = '//button[contains(@class, "jobs-apply-button")]'
submit_btn = "button[aria-label='Submit application']"
next_btn = "button[aria-label='Continue to next step']"
com_percent = 'html/body/div[3]/div/div/div[2]/div/div/span'

# apply_process
choose_btn = "//span[text()='Choose']"
review_btn = "button[aria-label='Review your application']"

# py
# get
load_flag = "/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[2]/article/div/div[1]"
job_title = "/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div/div/div[1]/div[1]/h1"
comp_name = "/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div/div/div[1]/div[2]/div/a"
job_type = "/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div/div/div[1]/div[3]/ul/li[1]/span[1]"
location = "/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div/div/div[1]/div[2]/div"
posted_by_name = "/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[2]/div/div/div[2]/a/span"
posted_by_desig = "/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[2]/div/div/div[2]/div[2]/div[1]"
job_desc = '/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[2]/article/div/div[1]/span'
job_desc_alt = '/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[4]/article/div/div[1]/span'
posting_time = "/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div/div/div[1]/div[2]/div/span[3]"
easy_apply = "/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div/div/div[1]/div[4]/div/div/div/button/span"
poster_profile = '/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[2]/div/div/div[2]/a/span/strong'