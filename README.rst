=============================
Django Zappa File Widget
=============================

.. image:: https://badge.fury.io/py/zappa-file-widget.png
:target: https://badge.fury.io/py/zappa-file-widget

Django Admin File Wiget for [django-zappa](https://github.com/Miserlou/django-zappa) based admin panels

Quickstart
----------

Install Django Zappa File Widget::

pip install zappa-file-widget

Then use it in a project::

settings.py
-----------

.. code:: py


    INSTALLED_APPS += "zappa_file_widget"

models.py
---------

.. code:: python


    from django.db import models


    class Order(models.Model):
    attachment = models.FileField(upload_to="media/")
    ordered_by = models.CharField(max_length=20)

    def __unicode__(self):
    return unicode(self.attachment)

admin.py
--------

.. code:: python


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

.. code:: sh

    git clone https://github.com/anush0247/zappa-file-widget
    cd zappa-file-widget/example
    mkvirtualenv zappa_file_widget
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

Point your browser at : http://127.0.0.1:8000/admin/example/order/

Credits
-------

Tools used in rendering this package:

-  https://github.com/audreyr/cookiecutter
-  https://github.com/pydanny/cookiecutter-djangopackage

