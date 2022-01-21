from scraper.methods import WebDriver
import unittest
from selenium.webdriver.chrome.options import Options
from time import sleep


class WebDriverTestCase(unittest.TestCase):
    '''Test Class for testing WebDriver class from main script'''
    def setUp(self):
        '''Setting up an instance of the webdriver class for testing'''
        self.username = "aicorebot2@outlook.com"
        self.password = "aicoreteam2"
        self.website = "https://www.linkedin.com/signup/cold-join?session_redirect=https%3A%2F%2Fwww%2Elinkedin%2Ecom%2Ffeed%2F&trk=login_reg_redirect"
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--headless")
        self.instance = WebDriver(chrome_options, self.website, self.username, self.password)
        self.instance.driver.get(self.website)

    def test_get_current_url(self):
        expected_result = "https://www.linkedin.com/signup/cold-join?session_redirect=https%3A%2F%2Fwww%2Elinkedin%2Ecom%2Ffeed%2F&trk=login_reg_redirect"
        actual_result = self.instance.get_current_url()
        self.assertEqual(expected_result, actual_result)

    def test_accept_cookies(self):
        sleep(5)
        self.instance.accept_cookies()

    def test_log_me_in(self):
        sleep(5)
        self.instance.accept_cookies()
        sleep(5)
        self.instance.log_me_in()
        expected_result = "https://www.linkedin.com/feed/"
        actual_result = self.instance.driver.current_url
        self.assertEqual(expected_result, actual_result)

    def tearDown(self):
        sleep(5)
        self.instance.driver.quit()


unittest.main(argv=[''], verbosity=2, exit=False)
