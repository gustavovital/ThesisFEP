# Author: gustavovital
# Date: 31/10/2021
#
# The main file provides a scraping through the web page of ECB (meetings)

# modules
# import requests
# import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

# URL of press conference
URL = "https://www.ecb.europa.eu/press/pressconf/html/index.en.html"

# Initialize Driver
driver = webdriver.Chrome()
driver.get(URL)

driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
last_height = driver.execute_script("return document.body.scrollHeight")

# Wait til load the page
sleep(0.5)

# Generalise for the full page
length = 1080
while (length < last_height):
    driver.execute_script(f'window.scrollTo(0, {length})')
    sleep(0.5)
    length += 1080
    last_height = driver.execute_script("return document.body.scrollHeight")

# Selenium to Bs4
main = BeautifulSoup(driver.page_source, 'html.parser')

# Get the page component
body = main.find('body', attrs='project-ecb section-press sub-pressconf -top-notice')
div = body.find('div', attrs={'id': 'main-wrapper'})
div_main = div.find('main')
div_div = div_main.find('div', attrs={'class': 'definition-list -filter'})
dl = div_div.find('dl', attrs={'id': 'lazyload-container'})
dl_div = dl.findAll('div', attrs={'class': 'lazy-load loaded'})

print(dl_div)
# print(dl_div.prettify)
# print(dl_div.findAll('dt')[0])
# print(driver.find_element_by_tag_name('dt'))


# for date in dl_div.findAll('dt'):
#     print('Date: ' + date['isodate'])
#
# for ref in dl_div.findAll('dd'):
#     print('href: ' + ref.find('a')['href'])


# print(dl_div[1])
dates = []
refs = []

for tags in dl_div:
    for date in tags.findAll('dt'):
        dates.append(date['isodate'])
    for ref in tags.findAll('dd'):
        refs.append(ref.find('a')['href'])

pd.DataFrame({'Dates': dates, 'Href': refs}).head()