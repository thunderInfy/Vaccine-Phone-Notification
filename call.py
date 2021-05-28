from twilio.rest import TwilioRestClient
import json

def dial():
    
    with open("data.json","r") as f:
        data = json.load(f)

    TWILIO_PHONE_NUMBER = data["twilio_phone_number"]
    number = data["recipient_phone_number"]

    TWIML_INSTRUCTIONS_URL ="https://gist.githubusercontent.com/thunderInfy/5fffbe366e990a2b057b872cfa49db73/raw/c8edb2b4ef044fb3806e3bb5ec459e08c1cecac1/twiml.xml"

    client = TwilioRestClient(data["account_sid"], data["auth_token"])
    
    client.calls.create(to=number, from_=TWILIO_PHONE_NUMBER, url=TWIML_INSTRUCTIONS_URL, method="GET")

if __name__ == "__main__":
    dial()
