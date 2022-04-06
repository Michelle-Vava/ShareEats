from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from ShareEats import settings

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
verify = client.verify.services('VA0c501788f7b23295ea6c712bf03bc607')


def send(phone):
    verify.verifications.create(to=phone, channel='sms')


def check(phone, code):
    try:
        result = verify.verification_checks.create(to=phone, code=code)
    except TwilioRestException:
        print('no')
        return False
    return result.status == 'approved'


def send_message_to_seller(to):
    # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body='Hi,a ShareEats user has just purchased an item from you.',
        to=to, from_=settings.TWILIO_PHONE_NUMBER)


def send_message_to_buyer(to):
    # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body='Thank you for purchasing an order on ShareEats,the vendor has been notified of your order',
        to=to, from_=settings.TWILIO_PHONE_NUMBER)
