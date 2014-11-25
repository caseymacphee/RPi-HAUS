from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# class TimeSeries(models.Model):
#     owner = models.ForeignKey(User, verbose_name="Owner of data",
#                               related_name='data', blank=True, null=True)
#     timestamp = models.DateTimeField("Time data point recorded", blank=True,
#                                      null=True)
#     value = models.DecimalField(max_digits=6, decimal_places=3,
#                                 verbose_name="Data point value")
