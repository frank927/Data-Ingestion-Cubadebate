import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
from ConnectionSQLITE import *
import random

agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
]
user_agent = random.choice(agent_list)

commentslist=[]
cleaning=[]
num=[]
Text=[]
Tag=[]
Temas=[]


def All():
  
  cursor.execute("SELECT Links FROM Links")
  Links=cursor.fetchall()
  dframe=pd.DataFrame(Links)
  newFrame=dframe.pop(0)
  count = 1
  
  for i in newFrame:       
     
     link=f'{i}'  
      
     n=link.find('202')
     date=link[n:n+10]
     
     def NumPage(link=link):
        url=f'{link}'
    
        page = requests.get(url, user_agent)
        
        soup = BeautifulSoup(page.text, 'html.parser')
    
        for numPage in soup.find_all('a', {'class':"page smaller"}):   
            num.append(numPage.get_text())
        if(len(num)==0):
                return 1
        elif(num[-1]=='10'):
              more=soup.find('span', {'class':"extend"}).get_text()
              if(more=='...'):
                  Count=soup.find('span', {'class':"comment_count"}).get_text()
                  pag=int(Count)/35
                  
                  return int(pag)
              else:  
                  return num[-1]  
        else:
                return num[-1]
                     
   
     def getComm(pag,link=link):
       url=f'{link}' + f'comentarios/pagina-{pag}/#comment_content'

       page = requests.get(url , user_agent)
       
       soup = BeautifulSoup(page.text, 'html.parser')


       for i in soup.find_all('div', class_=('title','commenttext')):
       
         commentslist.append(i.get_text())
     
     
     for x in range(1, int(NumPage(link))+1):
              getComm(x ,link)
             
     
     if(len(commentslist)>=1):
        page = requests.get(link , user_agent)
       
        soup = BeautifulSoup(page.text, 'html.parser')

        contenido = soup.find_all('div', {'class':'note_content'})
  
        for data in contenido:
            d = data.text
            Text.append(d)
            
        etiquetas = soup.find_all('a', {'rel':'category tag taxonomy'})
  
        for data in etiquetas:
            D = data.text
            Tag.append(D)
        
        temas = soup.find_all('a', {'rel':'category tag'})
  
        for data in temas:
            t = data.text
            Temas.append(t)
        if(Temas[5]=='Noticias'):   
            tem=''
        else:
            tem=Temas[5]    
            
        for element in Tag:
            while(Tag.count(element) > 1):
                Tag.remove(element)
            if(element=='Estallido de Comentarios'):
                Tag.remove(element)
            if(element==''):
                Tag.remove(element)  
            if(element.startswith('ir a')):    
                Tag.remove(element)
            
        inicio=link.find('cu/')
        fin=link.find('/202')
        categoria=link[inicio+3:fin]
    
        for element in commentslist:
            while(commentslist.count(element) > 1):
                commentslist.remove(element)
                  
        cursor.execute("INSERT OR REPLACE INTO Comments (Links, Contents, Tags, Comments, Num, Category, Themes, Date) VALUES (?,?,?,?,?,?,?,?)", (str(link),str(Text), str(Tag),str(commentslist), str(len(commentslist)),str(categoria),str(tem),str(date)))
        connection.commit()

     commentslist.clear()
     num.clear()  
     Text.clear()
     Tag.clear()
     Temas.clear()
    
     print(str(count)+' URLs Recorridas')
     count+=1
    
All()       
    
    
    

