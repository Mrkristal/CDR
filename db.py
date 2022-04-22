import mysql.connector


class DB:
    def __init__(self):
        self.connection = mysql.connector.connect(user='root',
                                                  password='Aa123456123456', host='127.0.0.1', database='cdr')
        self.cursor = self.connection.cursor()
        self.dic_cur = self.connection.cursor(dictionary=True)
        self.is_logged_in = False

    def login(self, user, password):
        if self.is_logged_in:
            return True
        else:
            self.cursor.execute('SELECT username,password FROM admin')
            admin = self.cursor.fetchone()
            if user == admin[0] and password == admin[1]:
                self.is_logged_in = True
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
        return self.dic_cur.fetchall()

    def close(self):
        self.connection.close()
