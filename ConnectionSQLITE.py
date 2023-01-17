import sqlite3

connection=sqlite3.connect("Cubadebate/Cubadebate.db")
cursor=connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS Links (Links TEXT PRIMARY KEY, StorageDate TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS Comments (Links TEXT PRIMARY KEY, Contents TEXT, Tags TEXT, Comments TEXT NOT NULL, Num TEXT, Category Text, Themes TEXT, Date TEXT, foreign key (Links) REFERENCES Links(Links))")

#cursor.execute("drop table Comments")
#connection.commit()   



#cursor.execute("DELETE FROM Comments WHERE Themes='Noticias' ")
#connection.commit()   
       

cursor.execute("SELECT SUM(Num) FROM Comments;")   
Total=cursor.fetchall()
#print(Total) 






   

         
  
   

   
   
