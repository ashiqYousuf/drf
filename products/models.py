import random

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse

User = settings.AUTH_USER_MODEL

TAG_MODEL_CHOICES = [
    'electronics',
    'cars',
    'notebook',
    'boats'
]


class ProductQuerySet(models.QuerySet):
    # Helps in chaining methods also
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
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, default=1, null=True, related_name='products')
    title = models.CharField(max_length=120)
    content = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=99.99)
    public = models.BooleanField(default=True)

    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.pk})

    @property
    def path(self):
        return f'/products/{self.pk}/'

    @property
    def body(self):
        return self.content

    def is_public(self) -> bool:
        return self.public

    def get_tags_list(self):
        return [random.choice(TAG_MODEL_CHOICES)]

    @property
    def sale_price(self):
        return "%.2f" % (float(self.price) * 0.8)

    def get_discount(self):
        return "%.2f" % (float(self.price) * 0.2)
