import logging
import mysql.connector
from flask import *

home_txt = "The CDR project is open-source solution for content disarm and reconstruction at Mailboxes.</br> The CDR " \
           "works by processing all incoming e-mails in a specific network, deconstructing them, and removing the " \
           "elements that do not match the file type's standards or set policies. CDR technology then rebuilds the " \
           "e-mail into clean versions that can be sent on to end users as intended "
home_title = "Welcome to the CDR Portal"
header_txt = "CDR Portal"

cnx = mysql.connector.connect(user='root', password='Aa123456123456',
                              host='127.0.0.1',
                              database='cdr')
my_cursor = cnx.cursor()
my_cursor.execute('SELECT username,password FROM admin')
admin = my_cursor.fetchone()


app = Flask(__name__)


@app.route('/index')
def index():
    return render_template("message.html", title=home_title, text=home_txt, header=header_txt)


@app.route('/logout', methods=('GET', 'POST'))
def logout():
    return render_template('logout.html')


@app.route('/', methods=('GET', 'POST'))
def root():
    if request.method == 'POST':
        username, password = request.form['username'], request.form['password']
        logging.warning(username + " " + password)
        if username == admin[0] and password == admin[1]:
            return render_template("message.html", title=home_title, text=home_txt, header=header_txt)
        else:
            error = "Wrong username or password."
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/mailbox_edit', methods=('GET', 'POST'))
def mailbox_edit():
    if request.method == 'GET':
        my_cursor.execute('SELECT * FROM mailbox')
        data = my_cursor.fetchall()
        return render_template('mailbox_edit.html', title="CDR-Edit Mailbox", data=data)
    else:
        mail_id = request.form['check']
        logging.warning(mail_id)
        my_cursor.execute('SELECT * FROM mailbox where Id=' + mail_id)
        data = my_cursor.fetchone()
        return render_template('mailbox_edit_form.html', data=data, title='CDR-Edit Mailbox')


@app.route('/mailbox_edit_form', methods=('GET', 'POST'))
def mailbox_edit_form():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        role = request.form['role']
        mailbox_name = request.form['mailbox_name']
        mailbox_id = request.form['id']
        exe_str = "UPDATE cdr.mailbox SET FirstName ='" + firstname + \
                  "', LastName = '" + lastname + "', MailBoxName = '" + mailbox_name + "' , Role = '" + \
                  role + "' WHERE(ID = '" + mailbox_id + "');"
        try:
            my_cursor.execute(exe_str)
            cnx.commit()
            return render_template('message.html', title="Mailbox edit", text='Change successful')
        except:
            return render_template('message.html', title="Mailbox edit", text='An Error occurred')


@app.route('/policy_all', methods=('GET', 'POST'))
def policy_all():
    if request.method == 'GET':
        my_cursor.execute('SELECT * FROM policy')
        data = my_cursor.fetchall()
        return render_template('policy_all.html', title='General policy edit', data=data)
    if request.method == 'POST':
        policy = request.form['check']
        exe_str = "UPDATE cdr.mailbox SET PolicyID = '" + policy + "';"
        try:
            my_cursor.execute(exe_str)
            cnx.commit()
            return render_template('message.html', title="General Policy Edit", text='Changed Successful')
        except:
            return render_template('message.html', title="General Policy Edit", text='Error occurred')


@app.route('/policy_one', methods=('GET', 'POST'))
def policy_one():
    if request.method == 'GET':
        my_cursor.execute('SELECT * FROM mailbox')
        data = my_cursor.fetchall()
        return render_template('policy_one.html', title='Edit mailbox policy', data=data)
    else:
        mail_id = request.form['check']
        return render_template('policy_one_form.html', id=mail_id, title="Choose wanted policy")


@app.route('/policy_one_form', methods=('GET', 'POST'))
def policy_one_form():
    if request.method == 'POST':
        policy = request.form['check']
        mailbox_id = request.form['id']
        exe_str = "UPDATE cdr.mailbox SET PolicyID = '" + policy + "' WHERE ID ='" + mailbox_id + "';"
        try:
            my_cursor.execute(exe_str)
            cnx.commit()
            return render_template('message.html', title="Policy Edit", text='Change Successful')
        except:
            return render_template('message.html', title="Policy Edit", text='Error occurred')


if __name__ == '__main__':
    app.run()

cnx.close()
