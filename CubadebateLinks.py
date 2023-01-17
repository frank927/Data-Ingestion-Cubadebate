import requests
from bs4 import BeautifulSoup
from time import sleep
from ConnectionSQLITE import *
import random
from datetime import datetime
from datetime import timedelta
import pandas as pd

agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
]
user_agent = random.choice(agent_list)

linklist=[]

def getLinks(category,page):
  url=f'http://www.cubadebate.cu/{category}/page/{page}/'
      
  page = requests.get(url, user_agent)

  soup = BeautifulSoup(page.text, 'html.parser')

  noticias = soup.find_all('div', {'class':'title'})
  
  for data in noticias:
     link = data.find('a')['href']
     linklist.append(link)
  

for x in range(1,4):
  getLinks('especiales', x)

for x in range(1,6):
  getLinks('noticias', x)

for x in range(1,3):
  getLinks('opinion', x)

for x in range(1,2):  
  getLinks('fotorreportajes', x)

for x in range(1,2): 
  getLinks('coletilla', x)

for x in range(1,2):  
  getLinks('libros-libres', x)
   
for data in linklist:
        now = datetime.now()
        date=now.date()
        cursor.execute("INSERT OR IGNORE INTO Links (Links,StorageDate) VALUES(?,?)", [data, date])
        connection.commit()
        
cursor.execute("SELECT StorageDate FROM Links")
Date=cursor.fetchall()
dframe=pd.DataFrame(Date)
newFrame=dframe.pop(0)

for i in newFrame:
    now=datetime.now()
    date=now.date()
    if(i<=str(date - timedelta(days=10))):
        cursor.execute(f"DELETE FROM Links WHERE StorageDate='{i}'")
        connection.commit()        
       
print('Todas las urls fueron almacenadas')



 