from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from mail.models import Mailing, SendMail


class Command(BaseCommand):
    help = "Отправка рассылок получателям"

    def handle(self, *args, **kwargs):
        mailings = Mailing.objects.filter(status_in=['created', 'started'])
        for mail in mailings:
            for addressees in mail.recipients.all():
                try:
                    send_mail(
                        mail.message.str_text,
                        mail.message.text,
                        from_email=EMAIL_HOST_USER,
                        recipient_list=[addressees.email],
                        fail_silently=False,
                    )
                    SendMail.objects.create(
                        date_attempt=timezone.now(),
                        status='status_ok',
                        server_response="Email отправлен",
                        campaign=mail,
                    )
                    print(f"Сообщение {mail.message.str_text} успешно отправлено на  {addressees.email}")
                except Exception as e:
                    SendMail.objects.create(
                        date_attempt=timezone.now(),
                        status='status_nok',
                        server_response=str(e),
                        mail=mail,
                    )
                    print(str(e))
            mail.save()