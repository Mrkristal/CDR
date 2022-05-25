from imbox import Imbox
import db
import bs4
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

ADMIN_MAIL = 'CDR-admin@localhost.com'
PASSWORD = '123456'
SERVER = "localhost"

is_gt = lambda x, y: x if x > y else y


def get_policy_actions_by_id(policy_id):
    actions = {
        "url_remove": False,
        "attachments_remove": False,
        "block_mail": False,
        "add_alert": False,
        "filtering": False
    }
    if policy_id <= 5:
        actions["add_alert"] = True
    if 4 >= policy_id >= 3:
        actions["filtering"] = True
    if policy_id <= 2:
        actions["attachments_remove"] = True
    if policy_id <= 3:
        actions["url_remove"] = True
    if policy_id == 1:
        actions["block_mail"] = True
    return actions


def get_content(message):
    if message:
        msg = message[1]
        return_msg = {
            'attachments': msg.attachments,
            'body': msg.body,
            'date': msg.parsed_date,
            'headers': msg.headers,
            'sent_to': msg.sent_to,
            'sent_from': msg.sent_from,
            'subject': msg.subject
        }
        return return_msg
    return None


def add_alert(mail_content):
    pass


def remove_attachment(mail_content):
    pass


def filter_content(mail_content):
    pass


def remove_urls(mail_content):
    pass


def exec_policy(actions, mail_content):
    log_text = ""
    if actions['block_mail']:
        return "Mail was blocked due to policy."
    if actions["attachments_remove"]:
        remove_attachment(mail_content)
        log_text += "Attachments were removed. "
    if actions["filtering"]:
        filter_content(mail_content)
        log_text += "Attachments and urls were filtered. "
    if actions["url_remove"]:
        remove_urls(mail_content)
        log_text += "Urls were removed. "
    if actions["add_alert"]:
        add_alert(mail_content)
        log_text += "Alert was added to the mail. "
    return log_text


class MailHandler:
    def __init__(self):
        self.mail = Imbox(SERVER, ADMIN_MAIL, PASSWORD, False)
        self.last_uid = 0
        self.db = db.DB()

    def fetch_mails(self):
        mails = self.mail.messages()
        for message in mails:
            # print(message)
            self.last_uid = is_gt(self.last_uid, int(message[0]))
        return mails

    def clear_mailbox(self):
        uid = '*:' + str(self.last_uid)
        for uid, massage in self.mail.messages(uid__range=uid):
            print(uid)
            self.mail.delete(uid)

    def get_policy_for_mailbox(self, mailbox):
        data = self.db.get_mailbox_by_mail(mailbox)
        if data:
            return data['PolicyID']
        return 0

    def process_mail(self, message):
        if message:
            sent_to = message[1].sent_to[0]['email']
        policy_id = self.get_policy_for_mailbox(sent_to)
        actions = get_policy_actions_by_id(policy_id)
        mail_content = get_content(message)
        log = exec_policy(actions, mail_content)
        print(log)
