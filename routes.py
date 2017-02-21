from flask import Flask, render_template, request, flash
from forms import ContactForm
from flask_mail import Message, Mail
import smtplib
import sys
import traceback
import pager
import random
import string
import configparser


# init our config parser and load our config file
config = configparser.RawConfigParser()
config.read('config.conf')

# create new mail and flask objects
mail = Mail()
app = Flask(__name__)

# not entirely sure what this is needed for tbh, flask example i adapted had it so ¯\_(ツ)_/¯
app.secret_key = config.get('general', 'appSecret')


# set our mail variables, change these in the config file to match your needs
app.config["MAIL_SERVER"] = config.get('general', 'mailServer')
app.config["MAIL_PORT"] = config.getint('general', 'mailPort')
app.config["MAIL_USE_SSL"] = config.getboolean('general', 'mailUseSSL')
app.config["MAIL_USE_TLS"] = config.getboolean('general', 'mailUseTLS')
app.config["MAIL_USERNAME"] = config.get('general', 'mailUsername')
app.config["MAIL_PASSWORD"] = config.get('general', 'mailPassword')

# aaaand we're off
mail.init_app(app)

# our page takes GET and POST records
@app.route('/', methods=['GET', 'POST'])
# create our contact form
def contact():
    form = ContactForm()
    # if the form is being submitted
    if request.method == 'POST':
        # verify everything validates
        if form.validate() == False:
            # if not, flash error messages and redirect back to form
            flash('All fields are required.')
            return render_template('contact.html', form=form)
        else:
            # if it does validate, grab all "Times Available" boxes that were ticked and save to a var
            if form.timesChecks.data:
                avail ="Times Available:\n" + "\n".join(item for item in form.timesChecks.data)
            else:
                avail = ""
            # generate an identifier, 5 characters long, a random combination of uppercase letters and numbers
            identifier = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(5))
            # create new email message w/ subject containing the form's subject field, our identifier, and priority identifier, set to go to our recipient email defined in the config
            msg = Message(form.subject.data + " " + identifier + " P: " + form.priority.data, sender=form.email.data, recipients=[config.get('general', 'mailRecipient')])
            # set our body to include the name, message from the form, email address, and availability info
            msg.body = """
From: %s


%s

%s
            """ % (form.name.data, form.message.data, avail)
            
            # if we chose the high priority option in our dropdown, use our high priority service key, otherwise use low
            if form.priority.data == "2":
                serviceKey = config.get('general', 'highServiceKey')
            else:
                serviceKey = config.get('general', 'lowServiceKey')
            
            # try to send our email and trigger our incident
            try:
                if config.getboolean('general', 'sendEmail'):
                    mail.send(msg)
                
                if config.getboolean('general', 'triggerIncident')
                    pager.trigger_incident(config.get('general', 'pagerdutyApiKey'),serviceKey,form.subject.data,identifier,msg.body)
                # set our returnmessage to our defined success message, and send the user to our results page
                returnMessage = config.get('general', 'successMessage')
                return render_template('contact.html', success=True, data=returnMessage)
            except Exception as e:
                # if we encounter an error, set our returnmessage to our defined error message, send the user to the results page, and print our error info
                err = str(e)
                returnMessage = config.get('general', 'errorMessage')
                messageBody = "<br />".join(msg.body.split("\n"))
                return render_template('contact.html', success=True, data=returnMessage, errmsg=err,subject=form.subject.data,priority=form.priority.data,sender=form.email.data, email=messageBody)
                pass
    # if we're just navigating to the page, present our form
    elif request.method == 'GET':
        return render_template('contact.html', form=form)
# run our flask app
if __name__ == '__main__':
    app.run(host= '0.0.0.0')
