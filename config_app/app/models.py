from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField


# class Ticker(models.Model):
#     ticker_id = models.(primary_key=True)
#     name = models.CharField(max_length=10)
#     values = ArrayField(models.CharField(max_length=10), size=5)
#
#
# class Config(models.Model):
#     chat_id = models.IntegerField()
#     print_all_tickers = models.BooleanField()
#     tickers = models.ForeignKey('Ticker', on_delete=models.CASCADE)
#     token = models.CharField(max_length=50)
#     interval = models.IntegerField()
