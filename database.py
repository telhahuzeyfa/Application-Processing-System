import sqlite3
conn = sqlite3.connect("database.sql")

conn.execute('''CREATE TABLE roleTable (rID    int(1) PRIMARY KEY,
    rName       varchar(20)''')


conn.execute('''CREATE TABLE userTable (userID int(8) PRIMARY KEY, 
            fname varchar(20), 
            lname varchar(20), 
            email varchar(40), 
            username varchar(20), 
            pass varchar(20), 
            roleNum int(1) FOREIGN KEY REFERENCES roleTable(rID), 
            rejected TEXT, 
            approved TEXT, 
            aidsOffered TEXT)''')

conn.commit()

conn.close()  
