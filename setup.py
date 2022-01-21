from setuptools import setup
from setuptools import find_packages

setup(
    name='linkedin_web_scraper',
    version='1.0.0',
    description='Webscraper package that collects specified job data from LinkedIn',
    url='https://github.com/IvanYingX/Linkedin-Scraper-Project',
    author='MateuszBar, armanh3k, JosephSolomon99, IvanYingX',
    license='MIT',
    packages=find_packages(),
    install_requires=['selenium', 'webdriver_manager', 'slqalchemy', 'pandas']
)
