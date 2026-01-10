from django.db import models

class Category(models.Model):
    name = models.CharField('Название', max_length=100)
    description = models.TextField('Описание', blank=True)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Категория'
    )
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    cost = models.DecimalField('Себестоимость', max_digits=10, decimal_places=2)
    image = models.ImageField('Изображение', upload_to='products/', blank=True)
    is_available = models.BooleanField('В наличии', default=True)
    preparation_time = models.IntegerField('Время приготовления (мин)', default=0)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['category', 'name']
    
    def __str__(self):
        return self.name