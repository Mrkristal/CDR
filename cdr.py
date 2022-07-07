import time, datetime
import logger
import mail_handler

last_mail_uid = 166
delay = 5
last_time_checked = datetime.datetime.now()
mail = mail_handler.MailHandler()

while (True):
    message = mail.fetch_mails()
    for m in message:
        id = str(int(m[0]))
        title = "Got new mail id:" + id
        logger.logger_logs(title, "start processing.")
        log = mail.process_mail(m)
        logger.logger_logs("CDR action taken", log)
        logger.logger_logs("Mail id:" + id + " delivered", "CDR completed the processing.")
    mail.clear_mailbox()
    time.sleep(delay)
