## Overview

Automated call centre built using Django and Twilio, accompanied by notes for future reference.

### Telephony Network

- the telephony network enables text and voice messages, it is older than the internet
- the telephony network is connected by carriers which integrate connections (i.e. cell phone or home internet) into that network
- to build additional functionality into the connection, specialised equipment or software is needed
- the internet runs on single foundational protocol (HTTP), whereas telephony networks run on diverse set of protocols, each tailored to the task at hand

### Twilio Basics

- twilio's infrastructure is on the internet but connects to carriers, bridging the internet and telephony networks
- twilio acquires phone numbers from carriers around the world, and these numbers provide virtual presence on the telephony network
- customers acquire twilio numbers according to use case, and these numbers can be configured
- the majority of use cases involve text and voice messaging

### Weather Application

- consider simple weather app where users can request information and receive daily automated message about the weather
- carrier initiated event is where person texts the weather app with their location and receives forecast in response
- the text message will reach the carrier which finds that twilio owns the recipient number, it will then be routed to twilio via the SMPP protocol
- twilio receives the message through its dedicated connection with the carrier, it will find that the recipient phone number has been configured with messaging URL pointing to application endpoint
- twilio will send HTTP request (webhook) to the weather app containing information in the text message
