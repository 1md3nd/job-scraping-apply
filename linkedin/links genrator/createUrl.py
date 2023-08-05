import config

linkJobUrl = "https://www.linkedin.com/jobs/search/"


def generateUrlLinks():
    path = []
    for location in config.location:
        for keyword in config.keywords:
            # url = linkJobUrl + "?f_AL=true&keywords=" +keyword+"""jobType()+remote()+"""checkJobLocation(
            # location)"""+jobExp()+datePosted()"""#+salary()+sortBy()
            url = linkJobUrl + "?f_AL=true&keywords=" + keyword + datePosted() + checkJobLocation(location)
            path.append(url)
    return path


def checkJobLocation(job):
    locations = {
        "Alberta": "103564821",
        "Ontario": "105149290",
        "Toronto, ON": "100025096",
        "Ottawa, ON": "106234700",
        "Vancouver, BC": "103366113",
        "Kitchener-Waterloo, ON": "102082786",
        "Calgary, AB": "102199904",
        "Victoria, BC": "100346955",
        "Halifax, NS": "103961363",
        "Hamilton, ON": "104444106",
        "San Francisco, CA": "102277331",
        "Seattle": "104116203",
        "Washington": "90000097",
        "Austin, TX": "90000064",
        "New York": "105080838",
        "Atlanta, Georgia": "106224388",
        "Denver, CO": "103736294",
        "San Jose, CA": "106233382",
        "Dallas, Texas": "104194190",
        "San Diego, California": "100737633",
        "Raleigh, North Carolina": "100197101",
        "Miami": "102394087",
        "Houston, TX": "103743442",
        "Boulder, Colorado": "102597912",
        "Portland, OR": "104727230",
        "Charlotte, North Carolina": "102264677",
        "Salt Lake City, Utah": "106513356",
        "Dallas-Fort Worth Metropolitan Area": "104194190",
        "SF Bay Area": "90000084",
        "Baltimore, MD": "106330734",
        "Minneapolis, Minnesota": "103039849"
    }

    jobLoc = "&location=" + job
    geoId = locations.get(job)
    if geoId:
        jobLoc += "&geoId=" + geoId

    return jobLoc


# def checkJobLocation(job):
#     jobLoc = "&location=" +job
#     match job.casefold():
#         case "ontario":
#             jobLoc += "&geoId=105149290"
#         case "bc":
#             jobLoc += "&geoId=102044150"
#         case "ns":
#             jobLoc += "&geoId=104823201"
#         # case "mt":
#         #     jobLoc +=  "&geoId=104423466"
#         # case "qb":
#         #     jobLoc +=  "&geoId=102237789"
#         # case "Vancouver":
#         #     jobLoc += "&geoId=103366113"
#
#     return jobLoc

def jobExp():
    jobtExpArray = config.experienceLevels
    firstJobExp = jobtExpArray[0]
    jobExp = ""
    match firstJobExp:
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
    for index in range(1, len(jobtExpArray)):
        match jobtExpArray[index]:
            case "Internship":
                jobExp += "%2C1"
            case "Entry level":
                jobExp += "%2C2"
            case "Associate":
                jobExp += "%2C3"
            case "Mid-Senior level":
                jobExp += "%2C4"
            case "Director":
                jobExp += "%2C5"
            case "Executive":
                jobExp += "%2C6"

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


def remote():
    remoteArray = config.remote
    firstJobRemote = remoteArray[0]
    jobRemote = ""
    match firstJobRemote:
        case "On-site":
            jobRemote = "f_WT=1"
        case "Remote":
            jobRemote = "f_WT=2"
        case "Hybrid":
            jobRemote = "f_WT=3"
    for index in range(1, len(remoteArray)):
        match remoteArray[index]:
            case "On-site":
                jobRemote += "%2C1"
            case "Remote":
                jobRemote += "%2C2"
            case "Hybrid":
                jobRemote += "%2C3"

    return jobRemote


def salary():
    salary = ""
    match config.salary[0]:
        case "$40,000+":
            salary = "f_SB2=1&"
        case "$60,000+":
            salary = "f_SB2=2&"
        case "$80,000+":
            salary = "f_SB2=3&"
        case "$100,000+":
            salary = "f_SB2=4&"
        case "$120,000+":
            salary = "f_SB2=5&"
        case "$140,000+":
            salary = "f_SB2=6&"
        case "$160,000+":
            salary = "f_SB2=7&"
        case "$180,000+":
            salary = "f_SB2=8&"
        case "$200,000+":
            salary = "f_SB2=9&"
    return salary


def sortBy():
    sortBy = ""
    match config.sort[0]:
        case "Recent":
            sortBy = "sortBy=DD"
        case "Relevent":
            sortBy = "sortBy=R"
    return sortBy


with open('urlData.txt', 'w') as f:
    linkedinJobLinks = generateUrlLinks()
    for url in linkedinJobLinks:
        f.write(url + "\n")
