from django.contrib import admin

from orderapp.models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['tg_username', 'first_name', 'tg_chat_id']
