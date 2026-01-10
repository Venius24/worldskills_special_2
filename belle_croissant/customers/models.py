from django.db import models
from django.core.validators import EmailValidator, RegexValidator

class Customer(models.Model):
    CUSTOMER_TYPE_CHOICES = [
        ('regular', 'Обычный'),
        ('loyalty', 'Участник программы лояльности'),
        ('corporate', 'Корпоративный'),
    ]
    
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    email = models.EmailField('Email', unique=True, validators=[EmailValidator()])
    phone = models.CharField(
        'Телефон', 
        max_length=20,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')]
    )
    customer_type = models.CharField(
        'Тип клиента',
        max_length=20,
        choices=CUSTOMER_TYPE_CHOICES,
        default='regular'
    )
    registration_date = models.DateTimeField('Дата регистрации', auto_now_add=True)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    address = models.TextField('Адрес', blank=True)
    is_active = models.BooleanField('Активен', default=True)
    
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['-registration_date']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class LoyaltyProgram(models.Model):
    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
        related_name='loyalty',
        verbose_name='Клиент'
    )
    points = models.IntegerField('Баллы', default=0)
    tier = models.CharField(
        'Уровень',
        max_length=20,
        choices=[
            ('bronze', 'Бронзовый'),
            ('silver', 'Серебряный'),
            ('gold', 'Золотой'),
        ],
        default='bronze'
    )
    joined_date = models.DateTimeField('Дата вступления', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Программа лояльности'
        verbose_name_plural = 'Программы лояльности'
    
    def __str__(self):
        return f"{self.customer} - {self.points} баллов"