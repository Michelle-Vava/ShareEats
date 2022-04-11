from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from ShareEats import settings

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
verify = client.verify.services('VA0c501788f7b23295ea6c712bf03bc607')


def send(phone):
    verify.verifications.create(to=phone, channel='sms')


def check(phone, code):
    result = verify.verification_checks.create(to=phone, code=code)
    if result.status == "approved":
        return True
    else:
        return False


def send_message_to_seller(to, name, businessname):
    # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body="Hi," + businessname + ' , ' + name + ' has just purchased an item from you.',
        to=to, from_=settings.TWILIO_PHONE_NUMBER)


def send_message_to_buyer(to, name, business):
    # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=" Hi," + name + ' ,Thank you for purchasing an order on ShareEats '  ',' + business + ' has been notified of your order.You will receive updates from ' + business + ' when your order is ready',
        to=to, from_=settings.TWILIO_PHONE_NUMBER)


def send_message_to_seller_inprogress(to, name):
    # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=" Hi," + name + ' the buyer has been notified that order is in progress. ',
        to=to, from_=settings.TWILIO_PHONE_NUMBER)


def send_message_to_buyer_inprogress(to, name, bussinessname):
    # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=" Hi," + name + ' , ' + bussinessname + ' is now currently making your meal. Order status: "In Progress " ',
        to=to, from_=settings.TWILIO_PHONE_NUMBER)


def send_message_to_seller_completed(to, name, businessname):
    # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=" Hi ," + businessname + " , " + name + " has been notified that order is completed." + name + " should be on the way to pickup the order. ",
        to=to, from_=settings.TWILIO_PHONE_NUMBER)


def send_message_to_buyer_completed(to, name, businessname):
    # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=" Hi," + name + ' , ' + businessname + ' has completed your order. It is now ready for pickup ',
        to=to, from_=settings.TWILIO_PHONE_NUMBER)
