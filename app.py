from flask import Flask, render_template, request, redirect,url_for,session, jsonify
from flask_mysqldb import MySQL
from flask_mail import *
import yaml
import random
app = Flask(__name__)

# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config["MAIL_SERVER"]='smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'associateskilldirectory@gmail.com'
app.config['MAIL_PASSWORD'] = '06794222165'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mysql = MySQL(app)
mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    msg = ''
    if request.method == 'POST':
        userDetails = request.form
        global ID
        global searchFlag
        global roadmapFlag
        global BuildTeamFlag
        ID = userDetails['ID']
        password = userDetails['pass']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT designation FROM associate_details WHERE ID = %s',[ID])
        temp = cursor.fetchall()[0][0]
        if temp == "HR":
            searchFlag = ""
            roadmapFlag = "hidden"
            BuildTeamFlag = ""
        if temp == "Associate":
            searchFlag = ""
            roadmapFlag = ""
            BuildTeamFlag = "hidden"
        if temp == "Engineer":
            searchFlag = ""
            roadmapFlag = ""
            BuildTeamFlag = "hidden"
        if temp == "Business Analyst":
            searchFlag = ""
            roadmapFlag = ""
            BuildTeamFlag = ""
        if temp == "Manager":
            searchFlag = ""
            roadmapFlag = "hidden"
            BuildTeamFlag = ""
        if temp == "admin":
            searchFlag = ""
            roadmapFlag = ""
            BuildTeamFlag = ""
        account = cursor.execute('SELECT * FROM authentation WHERE ID = % s AND password = % s', (ID, password))
        if account > 0:
            return render_template('dashboard.html', searchFlag = searchFlag, roadmapFlag = roadmapFlag, buildTeamFlag = BuildTeamFlag)
        else:
            msg = 'Incorrect username / password !'
    return render_template('index.html', msg = msg)

