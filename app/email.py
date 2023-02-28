from flask_mail import Message
from flask import render_template
from app import mail, app


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
    