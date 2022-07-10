import db
from _datetime import datetime

log_db = db.DB()


def logger_events(title, desc, mail_id=0):
    if title and desc:
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        log_db.add_log_event(title, desc, mail_id, date_time)
        return True
    else:
        return False


def logger_logs(title, details):
    if title and details:
        now = datetime.now()
        title = now.strftime("%m/%d/%Y, %H:%M:%S") + " : " + title
        log_db.add_log(title, details)
        return True
    else:
        return False
