# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Product(models.Model):
    pid = models.TextField()
    date = models.DateField(auto_now=True)
    shop = models.ForeignKey(User)
    name = models.TextField()
    price = models.TextField()
    description = models.TextField()
