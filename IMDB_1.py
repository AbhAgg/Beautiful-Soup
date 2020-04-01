## Import the various libraries.

from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import pandas as pd
import unidecode
import matplotlib.pyplot as plt
from time import sleep
from random import randint
import IPython
from IPython.core.display import clear_output
import time
import warnings
from IPython import display

#Initiate empty lists
movie_name=[]
movie_year=[]
movie_rating=[]
movie_metascore=[]





start_time = time.time()
requests1 = 0

#Limit the pages and years to be searched
pages     = [i for i in range(1,1000,50)]
years_url = [i for i in range(2000,2010)]



for year_url in years_url:
        for page in pages:          
            response = requests.get('https://www.imdb.com/search/title/?title_type=feature&release_date='+str(year_url)+'-01-01,'+str(year_url)+'-12-31&sort=num_votes,asc&start='+str(page)+'&ref_=adv_nxt')
            sleep(randint(1,2))
            requests1 += 1
            elapsed_time = time.time() - start_time
            print('Request:{}; Frequency: {} requests/s'.format(requests1, requests1/elapsed_time))
            clear_output(wait = True)
            
            
            html_soup = BeautifulSoup(response.text, 'html.parser')
            
        #Finding Movie Names
            
            rowx=html_soup.findAll('h3',class_='lister-item-header')
            for row in rowx:
               item=row.find('a')
               if item:
                    movie_name.append(item.text)
               else:
                    movie_name.append('0.0')
                    
               item=row.find('span',class_='lister-item-year text-muted unbold')
               if item:
                    movie_year.append(item.text)
               else:
                    movie_year.append('0.0')
                    
        #Finding Movie ratings
        
            score=html_soup.findAll(class_='inline-block ratings-imdb-rating')
            for row in score:
                item=row.find('strong')
                if item:
                    movie_rating.append(item.text)
                else:
                    movie_rating.append('0.0')

                    
            metascore=html_soup.findAll(class_='ratings-bar')
            for row in metascore:
                xyz=row.find(class_='inline-block ratings-metascore')
                if xyz is None:
                    movie_metascore.append('0.0')
                else:
                    item=xyz.find('span')
                    if item:
                            movie_metascore.append(int(item.text.strip()))
                    else:
                            movie_metascore.append('0.0')
                            
                            
# Cleaning the Movie year data and changing data types.

for i in range(0,len(movie_year)):
    movie_year[i]=int(movie_year[i][-5:-1].strip("()"))
    
movie_rating    = list(map(float, movie_rating))
movie_metascore = list(map(float, movie_metascore))

# Making a dataframe using pandas library and saving the data

df = pd.DataFrame({'Movie Name':movie_name,
                   'Movie Year':movie_year,
                   'Movie Star Rating':movie_rating, 
                   'Metascore':movie_metascore }) 
df.to_csv('Movie Database.csv', index=False, encoding='utf-8-sig')



#Plotting the data to view the distributions
fig, axes = plt.subplots(nrows = 1, ncols = 3, figsize = (16,4))
ax1, ax2, ax3 = fig.axes
ax1.hist(df['Movie Star Rating'], bins = 10, range = (0,10)) # bin range = 1
ax1.set_title('IMDB rating')
ax2.hist(df['Metascore'], bins = 10, range = (0,100)) # bin range = 10
ax2.set_title('Metascore')
ax3.hist(df['n_imdb'], bins = 10, range = (0,100), histtype = 'step')
ax3.hist(df['Metascore'], bins = 10, range = (0,100), histtype = 'step')
ax3.legend(loc = 'upper left')
ax3.set_title('The Two Normalized Distributions')
for ax in fig.axes:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
plt.show()