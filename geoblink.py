from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import pandas as pd
import unidecode

driver = webdriver.Chrome(executable_path=r"C:/Users/abhin/chromedriver_win32/chromedriver.exe")
name=[]
position=[]
driver.get("https://www.geoblink.com/about-geoblink/")
content = driver.page_source
soup = BeautifulSoup(content,'lxml')


rows = soup.find_all('strong',class_="title-cn")
for x in rows:
    print(x)
    accented_string=x.text
    unaccented_string = unidecode.unidecode(accented_string)
    name.append(unaccented_string)




rows = soup.find_all('small',class_="position-cn")
for x in rows:
    print(x)
    position.append(x.text)


  
df = pd.DataFrame({'Member Name':name,'Position':position}) 
df.to_csv('geoblink.csv', index=False, encoding='utf-8')

