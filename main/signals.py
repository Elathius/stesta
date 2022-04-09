from django.core.mail import EmailMessage, send_mail, BadHeaderError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from .models import *
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

@receiver(post_save, sender=User)
def account_creation_notification(sender, instance, created, **kwargs):
  """Send a mail to User after account creation"""
  if created:
    send_mail(
			subject = f'Welcome to Stesta!!!',
			message = f"""message\n""",
			from_email = settings.EMAIL_HOST_USER,
			recipient_list = [instance.email],
			fail_silently = False,
			html_message = render_to_string('email/account_creation_email.html', {
				'user': instance,
			})
		)
    logging.info('E-mail should have been sent to Stesta user')