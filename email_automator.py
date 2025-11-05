import json, re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Read the JSON file and format to python data types
def read_json(file_path):
    try:
        with open(file_path, 'r') as file:
            raw = file.read()
        return json.loads(raw)
    except FileNotFoundError as e:
        print("The file not found")
    except FileExistsError as e:
        print("The file does not exist")

# Check the format of the JSON file
def check_json_format(data):
    try:
        if isinstance(data, list):
            rows = []
            # Loops the data types and checks the format of the data and structures for missing values
            for item in data:
                if not isinstance(item, dict) or 'email' not in item:
                    print("The json format should be list of dict items")
                rows.append({
                        'email':item['email'], 
                        'name':item.get('name',''),
                        'status':item.get('status', 0)
                        })
            return rows
    except Exception:
        print("The json format should be list of dict items")

# Python dict to the JSON
def dumps_json_unsend(data):
    try:
        with open('unsend_emails.json', 'w') as file:
            data_json = json.dumps(data, indent=4)
            file.write(data_json)
    except Exception as e:
        print("Exception occured in undelivered mails", e)

def dumps_json_invalid(data):
    try:
        with open('invalid_emails.json', 'w') as file:
            data_json = json.dumps(data, indent=4)
            file.write(data_json)
    except Exception as e:
        print("Exception occured in invalid mails", e)


# Undelivered mails
ud_emails = []
invalid_emails = []

def invalid_address(verified_data):
   return {
                'email':verified_data['email'], 
                'name':verified_data['name'],
                'status':verified_data['status'],
                'error_type':"invalid_address"
        }

def unsend_emails(verified_data):
    return {
                'email':verified_data['email'], 
                'name':verified_data['name'],
                'status':verified_data['status'],
                'error_type':"unsent"
        }

        
# Needed variables
data = read_json('emails.json')
verified_data = check_json_format(data)
len_verified_data = len(verified_data)

# Setting the GMail server
SMTP_SERVER = 'smtp.gmail.com'
GMAIL_PORT = 587

# Email Regular Expression
EMAIL_RE = re.compile(r"[^@]+@[^@]+\.[^@]+")

def validate_email(e):
    return bool(e and EMAIL_RE.match(e))


# Sender email and app password
sender_email = ""
sender_email_app_password = ""

# Initializing the server
server = smtplib.SMTP(SMTP_SERVER, GMAIL_PORT)
server.starttls()
server.login(sender_email, sender_email_app_password)

for i in range(len_verified_data):
    try:
        if verified_data[i]['status'] == 1:
            if validate_email(verified_data[i]['email']) == 1: # Send mails only for the accepted ones
                receiver_email = verified_data[i]['email']
                subject = "Accepted Application"
                body = f""" HI {verified_data[i]['name']}"""
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = receiver_email
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'html'))
                server.sendmail(sender_email, receiver_email, msg.as_string())
            else:
                invalid_addr = invalid_addr(verified_data[i])
                invalid_emails.append(invalid_addr)
                dumps_json_invalid(invalid_emails)
        else: # Send mails only for rejected ones
            if validate_email(verified_data[i]['email']) == 1:
                receiver_email = verified_data[i]['email']
                subject = "Rejected Application"
                body = f""" HI {verified_data[i]['name']}"""
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = receiver_email
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'html'))
                server.sendmail(sender_email, receiver_email, msg.as_string())
            else:
                invalid_addr = invalid_addr(verified_data[i])
                invalid_emails.append(invalid_addr)
                dumps_json_invalid(invalid_emails)
    except Exception as e:
        unsend_addr = unsend_emails(verified_data[i])
        ud_emails.append(unsend_addr)
        dumps_json_unsend(ud_emails)
            
server.quit()
print("All mails sent succesfully")