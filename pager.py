import json
import requests
# Once the form has been submitted, trigger a pagerduty incident
def trigger_incident(apiKey, serviceKey,description,identifier,additionalInfo):
    #set headers w/ the passed API key
    headers = {
        'Authorization': 'Token token={0}'.format(apiKey),
        'Content-type': 'application/json',
    }
    
    # the data to be passed to the api endpoint, typically includes subject, body of the email, and an identifier
    payload = json.dumps({
        # service key, passed to the function, that decides which pagerduty service the trigger is for, from which you can define the escalation and notification policies
        "service_key": serviceKey,
        "event_type": "trigger",
        # the description is typically the subject of the email, with a 5-digit randomized identifier appended for easy matching w/ the email to your ticketing system
        "description": description + " " + identifier,
        "client": "Portal Helpdesk Form",
        "client_url": "momo.software",
        "details": {
        # can put whatever key/value pairs we want in Details, currently only include the body of the sent email as "additional info"
        "Additional Info": additionalInfo
        }
    })
    
    #make the request w/ the defined headers and payload
    r = requests.post(
        'https://events.pagerduty.com/generic/2010-04-15/create_event.json',
        headers=headers,
        data=payload,
    )
    #print(r.status_code)
    #print(r.text)
#trigger_incident()