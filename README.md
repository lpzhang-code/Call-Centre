## Automated Call Centre

Automated call centre built using Python Flask and Twilio, accompanied by notes for future reference.

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

**Markup Language**

- TwiML is an XML document with special twilio elements, we can use the helper library to create valid TwiML
- there is the response element, and case sensitive verb and noun elements; verb elements must be nested inside the root response element
- verb elements specify the actions to take for given call, they can be combined to create interactive user experiences

```
<Say>       # Read text

<Play>      # Play audio

<Dial>      # Add another party to the call

<Record>    # Record caller's voice

<Gather>    # Collect digits pressed on keypad

<Hangup>    # End the call

<Pause>     # Wait before executing more instructions

<Redirect>  # Run different XML document

<Reject>    # Decline incoming call
```

- the noun element is something that the verb element acts upon, such as a phone number
- an HTTP request from twilio includes params/values which we can use to customise our response; the following are always sent with an HTTP request, either through the URL (GET), or hidden (POST)

```
CallSid     # Unique call identifier

AccountSid  # Twilio account ID

From        # Phone number

To

CallStatus
```

- twilio will also look up the geographic data (city, state, zip, country) of the phone numbers involved in the call, and send them as params in the HTTP request
- the following TwiML reads 'Hello World' to the caller before playing an mp3 and hanging up

```
<Response>
    <Say>Hello World!</Say>
    <Play>https://api.twilio.com/cowbell.mp3</Play>
</Response>
```

- we can also construct TwiML using our helper library where the call ends when the mp3 has looped ten times or the caller hangs up

```
resp = VoiceResponse()

resp.say('Hello World')

resp.play('https://api.twilio.com/cowbell.mp3', loop=10)
```

**Gather Verb**

- use the `<Gather>` verb to collect digits or transcribe speech during the call; info entered by the user during set period will be sent to URL; if there is no info, twilio will move to next verb or end the call
- attributes can be specified to configure the behaviour of the `<Gather>` verb

```
<Response>
    <Gather>
        <Say>Please enter your account number, followed by the pound sign</Say>
    </Gather>
    <Say>We didn't receive any input. Goodbye!</Say>
</Response>
```

- the `action` attribute takes an absolute or relative URL and when the caller has finished entering info or time has run out, an HTTP request is made to this URL with data
- if we are gathering digits from the caller, twilio will include the `Digits` param containing numbers the caller entered
- after `<Gather>` ends and HTTP request is made to `action` URL, the current call will continue with TwiML returned by that URL, so any verb after `<Gather>` is ignored
- however if user didn't input any information, the call flow continues in the original TwiML document, we could say they haven't input anything and hang up
- if no `action` attribute is specified, twilio will make an HTTP request to the current URL and this can lead to looping behaviour, so it is recommended that the `action` attribute be a new URL
- so let's use the helper library to generate the same TwiML as before- with attributes

```
from twilio.twiml.voice_response import Gather, VoiceResponse

response = VoiceResponse()

gather = Gather(action='/process_gather.php', method='GET')

gather.say('Please enter your account number.')

response.append(gather)

response.say('We didn't receive any input. Goodbye!')

print(response)
```

- the `finishOnKey` attribute allows the user to press a value (#) to immediately submit their digits
- the `input` attribute is `dtmf` by default, however we can specify `speech` or `dtmf speech` (where the first detected input takes precedence)
- the `method` attribute is `POST` by default, however we can specify that `GET` request is made to the `action` URL
- the `numDigits` attribute specifies the number of digits expected from the caller, once the final digit is pressed, an HTTP request is immediately made to the `action` URL
- the `timeout` attribute is the number of seconds (default five) that twilio will wait for the user to press another key or say another word before submitting their data
- the `actionOnEmptyResult` attribute force sends HTTP request to `action` URL even when there is no input
- we can nest `<Say>, <Play>, <Pause>` verbs inside of `<Gather>` element

### SMS API

- use helper library to send simple SMS response

```
from twilio.twiml.messaging_response import MessagingResponse, Message

response = MessagingResponse()

message = Message()

message.body('Hello World!')

response.append(message)
```

- use helper library to send two SMS

```
from twilio.twiml.messaging_response import MessagingResponse

response = MessagingResponse()

response.message('Read this first message.')

response.message('Read this second message.')
```

- note that `MessagingResponse` only works for responding to incoming SMS; if used for incoming phone call, this function and TwiML produced has no effect