@app.route('/registration',methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        registerDetails = request.form
        name = registerDetails['name']
        birthday = registerDetails['birthday']
        designation = registerDetails['designation']
        email = registerDetails['email']
        phone = registerDetails['phone']
        password = registerDetails['password']
        repassword = registerDetails['repassword']
        country = registerDetails['country']
        team = registerDetails['team']
        experience = registerDetails['experience']
        skills = registerDetails.getlist('skills')
        id = random.randint(1,100000)
        if password != repassword:
            return render_template('index.html')
        cur = mysql.connection.cursor()
        for i in skills:
            cur.execute('SELECT * FROM skills_details WHERE skill_Name= %s',[i.lower()])
            skill_id = cur.fetchone()[0]
            cur.execute('INSERT INTO skills(ID,skills_id) VALUES(%s,%s)',(id,skill_id))
        cur.execute('INSERT INTO associate_details(ID, Name, DOB, email, designation, mobile,country, team, experience) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)',(id, name, birthday, email, designation, phone,country, team, experience))
        cur.execute('INSERT INTO authentation(ID, password) VALUES(%s, %s)',(id, password))
        mysql.connection.commit()
        cur.close()
        sendMail(email, id)

    return render_template('registration.html')
def sendMail(email, id):
    msg = Message('ASSOCIATE SKILL DIRECTORY',sender = 'username@gmail.com', recipients = [email])
    msg.html = "<h4>Hi, thank you for signing up with Associate skill directory. Please use the below given id for logging into you account.</h4><br>ID: "+"\n" + str(id)
    mail.send(msg)

@app.route('/aboutUs', methods=['GET', 'POST'])
def aboutUs():
    print(searchFlag)
    print(BuildTeamFlag)
    print(roadmapFlag)
    return render_template('aboutUs.html', searchFlag = searchFlag, roadmapFlag = roadmapFlag, buildTeamFlag = BuildTeamFlag)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        teamDetails = request.form
        team = teamDetails['team']
        designation = teamDetails['designation']
        country = teamDetails['country']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM associate_details WHERE team=%s AND designation=%s AND country=%s',([team],[designation],[country]))
        associates1 = cursor.fetchall()
        cursor.execute('SELECT team FROM associate_details')
        teams = cursor.fetchall()
        cursor.execute('SELECT designation FROM associate_details')
        designations = cursor.fetchall()
        cursor.execute('SELECT country FROM associate_details')
        countries = cursor.fetchall()
        filter = set()
        for i in teams:
            filter.add(i[0])
        filter1 = set()
        for i in designations:
            filter1.add(i[0])
        filter2 = set()
        for i in countries:
            filter2.add(i[0])
        return render_template('search.html',associates1 = associates1, teams = filter, designations= filter1, countries= filter2, searchFlag = searchFlag, roadmapFlag = roadmapFlag, buildTeamFlag = BuildTeamFlag)
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT team FROM associate_details')
    teams = cursor.fetchall()
    cursor.execute('SELECT designation FROM associate_details')
    designations = cursor.fetchall()
    cursor.execute('SELECT country FROM associate_details')
    countries = cursor.fetchall()
    filter = set()
    for i in teams:
        filter.add(i[0])
    filter1 = set()
    for i in designations:
        filter1.add(i[0])
    filter2 = set()
    for i in countries:
        filter2.add(i[0])
    return render_template('search.html', teams=filter, designations= filter1, countries= filter2, searchFlag = searchFlag, roadmapFlag = roadmapFlag, buildTeamFlag = BuildTeamFlag)

@app.route('/profile' ,methods=['GET', 'POST'])
def profile():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM associate_details WHERE ID= %s', [ID])
    details_emp = cursor.fetchall()[0]
    cursor.execute('SELECT * FROM skills WHERE ID= %s', [ID])
    skillid = cursor.fetchall()
    skillss = []
    for i in range(len(skillid)):
        record = []
        k = skillid[i][1]
        record.append(skillid[i][2])
        cursor.execute('SELECT * FROM skills_details WHERE skill_ID= %s', [k])
        record.append(cursor.fetchone())
        skillss.append(record)
    to_send = details_emp
    return render_template('profile.html', to_send = to_send, skillss=skillss, searchFlag = searchFlag, roadmapFlag = roadmapFlag, buildTeamFlag = BuildTeamFlag)

@app.route('/roadmap', methods=['GET', 'POST'])
def roadmap():
    if request.method == 'POST':
        formDetails = request.form
        roadmap = formDetails['roadmap']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM skills WHERE ID= %s',[ID])
        skillDetails = cursor.fetchall()
        skills1 = []
        aquiredSkills=[]
        remainingTime = 0
        for i in skillDetails:
            cursor.execute('SELECT * FROM skills_details WHERE skill_ID= %s', [str(i[1])])
            temp = cursor.fetchone()
            skills1.append(temp[1])
        cursor.execute('SELECT * FROM roadmap WHERE profile LIKE %s', [roadmap])
        roadmapdetails = cursor.fetchone()
        progress = 0
        if roadmapdetails[0] == 'AWS Roadmap':
            remainingTime = 8
            for i in skills1:
                if i.startswith("AWS"):
                    if i.endswith("Foundation"):
                        progress+=25
                        remainingTime-=1
                        skillPair = []
                        skillPair.append(1)
                        skillPair.append(i)
                        aquiredSkills.append(skillPair)
                    if i.endswith("Associate"):
                        progress+=25
                        remainingTime-=2
                        skillPair = []
                        skillPair.append(2)
                        skillPair.append(i)
                        aquiredSkills.append(skillPair)
                    if i.endswith("Professional"):
                        progress+=25
                        remainingTime-=2
                        skillPair = []
                        skillPair.append(2)
                        skillPair.append(i)
                        aquiredSkills.append(skillPair)
                    if i.endswith("Specility"):
                        remainingTime-=3
                        progress+=25
                        skillPair = []
                        skillPair.append(3)
                        skillPair.append(i)
                        aquiredSkills.append(skillPair)
        if roadmapdetails[0] == 'Azure Roadmap':
            remainingTime = 8
            for i in skills1:
                if i.startswith("Azure"):
                    if i.endswith("Fundamentals"):
                        progress+=25
                        remainingTime-=1
                        skillPair = []
                        skillPair.append(1)
                        skillPair.append(i)
                        aquiredSkills.append(skillPair)   
                    if i.endswith("Admin"):
                        progress+=25
                        remainingTime-=2
                        skillPair = []
                        skillPair.append(2)
                        skillPair.append(i)
                        aquiredSkills.append(skillPair)
                    if i.endswith("developer"):
                        progress+=25
                        remainingTime-=2
                        skillPair = []
                        skillPair.append(2)
                        skillPair.append(i)
                        aquiredSkills.append(skillPair)
                    if i.endswith("Architect"):
                        progress+=25
                        remainingTime-=3
                        skillPair = []
                        skillPair.append(3)
                        skillPair.append(i)
                        aquiredSkills.append(skillPair)
        if roadmapdetails[0] == 'Devops Engineer':
            remainingTime = 5
            for i in skills1:
                if i == "python":
                    progress+=20
                    remainingTime-=0.5
                    skillPair = []
                    skillPair.append(0.5)
                    skillPair.append(i)
                    aquiredSkills.append(skillPair)
                if i == "cloud":
                    progress+=20
                    remainingTime-=1.5
                    skillPair = []
                    skillPair.append(1.5)
                    skillPair.append(i)
                    aquiredSkills.append(skillPair)
                if i == "linux":
                    progress+=10
                    remainingTime-=0.5
                    skillPair = []
                    skillPair.append(0.5)
                    skillPair.append(i)
                    aquiredSkills.append(skillPair)
                if i == "shell":
                    progress+=10
                    remainingTime-=0.5
                    aquiredSkills.append(i)
                if i == "Containers":
                    progress+=20
                    remainingTime-=1
                    skillPair = []
                    skillPair.append(1)
                    skillPair.append(i)
                    aquiredSkills.append(skillPair)
                if i == "Kubernetes":
                    progress+=20
                    remainingTime-=1
                    skillPair = []
                    skillPair.append(1)
                    skillPair.append(i)
                    aquiredSkills.append(skillPair)
        roadmapData = []
        print(roadmapdetails)
        for i in range(1,len(roadmapdetails)-1):
            if roadmapdetails[i] is not None:
                if roadmapdetails[i] == "programming":
                    temp1 = []
                    temp1.append(0.5)
                if roadmapdetails[i] == "administration":
                    temp1 = []
                    temp1.append(1)
                if roadmapdetails[i] == "cloud management":
                    temp1 = []
                    temp1.append(1.5)
                if roadmapdetails[i] == "containers":
                    temp1 = []
                    temp1.append(1)
                if roadmapdetails[i] == "orchestration":
                    temp1 = []
                    temp1.append(1)
                if roadmapdetails[i] == "Fundamentals":
                    temp1 = []
                    temp1.append(1)
                if roadmapdetails[i] == "administrator(Associate)":
                    temp1 = []
                    temp1.append(2)
                if roadmapdetails[i] == "Developer(Associate)":
                    temp1 = []
                    temp1.append(2)
                if roadmapdetails[i] == "Solution Architect(Expert)":
                    temp1 = []
                    temp1.append(3)
                if roadmapdetails[i] == "Foundational":
                    temp1 = []
                    temp1.append(1)
                if roadmapdetails[i] == "Associate":
                    temp1 = []
                    temp1.append(2)
                if roadmapdetails[i] == "Professional":
                    temp1 = []
                    temp1.append(2)
                if roadmapdetails[i] == "Specility":
                    temp1 = []
                    temp1.append(3)
                temp1.append(roadmapdetails[i])
                roadmapData.append(temp1)
        duration = roadmapdetails[len(roadmapdetails)-1]
        return render_template('roadmap.html', roadmapdetails=roadmapData, skills1=aquiredSkills, progress=progress, duration = duration, remainingTime=remainingTime, searchFlag = searchFlag, roadmapFlag = roadmapFlag, buildTeamFlag = BuildTeamFlag)
    return render_template('roadmap.html', searchFlag = searchFlag, roadmapFlag = roadmapFlag, buildTeamFlag = BuildTeamFlag)
@app.route('/teamBuild' ,methods=['GET', 'POST'])
def teamBuild():
    if request.method == 'POST':
        formDetails = request.form
        cur = mysql.connection.cursor()
        associates = []
        projectName = ""
        if formDetails['search'] == 'search':
            projectDetails = request.form
            projectName = projectDetails['projectName']
            skills = projectDetails.getlist('skills')
            for i in skills:
                cur.execute('SELECT * FROM skills_details WHERE skill_Name= %s',[i.lower()])
                temp = cur.fetchone()
                cur.execute('SELECT * FROM skills WHERE skills_ID= %s',[temp[0]])
                skills_associates = cur.fetchall()
                for j in skills_associates:
                    cur.execute('SELECT * FROM associate_details WHERE ID= %s',[j[0]])
                    associates_list = list(cur.fetchone())
                    associates_list.append(i.lower())
                    associates.append(associates_list)
        cur.execute('SELECT id FROM associate_details')
        details12 = cur.fetchall()
        selectedAssociates = []
        if formDetails['search'] == 'getDetails':
            for i in details12:
                try:
                    selectedAssociates.append(formDetails[str(i[0])])
                except:
                    print("not valid")
            message1 = "<h4>Hi, <br>Your Requested List of associates and their details.</h4><br><ul>"
            for i in selectedAssociates:
                cur.execute('SELECT * FROM associate_details WHERE ID=%s',[i])
                message1 += "<li>"
                for j in cur.fetchone():
                    message1 += str(j) + " "
                message1 += "</li>"
                message1 += "</ul>"
            cur.execute('SELECT email FROM associate_details WHERE ID=%s',[ID])
            email = str(cur.fetchone()[0])
            print(email)
            msg = Message('ASSOCIATE SKILL DIRECTORY',sender = 'username@gmail.com', recipients = [email])
            msg.html = message1
            mail.send(msg)
        return render_template('teamBuild.html', associates = associates, projectName = projectName, searchFlag = searchFlag, roadmapFlag = roadmapFlag, buildTeamFlag = BuildTeamFlag)
    return render_template('teamBuild.html', searchFlag = searchFlag, roadmapFlag = roadmapFlag, buildTeamFlag = BuildTeamFlag)

@app.route('/editprofile' ,methods=['GET', 'POST'])
def editprofile():
    if request.method == 'POST':
        registerDetails = request.form
        name = registerDetails['name']
        birthday = registerDetails['DOB']
        email = registerDetails['email']
        phone = registerDetails['phone']
        country = registerDetails['country']
        team = registerDetails['team']
        experience = registerDetails['experience']
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE  associate_details SET Name= %s WHERE ID= %s',([name],[ID]))
        cursor.execute('UPDATE  associate_details SET DOB=%s WHERE ID= %s',([birthday],[ID]))
        cursor.execute('UPDATE  associate_details SET email=%s WHERE ID= %s',([email],[ID]))
        cursor.execute('UPDATE  associate_details SET mobile=%s WHERE ID= %s',([phone],[ID]))
        cursor.execute('UPDATE  associate_details SET country=%s WHERE ID= %s',([country],[ID]))
        cursor.execute('UPDATE  associate_details SET team=%s WHERE ID= %s',([team],[ID]))
        cursor.execute('UPDATE  associate_details SET experience=%s WHERE ID= %s',([experience],[ID]))
        mysql.connection.commit()

        cursor.execute('SELECT * FROM associate_details WHERE ID= %s', [ID])
        details_emp = cursor.fetchall()[0]
        cursor.execute('SELECT * FROM skills WHERE ID= %s', [ID])
        skillid = cursor.fetchall()
        skillss = []
        for i in range(len(skillid)):
            record = []
            k = skillid[i][1]
            record.append(skillid[i][2])
            cursor.execute('SELECT * FROM skills_details WHERE skill_ID= %s', [k])
            record.append(cursor.fetchone())
            skillss.append(record)
        to_send = details_emp
        return render_template('profile.html', to_send = to_send, skillss=skillss, searchFlag = searchFlag, roadmapFlag = roadmapFlag, buildTeamFlag = BuildTeamFlag)

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM associate_details WHERE ID= %s', [ID])
    details_emp = cursor.fetchall()[0]
    cursor.execute('SELECT * FROM skills WHERE ID= %s', [ID])
    skillid = cursor.fetchall()
    skillss = []
    for i in range(len(skillid)):
        record = []
        k = skillid[i][1]
        record.append(skillid[i][2])
        cursor.execute('SELECT * FROM skills_details WHERE skill_ID= %s', [k])
        record.append(cursor.fetchone())
        skillss.append(record)
    to_send = details_emp
    return render_template('editprofile.html', to_send = to_send, skillss=skillss, searchFlag = searchFlag, roadmapFlag = roadmapFlag, buildTeamFlag = BuildTeamFlag)

@app.route('/addcertifications' ,methods=['GET', 'POST'])
def addcertifications():
    if request.method == 'POST':
        certificationDetails = request.form
        cursor = mysql.connection.cursor()  
        cursor.execute('SELECT * FROM skills WHERE ID= %s', [ID])
        skillid = cursor.fetchall()
        for i in range(len(skillid)):
            k = skillid[i][1]
            cursor.execute('SELECT * FROM skills_details WHERE skill_ID= %s', [k])
            skill_name = cursor.fetchone()[1]
            cursor.execute('UPDATE  skills SET certification= %s WHERE skills_id= %s AND ID=%s',(certificationDetails[skill_name],[k],[ID]))
            mysql.connection.commit()
        
        cursor.execute('SELECT * FROM associate_details WHERE ID= %s', [ID])
        details_emp = cursor.fetchall()[0]
        cursor.execute('SELECT * FROM skills WHERE ID= %s', [ID])
        skillid = cursor.fetchall()
        skillss = []
        for i in range(len(skillid)):
            record = []
            k = skillid[i][1]
            record.append(skillid[i][2])
            cursor.execute('SELECT * FROM skills_details WHERE skill_ID= %s', [k])
            record.append(cursor.fetchone())
            skillss.append(record)
        to_send = details_emp
        return render_template('profile.html', to_send = to_send, skillss=skillss, searchFlag = searchFlag, roadmapFlag = roadmapFlag, buildTeamFlag = BuildTeamFlag)
        
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM associate_details WHERE ID= %s', [ID])
    details_emp = cursor.fetchall()[0]
    cursor.execute('SELECT * FROM skills WHERE ID= %s', [ID])
    skillid = cursor.fetchall()
    skillss = []
    for i in range(len(skillid)):
        record = []
        k = skillid[i][1]
        if skillid[i][2] is None:
            record.append("")
        else:
            record.append(skillid[i][2]) 
        cursor.execute('SELECT * FROM skills_details WHERE skill_ID= %s', [k])
        record.append(cursor.fetchone())
        skillss.append(record)
    to_send = details_emp
    return render_template('addcertifications.html', to_send = to_send, skillss=skillss, searchFlag = searchFlag, roadmapFlag = roadmapFlag, buildTeamFlag = BuildTeamFlag)


if __name__ == '__main__':
    app.run(debug=True)

