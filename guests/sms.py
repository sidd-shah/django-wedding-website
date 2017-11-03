from twilio.rest import Client

# Your Account SID from twilio.com/console
#account_sid = "AC3eaae3e0e3447653dde8de37f385937e"
account_sid="AC5ec8ed1c98a7d5192a25eafdc42ba485"
# Your Auth Token from twilio.com/console
#auth_token = "901ed36b5ea2200b3de8fd911885769c"
auth_token ="58f23b261e25b9cc772f048f8bb80041"
twilio_number ="+16318237195"
client = Client(account_sid, auth_token)

def send_sms(to_number, message):
    client.messages.create(
        to=to_number,
        from_=twilio_number,
        body=message)

    print(message)
