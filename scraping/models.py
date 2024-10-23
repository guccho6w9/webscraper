from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()



class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=3)  
    url = models.URLField(max_length=1000)
    store = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    date_scrapping = models.DateTimeField(auto_now_add=True)
    img_url = models.URLField(max_length=500)
    discount = models.CharField(max_length=10)

    saved_by = models.ManyToManyField(User, blank=True, related_name='saved_products')

    def __str__(self):
        return self.name
    

class PriceHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_history')
    date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.product.name} - {self.price}"
    
