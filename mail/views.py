from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.utils import timezone
from mail.models import Addressees, Message, Mailing, SendMail
from mail.forms import AddresseesForm, MessageForm, MailingForm


# CRUD для получателей (Recipient)


class AddresseesListView(generic.ListView):
    model = Addressees
    context_object_name = "addressees"


class AddresseesCreateView(generic.CreateView):
    model = Addressees
    form_class = AddresseesForm
    success_url = reverse_lazy("mail.addressees_list")


class AddresseesUpdateView(generic.UpdateView):
    model = Addressees
    form_class = AddresseesForm
    success_url = reverse_lazy("mail.addressees_list")


class AddresseesDeleteView(generic.DeleteView):
    model = Addressees
    success_url = reverse_lazy("mail.addressees_list")


# CRUD для сообщений (Message)


class MessageListView(generic.ListView):
    model = Message
    context_object_name = "message"


class MessageDetailView(generic.DetailView):
    model = Message


class MessageCreateView(generic.CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mail.message_list")


class MessageUpdateView(generic.UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mail.message_list")


class MessageDeleteView(generic.DeleteView):
    model = Message
    success_url = reverse_lazy("mail.message_list")


# CRUD для рассылок (Mailing)


class MailingListView(generic.ListView):
    model = Mailing
    context_object_name = "mailing"


class MailingCreateView(generic.CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mail.mailing_list")


class MailingDetailView(generic.DetailView):
    model = Mailing


class MailingUpdateView(generic.UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mail.mailing_list")


class MailingDeleteView(generic.DeleteView):
    model = Mailing
    success_url = reverse_lazy("mail.mailing_list")


# Генерация отчета и отправка рассылки


class SendMailView(generic.View):
    def post(self, request, mailing_id):
        mailing = self.get_object(mailing_id)
        addressees = mailing.addressees.all()

        # Инициация отправки
        for addressee in addressees:
            try:
                send_mail(
                    mailing.message.str_text,
                    mailing.message.text,
                    "from@example.com",  # email from
                    [addressee.email],
                    fail_silently=False,
                )
                status = "Успешно"
                server_answer = "Письмо отправлено успешно."
            except Exception as e:
                status = "Не успешно"
                server_answer = str(e)

            # Сохранение попытки рассылки
            SendMail.objects.create(
                mailing=mailing, status=status, server_response=server_answer
            )

        # Обновление статуса рассылки
        if mailing.status == "Создана":
            mailing.status = "Запущена"
            mailing.first_date_send = timezone.now()
            mailing.save()

        return render(request, "mailing_status.html", {"mailing": mailing})

    def get_object(self, mailing_id):
        return Mailing.objects.get(pk=mailing_id)


# Главная страница


class HomeView(generic.TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_mailings"] = Mailing.objects.count()
        context["active_mailings"] = Mailing.objects.filter(status="Запущена").count()
        context["unique_addressees"] = Addressees.objects.count()
        return context
