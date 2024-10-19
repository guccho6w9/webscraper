from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=50)
    url = models.URLField(max_length=200)
    store = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    date_scrapping = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name