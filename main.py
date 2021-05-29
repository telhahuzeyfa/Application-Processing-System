from flask import Flask, render_template, request, session, url_for, redirect, abort, send_file 
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import os
import sqlite3
import random
from werkzeug.utils import secure_filename
app = Flask('app')
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'huzeyfaprep@gmail.com'
app.config['MAIL_PASSWORD'] = '1234abdc'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.secret_key = 'secretKey'
buffered = True
#upload transcript to it's specified folder
UPLOAD_FOLDER = 'static/transcripts'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#upload recommendation letter to it's specified folder
UPLOAD_FOLDER_RECOMMENDER = 'static/RecommendationLetters'
app.config['UPLOAD_FOLDER_RECOMMENDER'] = UPLOAD_FOLDER_RECOMMENDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
  if request.method == 'POST':
    # session['user'] = request.form['username']
    password = request.form['password']
    username = request.form['username']

    mydb = sqlite3.connect('database.sql')
    cur = mydb.cursor()
    cur.execute('SELECT * FROM userTable WHERE username = ? AND pass = ?', (username, password))
    results = cur.fetchone()
    if results is None:
      return 'Username/Password Incorrect'
    #created a session variable for roleNum (index 4)
    session['roleNum'] = results[6]
    session['userID'] = results[0]

    #cur.execute('SELECT userID FROM userTable WHERE username = ? AND pass = ?', (username, password))
    result = cur.fetchone()    
    cur.close()
  return render_template ('home.html', user = results[1])

@app.route('/accountCreation', methods = ['GET', 'POST'])
def accountCreation():
  if request.method == 'POST':
    # userId = request.form.get('universityId', False)
    email = request.form['email']
    username = request.form['username']
    #Checks if userID, username or email have already been used

    mydb = sqlite3.connect('database.sql')
    cur = mydb.cursor()
    cur.execute('SELECT * FROM userTable WHERE username = ? OR email = ?', (username, email))
    results = cur.fetchone()
    if results is not None:
        return "Input a different University ID or username or email, this one already exists"
    fname = request.form['firstName']
    lname = request.form['lastName']
    roleNum = request.form.get('department', False)
    password = request.form['password']
    cur = mydb.cursor()
    #Generate a random userID
    findID = False
    while findID == False:
      userID = random.randint(11111111,99999999)
      cur.execute('SELECT * FROM userTable WHERE userID = ?', (userID,))
      session['userID'] = userID
      user = cur.fetchone()
      if not user:
        findID = True

    cur.execute('INSERT INTO userTable (fname, lname, email, username, roleNum, pass, userID) VALUES (?, ?, ?, ?, ?, ?, ?)', (fname, lname, email, username, roleNum, password, userID,))
    cur = mydb.commit()
  return render_template('registered.html', error="error")  

@app.route("/registerForm")
def registrationFormStudent():
    return render_template("accountCreation.html")

@app.route("/SignInForm")
def signinPage():
    return render_template("signinPage.html")

@app.route('/home', methods = ['GET'])
def home():
    return render_template('home.html')  


@app.route('/MsApplication', methods = ['GET', 'POST'])
def uploadTranscript():
  if request.method == 'POST':
    f = request.files['transcript']
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
    
    session['user'] = request.form['firstName']
    userID = session['userID']
    fname = request.form['firstName']
    lname = request.form['lastName']
    department = request.form['program']
    semester = request.form['semester']
    semester_year = request.form['semester']
    SocialSecurity = request.form['SocialSecurity']
    address_id = request.form['address_id']
    cityAndState = request.form['cityAndState']
    country = request.form['country']
    zipcode = request.form['zipcode']
    program = request.form['program']
    prior_degree = request.form['priorDegree']
    degree_year = request.form['degree_year']
    institutionName = request.form['institutionName']
    prior_experiance = request.form['prior_experiance']
    GPA = request.form['GPA']
    nameOfRecommender = request.form['nameOfRecommender']
    emailOfRecommender = request.form['emailOfRecommender']
    titleOfRecommender = request.form['titleOfRecommender']
    affiliationOfRecommender = request.form['affiliationOfRecommender']
    confirmApp = request.form['confirmApp']

    mydb = sqlite3.connect('database.sql')
    cur = mydb.cursor()
    cur.execute('INSERT INTO addmissionForm (userID, fname, lname, department, semester, semester_year, prior_degrees, SocialSecurity, address_id, cityAndState, country, zipcode, program, GPA, degree_year, institutionName, prior_experiance, nameOfRecommender, emailOfRecommender, titleOfRecommender, affiliationOfRecommender) VALUES (?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?, ?, ?, ?)',(userID, fname, lname, department, semester, semester_year, prior_degree, SocialSecurity, address_id, cityAndState, country, zipcode, program, GPA, degree_year, institutionName, prior_experiance, nameOfRecommender, emailOfRecommender, titleOfRecommender, affiliationOfRecommender))
    cur = mydb.commit()

    cur = mydb.cursor()
    cur.execute('INSERT INTO confirmMsApplication(userID, confirmApp) VALUES(?, ?)', (userID, confirmApp))
    cur = mydb.commit()

    return render_template("sentApplicationPage.html")

  # check if the applicant has already applied for MS program
  # if the applicatn already has a generated userID it means that they have applied for MS program
  userID = session['userID']
  #before applicant received thier status

  mydb = sqlite3.connect('database.sql')
  cur = mydb.cursor()
  cur.execute('SELECT userID FROM addmissionForm WHERE userID = ?', (userID,))
  application = cur.fetchone() #--> null after updating addmissionForm table

  if application is not None:
    return render_template("applied.html")

  cur = mydb.cursor()
  cur.execute("SELECT * FROM finalDecision WHERE userID = ?", (userID,))
  applicationAfter = cur.fetchone()

  if applicationAfter is not None:
    return render_template("applied.html")
  cur.close()  
  
  return render_template("MsProgramApplication.html", error="error")

