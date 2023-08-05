# Web Scraping Project User Manual

## 1. Introduction

Welcome to the Web Scraping Project User Manual. This document provides step-by-step instructions on how to use the web scraping project to gather job-related information from various websites. The project consists of three main scripts: createUrl.py, linkGrabber.py, and linEasyApplyBot.py. The project's goal is to scrape job details, store them in a MySQL database, and perform automated job applications for relevant and easy-to-apply jobs.

## 2. Prerequisites

Before using the web scraping project, ensure that you have the following prerequisites installed:

Python (version 3.6 or higher)
MySQL server (with the necessary credentials to create a database and tables)
## 3. Setting up the MySQL Database

Before running any of the scripts, create a MySQL database and the required tables using the following steps:

Log in to your MySQL server using the appropriate client (e.g., MySQL Command Line, MySQL Workbench).

##### Create a new database using the following command:

###### sql
`CREATE DATABASE job_applydb;`

##### Use the newly created database:
`USE job_applydb;`

##### Create the necessary tables for storing job information and application status:

###### sql
`CREATE TABLE jobs (
    job_link VARCHAR(255),
    job_title VARCHAR(255),
    company_name VARCHAR(255),
    job_type VARCHAR(50),
    location VARCHAR(100),
    job_description TEXT,
    posted_by_name VARCHAR(100),
    posted_by_designation VARCHAR(100),
    poster_url VARCHAR(255),
    posting_time DATETIME,
    keywords VARCHAR(255),
    is_relevant BOOLEAN,
    easy_apply BOOLEAN,
    applied BOOLEAN DEFAULT 0,
    apply_problem BOOLEAN DEFAULT 0
    applied_date DATETIME DEFAULT NULL
);`

## 4. Running the Scripts

### Step 1: Generating the List of Jobs

Open a terminal or command prompt on your computer.

Navigate to the directory where you have stored the web scraping project files, including the createUrl.py script.

Ensure that you have the necessary prerequisites installed, including Python (version 3.6 or higher).

#### Run the createUrl.py script by entering the following command:

`python data/createUrl.py`

###### This script is responsible for generating a list of job URLs based on certain criteria (e.g., job location, job type, keywords). The script will access job listing websites or APIs to collect job URLs and store them in a file called job_urls.txt in the project directory.


After the script finishes running, you will find the `job_urls.txt` file containing a list of job URLs that match your search criteria. You can review the contents of this file to ensure the URLs have been generated correctly.

### Step 2: Scraping Job Information

With the job_urls.txt file now populated with job URLs, you are ready to run the `linkGrabber.py` script.

Ensure that you have the MySQL server installed and set up with the necessary credentials to create a database and tables.

Open a terminal or command prompt and navigate to the project directory.

#### Run the `linkGrabber.py` script by entering the following command:
`python linkGrabber.py`

###### The `linkGrabber.py` script will read the list of job URLs from `job_urls.txt` and start visiting each URL one by one. For each job page, it will extract relevant job information such as job title, job description, company name, location, and more. The extracted data will be stored in the MySQL database tables created earlier.

Depending on the number of job URLs in the `job_urls.txt` file, this process may take some time to complete.

Once the script finishes running, all the job-related information from the visited URLs will be stored in the MySQL database. You can check the database tables to review the scraped data.

### Step 3: Applying to Relevant and Easy-to-Apply Jobs

Before running the `linEasyApplyBot.py` script, ensure that you have a MySQL database set up and the tables created, as explained in the prerequisites.

Open a terminal or command prompt and navigate to the project directory.

#### Run the `linEasyApplyBot.py` script by entering the following command:

`python linEasyApplyBot.py`

###### The `linEasyApplyBot.py` script will query the MySQL database for job entries that are marked as relevant and easy to apply (i.e., where `is_relevant` and `easy_apply` are both `TRUE`). It will then attempt to apply to each relevant job automatically.

During the application process, the script will navigate to each job page, fill out the necessary application forms, and submit applications.

##### If a job application is successful, the corresponding `applied` field in the database will be updated to `TRUE` and `applied_date` to current datetime. If the application encounters an issue (e.g., the website changes its form layout, the job is no longer available), the apply_problem field for that job will be updated to TRUE.

The script will continue attempting to apply to all relevant jobs in the database until it has processed all of them.

## Conclusion

By following these step-by-step instructions, you can successfully run the web scraping project to gather job-related information, store it in a MySQL database, and perform automated job applications. Always ensure that you have the right to scrape data from the targeted websites and use the project responsibly and ethically.