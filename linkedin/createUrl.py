import config
from datetime import datetime
import os

linkJobUrl = "https://www.linkedin.com/jobs/search/"


def generateUrlLinks():
    path = []
    for location in config.locations:
        for keyword in config.keywords:
            # url = linkJobUrl + "?f_AL=true&keywords=" +keyword+"""jobType()+remote()+"""checkJobLocation(
            # location)"""+jobExp()+datePosted()"""#+salary()+sortBy()
            for exp in config.experienceLevels:
                url = linkJobUrl + "?f_AL=true&keywords=" + keyword + datePosted() + "&location="+ location + jobExp(experience=exp)
                path.append((exp,url))
    return path


def jobExp(experience):
    # jobtExpArray = config.experienceLevels
    # firstJobExp = jobtExpArray[0]
    jobExp = ""
    match experience:
        case "Internship":
            jobExp = "&f_E=1"
        case "Entry level":
            jobExp = "&f_E=2"
        case "Associate":
            jobExp = "&f_E=3"
        case "Mid-Senior level":
            jobExp = "&f_E=4"
        case "Director":
            jobExp = "&f_E=5"
        case "Executive":
            jobExp = "&f_E=6"
   
    return jobExp


def datePosted():
    datePosted = ""
    match config.datePosted[0]:
        case "Any Time":
            datePosted = ""
        case "Past Month":
            datePosted = "&f_TPR=r2592000&"
        case "Past Week":
            datePosted = "&f_TPR=r604800&"
        case "Past 24 hours":
            datePosted = "&f_TPR=r86400&"
    return datePosted


def jobType():
    jobTypeArray = config.jobType
    firstjobType = jobTypeArray[0]
    jobType = ""
    match firstjobType:
        case "Full-time":
            jobType = "&f_JT=F"
        case "Part-time":
            jobType = "&f_JT=P"
        case "Contract":
            jobType = "&f_JT=C"
        case "Temporary":
            jobType = "&f_JT=T"
        case "Volunteer":
            jobType = "&f_JT=V"
        case "Intership":
            jobType = "&f_JT=I"
        case "Other":
            jobType = "&f_JT=O"
    for index in range(1, len(jobTypeArray)):
        match jobTypeArray[index]:
            case "Full-time":
                jobType += "%2CF"
            case "Part-time":
                jobType += "%2CP"
            case "Contract":
                jobType += "%2CC"
            case "Temporary":
                jobType += "%2CT"
            case "Volunteer":
                jobType += "%2CV"
            case "Intership":
                jobType += "%2CI"
            case "Other":
                jobType += "%2CO"
    jobType += "&"
    return jobType


def sortBy():
    sortBy = ""
    match config.sort[0]:
        case "Recent":
            sortBy = "sortBy=DD"
        case "Relevent":
            sortBy = "sortBy=R"
    return sortBy

current_date = datetime.now()

# Format the current date and month strings
date_string = current_date.strftime("%Y-%m-%d")
script_path = os.path.abspath(__file__)

# Get the directory containing the script
script_directory = os.path.dirname(script_path)
file_path = os.path.join(script_directory,f"jobs/urlData_{date_string}")
with open(file_path, 'w') as f:
    linkedinJobLinks = generateUrlLinks()
    for (exp,url) in linkedinJobLinks:
        f.write(exp + "\t")
        f.write(url + "\n")
