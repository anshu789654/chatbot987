from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

from utlis import fetch_reply

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    print(request.form)
    msg = request.form.get('Body')
    sender=request.form.get('From')


    # Create reply
    resp = MessagingResponse()
    mess, url = fetch_reply(msg,sender)
    if url != None:
        print(url)
        url = "https://www.countryflags.io/" + str.lower(url) + "/shiny/64.png"
        resp.message(mess).media(url)
    else:
        resp.message(mess)
    return str(resp)

if __name__ == "__main__":
    app.run(use_reloader = True)
