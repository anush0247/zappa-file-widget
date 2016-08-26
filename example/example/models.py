from django.db import models


class Order(models.Model):
    attachment = models.FileField(upload_to="media/")
    ordered_by = models.CharField(max_length=20)

    def __unicode__(self):
        return unicode(self.attachment)