from flask import Flask
from flask import render_template
from flask import request
from werkzeug.security import generate_password_hash, \
     check_password_hash
import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
from flask import send_from_directory
import mysql.connector
from flask import Flask, session
from flask.sessions import SessionInterface
from flask import jsonify
import json
import urllib
import smtplib

server = smtplib.SMTP('smtp.gmail.com', 587)

server.starttls()
server.ehlo()
server.login('jonathano1367@gmail.com','jonjon921')
server.ehlo()
#smtpObj = smtplib.SMTP( [ [, 8889 [, local_hostname]]] )
# import smtplib

#sender = ""
#receivers = ""

#message form form 

#smt.pOBJ = smtplib.SMTP('localhost')
#smt.pOBJ = sendmail(sender,,recivers,message)



app = Flask(__name__)
app.secret_key = 'jon'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

# def allowed_file(filename):
#     return '.' in filename and \
#     	filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
#addform
#adduser


@app.route('/')
def index():
    
    db =  mysql.connector.connect(host='localhost',port='8889',database='ssl',user='root',password='root')
    cur = db.cursor()
    cur.execute('select id ,username , password from users')
    data = cur.fetchall()
    return render_template('header.html',data=data) + render_template('body.html',data=data) 
@app.route('/jsonout')
def jsonout():
    
    db =  mysql.connector.connect(host='localhost',port='8889',database='ssl',user='root',password='root')
    cur = db.cursor()
    cur.execute('select id ,username , password from users')
    data = cur.fetchall()

    #data = {"test":"hello"}
    return jsonify({"users":data})


@app.route('/getjson')
def getjson():

    # db =  mysql.connector.connect(host='localhost',port='8889',database='ssl',user='root',password='root')
    # cur = db.cursor()
    # cur.execute('select id ,username , password from users')
    # data = cur.fetchall()

    # url = "http://maps.googleapis.com/maps/api/geocode/json?address=orlando,%20FL"
    # loadurl = urllib.urlopen(url) # python verson of file get contents
    # data = json.loads(loadurl.read().decode(loadurl.info().getparam('charset') or 'utf-8'))
    # #item = data["results"][0]["formatted_address"]
    # item = data["results"][0]["address_components"][1]["long_name"]
    # return item


    #google key : AIzaSyC0iY_V_7CCDAZdbKYso2yRjjR3yJ5QYFM
    #https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-33.8670522,151.1957362&radius=500&types=food&name=cruise&key=AIzaSyC0iY_V_7CCDAZdbKYso2yRjjR3yJ5QYFM
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-33.8670522,151.1957362&radius=500&types=food&name=cruise&key=AIzaSyC0iY_V_7CCDAZdbKYso2yRjjR3yJ5QYFM"
    loadurl = urllib.urlopen(url) # python verson of file get contents
    data = json.loads(loadurl.read().decode(loadurl.info().getparam('charset') or 'utf-8'))
    #item = data["results"][0]["formatted_address"]
    #item = data["data"]
    print '--------------- Data --------------------'
    results =  data['results']
    return str(results)
   
    #data = {"test":"hello"}
    return jsonify({"users":data})


@app.route('/loginForm')	
def loginForm():
	return render_template('header.html') + render_template('/loginForm.html')

@app.route('/updateUser/<id>', methods=['GET','POST'])
def updateUser(id):
    id = id
    username = request.form["username"]
    print username
    db =  mysql.connector.connect(host='localhost',port='8889',database='ssl',user='root',password='root')
    cur = db.cursor()
    cur.execute("update users set username = %s where id = %s",(username,id,))
    db.commit()
    return redirect('/')

    return render_template('/loginForm.html')

@app.route('/addForm')
def addForm():
    return render_template('header.html') + render_template('/addForm.html')

@app.route('/addUser', methods=['GET','POST'])
def addUser():
    username = request.form["username"]
    password = request.form["password"]
    db =  mysql.connector.connect(host='localhost',port='8889',database='ssl',user='root',password='root')
    cur = db.cursor()
    cur.execute("insert into users(username,password)values(%s,%s)",(username,password,))
    #data = cur.fetchall()
    db.commit()
    return redirect('/')


@app.route('/editForm/<id>', methods=['GET','POST'])
def editForm(id):
    id = id
    db =  mysql.connector.connect(host='localhost',port='8889',database='ssl',user='root',password='root')
    cur = db.cursor()
    cur.execute("select id,username,password from users where id=%s",(id,))
    data = cur.fetchall()
    return render_template('editForm.html',data=data)
@app.route('/deleteUser/<id>', methods=['GET','POST'])
def deleteUser(id):
    id = id
    db =  mysql.connector.connect(host='localhost',port='8889',database='ssl',user='root',password='root')
    cur = db.cursor()
    cur.execute("delete from users where id=%s",(id,))
    #data = cur.fetchall()
    db.commit()
    return redirect('/') 

@app.route('/profile/', methods=['GET','POST'])
def profile():
    if session["login"] == True:

        return render_template('header.html') + render_template('/profile.html')
    else:
        return redirect('/') 
    

@app.route('/logOut', methods=['GET','POST'])
def logOut():
    #turn seesion off
    session["login"] = False
    return redirect('/') 
@app.route('/locationForm', methods=['GET','POST'])
def locationForm():
    #turn seesion off
    
    return render_template('/locationForm.html')

@app.route('/processForm', methods=['GET','POST'])
def processForm():

    username = request.form['username']
    password = request.form['password']
    db =  mysql.connector.connect(host='localhost',port='8889',database='ssl',user='root',password='root')
    cur = db.cursor()
    cur.execute("select username from users where (username = %s) and (password = %s)",(username,password,))
    data = cur.fetchall()
    #db.commit()
    print data
    session["login"] = True


    # 
    # return data
    #session part
    #request.form["username"]
   

    
    return render_template('header.html') + render_template('/profile.html',data=data)
    # data = []
    # sha1 = hashlib.sha1()
    # sha1.update(request.form["firstname"])
    # data.append(sha1.hexdigest())
    # return render_template('body.html',data=data)



    #data=[]
    # data.append(userid)
    # data.append(request.form["firstname"])
    # return render_template('body.html',data=data)
    # if request.method == 'POST':
    #     file = request.files['file']
    #     if file and allowed_file(file.filename):
    #         filename = secure_filename(file.filename)
    #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #         return redirect(url_for('uploaded_file',filename=filename))
    # 	#return render_template('form.html' , request.form["firstname"])
	
	#return request.form["firstname"] + "\n" + generate_password_hash(request.form["password"]);


@app.route('/sendEmail', methods=['GET','POST'])
def sendEmail():
    return render_template('/header.html') + render_template('/emailForm.html')
@app.route('/processEmail', methods=['GET','POST'])
def processEmail():
    sender = request.form["sender"]
    receiver = request.form["receiver"]
    message = request.form["message"]

    print sender
    print receiver
    print message

    server.sendmail(receiver,sender, message)

    server.quit()

    return render_template('/header.html') + render_template('/emailForm.html')


if __name__ == '__main__':
	app.run(debug=True)



