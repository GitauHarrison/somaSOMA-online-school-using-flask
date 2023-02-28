from flask import current_app
from twilio.rest import Client, TwilioException


def _get_twilio_verify_client():
    """
    Get the Twilio Verify API client
    """
    return Client(
        current_app.config['TWILIO_ACCOUNT_SID'],
        current_app.config['TWILIO_AUTH_TOKEN']
    ).verify.services(current_app.config['TWILIO_VERIFY_SERVICE_ID'])


# ============= #
# === Admin === #
# ============= #

def request_verification_token(phone):
    """
    Request a verification token
    """
    verify = _get_twilio_verify_client()
    try:
        verify.verifications.create(to=phone, channel='sms')
    except TwilioException as e:
        verify.verifications.create(to=phone, channel='call')


def check_verification_token(phone, token):
    """
    Verify token received by user
    """
    verify = _get_twilio_verify_client()
    try:
        result = verify.verification_checks.create(to=phone, code=token)
        return result.status == 'approved'
    except TwilioException as e:
        return False


# ============== #
# === Client === #
# ============== #

def request_email_verification_token(email):
    """Generate a token to be sent to client email"""
    verify = _get_twilio_verify_client()
    verify.verifications.create(to=email, channel='email')


def check_email_verification_token(email, token):
    """Client's token is verified"""
    verify = _get_twilio_verify_client()
    try:
        result = verify.verification_checks.create(to=email, code=token)
        return result.status == 'approved'
    except TwilioException as e:
        return False