# @app.route('/checkStatus', methods = ['GET', 'POST'])  
# this one just returns the check status page
@app.route('/checkStatus')
def checkStatus():
  #this function checks if addmission for was filled out yet
  userID = session['userID']

  #for approval
  mydb = sqlite3.connect('database.sql')
  cur = mydb.cursor()
  cur.execute("SELECT approved FROM userTable WHERE userID = ?", (userID,))  
  approved = cur.fetchall()
  approved = [i[0] for i in approved]
  #for denial
  cur = mydb.cursor()
  cur.execute("SELECT rejected FROM userTable WHERE userID = ?", (userID,))  
  rejected = cur.fetchall()
  rejected =[i[0] for i in rejected]
  #for aid 
  cur = mydb.cursor()
  cur.execute("SELECT aidsOffered FROM userTable WHERE userID = ?", (userID,))  
  aidsOffered = cur.fetchall()
  aidsOffered =[i[0] for i in aidsOffered]
  cur.close()  

  #Checking if addmission form was filled out yet
  cur = mydb.cursor()
  cur.execute('SELECT userID FROM confirmMsApplication WHERE userID = ?', (userID,))
  results = cur.fetchone()  
  if results is None:
    return render_template("incompleteApplication.html")  
  #------------------------------------------------- 
  cur = mydb.cursor()
  cur.execute('SELECT userID FROM addmissionForm WHERE userID = ?', (userID,))
  results = cur.fetchone()
  if results is not None:
    return render_template("applicationProcessing.html")
  #------------------------------------------------- 
  return render_template("checkStatus.html", approved=approved, rejected=rejected, aidsOffered=aidsOffered)

@app.route('/displayApplicantsData', methods = ['GET', 'POST'])
def displayApplicantsData():
  mydb = sqlite3.connect('database.sql')
  cur = mydb.cursor()
  cur.execute('SELECT * FROM addmissionForm')
  applicantData = cur.fetchall()
  if not applicantData:
    return render_template("noCurrentApplication.html")
  cur.close()    
  return render_template('displayApplicantsData.html', applicantData=applicantData)

