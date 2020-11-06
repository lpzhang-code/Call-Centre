from flask import Flask, request
from decouple import config
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client

app = Flask(__name__)


@app.route("/answer", methods=["POST"])
def answer_call():
    """Respond to phone call from user."""
    response = VoiceResponse()

    # Play message and record user's choice.
    gather = Gather(action="/collect", numDigits=1)
    gather.say(
        "Thank you for calling Anika Legal. \
        For information about repairing your rental property, please press 1. \
        For information about negotiating a rent reduction, please press 2. \
        For all other enquiries, please press 3.",
        voice="alice",
        language="en-AU",
    )
    response.append(gather)

    # End the call if user doesn't respond.
    response.say(
        "Sorry, we haven't received a response, goodbye.",
        voice="alice",
        language="en-AU",
    )
    return str(response)


@app.route("/collect", methods=["POST"])
def collect_info():
    """Retrieve information from user's call"""
    response = VoiceResponse()

    # Retrieve caller's number and choice.
    number = request.values["From"]
    choice = request.values["Digits"]

    # Authenticate to send SMS
    account_sid = config("ACCOUNT_SID")
    auth_token = config("AUTH_TOKEN")
    client = Client(account_sid, auth_token)

    # Generate response depending on user choice.
    if choice == "1":
        message = "Thank you for enquiring about repairing your rental property, please fill in the form at this link: https://test-intake.anikalegal.com/"
    elif choice == "2":
        message = "Thank you for enquiring about reducing your rent, please fill in the form at this link: https://test-intake.anikalegal.com/"
    elif choice == "3":
        message = "Thank you for contacting us about your specific enquiry, one of our staff will call back in the next few days."
    else:
        response.say(
            "Sorry we haven't received a valid choice, please try again.",
            voice="alice",
            language="en-AU",
        )
        response.redirect("/answer", method="POST")
        return str(response)

    # for choices 1 - 3 send SMS then finish
    send = client.messages.create(to=number, from_="+61488839562", body=message)
    return str(response)


if __name__ == "__main__":
    app.run(debug=True)
