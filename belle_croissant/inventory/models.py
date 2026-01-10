from django.db import models
from products.models import Product

class Ingredient(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Килограмм'),
        ('g', 'Грамм'),
        ('l', 'Литр'),
        ('ml', 'Миллилитр'),
        ('pcs', 'Штуки'),
    ]
    
    name = models.CharField('Название', max_length=200)
    unit = models.CharField('Единица измерения', max_length=10, choices=UNIT_CHOICES)
    current_stock = models.DecimalField('Текущий запас', max_digits=10, decimal_places=2)
    min_stock = models.DecimalField('Минимальный запас', max_digits=10, decimal_places=2)
    max_stock = models.DecimalField('Максимальный запас', max_digits=10, decimal_places=2)
    cost_per_unit = models.DecimalField('Стоимость за единицу', max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
    
    def __str__(self):
        return f"{self.name} ({self.current_stock} {self.unit})"
    
    @property
    def needs_restock(self):
        return self.current_stock <= self.min_stock

class ProductIngredient(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Продукт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        verbose_name='Ингредиент'
    )
    quantity = models.DecimalField('Количество', max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'Ингредиент продукта'
        verbose_name_plural = 'Ингредиенты продуктов'
        unique_together = ['product', 'ingredient']
    
    def __str__(self):
        return f"{self.product.name}: {self.ingredient.name}"