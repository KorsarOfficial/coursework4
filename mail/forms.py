from django import forms
from .models import Addressees, Message, Mailing


class AddresseesForm(forms.ModelForm):
    class Meta:
        model = Addressees
        fields = ["email", "full_name", "comment"]


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["str_text", "text"]


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["end_date_send", "message", "addressees"]
