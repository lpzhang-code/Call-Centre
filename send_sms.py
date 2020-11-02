from twilio.rest import Client
from decouple import config

# Your Account SID from twilio.com/console
account_sid = config("ACCOUNT_SID")
# Your Auth Token from twilio.com/console
auth_token = config("AUTH_TOKEN")

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+61431695399", from_="+61488839562", body="Hello from Python!"
)

print(message.sid)
