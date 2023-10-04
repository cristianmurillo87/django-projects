import random

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet

# Create your models here.

User = settings.AUTH_USER_MODEL

TAGS_MODEL_VALUES = ["cars", "posts", "items", "shoes"]


class ProductQuerySet(models.QuerySet):
    def is_public(self):
        return self.filter(public=True)

    def search(self, query, user=None):
        lookup = Q(title__icontains=query) | Q(content__icontains=query)
        qs = self.is_public().filter(lookup)
        if user is not None:
            qs2 = self.filter(user=user).filter(lookup)
            qs = (qs | qs2).distinct()
        return qs


class ProductManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return ProductQuerySet(self.model, using=self._db)

    def search(self, query, user=None):
        return self.get_queryset().search(query, user=user)


class Product(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=99.99)
    public = models.BooleanField(default=True)
    # overrides the default objects property
    objects = ProductManager()

    def is_public(self):
        return self.public

    def get_discount(self):
        return float(self.price) * 0.3

    def get_sale_price(self):
        return float(self.price) - self.get_discount()

    def get_tags_list(self):
        return [random.choice(TAGS_MODEL_VALUES)]
