from flask import Flask
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route("/message", methods=["GET", "POST"])
def answer_call():
    """Respond to incoming SMS with our own SMS."""
    response = MessagingResponse()
    response.message(
        "Thank you for sending us an SMS. Please call us on this number or direct written enquiries to contact@anikalegal.com"
    )

    return str(response)


if __name__ == "__main__":
    app.run(debug=True)
