from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import pandas as pd

#page = requests.get("https://www.flipkart.com/laptops/</a>~buyback-guarantee-on-laptops-/pr?sid=6bo%2Cb5g&uniq")

products=[] #List to store name of the product
prices=[] #List to store price of the product
ratings=[] #List to store rating of the product

def export_save(data):    
     df = pd.DataFrame({'Product Name':products,'Price':prices,'Rating':ratings}) 
     df.to_csv('products.csv', index=False, encoding='utf-8')


driver = webdriver.Chrome(executable_path=r"C:/Users/abhin/chromedriver_win32/chromedriver.exe")
driver.get("https://www.flipkart.com/laptops/</a>~buyback-guarantee-on-laptops-/pr?sid=6bo%2Cb5g&uniq")
content = driver.page_source
soup = BeautifulSoup(content,'lxml')

for a in soup.findAll('a',href=True, attrs={'class':'_31qSD5'}):
    name   = a.find('div', attrs={'class':'_3wU53n'})
    price  = a.find('div', attrs={'class':'_1vC4OE _2rQ-NK'})
    rating = a.find('div', attrs={'class':'hGSR34'})
    if rating:
        ratings.append(rating.text) 
    else:
        ratings.append('0.0') 
    products.append(name.text)
    
    price=str(price.text).replace('₹','')
    prices.append(price)
    
    
export_save()
#df = pd.DataFrame({'Product Name':products,'Price':prices,'Rating':ratings}) 
#df.to_csv('products.csv', index=False, encoding='utf-8')

