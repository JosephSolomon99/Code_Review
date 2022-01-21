# Linkedin-Scraper-Project

A selenium based web scraper that scrapes job advertisement data from Linkedin. 
Can search for any job and location, scrapes all 40 visible pages and sends data to AWS RDS.

## Installation

Use the package manager [pip](https://pypi.org/) and search for linkedin_web_scraper to install whole package.

OR 

```bash
pip install linkedin_web_scraper
```

## Usage

Before using, configure the following:
Create and add a secrets.py file to the scraper folder, with the following variables inside:

#LinkedIn login details
LINKEDINUSERNAME = ''
LINKEDINPASSWORD = ''

#Database info
DATABASE_TYPE = ''
DBAPI = ''
ENDPOINT = '' #AWS Endpoint
USER = ''
PASSWORD = ''
PORT= ''
DATABASE= ''

Usage:
Run scraper.py and use a relation database manager of your choice to view and query scraped data.

## License
[MIT](https://choosealicense.com/licenses/mit/)