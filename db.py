import mysql.connector
import os

HOST = os.environ.get('DB_URL', '127.0.0.1')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', '123456')
os.environ['LOGGED'] = 'False'


class DB:
    def __init__(self):
        self.connection = mysql.connector.connect(user=DB_USER,
                                                  password=DB_PASS, host=HOST, database='cdr')
        self.cursor = self.connection.cursor(buffered=True)
        self.dic_cur = self.connection.cursor(dictionary=True, buffered=True)
        self.is_logged_in = os.environ['LOGGED']

    def login(self, user, password):
        if self.is_logged_in:
            return True
        else:
            self.cursor.execute('SELECT username,password FROM admin')
            admin = self.cursor.fetchone()
            if user == admin[0] and password == admin[1]:
                self.is_logged_in = True
                os.environ['LOGGED'] = 'True'
                return True
            else:
                return False

    def fetch_policies(self):
        self.cursor.execute('SELECT * FROM policy')
        return self.cursor.fetchall()

    def fetch_mailboxes(self):
        self.cursor.execute('SELECT * FROM mailbox')
        return self.cursor.fetchall()

    def fetch_mailbox_data(self, mail_id):
        self.cursor.execute('SELECT * FROM mailbox where Id=' + mail_id)
        return self.cursor.fetchone()

    def fetch_mailbox_data_dic(self, mail_id):
        self.dic_cur.execute('SELECT * FROM mailbox where Id=' + mail_id)
        return self.dic_cur.fetchone()

    def fetch_mailbox_name(self, mail_id):
        self.cursor.execute('SELECT FirstName,LastName FROM mailbox where Id=' + mail_id)
        return self.cursor.fetchone()

    def update_policy_all(self, policy_id):
        self.cursor.execute("UPDATE cdr.mailbox SET PolicyID = '" + policy_id + "';")
        self.connection.commit()

    def update_policy_one(self, mail_id, policy_id):
        self.cursor.execute("UPDATE cdr.mailbox SET PolicyID = '" + policy_id + "' WHERE ID ='" + mail_id + "';")
        self.connection.commit()

    def update_mailbox_info(self, mail_id, first_name, last_name, mailbox_name, role):
        self.cursor.execute("UPDATE cdr.mailbox SET FirstName ='" + first_name + "', LastName = '" + last_name +
                            "',MailBoxName = '" + mailbox_name + "' , Role = '" + role +
                            "' WHERE(ID = '" + mail_id + "');")
        self.connection.commit()

    def add_mailbox(self, first_name, last_name, mailbox_name, role):
        self.cursor.execute("INSERT INTO `cdr`.`mailbox` (`FirstName`, `LastName`, `MailBoxName`, `Role`,"
                            " `PolicyID`) VALUES ('" + first_name + "', '" + last_name + "', '" + mailbox_name +
                            "', '" + role + "', '1');")
        self.connection.commit()

    def delete_mailbox(self, mailbox_id):
        self.cursor.execute("DELETE FROM cdr.mailbox WHERE (ID='" + mailbox_id + "');")
        self.connection.commit()

    def fetch_reports(self):
        self.dic_cur.execute('SELECT * FROM events')
        ret = self.dic_cur.fetchall()
        self.connection.commit()
        return ret

    def fetch_logs(self):
        self.dic_cur.execute('SELECT * FROM logs')
        ret = self.dic_cur.fetchall()
        self.connection.commit()
        return ret

    def fetch_mailboxes_dic(self):
        self.dic_cur.execute('SELECT * FROM mailbox')
        return self.dic_cur.fetchall()

    def fetch_mailboxes_with_policy(self):
        data = self.fetch_mailboxes_dic()
        policy = self.fetch_policies()
        for i in range(len(data)):
            data[i]['PolicyID'] = policy[data[i]['PolicyID'] - 1][1]
        return data

    def add_log_event(self, title, description, mail_id, date):
        mail_id = str(mail_id)
        self.cursor.execute("INSERT INTO `cdr`.`events` (`title`, `details`, `mailboxid`, `date`) "
                            "VALUES ('" + title + "', '" + description + "', '" + mail_id +
                            "', '" + date + "');")
        self.connection.commit()

    def add_log(self, title, details):
        txt = "INSERT INTO `cdr`.`logs` (`title`, `details`) VALUES ('" + title + "', '" + details + "');"
        self.cursor.execute(txt)
        self.connection.commit()

    def get_mailbox_by_mail(self, mailbox):
        txt = 'SELECT * FROM mailbox where MailBoxName="' + mailbox + '";'
        self.dic_cur.execute(txt)
        return self.dic_cur.fetchone()

    def close(self):
        self.connection.close()

    def clear(self):
        self.connection.commit();