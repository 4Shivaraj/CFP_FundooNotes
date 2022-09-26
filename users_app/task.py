from django.conf import settings
from django.core.mail import send_mail
from rest_framework.reverse import reverse
from celery import shared_task
from time import sleep


@shared_task()  # this to create tasks that'll work for any app environment.
def send_email_task(token, email_id):
    """Sends an email if user registered using celery."""
    # sleep(5)
    send_mail(subject="User Registration using celery",
              message=settings.BASE_URL +
              reverse('verify_token', kwargs={"token": token}),
              from_email=None,
              recipient_list=email_id,
              fail_silently=False,
              )
