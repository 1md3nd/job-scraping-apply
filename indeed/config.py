chrome_profile = r'C:\Users\{username}\AppData\Local\Google\Chrome\User Data\System Profile'
TABLE_NAME = 'indeed_jobdb'
"""
scrap_data
"""
locations = ['pune','gurgram','noida','banglore','delhi','mumbai']

keywords = ['software development','software engineering','devops','machine learning','data engineer']
EMAIL = ''
PASS = ''


job_title = '/html/body/div[1]/div/div[2]/div/div/div/div[2]/div[1]/div[1]/h1/span'
company_name = '/html/body/div[1]/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div/div/div[1]/div[1]'
location_ = '/html/body/div[1]/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div/div/div[2]/div'
job_desc = 'jobDescriptionText'
job_type = '/html/body/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/span'
apply_btn = 'jobsearch-IndeedApplyButton-newDesign'
apply_btn_ = 'applyButtonLinkContainer'
contiune_btn = "/html/body/div/div[2]/main/div/div/div[2]/div/form/button"
login_btn = '/html/body/div/div[2]/main/div/div/div[2]/div/form[1]/button'



'''
 scrap_links
'''
# url_params
query_keyword = ['software development','software engineering','devops','machine learning','data engineer']

sort = 'date'
fromage = [1, 3, 7, 14]

# Login
signin_page = 'https://secure.indeed.com/auth?hl=en_IN&continue=%2Fsettings%2Faccount'
singin_flag = 'https://secure.indeed.com/settings/account'
email_input = '__email'
password_input = '__password'

# load_indeed
start_url = 'https://in.indeed.com/jobs?'

# extract_job_links
no_job_flag = 'jobsearch-NoResult-messageContainer'
job_list_ele = 'jcs-JobTitle'
next_page = '//a[@aria-label="Next Page"]'


"""
applybot
"""

# apply_job
prog_bar = 'div[role="progressbar"]'
prog_att = "aria-valuenow"
cont_btn = 'ia-continueButton'
post_apply_flag = 'ia-PostApply-header'
post_apply_url = 'https://m5.apply.indeed.com/beta/indeedapply/form/post-apply'

# add_contact
firstName = 'first name'
lastName = 'last name'
location_city = 'location'
phoneNumber = 9988775544
contact_values = {
                'firstName': firstName,
                'lastName': lastName,
                'location.city': location_city,
                'phoneNumber': phoneNumber
            }

# enter_experience
experience_jobTitle = ''
experience_companyName = ''
exp_values = {
        'jobTitle': experience_jobTitle,
        'companyName': experience_companyName
        }

# fill_page
header_cname = 'ia-BasePage-heading'
review_page = 'Please review your application'
experience_page = 'Enter a past job that shows relevant experience'
em_question_page = 'Questions from the employer'
resume_page = 'Add a resume for the employer'
contact_page = 'Add your contact information'
