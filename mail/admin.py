from django.contrib import admin
from .models import Message, Mailing, Addressees


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "str_text",
    )
    search_fields = ("str_text",)


@admin.register(Mailing)
class CampaignAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
    )
    search_fields = ("status",)


@admin.register(Addressees)
class AddresseesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
    )
    search_fields = ("full_name",)
