import requests
import pandas as pd
from bs4 import BeautifulSoup


href_data = pd.read_pickle("data\\href_data.pkl")
href_data["Doc"] = ""
# print(href_data['Href'][200])
URL = "https://www.ecb.europa.eu"

for index, references in enumerate(href_data['Href']):

    content = requests.get(URL + references).content
    main = BeautifulSoup(content, "html.parser").find('main')
    section = main.find("div", attrs={"class": "section"})
    texts = section.findAll("p")

    doc = ""
    for text in texts:
        doc += text.text

    href_data["Doc"][index] = doc

href_data.to_pickle("data\\press_data.pkl")

# content = requests.get(URL + href_data['Href'][200]).content
# main = BeautifulSoup(content, "html.parser").find('main')
#
# section = main.find('div', attrs={'class': 'section'})
# texts = section.findAll('p')
#
# doc = ""
# for text in texts:
#     doc += text.text
