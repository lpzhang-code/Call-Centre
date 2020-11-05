from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)


@app.route("/answer", methods=["GET", "POST"])
def answer_call():
    """Respond to incoming phone call."""
    response = VoiceResponse()

    # Deliver message and collect user's choice.
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

    # End the call if they don't give any response.
    response.say(
        "Sorry we haven't received a response. Goodbye.",
        voice="alice",
        language="en-AU",
    )
    return str(response)


@app.route("/collect", methods=["GET", "POST"])
def collect_info():
    """Collect digit that user has pressed."""
    response = VoiceResponse()

    if "Digits" in request.values:
        choice = request.values["Digits"]
        response.say("You have selected %s" % choice)

    # response.redirect('/collect', method='POST')
    return str(response)


if __name__ == "__main__":
    app.run(debug=True)
