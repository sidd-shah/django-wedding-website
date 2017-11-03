from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "AC3eaae3e0e3447653dde8de37f385937e"
# Your Auth Token from twilio.com/console
auth_token = "901ed36b5ea2200b3de8fd911885769c"
twilio_number ="+16318237195"
client = Client(account_sid, auth_token)

def send_sms(to_number, message):
    client.messages.create(
        to="+5132934561",
        from_='+15005550006',
        body=message)

    print(message)