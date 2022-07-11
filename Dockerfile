FROM python:3

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./ /app

ENV DB_URL=host.docker.internal
ENV MAIL_SERVER=host.docker.internal
ENV ADMIN_MAIL=CDR-admin@localhost.com
ENV ADMIN_PASS=123456
#The ENV Variables:
#DB_PASS - password to the database
#DB_URL - the url to the database
#DB_USER - the root user of the database
#ADMIN_MAIL - the admin mailbox for processing
#ADMIN_PASS - the admin password
#MAIL_SERVER - the mail server
