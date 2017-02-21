from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, SelectField, validators, ValidationError, widgets, SelectMultipleField

#define a multi-checkbox field
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

#create our form
class ContactForm(Form):
    # build our multicheckbox field
    timesAvailable = ["Sunday Morning","Sunday Evening","Monday Morning","Monday Evening","Tuesday Morning","Tuesday Evening","Wednesday Morning","Wednesday Evening","Thursday Morning","Thursday Evening","Friday Morning", "Friday Evening","Saturday Morning", "Saturday Evening"]
    times = [(x, x) for x in timesAvailable]
    #name and email w/ validators, self explanatory
    name = TextField("Name",  [validators.Required("Please enter your name.")])
    email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter a valid email address in the form of example@example.com.")])
    # priorities available in dropdown
    priority = SelectField("Priority", [validators.Required("How did you unselect")], choices=[('1', 'Notify the Team - Does not require Immediate Assistance'), ('2', 'Wake a Tech - Requesting Immediate Assistance'), ('3', 'Incident Report - Request security footage archival'), ('4', 'Price Key - Request addition, modification, or removal of keys')])
    # actually buidl theavailability  multicheckbox field
    timesChecks = MultiCheckboxField("When do you work the next couple days?", choices=times)
    subject = TextField("Subject",  [validators.Required("Please enter a subject.")])
    message = TextAreaField("Message", [validators.Required("Please enter a message.")])
    submit = SubmitField("Send")
