from flask import Flask
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route("/answer", methods=["GET", "POST"])
def answer_call():
    """Respond to incoming SMS with our own SMS."""
    response = MessagingResponse()
    response.message("Sent this SMS.")

    return str(response)


if __name__ == "__main__":
    app.run(debug=True)
