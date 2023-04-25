from flask import Flask, render_template, url_for, request
import csv
import smtplib
from email.message import EmailMessage


app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        write_to_database_txt(data)
        write_to_database_csv(data)
        send_email(data)
        return render_template('thankyou.html')
    else:
        return 'Something went wrong, try again please'


def write_to_database_txt(data):
    with open('database.txt', 'a') as f:
        entry = ", ".join([f"{key}: {value}" for key, value in data.items()])
        f.write(entry + "\n")


def write_to_database_csv(data):
    with open('database.csv', 'a') as f:
        email = data['email']
        message = data['message']
        subject = data['subject']
        csv_writer = csv.writer(f, delimiter=',', quotechar=' ', quoting=csv.QUOTE_MINIMAL)

        csv_writer.writerow([email, subject, message])


def send_email(data):
    email = EmailMessage()

    email['from'] = 'Zeke Duvied'
    email['to'] = 'ezequieldiglesias@gmail.com'
    email['subject'] = 'New contact message from Zeke Duvied site'

    # Create a string representation of the data dictionary
    content = ''
    for key, value in data.items():
        content += f"{key}: {value}\n"

    email.set_content(content)

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('pypysender@gmail.com', 'aruuehviqvmlvtgf')
        smtp.send_message(email)
        print('mail sent, all good')