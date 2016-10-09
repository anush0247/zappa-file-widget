=============================
Django Zappa File Widget
=============================

[![pypi-version]][pypi]

Django Admin File Wiget for [django-zappa](https://github.com/Miserlou/django-zappa) based admin panels

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
    attachment = models.FileField(upload_to="media/") # file size < 1 MB
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

Zappa URL Widget:
-----------------

As AWS API Gateway has char limit on request payload we can't send a file size more that 1 MB. 
We have implemented client size solution to upload files direct to s3 and save the URL in Server


``models.py``

```python

from django.db import models


class Order(models.Model):
    attachement2 = models.URLField() # file size >= 1 MB
    ordered_by = models.CharField(max_length=20)

    def __unicode__(self):
        return unicode(self.attachment)


```

``admin.py``

```python

from django import forms
from django.contrib import admin

from zappa_file_widget.url_widget import URLWidget
from django_custom_admin.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        widgets = {
            'attachment2':  URLWidget(upload_to="child_profile_pic/"), 
        }


class OrderAdmin(admin.ModelAdmin):
    form = OrderForm


admin.site.register(Order, OrderAdmin)

```

``Sample S3 Bucket ACLs to support Uploads from java script sdk / clients``

```xml
<?xml version="1.0" encoding="UTF-8"?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
    <CORSRule>
        <AllowedOrigin>*</AllowedOrigin>
        <AllowedMethod>GET</AllowedMethod>
        <MaxAgeSeconds>3000</MaxAgeSeconds>
        <AllowedHeader>Authorization</AllowedHeader>
    </CORSRule>
    <CORSRule>
        <AllowedOrigin>*</AllowedOrigin>
        <AllowedMethod>HEAD</AllowedMethod>
        <AllowedMethod>GET</AllowedMethod>
        <AllowedMethod>PUT</AllowedMethod>
        <AllowedMethod>POST</AllowedMethod>
        <AllowedMethod>DELETE</AllowedMethod>
        <ExposeHeader>ETag</ExposeHeader>
        <ExposeHeader>x-amz-meta-custom-header</ExposeHeader>
        <AllowedHeader>*</AllowedHeader>
    </CORSRule>
</CORSConfiguration>
```

Common Configuration:
---------------------

``settings.py``

```
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_CLOUDFRONT_DOMAIN = os.environ.get("AWS_CLOUDFRONT_DOMAIN")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
```

* Follow [https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/](https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/) to Configure S3 Static / Media storage files 
* Follow [http://stackoverflow.com/questions/31357353/using-cloudfront-with-django-s3boto](http://stackoverflow.com/questions/31357353/using-cloudfront-with-django-s3boto) to enable cloudfront for your static / media storage


Example:
--------

```sh
git clone https://github.com/anush0247/zappa-file-widget
cd zappa-file-widget/example
mkvirtualenv zappa_file_widget
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Point your browser at : [http://127.0.0.1:8000/admin/example/order/](http://127.0.0.1:8000/admin/example/order/)

Other Projects:
---------------

* [https://github.com/anush0247/django-fine-uploader-s3](https://github.com/anush0247/django-fine-uploader-s3)


Credits
---------

Tools used in rendering this package:

*  https://github.com/audreyr/cookiecutter
*  https://github.com/pydanny/cookiecutter-djangopackage


[pypi-version]: https://img.shields.io/pypi/v/zappa-file-widget.svg
[pypi]: https://pypi.python.org/pypi/zappa-file-widget