@app.route('/viewTranscripts', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def dir_listing(req_path):
    transcript_dir = 'static/transcripts'

    # Joining the base and the requested path
    f = os.path.join(transcript_dir, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(f):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(f):
        return send_file(f)

    # Show directory contents
    trancript = os.listdir(f)
    mydb = sqlite3.connect('database.sql')
    cur = mydb.cursor()
    cur.execute('SELECT * FROM addmissionForm')
    transcript = cur.fetchall()
    if not transcript:
      return render_template("notAvailableMsg.html")
    cur = mydb.cursor()
    cur.execute('SELECT * FROM addmissionForm')
    applicantInfoForTranscript = cur.fetchall()  
    return render_template('viewTranscript.html', trancript=trancript, applicantInfoForTranscript=applicantInfoForTranscript)
@app.route('/viewRecommendationLeteter', defaults={'req_path':''})
@app.route('/<path:req_path>')
def rec_dirListing(req_path):
    recommendation_dir = 'static/RecommendationLetters'
    # Joining the base and the requested path
    f = os.path.join(recommendation_dir, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(f):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(f):
        return send_file(f)

    # Show directory contents
    recommendationLetter = os.listdir(f)
    # if not recommendationLetter:
    #   return render_template("notAvailableMsg.html")
    mydb = sqlite3.connect('database.sql')
    cur = mydb.cursor()
    cur.execute('SELECT * FROM addmissionForm')
    recLetter = cur.fetchall()
    if not recLetter:
      return render_template("notAvailableMsg.html") 
    cur = mydb.cursor()
    cur.execute('SELECT * FROM addmissionForm')
    applicantInfoForRecommendationLatter = cur.fetchall()  
    return render_template('/viewRecommendationLetter.html', recommendationLetter=recommendationLetter, applicantInfoForRecommendationLatter=applicantInfoForRecommendationLatter)
@app.route('/facultyReview', methods=['GET', 'POST'])
def facultyReview():
  if request.method == 'POST':
    fname = request.form['fname']
    lname = request.form['lname']
    semester = request.form['semester']
    program = request.form['program']
    GreVerbalScore = request.form['GreVerbalScore']
    greQuantitative = request.form['greQuantitative']
    yearOfExam = request.form['yearOfExam']
    priorDegreeStatus = request.form['priorDegreeStatus']
    BSorBA_GPA = request.form['BSorBA_GPA']
    major = request.form['major']
    graduationYear = request.form['graduationYear']
    university = request.form['university']
    areaOfInterest = request.form['areaOfInterest']
    experiance = request.form['experiance']
    rec1Rating = request.form['rec1Rating']
    rec1Quality = request.form['rec1Quality']
    rec1Institution = request.form['rec1Institution']
    recommendedAdvisor = request.form['recommendedAdvisor']
    mydb = sqlite3.connect('database.sql')
    cur = mydb.cursor()
    cur.execute('INSERT INTO reviewForm(fname, lname, semesterAndYear, applyingForDegree, GreVerbalScore, greQuantitative, yearOfExam, BSorBA, BSorBA_GPA, major, graduationYear, university, areaOfInterest, experiance, rec1Rating, rec1Quality, rec1Institution, recommendedAdvisor) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (fname, lname, semester, program, GreVerbalScore, greQuantitative, yearOfExam, priorDegreeStatus, BSorBA_GPA, major, graduationYear, university, areaOfInterest, experiance, rec1Rating, rec1Quality, rec1Institution, recommendedAdvisor))
    cur = mydb.commit()
    return render_template("pageAfterSentReview.html")
    cur.close()
  mydb = sqlite3.connect('database.sql')
  cur = mydb.cursor()
  cur.execute('SELECT * FROM addmissionForm')
  reviewForm = cur.fetchall()
  if not reviewForm:
    return render_template("noCurrentApplication.html")
  cur.close()
  return render_template("facultyReview.html", error="error")

@app.route('/displayFacultyReviewData', methods=['GET', 'POST'])
def displayFacultyReviewData():
  mydb = sqlite3.connect('database.sql')
  cur = mydb.cursor()
  cur.execute('SELECT * FROM reviewForm')
  facultyReviewData = cur.fetchall()
  if not facultyReviewData:
    return render_template("notAvailableMsg.html")
  cur.close()  
  return render_template("displayFacultyReviewData.html", facultyReviewData=facultyReviewData)

@app.route('/CACandChairDecision', methods=['GET', 'POST'])  
def CACandChair():
  if request.method == 'POST':
    userID = request.form['userDataDisplay']
    CACandChairDecision = request.form["CACandChairDecision"]
    yesNoOption = request.form["yesNoOption"]
    GASreviewerComments = request.form["GASreviewerComments"]
    recommendedAdvisor = request.form["recommendedAdvisor"]
    mydb = sqlite3.connect('database.sql')
    cur = mydb.cursor()
    cur.execute('INSERT INTO finalDecision(userID, CACandChairDecision, GASreviewerComments, recommendedAdvisor, aidsOffered) VALUES(?, ?, ?, ?, ?)', (userID, CACandChairDecision, GASreviewerComments, recommendedAdvisor, yesNoOption))
    cur.execute("DELETE FROM addmissionForm WHERE userID = ?", (userID,))
    cur = mydb.commit()

    #approved message
    approvedMsg = "Congratulations!, We're delighted to inform you that you have been admitted to HT College!"
    #rejected message
    rejectedMsg = "I regret to inform you that we are unable to offer you a spot at HT College."
    #aid has been offered to applicant
    aidOffered = "We're also pleased to offer you $25,0000 grant"

    #if the applicant is approved update the userTable
    if request.form["CACandChairDecision"] == "Admit Applicant":
      cur = mydb.cursor()
      cur.execute("UPDATE userTable SET approved = ?, roleNum = ? WHERE userID = ?", (approvedMsg, 1, userID))
      cur = mydb.commit()

    #if the applicant is rejected update the userTable
    if request.form["CACandChairDecision"] == "Reject Applicant":
      cur = mydb.cursor()
      cur.execute("UPDATE userTable SET approved = ?, roleNum = ? WHERE userID = ?", (rejectedMsg, 1, userID))
      cur = mydb.commit()

    #if aid is offered update the userTable
    if request.form["yesNoOption"] == "Yes":
      cur = mydb.cursor()
      cur.execute("UPDATE userTable SET aidsOffered = ?, roleNum = ? WHERE userID = ?", (aidOffered, 1, userID))
      cur = mydb.commit()

    return render_template("applicationTracker.html")
  userID = session['userID']
  mydb = sqlite3.connect('database.sql')
  cur = mydb.cursor()
  cur.execute('SELECT DISTINCT userID FROM addmissionForm')
  finalDecision = cur.fetchall()
  finalDecision=[i[0] for i in finalDecision]
  cur.close()
  if finalDecision is None:
    return render_template("applicationNotApplicable.html")

  #checking to see if there are applications to approve or deny
  if not finalDecision:
    return render_template("applicationNotApplicable.html")  
  cur.close()
  return render_template('CACandChairDecision.html', finalDecision=finalDecision)

@app.route("/viewCACandChairDecision", methods=['GET','POST'])
def viewCACandChairDecision():
  userID = session["userID"]
  mydb = sqlite3.connect('database.sql')
  cur = mydb.cursor()
  cur.execute("SELECT * FROM finalDecision")
  CACdata = cur.fetchall()
  if not CACdata:
    return render_template("notAvailableMsg.html")
  cur.close()
  return render_template("displayCAC_ChairFinalDecision.html", CACdata=CACdata)  

@app.route("/uploadRecommendation", methods=['GET', 'POST'])  
def uploadRecommendation():
  if request.method == 'POST':
    f = request.files['recommendation']
    f.save(os.path.join(app.config['UPLOAD_FOLDER_RECOMMENDER'], secure_filename(f.filename)))
    return render_template("sentRecommendationPage.html")
  return render_template("uploadRecommendation.html", error="error")

@app.route('/viewPersonalInfo', methods=['GET', 'POST'])
def studentPersonalInfo():
  userID = session['userID']
  mydb = sqlite3.connect('database.sql')
  cur = mydb.cursor()
  cur.execute('SELECT * FROM userTable WHERE userID = ?', (userID,))
  studentData = cur.fetchall()
  return render_template("studentViewPersonalInfo.html", studentData=studentData)
@app.route("/updateUserProfile", methods=['GET', 'POST'])
def updateUserProfile():
  if request.method == 'POST':
    userID = session['userID']
    firstName = request.form["firstName"]
    lastName = request.form["lastName"]
    email = request.form["email"]
    userName = request.form["username"]
    
    mydb = sqlite3.connect('database.sql')
    cur = mydb.cursor()
    cur.execute("UPDATE userTable SET fname = ?, lname = ?, email = ?, username = ? WHERE userID = ?", (firstName, lastName, email, userName, userID))
    cur = mydb.commit()
    return redirect(url_for('studentPersonalInfo'))
  return render_template("updateUserProfile.html", error="error")      

@app.route("/recommenderInfo", methods=['GET', 'POST'])
def recommenderInfo():
  mydb = sqlite3.connect('database.sql')
  cur = mydb.cursor()
  cur.execute('SELECT * FROM addmissionForm')
  recommenderData = cur.fetchall()
  if not recommenderData:
    return render_template("notAvailableMsg.html")
  return render_template("recommenderInfo.html", recommenderData=recommenderData)
  
@app.route("/forgetPassword", methods=['GET', 'POST'])
def forgetPassord():
  if request.method == 'POST':
    userID = session['userID']
    newPassword = request.form['password']

    mydb = sqlite3.connect('database.sql')
    cur = mydb.cursor()
    cur.execute('UPDATE userTable SET pass = ? WHERE userID = ?', (newPassword, userID))
    cur = mydb.commit()
    return redirect(url_for('home'))
  return render_template('forgetPassword.html')
  
@app.route("/forgetUserPass", methods=['GET', 'PASS'])
def forgetUserPass():
  if request.method == 'POST':
    email = request.form['email']
app.run(host='0.0.0.0', port=8081, debug=True)