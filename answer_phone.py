from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather

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

    # Retrieve caller's number and choice
    number = request.values["From"]
    choice = request.values["Digits"]

    # Send SMS depending on user's choice
    response.message("You are calling from %s and have selected %s" % (number, choice))

    # response.redirect('/collect', method='POST')
    return str(response)


if __name__ == "__main__":
    app.run(debug=True)
