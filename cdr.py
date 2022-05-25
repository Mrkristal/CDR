import time, datetime
import logger
import mail_handler

last_mail_uid = 166
delay = 5
last_time_checked = datetime.datetime.now()
mail = mail_handler.MailHandler()
# mail.clear_mailbox()

while (True):
    message = mail.fetch_mails()
    for m in message:
        mail.process_mail(m)
        # work on the message
        # a = m[1].sent_to[0]['email']
        # b = mail.get_policy_for_mailbox(a)
    mail.clear_mailbox()
    #     mail = Imbox(server, ADMIN_MAIL, password, False)
    #     # mails = mail.messages(uid__range=str(last_mail_uid) + ':*')
    #
    #     mails = mail.messages(date__gt=last_time_checked)
    #     for uid, message in mails:
    #         if last_mail_uid <= int(uid):
    #             last_mail_uid = int(uid) + 1
    #         print(last_mail_uid)
    #         print(uid)
    #         print(message)
    #         txt = "new mail uid"
    #         logger.logger_logs("got new mail", txt)
    #         out_message = MIMEMultipart("alternative")
    #         out_message["cdrApproved"] = "True"
    #         out_message["Subject"] = message.subject
    #         out_message["From"] = message.sent_from[0]["email"]
    #         out_message["To"] = message.sent_to[0]["email"]
    #
    #         # Create the plain-text and HTML version of your message
    #         text = message.body["plain"][0] + "\ncheck-text - approved by CDR"
    #         html = message.body["html"][0] + "\nhtml approved by CDR"
    #
    #         # Turn these into plain/html MIMEText objects
    #         part1 = MIMEText(text, "plain")
    #         part2 = MIMEText(html, "html")
    #
    #         # Add HTML/plain-text parts to MIMEMultipart message
    #         # The email client will try to render the last part first
    #         out_message.attach(part1)
    #         out_message.attach(part2)
    #         txt = "from: " + out_message["From"] + " to: " + out_message["To"]
    #         logger.logger_logs("cdr functions here", txt)
    #
    #         with smtplib.SMTP(server, 25) as smtp_server:
    #             smtp_server.login(ADMIN_MAIL, password)
    #             smtp_server.sendmail(
    #                 message.sent_from[0]["email"], message.sent_to[0]["email"], out_message.as_string()
    #             )
    #         logger.logger_logs("mail was foreword", "mail was delivered")
    #
    time.sleep(delay)
