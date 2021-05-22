import sqlite3
conn = sqlite3.connect("database.sql")

conn.execute('''CREATE TABLE IF NOT EXISTS roleTable (rID    int(1) PRIMARY KEY,
    rName       varchar(20))''')


conn.execute('''CREATE TABLE IF NOT EXISTS userTable (userID int(8) PRIMARY KEY, 
            fname varchar(20), 
            lname varchar(20), 
            email varchar(40), 
            username varchar(20), 
            pass varchar(20), 
            roleNum int(1), 
            rejected TEXT, 
            approved TEXT, 
            aidsOffered TEXT,
            FOREIGN KEY (roleNum) REFERENCES roleTable(rID))''')

#testing for applicant
conn.execute("INSERT INTO userTable VALUES(88888888, 'testUser', 'testUser', 'test@gmail.com', 'user', 'pass', 1, null, null, null)");            

conn.commit()

conn.close()  
