chrome_profile = r'C:\Users\Sushant\AppData\Local\Google\Chrome\User Data\System Profile'
TABLE_NAME = 'indeed_jobdb'
"""
scrap_data
"""

keywords = ['CISSP', 'Information Security', 'Network Security', 'cyber']
EMAIL = 'cedaje2538@sportrid.com'
PASS = '123456@@'


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
query_keyword = ['CISSP', 'Information Security', 'Network Security', 'cyber']
# query_keyword = ['Information Security']

# locations = ['Alberta']
locations = [
    "Alberta",
    "Ontario",
    "Toronto, ON",
    "Ottawa, ON",
    "Vancouver, BC",
    "Kitchener-Waterloo, ON",
    "Calgary, AB",
    "Victoria, BC",
    "Halifax, NS",
    "Hamilton, ON",
    "San Francisco, CA",
    "Seattle",
    "Washington",
    "Austin, TX",
    "New York",
    "Atlanta, Georgia",
    "Denver, CO",
    "San Jose, CA",
    "Dallas, Texas",
    "San Diego, California",
    "Raleigh, North Carolina",
    "Houston, TX",
    "Boulder, Colorado",
    "Portland, OR",
    "Charlotte, North Carolina",
    "Salt Lake City, Utah",
    "Dallas-Fort Worth Metropolitan Area",
    "SF Bay Area",
    "Baltimore, MD",
    "Minneapolis, Minnesota"]

sort = 'date'
fromage = [1, 3, 7, 14]

# Login
signin_page = 'https://secure.indeed.com/auth?hl=en_IN&continue=%2Fsettings%2Faccount'
singin_flag = 'https://secure.indeed.com/settings/account'
email_input = '__email'
password_input = '__password'

# load_indeed
start_url = 'https://ca.indeed.com/jobs?'

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
firstName = 'ajaxx1'
lastName = 'ajaxx1'
location_city = 'loca_ajaxx1'
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
