from datetime import datetime
from app.email import send_first_newsletter, send_second_newsletter, send_third_newsletter


def register(app):
    @app.cli.group()
    def send_newsletter_email():
        """Send email to individual clients"""
        pass


    @send_newsletter_email.command()
    def first_newsletter_command():
        """Send first newsletter"""
        send_first_newsletter()
        print(str(datetime.utcnow()), 'First newsletter sent to all subscribers\n\n')


    @send_newsletter_email.command()
    def second_newsletter_command():
        """Send second newsletter"""
        send_second_newsletter()
        print(str(datetime.utcnow()), 'Second newsletter sent to all subscribers\n\n')


    @send_newsletter_email.command()
    def third_newsletter_command():
        """Send thrid newsletter"""
        send_third_newsletter()
        print(str(datetime.utcnow()), 'Third newsletter sent to all subscribers\n\n')
