import sqlite3
conn = sqlite3.connect("database.sql")

# role table
conn.execute('''CREATE TABLE IF NOT EXISTS roleTable (rID    int(1) PRIMARY KEY,
    rName       varchar(20))''')

# user table
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

conn.execute('''CREATE TABLE IF NOT EXISTS addmissionForm(
    userID              int(8),
    fname               varchar(20),
    lname               varchar(20),
    department          varchar(20),
    semester            varchar(20),
    semester_year       varchar(20),
    prior_degrees       varchar(30),
    SocialSecurity      int(8),
    address_id          int(8),
    cityAndState        varchar(20),
    country             varchar(30),
    zipcode             int(8),
    program             varchar(20),
    GPA                 decimal(4,2),
    degree_year         int(4),
    institutionName     varchar(40),
    prior_experiance    varchar(60),
    nameOfRecommender   varchar(40),
    emailOfRecommender  varchar(50),
    titleOfRecommender  varchar(50),
    affiliationOfRecommender varchar(60),
    PRIMARY KEY (userID, department)
)''')

conn.execute('''CREATE TABLE IF NOT EXISTS reviewForm(
    fname               varchar(20),
    lname               varchar(20),
    semesterAndYear     varchar(20), 
    applyingForDegree   varchar(20),
    GreVerbalScore      DECIMAL,
    greQuantitative     DECIMAL,
    yearOfExam          int(5),
    BSorBA              varchar(10),
    BSorBA_GPA          decimal(4,2),
    major               varchar(10),
    graduationYear      int(5),   
    university          varchar(40), 
    areaOfInterest      varchar(40),
    experiance          varchar(40),
    rec1Rating          int(1),
    rec1Quality         varchar(20),
    rec1Institution     varchar(50),
    recommendedAdvisor  varchar(20))''')

conn.execute('''CREATE TABLE IF NOT EXISTS finalDecision(
    userID              int(8),
    CACandChairDecision varchar(20),
    GASreviewerComments varchar(40),
    recommendedAdvisor  varchar(15),
    aidsOffered         varchar(5),
    PRIMARY KEY (userID))''')

conn.execute('''CREATE TABLE IF NOT EXISTS confirmMsApplication(
    userID             int (8),
    confirmApp         varchar(10),
    PRIMARY KEY (userID))''')    

# #testing for applicant
conn.execute("INSERT OR IGNORE INTO userTable VALUES(88888888, 'testUser', 'testUser', 'test@gmail.com', 'user', 'pass', 1, null, null, null)");            

# application complete but no reviews testing user
conn.execute("INSERT OR IGNORE INTO userTable VALUES(55555555, 'John', 'Lennon', 'JohnLennon@gmail.com', 'JohnLennon', 'pass', 1, null,null,null)")

# incomplete application
conn.execute("INSERT OR IGNORE INTO userTable VALUES(66666666, 'Ringo', 'Starr', 'RingoStarr@gmail.com', 'RingoStarr', 'pass', 1, null,null,null)")

# for graduate Secretary
conn.execute("INSERT OR IGNORE INTO userTable VALUES(10101010, 'Graduate Secretary', 'Graduate Secretary', 'graduateSecretarty@gmail.com', 'gs', 'pass', 2, null,null,null)")

# for faculty reviewer 
conn.execute("INSERT OR IGNORE INTO userTable VALUES(20202020, 'Narahari', 'Narahari', 'Narahari@gmail.com', 'Narahari', 'pass', 3, null,null,null)")

# another faculty reviewer
conn.execute("INSERT OR IGNORE INTO userTable VALUES(30303030, 'Wood', 'Heller', 'WoodHeller@gmail.com', 'WoodHeller', 'pass', 3, null,null,null)")  

# for CAC/Chair
conn.execute("INSERT OR IGNORE INTO userTable VALUES(40404040, 'CAC/Chair', 'CAC/Chair', 'CAC/Chair@gmail.com', 'CAC/Chair', 'pass', 4, null,null,null)")

conn.execute("INSERT OR IGNORE INTO userTable VALUES(50505050, 'Recommenders', 'Recommenders', 'Recommenders@gmail.com', 'rec', 'pass', 5, null,null,null)")


conn.execute("INSERT OR IGNORE INTO roleTable VALUES(1, 'Applicants')")
conn.execute("INSERT OR IGNORE INTO roleTable VALUES(2, 'Graduate Secretary')")
conn.execute("INSERT OR IGNORE INTO roleTable VALUES(3, 'Faculty Reviewers')")
conn.execute("INSERT OR IGNORE INTO roleTable VALUES(4, 'CAC/Chair')")
conn.execute("INSERT OR IGNORE INTO roleTable VALUES(5, 'Recommenders')")

conn.commit()

conn.close()  
