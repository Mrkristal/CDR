import os
import json
from imbox import Imbox
import db
import base64
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
from email.mime.application import MIMEApplication

ADMIN_MAIL = os.environ.get('ADMIN_MAIL', 'CDR@localhost')
PASSWORD = os.environ.get('ADMIN_PASS', '123456')
SERVER = os.environ.get('MAIL_SERVER', "localhost")
BAD_FILETYPES = ['pdf', 'exe', 'doc', 'xls', 'vbs', 'jpeg', 'zip', 'rtf', 'scr']

is_gt = lambda x, y: x if x > y else y


def get_policy_actions_by_id(policy_id):
    actions = {
        "url_remove": False,
        "attachments_remove": False,
        "block_mail": False,
        "add_alert": False,
        "filtering": False
    }
    if policy_id == 0:
        return actions
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
    mail_content['body']['plain'].append(
        "\n This mail has been scanned by CDR - Don't open links and attachments from unknown senders.")
    soup = BeautifulSoup(mail_content['body']['html'][0], 'html.parser')
    tag = soup.new_tag('div')
    tag.string = "This mail has been scanned by CDR - Don't open links and attachments from unknown senders."
    soup.body.append(tag)
    mail_content['body']['html'][0] = str(soup)


def remove_attachment(mail_content, filter=False):
    if not filter:
        mail_content['attachments'].clear()
    else:
        for att in mail_content['attachments']:
            if (att['filename'].split('.')[-1] in BAD_FILETYPES):
                mail_content['attachments'].remove(att)


def filter_content(mail_content):
    path = os.path.join(os.path.dirname(__file__), 'static', 'url_blocklist.json')
    f_url = open(path, 'r')
    blocklist = json.load(f_url)
    f_url.close()
    soup = BeautifulSoup(mail_content['body']['html'][0], 'html.parser')
    for a in soup.findAll('a', href=True):
        for url in blocklist:
            if (a.get('href') == url['url']):
                a.extract()
    mail_content['body']['html'][0] = str(soup)


def remove_urls(mail_content):
    soup = BeautifulSoup(mail_content['body']['html'][0], 'html.parser')
    for a in soup.findAll('a', href=True):
        a.extract()
    mail_content['body']['html'][0] = str(soup)


def format_mail_to_send(mail_content):
    out_message = EmailMessage()
    out_message.add_header("cdrApproved", "True")
    out_message["Subject"] = mail_content['subject']
    out_message["From"] = mail_content['sent_from'][0]["email"]
    out_message["To"] = mail_content['sent_to'][0]["email"]
    text = mail_content['body']["plain"][0]
    html = mail_content['body']["html"][0]
    out_message.set_content(html, subtype='html')

    for idx, attachment in enumerate(mail_content['attachments']):
        try:
            data = MIMEApplication(attachment.get('content').read())
            file_name = attachment.get('filename')
            maintype, subtype = attachment['content-type'].split('/', 1)
            dec_data = base64.b64decode(data.get_payload())
            full_path = os.path.join(os.path.dirname(__file__), file_name)
            fb = open(full_path, "wb")
            fb.write(dec_data)
            fb.close()
            fa = open(full_path, "rb")
            out_message.add_attachment(fa.read(), maintype=maintype, subtype=subtype, filename=file_name)
            fa.close()
            os.remove(full_path)
        except:
            print('problem with attachment')
    return out_message


def send_mail(mail_content):
    with smtplib.SMTP(SERVER, 25) as smtp_server:
        smtp_server.login(ADMIN_MAIL, PASSWORD)
        out_message = format_mail_to_send(mail_content)
        smtp_server.sendmail(
            mail_content['sent_from'][0]["email"], mail_content['sent_to'][0]["email"], out_message.as_string()
        )


def exec_policy(actions, mail_content):
    log_text = ""
    if actions['block_mail']:
        return "Mail was blocked due to policy."
    if actions["attachments_remove"]:
        remove_attachment(mail_content)
        log_text += "Attachments were removed. "
    if actions["filtering"]:
        filter_content(mail_content)
        remove_attachment(mail_content, True)
        log_text += "Attachments and urls were filtered. "
    if actions["url_remove"]:
        remove_urls(mail_content)
        log_text += "Urls were removed. "
    if actions["add_alert"]:
        add_alert(mail_content)
        log_text += "Alert was added to the mail. "
    send_mail(mail_content)
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
        self.db.clear()
        data = self.db.get_mailbox_by_mail(mailbox)
        if data:
            return data['PolicyID']
        return 0

    def process_mail(self, message):
        if type(message) is tuple:
            sent_to = message[1].sent_to[0]['email']
            policy_id = self.get_policy_for_mailbox(sent_to)
            actions = get_policy_actions_by_id(policy_id)
            mail_content = get_content(message)
            log = "From: " + mail_content['sent_from'][0]["email"] + " Sent to:" + mail_content['sent_to'][0][
                "email"] + ": "
            log = log + exec_policy(actions, mail_content)
            return log
