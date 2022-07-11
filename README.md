# Open CDR Project
## overview
The CDR project is open-source solution for content disarm and reconstruction at Mailboxes. 
The CDR works by processing all incoming e-mails in a specific network, 
deconstructing them, and removing the elements that do not match the file type's standards or set policies. 
CDR technology then rebuilds the e-mail into clean versions that can be sent on to end users as intended.

**The project created by Elad Kristal and Shahar Hazan for Achva Collage.**

## Project Content
This project consisting of:
- **Admin Portal** for managing.
- **CDR app** that listen to the mail server and disarm its contents.
- **Hmailserver** - The mail server that the CDR is running on.
> ⚠️ The mail server is not in this project, and you need to install it separately.
- **MySQL server** - The Database for all the project`s contents.
> ⚠️ The MySQL server is not in this project, and you need to install it separately.
> 
> **The Schema for the CDR project is in this repository for deployment in your MySQL server.**

## Prerequisites
- MySQL server running with CDR schema as given in the sql_files folder of this repo.
- Hmailserver running with:
  1. CDR-admin mailbox for processing the incoming mails.
  2. 2 rules to enforce the incoming mail goes through the CDR component:
  
  <a href="https://imgur.com/z1Nwckv"><img src="https://i.imgur.com/z1Nwckv.png" title="source: imgur.com" /></a>
  
  First rule:
  
  <a href="https://imgur.com/ew9yle7"><img src="https://i.imgur.com/ew9yle7.png" title="source: imgur.com" /></a>
  
  Second rule:
  
  <a href="https://imgur.com/a/R8eiuLS"><img src="https://i.imgur.com/UEqwUpO.png" title="source: imgur.com" /></a>

# Installation and Configuration
1. Clone repo:
> git clone https://github.com/Mrkristal/CDR.git

2. Edit Dockerfile with your database and mailserver info with the ENV variables in the Dockerfile.

3. Build Docker images:
> docker compose build

4. run Docker containers:
> docker  compose up



