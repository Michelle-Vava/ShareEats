from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

client = Client('ACf91579ced56697582b00416541947683', '9a2f8474b329324195b3ec3432f23eba')
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
