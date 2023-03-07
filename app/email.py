from flask_mail import Message
from flask import render_template
from app import mail, app, db
from app.models import Newsletter_Subscriber



def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


# Password reset email

def send_password_reset_email(user):
    """Send password reset email"""
    token = user.get_reset_password_token()
    send_email(
        "[somaSOMA] Reset Your Password",
        sender=app.config['MAIL_DEFAULT_SENDER'],
        recipients=[user.email],
        text_body=render_template(
                    "emails/reset_password.txt", user=user, token=token),
        html_body=render_template(
                    "emails/reset_password.html", user=user, token=token))



# Thank client for signing up for the newsletter

def thank_you_client(client, client_username):
    """Client received thank you note once signed up"""
    send_email(
        "[somaSOMA] Thank You!",
        sender=app.config["MAIL_DEFAULT_SENDER"],
        recipients=[client.email],
        text_body=render_template(
            "emails/newsletter_client_thank_you_signup.txt",
            client=client,
            client_username=client_username),
        html_body=render_template(
            "emails/newsletter_client_thank_you_signup.html",
            client=client,
            client_username=client_username))


# Email subscriber individually

def send_subscriber_private_email(email, subscriber_username):
    """Send newsletter subscriber a private email"""
    send_email(
        subject=email.subject,
        sender=app.config["MAIL_DEFAULT_SENDER"],
        recipients=[email.email],
        text_body=render_template(
            "emails/newsletter_subscriber_private_email.txt",
            email=email,
            subscriber_username=subscriber_username),
        html_body=render_template(
            "emails/newsletter_subscriber_private_email.html",
            email=email,
            subscriber_username=subscriber_username))


# Email user individually

def send_user_private_email(email, user_username):
    """Send user a private email"""
    send_email(
        subject=email.subject,
        sender=app.config["MAIL_DEFAULT_SENDER"],
        recipients=[email.email],
        text_body=render_template(
            "emails/private_email.txt",
            email=email,
            user_username=user_username),
        html_body=render_template(
            "emails/private_email.html",
            email=email,
            user_username=user_username))



# ==================================================
# SAMPLE NEWSLETTERS
# ==================================================

# Newsletter 1

def first_newsletter(client_email, client_username):
    """Subscriber receives first newsletter"""
    send_email(
        '[somaSOMA] Why Learn To Code',
        sender=app.config['MAIL_DEFAULT_SENDER'],
        recipients=[client_email],
        text_body=render_template(
            '/emails/newsletters/week1_why_learn_to_code.txt',
            client_email=client_email,
            client_username=client_username),
        html_body=render_template(
            '/emails/newsletters/week1_why_learn_to_code.html',
            client_email=client_email,
            client_username=client_username))


# Newsletter 2

def second_newsletter(client_email, client_username):
    """Subscriber receives second newsletter"""
    send_email(
        '[somaSOMA] Why Start With Flask',
        sender=app.config['MAIL_DEFAULT_SENDER'],
        recipients=[client_email],
        text_body=render_template(
            '/emails/newsletters/week2_why_start_with_flask.txt',
            client_email=client_email,
            client_username=client_username),
        html_body=render_template(
            '/emails/newsletters/week2_why_start_with_flask.html',
            client_email=client_email,
            client_username=client_username))


# Newsletter 3

def third_newsletter(client_email, client_username):
    """Subscriber receives third newsletter"""
    send_email(
        '[somaSOMA] Welcome To Tailwind CSS',
        sender=app.config['MAIL_DEFAULT_SENDER'],
        recipients=[client_email],
        text_body=render_template(
            '/emails/newsletters/week3_welcome_to_tailwind_css.txt',
            client_email=client_email,
            client_username=client_username),
        html_body=render_template(
            '/emails/newsletters/week3_welcome_to_tailwind_css.html',
            client_email=client_email,
            client_username=client_username))

# ==================================================
# END OF SAMPLE NEWSLETTERS
# ==================================================



# ==================================================
# SENDING NEWSLETTERS
# ==================================================

# Send first newsletter

def send_first_newsletter():
    """Send first newsletter"""
    subscribers = Newsletter_Subscriber.query.all()
    for subscriber in subscribers:
        # Get subscriber details
        subscriber_email = subscriber.email
        subscriber_username = subscriber.email.split('@')[0].capitalize()
        # Check if the subscriber is subscribed
        if subscriber.subscription_status is not False:
            # Check if the subscriber has received any newsletter before
            if subscriber.num_newsletter == 0:
                first_newsletter(subscriber_email, subscriber_username)
                # Update subscriber newsletter status
                subscriber.num_newsletter = 1
                db.session.commit()


# Send second newsletter

def send_second_newsletter():
    """Send second newsletter"""
    subscribers = Newsletter_Subscriber.query.all()
    for subscriber in subscribers:
        # Get subscriber details
        subscriber_email = subscriber.email
        subscriber_username = subscriber.email.split('@')[0].capitalize()
        # Check if the subscriber is subscribed
        if subscriber.subscription_status is not False:
            # Check if the subscriber has received any newsletter before
            if subscriber.num_newsletter == 0:
                second_newsletter(subscriber_email, subscriber_username)
                # Update subscriber newsletter status
                subscriber.num_newsletter = 1
                db.session.commit()


# Send third newsletter

def send_third_newsletter():
    """Send third newsletter"""
    subscribers = Newsletter_Subscriber.query.all()
    for subscriber in subscribers:
        # Get subscriber details
        subscriber_email = subscriber.email
        subscriber_username = subscriber.email.split('@')[0].capitalize()
        # Check if the subscriber is subscribed
        if subscriber.subscription_status is not False:
            # Check if the subscriber has received any newsletter before
            if subscriber.num_newsletter == 0:
                third_newsletter(subscriber_email, subscriber_username)
                # Update subscriber newsletter status
                subscriber.num_newsletter = 1
                db.session.commit()


# ==================================================
# END OF SENDING NEWSLETTERS
# ==================================================
