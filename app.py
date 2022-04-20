import logging
import db
from flask import *

db = db.DB()
home_txt = "The CDR project is open-source solution for content disarm and reconstruction at Mailboxes.</br> The CDR " \
           "works by processing all incoming e-mails in a specific network, deconstructing them, and removing the " \
           "elements that do not match the file type's standards or set policies. CDR technology then rebuilds the " \
           "e-mail into clean versions that can be sent on to end users as intended "
home_title = "Welcome to the CDR Portal"
header_txt = "CDR Portal"
policy_list = db.fetch_policies()

app = Flask(__name__)


def login_check():
    return db.is_logged_in


@app.route('/index')
def index():
    return render_template("message.html", title=home_title, text=home_txt, header=header_txt)


@app.route('/logout', methods=('GET', 'POST'))
def logout():
    db.is_logged_in = False
    return render_template('logout.html')


@app.route('/', methods=('GET', 'POST'))
def root():
    if request.method == 'POST':
        username, password = request.form['username'], request.form['password']
        if db.login(username, password):
            return render_template("message.html", title=home_title, text=home_txt, header=header_txt)
        else:
            error = "Wrong username or password."
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/mailbox_edit', methods=('GET', 'POST'))
def mailbox_edit():
    if not login_check():
        return redirect('/')
    if request.method == 'GET':
        data = db.fetch_mailboxes()
        return render_template('mailbox_edit.html', title="CDR-Edit Mailbox", data=data, policy_list=policy_list)
    else:
        mail_id = request.form['check']
        data = db.fetch_mailbox_data(mail_id)
        return render_template('mailbox_edit_form.html', data=data, title='CDR-Edit Mailbox')


@app.route('/mailbox_edit_form', methods=('GET', 'POST'))
def mailbox_edit_form():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        role = request.form['role']
        mailbox_name = request.form['mailbox_name']
        mailbox_id = request.form['id']
        try:
            db.update_mailbox_info(mailbox_id, firstname, lastname, mailbox_name, role)
            return render_template('message.html', title="Mailbox edit", text='Change successful')
        except:
            return render_template('message.html', title="Mailbox edit", text='An Error occurred')


@app.route('/policy_all', methods=('GET', 'POST'))
def policy_all():
    if not login_check():
        return redirect('/')
    if request.method == 'GET':
        return render_template('policy_all.html', title='General policy edit', data=policy_list)
    if request.method == 'POST':
        policy = request.form['check']
        try:
            db.update_policy_all(policy)
            return render_template('message.html', title="General Policy Edit", text='Changed Successful')
        except:
            return render_template('message.html', title="General Policy Edit", text='Error occurred')


@app.route('/policy_one', methods=('GET', 'POST'))
def policy_one():
    if not login_check():
        return redirect('/')
    if request.method == 'GET':
        data = db.fetch_mailboxes()
        return render_template('policy_one.html', title='Edit mailbox policy', data=data, policy_list=policy_list)
    else:
        mail_id = request.form['check']
        return render_template('policy_one_form.html', id=mail_id, title="Choose wanted policy", data=policy_list)


@app.route('/policy_one_form', methods=('GET', 'POST'))
def policy_one_form():
    if not login_check():
        return redirect('/')
    if request.method == 'POST':
        policy = request.form['check']
        mailbox_id = request.form['id']
        try:
            db.update_policy_one(mailbox_id, policy)
            return render_template('message.html', title="Policy Edit", text='Change Successful')
        except:
            return render_template('message.html', title="Policy Edit", text='Error occurred')


@app.route('/about', methods=('GET', 'POST'))
def about():
    if not login_check():
        return redirect('/')
    return render_template('about.html', title="About")


@app.route('/mailbox_add', methods=('GET', 'POST'))
def mailbox_add():
    if not login_check():
        return redirect('/')
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        role = request.form['role']
        mailbox_name = request.form['mailbox_name']
        try:
            db.add_mailbox(firstname, lastname, mailbox_name, role)
            return render_template('message.html', title="Mailbox add", text='Created successfully')
        except:
            return render_template('message.html', title="Mailbox add", text='An Error occurred')
    else:
        return render_template('mailbox_add.html', title="Add new Mailbox")


@app.route('/delete_mailbox', methods=('GET', 'POST'))
def delete_mailbox():
    if not login_check():
        return redirect('/')
    if request.method == 'GET':
        mailbox_data = db.fetch_mailboxes()
        policy_list = db.fetch_policies()
        return render_template('delete_mailbox.html', title='Delete Mailbox', data=mailbox_data, policy_list=policy_list)
    if request.method == 'POST':
        mail_id = request.form['check']
        try:
            db.delete_mailbox(mail_id)
            return render_template('message.html', title="Delete Mailbox", text='Delete Successful')
        except:
            return render_template('message.html', title="Delete Mailbox", text='Error occurred')


@app.route('/reports', methods=('GET', 'POST'))
def reports():
    if not login_check():
        return redirect('/')
    if request.method == 'GET':
        data = db.fetch_reports()
        return render_template('reports.html', title="Show reports", data=data)
    else:
        mail_id = request.form['check']
        data = db.fetch_mailbox_data(mail_id)
        return render_template('mailbox_edit_form.html', data=data, title='CDR-Edit Mailbox')



if __name__ == '__main__':
    app.run()

db.close()
