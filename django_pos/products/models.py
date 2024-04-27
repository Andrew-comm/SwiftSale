from django.db import models
from django.forms import model_to_dict

class Category(models.Model):
    STATUS_CHOICES = (
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive")
    )

    name = models.CharField(max_length=256)
    description = models.TextField(max_length=256)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=100,
        verbose_name="Status of the category",
    )

    class Meta:
        db_table = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='subcategories',
        on_delete=models.CASCADE,  # Delete related products when deleted
        null=True,
    )
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    STATUS_CHOICES = (
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive")
    )

    name = models.CharField(max_length=256)
    description = models.TextField(max_length=256)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=100,
        verbose_name="Status of the product",
    )
    category = models.ForeignKey(
        Category,
        related_name="category",
        on_delete=models.SET_NULL,  # Set to SET_NULL for deleting product
        db_column='category',
        null=True,
    )
    subcategory = models.ForeignKey(
        SubCategory,
        related_name="products",
        on_delete=models.SET_NULL,  # Set to SET_NULL for deleting product
        db_column="subcategory",
        blank=True,
        null=True,
    )
    buying_price = models.FloatField(default=0)
    price = models.FloatField(default=0)
    stock = models.PositiveIntegerField(default=0)  # New field for stock count


    class Meta:
        db_table = "Product"

    def __str__(self) -> str:
        return self.name

    def to_json(self):
        item = model_to_dict(self)
        item['id'] = self.id
        item['text'] = self.name
        item['category'] = self.category.name
        item['quantity'] = 1
        item['total_product'] = 0
        return item
