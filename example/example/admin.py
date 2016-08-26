from django import forms
from django.contrib import admin

from zappa_file_widget.file_widget import FileWidget
from django_custom_admin.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        widgets = {
            'attachment': FileWidget(),
        }


class OrderAdmin(admin.ModelAdmin):
    form = OrderForm


admin.site.register(Order, OrderAdmin)
