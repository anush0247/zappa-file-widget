=============================
Django Zappa File Widget
=============================

[![pypi-version]][pypi]

Django Admin File Wiget for Zappa based admin panels

Documentation
-------------

The full documentation is at https://zappa-file-widget.readthedocs.org.

Quickstart
----------

Install Django Zappa File Widget::

    pip install zappa-file-widget

Then use it in a project::

``settings.py``

```py

INSTALLED_APPS += "zappa_file_widget"

```

``models.py``

```python

from django.db import models


class Order(models.Model):
    attachment = models.FileField(upload_to="media/")
    ordered_by = models.CharField(max_length=20)

    def __unicode__(self):
        return unicode(self.attachment)


```

``admin.py``

```python

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

```

```sh
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```


Point your browser at : [http://127.0.0.1:8000/admin/example/order/](http://127.0.0.1:8000/admin/example/order/)


Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
