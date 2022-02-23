from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
import pandas as pd
from sqlalchemy import create_engine
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import datetime
import uuid
# from secrets import (
#     DATABASE_TYPE,
#     DBAPI,
#     ENDPOINT,
#     USER,
#     PASSWORD,
#     PORT,
#     DATABASE
# )

class WebDriver():
    '''
    WebDriver class used to move through a website and find elements inside

    Attributes:
        address (str): The address of the website that will be scraped
        username (str): The username for the account on the website
        password (str): The password for the account on the website
        driver : webdriver instance
    '''

    def __init__(self, chrome_options: Options, address: str, username: str, password: str):
        # ChromeDriverManager installs webdriver into cache automatically
        self.address = address
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
        self.scraper_DATABASE_TYPE = ""
        self.scraper_DBAPI = ""
        self.scraper_ENDPOINT = ""
        self.scraper_USER = ""
        self.scraper_PASSWORD = ""
        self.scraper_PORT = ""
        self.scraper_DATABASE = ""

    def accept_cookies(self):
        '''
        Method that finds manage cookies and accept cookies buttons by
        class name and then clicks the accept cookies button
        '''
        # Find both buttons using class_name
        print("\n Accepting cookies \n")
        try:
            both_buttons = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "artdeco-global-alert-action.artdeco-button.artdeco-button--inverse.artdeco-button--2.artdeco-button--primary")))
            accept_button = both_buttons[1]
            accept_button.click()
        except(TimeoutException):
            "Cookies not found, moving on"

    def log_me_in(self):
        '''
        Method that finds sign in link, clicks it,
        finds email and password boxes and fills in information
        clicks sign in button

        Args:
            None

        Returns:
            Home webpage where user is logged in
        '''
        # Find sign in link and load that page
        print("\n Logging in \n")
        sign_in_container = self.driver.find_element_by_class_name('main__sign-in-container')
        sign_in_link = sign_in_container.find_element_by_link_text('Sign in')
        sign_in_link.click()
        sleep(2)  # let website load
        # Find box and enter email address
        email_or_phone_box = self.driver.find_element_by_id('username')
        email_or_phone_box.send_keys(self.username)
        # Find box and enter password
        password_box = self.driver.find_element_by_id('password')
        password_box.send_keys(self.password)
        # Find Sign in button and click
        sign_in_button = self.driver.find_element_by_class_name('btn__primary--large.from__button--floating')
        sign_in_button.click()
        sleep(3)
        print(self.get_current_url())

    def get_database_details(self):
        '''
        Method that asks user for database information so we can connect to RDS

        Args:
            None

        Returns:
            None
        '''
        self.scraper_DATABASE_TYPE = input("Enter database type (postgres default is postgresql): ")
        self.scraper_DBAPI = input("Enter database API to use (postgres API is psycopg2): ")
        self.scraper_ENDPOINT = input("Enter RDS endpoint link: ")
        self.scraper_USER = input("Enter database server name: ")
        self.scraper_PASSWORD = input("Enter database server password: ")
        self.scraper_PORT = input("Enter database port (postgres default is 5432): ")
        self.scraper_DATABASE = input("Enter database name: ")

    def search_term(self, job: str, location: str):
        '''
        Method that uses the search bar to search for a term and a location.

        Args:
            job (str): term that we are searching for
            location (str): geographical location where we want to search for jobs

        Returns:
            webpage with results from search
        '''
        print(f"\n Searching for {job} jobs in the {location} area \n")
        self.driver.get("https://www.linkedin.com/jobs/")

        sleep(1)
        try:
            search_box = self.driver.find_element_by_class_name("jobs-search-box__text-input.jobs-search-box__keyboard-text-input")
            search_box.send_keys(job)

            location_box = self.driver.find_elements_by_class_name('jobs-search-box__text-input')[3]
            location_box.send_keys(location)

            search_button = self.driver.find_element_by_class_name('jobs-search-box__submit-button.artdeco-button.artdeco-button--2.artdeco-button--secondary')
            search_button.click()
        except(NoSuchElementException):
            self.driver.get("https://www.linkedin.com/jobs/search/?keywords=data%20science")

    def get_current_url(self):
        '''
        Method that returns current URL of webdriver

        Args:
            None

        Returns:
            URL (str) : URL of current webpage
        '''
        URL = self.driver.current_url
        return URL

    def find_all_pages(self):
        '''
        Method that finds the next page of results. Finds total number of search results, gets current URL, appends URL which causes next page to load

        Args:
            None

        Returns:
            next page of search results
        '''
        print("\n Finding all pages to scrape \n")
        # finds total number of job results and saves value as integer
        try:
            results = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'jobs-search-results-list__text')))[1].text
            result = int(''.join(c for c in results if c.isdigit()))
            base_url = self.get_current_url()
            all_pages = []
        except(TimeoutException):
            url = self.get_current_url()
            print(url)
            page_source = self.driver.page_source
            fileToWrite = open("page_source.html", "w")
            fileToWrite.write(page_source)
            fileToWrite.close()
            fileToRead = open("page_source.html", "r")
            print(fileToRead.read())
            fileToRead.close()

        # linkedin displays maximum of 40 pages of 25 results, thus any results after the initial 1000 will be ignored
        if result > 975:
            for page in range(25, 1000, 25):
                url = base_url + f"&start={page}"
                all_pages.append(url)

        elif result <= 975:
            pages = (result // 25)  # round number up expression
            for page in range(25, 25 * pages, 25):
                url = base_url + f"&start={page}"
                all_pages.append(url)
        return all_pages

    def pd_from_list(self, list1: list, list2: list, list3: list, list4: list, list5: list, list6: list, list7: list, list8: list, list9: list):
        df = {'uuid': list1,
              'Job_title': list2,
              'Company_name': list3,
              'Company_location': list4,
              'Job_detail': list5,
              'Job_description': list6,
              'Job_link': list7,
              'Job_id': list8,
              'date_scraped': list9}
        dataframe = pd.DataFrame.from_dict(df, orient='index')
        return dataframe.transpose()

    def read_postgres_table(self):
        '''
        Method that reads postgres table and returns job links column
        Args:
            None

        Returns:
            list of links from postgres table
        '''
        engine = create_engine(f"{self.scraper_DATABASE_TYPE}+{self.scraper_DBAPI}://{self.scraper_USER}:{self.scraper_PASSWORD}@{self.scraper_ENDPOINT}:{self.scraper_PORT}/{self.scraper_DATABASE}")
        # column needs quotation marks around it for some reason
        try:
            postgres_links = engine.execute('''SELECT "Job_link" FROM scraped_data''').fetchall()
        except Exception:
            postgres_links = []
        return postgres_links

    def job_ids_from_table(self):
        '''
        Method that extracts job id's from postgres table links and returns them in a list
        Args:
            None

        Returns:
            postgres_ids (list) : list of all job id's in postgres table
        '''
        postgres_links = self.read_postgres_table()
        postgres_ids = []
        for link in postgres_links:
            ids = str(link[0])
            ids = ids[35:45]
            postgres_ids.append(ids)
        return postgres_ids

    def gen_uuid(self, link_list: list) -> list:
        '''
        Method that generates a unique ID for each job record

        Args:
            link_list: List of job links

        Returns:
            list: List of Unique ID

        '''
        uuid_list = []
        for i in range(len(link_list)):
            uuid_list.append(uuid.uuid4())
        return uuid_list

    def extract_job_details(self):
        '''
        Method that collects job details from the current searched terms, collects up to 40 pages from linkedin results and sends them to AWS RDS
        Args:
            None

        Returns:
            None
        '''
        print("\n Scraping page data \n")
        # finding path to job container
        all_pages = self.find_all_pages()
        postgres_ids = self.job_ids_from_table()
        sleep(3)
        # loop through each page
        # for page in range(1):
        for page in range(len(all_pages)):
            sleep(1)
            # Find container with job tiles
            try:
                container = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-results__list")))
                jobs = container.find_elements_by_class_name("jobs-search-results__list-item")
            except(TimeoutException):
                self.driver.refresh()
                sleep(2)
                container = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-results__list")))
                jobs = container.find_elements_by_class_name("jobs-search-results__list-item")
                continue
            # create lists which will append important job details for each job scraped
            link_list = []
            job_title_list = []
            company_name_list = []
            company_location_list = []
            job_description_list = []
            job_detail_list = []
            job_id_list = []
            # loop through each job on given page
            for job in jobs:
                try:
                    sleep(1)
                    job.click()
                    sleep(0.5)
                    # Find panel with main info
                    job_panel = self.driver.find_element_by_class_name("job-view-layout.jobs-details")
                    # Extract Linkedin job listing url and id
                    a_tag = job_panel.find_element_by_tag_name("a")
                    job_links = a_tag.get_attribute('href')
                    job_id = job_links[35:45]
                    # Compare job id to postgres table
                    if job_id in str(postgres_ids):
                        continue
                    else:
                        link_list.append(job_links)
                        job_id_list.append(job_id)
                    # Extract job title
                    job_title = job_panel.find_element_by_tag_name("h2").text
                    job_title_list.append(job_title)
                    # Extract company details
                    company_details = job_panel.find_element_by_class_name("jobs-unified-top-card__subtitle-primary-grouping")
                    company_name = company_details.find_element_by_tag_name("a").text
                    company_name_list.append(company_name)
                    company_location = company_details.find_element_by_class_name("jobs-unified-top-card__bullet").text
                    company_location_list.append(company_location)
                    # Extract job desctiption
                    job_description = job_panel.find_element_by_id("job-details")
                    job_description = job_description.find_element_by_tag_name("span").text
                    job_description_list.append(job_description)
                    # Extract job details (full time/part time )
                    ul_tag = job_panel.find_element_by_tag_name("ul")
                    li_tag = ul_tag.find_element_by_class_name("jobs-unified-top-card__job-insight")
                    job_detail = li_tag.find_element_by_tag_name("span").text
                    job_detail_list.append(job_detail)
                # Catch exceptions
                except (StaleElementReferenceException, NoSuchElementException):
                    continue
            uuid_list = self.gen_uuid(link_list)
            data_frame = self.pd_from_list(uuid_list, job_title_list, company_name_list, company_location_list, job_detail_list, job_description_list, link_list, job_id_list, [datetime.datetime.now().date()]*len(job_id_list))
            cleaned_data_frame = data_frame.dropna(axis=0, thresh=4)
            print(f"\nSending data from page {page+1} to AWS\n")
            self.send_data_to_aws(cleaned_data_frame)
            self.driver.get(all_pages[page])

    def dataframe_to_csv(self, dataframe: pd.DataFrame):
        '''
        Method that creates a csv file called output_data.csv from a pandas dataframe

        Arguments:
            pd.DataFrame

        Returns:
            csv file with input data inside

        '''
        dataframe.to_csv('output_data.csv', index=False, header=True, encoding='utf-8')

    def send_data_to_aws(self, dataframe: pd.DataFrame):
        '''
        Method that sends dataframe to AWS RDS

        Arguments:
            pd.DataFrame

        Returns:
            None
        '''

        engine = create_engine(f"{self.scraper_DATABASE_TYPE}+{self.scraper_DBAPI}://{self.scraper_USER}:{self.scraper_PASSWORD}@{self.scraper_ENDPOINT}:{self.scraper_PORT}/{self.scraper_DATABASE}")
        dataframe.to_sql('scraped_data', engine, if_exists='append')
