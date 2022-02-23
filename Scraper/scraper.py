from methods import *
#from secrets import (LINKEDINUSERNAME, LINKEDINPASSWORD)

def main():
    '''
    Function that controls scraper script
    '''

    website = "https://www.linkedin.com/feed/"
    chrome_options = webdriver.ChromeOptions()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    chrome_options.add_argument("window-size=1920,1080")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument("--allow-insecure-localhost")
    chrome_options.add_experimental_option('detach', True)
    LINKEDINUSERNAME = input("Enter Linkedin username: ")
    LINKEDINPASSWORD = input("\n Enter Linkedin password: ")
    scraper = WebDriver(chrome_options, website, LINKEDINUSERNAME, LINKEDINPASSWORD)
    scraper.driver.implicitly_wait(2)
    scraper.driver.get(website)
    sleep(3)
    scraper.accept_cookies()
    sleep(2)
    scraper.log_me_in()
    sleep(2)
    scraper.get_database_details()
    sleep(1)
    # Edit this to change search term and location
    search_term = input("Enter job title to search for: ")
    search_location = input("Enter location to search in: ")
    scraper.search_term(search_term, search_location)
    sleep(2)
    scraper.extract_job_details()
    sleep(2)
    print("\n\nScraping has been completed")
    scraper.driver.quit()

if __name__ == "__main__":
    # safeguard used to prevent script running
    # automatically if it's imported into another file
    main()
