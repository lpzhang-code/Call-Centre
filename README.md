## Automated Call Centre

Automated call centre built using Django and Twilio, accompanied by notes for future reference.

### Telephony Network

- the telephony network enables text and voice messages, it is older than the internet
- the telephony network is connected by carriers which integrate connections (i.e. cell phone or home internet) into that network
- to build additional functionality into the connection, specialised equipment or software is needed
- the internet runs on single foundational protocol (HTTP), whereas telephony networks run on diverse set of protocols, each tailored to the task at hand

### Twilio Basics

- twilio's infrastructure is on the internet but connects to carriers, bridging the internet and telephony network
- twilio acquires phone numbers from carriers around the world, and these numbers provide virtual presence on the telephony network
- customers acquire twilio numbers according to use case (text and voice messaging), and these numbers can be configured
- twilio uses webhooks to let your application know that an event has occurred; for example, when there is an SMS or phone call, twilio will make an HTTP request (GET/POST) to the url configured for the webhook
- the HTTP request will contain details of the event; the application will perform its logic then respond to twilio with instructions in the form of Twilio Markup Language (TwiML)

### Weather Application

- consider simple weather app where users can request information and receive daily automated message about the weather
- carrier initiated event is where person texts the weather app with their location and receives forecast in response
- the text message will reach the carrier which finds that twilio owns the recipient number, it will then be routed to twilio via the SMPP protocol
- twilio receives the message through its dedicated connection with the carrier, it will find that the recipient phone number has been configured with messaging URL pointing to application endpoint
- twilio will send HTTP request (webhook) to the weather app containing the information in the text message
- weather app will return TwiML instructing how to respond to the text message

```
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<Response>
    <Message>It is very sunny!</Message>
</Response>
```

- the TwiML is returned to twilio via HTTP, it is transformed into SMS and sent to the carrier via SMPP
- nothing in the response tells twilio who to send to, instead response will be automatically directed to the number which sent the original message
- application initiated events are triggered via calls to twilio's REST API which provides whole host of services
- for example, weather app makes HTTP request to twilio API asking for text message containing weather forecast to be sent from application phone number to customer phone number

### REST API

- API is a way of making data and functionality available to other programs across the internet, there are range of twilio APIs available allowing calls and messages to anyone in the world
- REST API maps predefined set of URLs to resources which can be returned as HTML, JSON, images, etc; different kinds of HTTP requests (i.e. GET or POST) can be made over the resource
- there are separate REST APIs for each of twilio's products, but they are accessed in roughly the same way

**First Example**

- we are going to send SMS using our twilio account, which requires protecting sensitive information by storing them inside `.env` file and adding it to `.gitignore`

```
ACCOUNT_SID=XXXXX
AUTH_TOKEN=XXXXX
```

- then install the following packages

```
pip install twilio

pip install python-decouple
```

- allowing us to run the script with env vars

```
from twilio.rest import Client
from decouple import config

# env vars
account_sid = config("ACCOUNT_SID")
auth_token = config("AUTH_TOKEN")

# authentication
client = Client(account_sid, auth_token)

# send SMS
message = client.messages.create(
    to="+61431795489", from_="+61488839562", body="Hello from Python!"
)

print(message.sid)
```

**Second Example**

- now that we have sent the SMS, we can retrieve its details

```
message = client.messages.get('SM0fb22c4eb1ab45159f13e506f6bd1915')

print(message.to)
```

- we can iterate through all of the SMS we have sent

```
for message in client.messages.list():
    print(message.sid)
```

### Voice API

- this allows us to programatically make, receive, and manage calls
- make isolated python environment by creating and activating virtual environment in our project folder

```
virtualenv .

source bin/activate
```

- insert `Flask` and `twilio` into `requirements.txt` then install into the virtual environment

```
pip install -r requirements.txt
```

- create file named `answer_phone.py` and insert these lines

```
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
```

- run this lightweight flask application

```
python answer_phone.py

# Running on http://127.0.0.1:5000/
```

- when twilio receives a phone call, it sends an HTTP request to your application seeking instructions on how to respond; however, by default the flask application running on local dev is only available to programs on the computer
- make it accessible from the internet by using a tool called ngrok which ensures that HTTP requests to a public url end up hitting the flask app served on local dev

```
ngrok http 5000
```

- extend our flask app to answer phone calls

```
from twilio.twiml.voice_response import VoiceResponse

@app.route("/answer", methods=['GET', 'POST'])
def answer_call():
    """Respond to incoming phone calls with a brief message."""
    # Start our TwiML response
    resp = VoiceResponse()

    # Read a message aloud to the caller
    resp.say("Thank you for calling! Have a great day.", voice='alice')

    return str(resp)
```

- now on the twilio console, configure the phone number so that incoming calls lead to HTTP request hitting the URL provided by ngrok
