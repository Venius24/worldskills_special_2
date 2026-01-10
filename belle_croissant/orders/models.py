from django.db import models
from customers.models import Customer
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('preparing', 'Готовится'),
        ('ready', 'Готов'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    ]
    
    ORDER_TYPE_CHOICES = [
        ('in_store', 'В магазине'),
        ('online', 'Онлайн'),
        ('delivery', 'Доставка'),
    ]
    
    order_number = models.CharField('Номер заказа', max_length=20, unique=True)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='Клиент',
        null=True,
        blank=True
    )
    order_type = models.CharField(
        'Тип заказа',
        max_length=20,
        choices=ORDER_TYPE_CHOICES,
        default='in_store'
    )
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    total_amount = models.DecimalField('Общая сумма', max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField('Скидка', max_digits=10, decimal_places=2, default=0)
    final_amount = models.DecimalField('Итоговая сумма', max_digits=10, decimal_places=2)
    notes = models.TextField('Примечания', blank=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлен', auto_now=True)
    completed_at = models.DateTimeField('Завершен', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Заказ {self.order_number}"

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name='Продукт'
    )
    quantity = models.PositiveIntegerField('Количество')
    unit_price = models.DecimalField('Цена за единицу', max_digits=10, decimal_places=2)
    total_price = models.DecimalField('Общая цена', max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"