from django.db import models

class Product(models.Model):
    product_code = models.CharField(max_length=100, unique=True)
    brand = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    stock = models.IntegerField()

    def __str__(self):
        return self.name

class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prices')
    date = models.DateTimeField()
    value = models.FloatField()

    def __str__(self):
        return f"{self.product.name} - {self.date}"
