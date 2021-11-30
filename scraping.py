# Author: gustavovital
# Date: 31/10/2021
#
# The main file provides a scraping through the web page of ECB (meetings)

####################################################################
# IT IS NECESSARY TO UPDATE THE CODE FOR THE NEW PRESS CONFERENCES #
####################################################################

# modules
import requests
from selenium import webdriver
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

# Preparing data frame
dates = []
refs = []
title = []

for tags in dl_div:
    for date in tags.findAll('dt'):
        dates.append(date['isodate'])
    for ref in tags.findAll('dd'):
        title.append(ref.find('div', attrs={'class': 'title'}).text)
        refs.append(ref.find('a')['href'])

# save data
href_data = pd.DataFrame({'Dates': dates, 'Href': refs, 'title': title})

# Getting the texts from href
# create column for the docs

# href_data = pd.read_pickle('data\\href_data.pkl')
href_data["Doc"] = ""

# base url
URL = "https://www.ecb.europa.eu"

# iterate to get the texts and add in the data frame new col, get the <'p'>
for index, references in enumerate(href_data['Href']):

    doc = ""

    content = requests.get(URL + references).content
    main = BeautifulSoup(content, "html.parser").find('main')

    if index >= 29 and index <= 37:
        section = main.findAll("div", attrs={"class": "section"})
        texts = section[1].findAll("p")

        for text in texts:
            doc += text.text
    else:
        section = main.find("div", attrs={"class": "section"})
        texts = section.findAll("p")

        for text in texts:
            doc += text.text

    href_data["Doc"][index] = doc

href_data.drop([199], inplace=True)  # remove line 199 (just slides and Q&A)
href_data.reset_index(drop=True, inplace=True)

# save data
href_data.to_pickle("data\\press_data.pkl")