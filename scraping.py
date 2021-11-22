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
# import pandas as pd

URL = "https://www.ecb.europa.eu/press/pressconf/html/index.en.html"

driver = webdriver.Chrome()
driver.get(URL)

driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
last_height = driver.execute_script("return document.body.scrollHeight")
sleep(1)

#
# driver.execute_script("window.scrollTo(0, 1080.49)")
# sleep(2)
# driver.execute_script("window.scrollTo(0, 2160)")
# sleep(10)

length = 1080


while (length < last_height):
    driver.execute_script(f'window.scrollTo(0, {length})')
    sleep(1)
    length += 1080
    last_height = driver.execute_script("return document.body.scrollHeight")

# while driver.find_element(By.TAG_NAME, 'div'):
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     Divs=driver.find_element(By.TAG_NAME, 'div').text
#     if 'End of Results' in Divs:
#         print('end')
#         break
#     else:
#         print(Divs)
#         continue

main = BeautifulSoup(driver.page_source, 'html.parser')
# print(main.prettify())

body = main.find('body', attrs='project-ecb section-press sub-pressconf -top-notice')
div = body.find('div', attrs={'id': 'main-wrapper'})
div_main = div.find('main')
div_div = div_main.find('div', attrs={'class': 'definition-list -filter'})
dl = div_div.find('dl', attrs={'id': 'lazyload-container'})
dl_div = dl.findAll('div', attrs={'class': 'lazy-load loaded'})
print('=========== PRINT DIV ==============')
print(dl_div)
# print(div)
# print(dl_div.find('dt'))