from flask import Flask, render_template, send_from_directory, request
from flask import *
import mysql.connector
import logging
hometxt = "The CDR project is open-source solution for content disarm and reconstruction at Mailboxes.</br> The CDR works by processing all incoming e-mails in a spesific network, deconstructing them, and removing the elements that do not match the file type's standards or set policies. CDR technology then rebuilds the e-mail into clean versions that can be sent on to end users as intended"
hometitle = "Welcome to the CDR Portal"
headertxt = "CDR Portal"

cnx = mysql.connector.connect(user='root', password='Aa123456123456',
                              host='127.0.0.1',
                              database='cdr')
mycursor=cnx.cursor()
mycursor.execute('SELECT username,password FROM admin')
admin=mycursor.fetchone()
logging.warning(admin[0])


app = Flask(__name__)


@app.route('/index')
def index():
    return render_template("message.html", title=hometitle, text=hometxt, header=headertxt)


# @app.route('/testing')
# def test():
#     conn = MySQL()
#     conn.query('blabla')
#     table = ''
#     for row in conn.results():
#         table += f"<td>{row[0]}, {row[1]}</td>\n"
#
#     return render_template('test.html', data=table)
@app.route('/logout',methods=('GET', 'POST'))
def logout():
    return render_template('logout.html')


@app.route('/',methods=('GET', 'POST'))
def root():
    if request.method == 'POST':
        username, password = request.form['username'], request.form['password']
        logging.warning(username +" " + password)
        if username == admin[0] and password == admin[1]:
            return render_template("message.html", title=hometitle, text=hometxt, header=headertxt)
        else:
            error="Wrong username or password."
            return render_template('login.html', error=error)
    # return send_from_directory('static', 'login.html')
    return render_template('login.html')


# @app.route('/mailboxeditform' ,methods=('GET','POST'))
# def mailboxeditform():
#     id = request.form['check']
#     logging.warning(id)
#     return render_template('mailboxeditform.html')


@app.route('/mailboxedit',methods=('GET','POST'))
def mailboxedit():
    if request.method=='GET':
        mycursor.execute('SELECT * FROM mailbox')
        data = mycursor.fetchall()
        return render_template('mailboxedit.html', title="CDR-Edit Mailbox", data=data)
    else:
        mailid = request.form['check']
        logging.warning(mailid)
        mycursor.execute('SELECT * FROM mailbox where Id='+mailid)
        data = mycursor.fetchone()
        return render_template('mailboxeditform.html', data=data , title='CDR-Edit Mailbox')

@app.route('/mailboxeditform',methods=('GET','POST'))
def mailboxeditform():
    if request.method =='POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        role = request.form['role']
        mailboxname = request.form['mailboxname']
        mailboxid = request.form['id']
        exestr = "UPDATE cdr.mailbox SET FirstName ='" + firstname +"', LastName = '" + lastname +"', MailBoxName = '" + mailboxname +"' , Role = '" + role +"' WHERE(ID = '" + mailboxid + "');"
        try:
            mycursor.execute(exestr)
            cnx.commit()
            return render_template('message.html', title="Mailbox edit", text='Change successful')
        except:
            return render_template('message.html', title="Mailbox edit", text='An Error occurred')

@app.route('/policyall',methods=('GET','POST'))
def policyall():
    if request.method=='GET':
        return render_template('policyall.html', title='עריכת מדיניות כללית')
    if request.method =='POST':
        policy = request.form['check']
        exestr = "UPDATE cdr.mailbox SET PolicyID = '"+policy +"';"
        try:
            mycursor.execute(exestr)
            cnx.commit()
            return render_template('message.html', title ="שינוי פוליסה כללית", text = 'השינוי התבצע בהצלחה')
        except:
            return render_template('message.html',title ="שינוי פוליסה כללית", text='ארעה שגיאה')


@app.route('/policyone', methods=('GET', 'POST'))
def policyone():
    if request.method == 'GET':
        mycursor.execute('SELECT * FROM mailbox')
        data = mycursor.fetchall()
        return render_template('policyone.html', title='עריכת מדיניות לתיבה', data=data)
    else:
        mailid = request.form['check']
        return render_template('policyoneform.html', id=mailid, title="בחר בפוליסה הרצויה:")

@app.route('/policyoneform', methods=('GET', 'POST'))
def policyoneform():
    if request.method =='POST':
        policy = request.form['check']
        mailboxid = request.form['id']
        exestr = "UPDATE cdr.mailbox SET PolicyID = '"+policy + "' WHERE ID ='" + mailboxid + "';"
        try:
            mycursor.execute(exestr)
            cnx.commit()
            return render_template('message.html', title ="שינוי פוליסה", text = 'השינוי התבצע בהצלחה')
        except:
            return render_template('message.html',title ="שינוי פוליסה", text='ארעה שגיאה')


if __name__ == '__main__':
    app.run()

cnx.close()