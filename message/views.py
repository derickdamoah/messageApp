from django.shortcuts import render
from twilio.rest import Client
from django_twilio.decorators import twilio_view
from twilio.twiml.messaging_response import MessagingResponse
import os

# Create your views here.
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

def home(request):
    return render(request, "home.html",)

def message(request):
    return render(request, "message.html",)

messageSID = ""

def sendMessage(request):
    try:
        allMessages = client.messages.list()
        for message in allMessages:
            message_SID = message.sid
            client.messages(message_SID).delete()
        message = client.messages.create(
            from_='+12816039967',
            body= request.POST['messageField'],
            to= (request.POST['codenumber'] + request.POST['phone']),
        )

        global messageSID
        messageSID = message.sid
        message = client.messages(messageSID).fetch()
        sender = message.from_
        receiver = message.to
        body = message.body
        sentMessage = "Sent From: " + sender + "\n" + "Sent To: " + receiver + "\n" + "\n" \
                      + "Message Body: " + body

        return render(request, "sentMessages.html", {"messages":sentMessage})

    except:
        return render(request, "message_not_sent.html", {"messages": "Your message was not sent please check your number and try again"})


def reply(request):
    message = client.messages(messageSID).fetch()
    sender = message.from_
    receiver = message.to
    body = message.body
    sentMessage = "Sent From: " + sender + "\n" + "Sent To: " + receiver + "\n" + "\n" + "Message Body: " + body

    allMessages = client.messages.list()
    lis = []

    for message in allMessages:
        if message.direction == 'inbound':
            lis.append(message.sid)
            for SID in lis:
                get_message_info = client.messages(SID).fetch()
                reply_body = get_message_info.body
                reply_from = get_message_info.from_
                reply_to = get_message_info.to
                message_reply = "Reply:\n" + "Sent From: " + reply_from + "\n" + "Sent To: " \
                                + reply_to + "\n" + "\n" + "Message Body: " + reply_body

                return render(request, "reply.html", {"reply": message_reply, "messages":sentMessage})

        elif message.direction == 'outbound-api':
            message_reply = "This person is yet to reply"
            return render(request, "reply.html", {"reply": message_reply, "messages": sentMessage})

        else:
            message_reply = "This person is yet to reply"
            return render(request, "reply.html", {"reply": message_reply, "messages": sentMessage})

@twilio_view
def sms_response(request):
    msg = ''
    r = MessagingResponse()
    r.message(msg)
    return r