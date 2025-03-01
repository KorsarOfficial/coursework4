from django.db import models
from users.models import User

class Addressees(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.email


class Message(models.Model):
    str_text = models.CharField(
        max_length=255,
        verbose_name="Тема сообщения",
        help_text="Введите тему сообщения",
    )
    text = models.TextField(
        verbose_name="Тело сообщения", help_text="Введите текст сообщения"
    )

    def __str__(self):
        return self.str_text


    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        ordering = ["id"]
        permissions = [
            ("view_all_addressees", "Can view all addressees"),
        ]


class Mailing(models.Model):
    STATUS_CHOICES = [
        ("Создана", "Создана"),
        ("Запущена", "Запущена"),
        ("Завершена", "Завершена"),
    ]

    first_date_send = models.DateTimeField(null=True, blank=True)
    end_date_send = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Создана")
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    addressees = models.ManyToManyField(Addressees)

    def __str__(self):
        return f"{self.message.str_text} - {self.status}"


class SendMail(models.Model):
    STATUS_CHOICES = [("Успешно", "Успешно"), ("Не успешно", "Не успешно")]

    time_deal = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    server_answer = models.TextField(blank=True)
    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, related_name="send_mail"
    )

    def __str__(self):
        return f"send_mail: {self.time_deal} - {self.status}"
