import sys
sys.path.append('Linkedin-Scraper-Project')
from scraper.methods import WebDriver
from scraper.secrets import (LINKEDINUSERNAME, LINKEDINPASSWORD)
import unittest
from pandas import DataFrame
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from time import sleep
import uuid

class WebDriverTestCase(unittest.TestCase):
    '''Test Class for testing WebDriver class from main script'''
    def setUp(self):
        '''Setting up an instance of the webdriver class for testing'''
        self.username = LINKEDINUSERNAME
        self.password = LINKEDINPASSWORD
        self.website = "https://www.linkedin.com/signup/cold-join?session_redirect=https%3A%2F%2Fwww%2Elinkedin%2Ecom%2Ffeed%2F&trk=login_reg_redirect"
        chrome_options = Options()
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument("--headless")
        chrome_options.add_argument(f'user-agent={user_agent}')
        self.instance = WebDriver(chrome_options, self.website, self.username, self.password)
        self.instance.driver.get(self.website)

    def test_get_current_url(self):
        expected_result = "https://www.linkedin.com/signup/cold-join?session_redirect=https%3A%2F%2Fwww%2Elinkedin%2Ecom%2Ffeed%2F&trk=login_reg_redirect"
        actual_result = self.instance.get_current_url()
        self.assertEqual(expected_result, actual_result)

    def test_accept_cookies(self):
        sleep(5)
        self.instance.accept_cookies()
        sleep(2)
        self.instance.driver.find_elements_by_class_name("artdeco-global-alert-action.artdeco-button.artdeco-button--inverse.artdeco-button--2.artdeco-button--primary")
        self.assertRaises(NoSuchElementException)

    def test_log_me_in(self):
        sleep(5)
        self.instance.accept_cookies()
        sleep(5)
        self.instance.log_me_in()
        expected_result = "https://www.linkedin.com/feed/"
        actual_result = self.instance.driver.current_url
        self.assertEqual(expected_result, actual_result)
    
    def test_search_term(self):
        sleep(2)
        self.instance.accept_cookies()
        sleep(2)
        self.instance.log_me_in()
        sleep(2)
        self.instance.search_term('Data Science', 'England, United Kingdom')
        sleep(2)
        expected_result = "https://www.linkedin.com/jobs/search/?geoId=102299470&keywords=Data%20Science&location=England%2C%20United%20Kingdom"
        actual_result = self.instance.driver.current_url
        self.assertEqual(expected_result, actual_result)

    def test_find_all_pages(self):
        sleep(2)
        self.instance.accept_cookies()
        sleep(2)
        self.instance.log_me_in()
        sleep(2)
        self.instance.search_term('Data Science', 'England, United Kingdom')
        sleep(2)
        links = self.instance.find_all_pages()
        self.assertGreater(len(links), 0)

    def test_pd_from_list(self):
        list1 = [1,2,3,4,5]
        list2 = [1,2,3,4,5]
        list3 = [1,2,3,4,5]
        list4 = [1,2,3,4,5]
        list5 = [1,2,3,4,5]
        list6 = [1,2,3,4,5]
        list7 = [1,2,3,4,5]
        list8 = [1,2,3,4,5]
        list9 = [1,2,3,4,5]
        test_df = self.instance.pd_from_list(list1,list2,list3,list4,list5,list6,list7,list8,list9)
        columns = test_df.shape[1]
        rows = test_df.shape[0]
        self.assertEqual(columns,9)
        self.assertEqual(rows,5)

    def test_gen_uuid(self):
        list = [1,2,3,4,5]
        uuids = self.instance.gen_uuid(list)
        first_uuid = uuids[0]
        self.assertTrue(isinstance(first_uuid, uuid.UUID))
    
    def tearDown(self):
        sleep(5)
        self.instance.driver.quit()


unittest.main(argv=[''], verbosity=2, exit=False)
