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
- REST API maps predefined set of URLs to resources which can be returned as HTML, JSON, images, etc; different kinds of HTTP requests (GET/POST/PUT/DELETE) can be made over the resource
- there are separate REST APIs for each of twilio's products, but they are accessed in roughly the same way

**Authentication**

- to access twilio API, authenticate using HTTP or helper library
