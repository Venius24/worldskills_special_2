# Belle Croissant Lyonnais - Django MVP Project
# Структура проекта и основные файлы

# ============================================================================
# 1. requirements.txt
# ============================================================================
"""
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.0
Pillow==10.1.0
python-decouple==3.8
psycopg2-binary==2.9.9
"""

# ============================================================================
# 2. belle_croissant/settings.py
# ============================================================================
"""
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-change-in-production')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'customers',
    'products',
    'orders',
    'inventory',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'belle_croissant.urls'
WSGI_APPLICATION = 'belle_croissant.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Asia/Almaty'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

CORS_ALLOW_ALL_ORIGINS = True
"""

# ============================================================================
# 3. customers/models.py - Модели для управления клиентами
# ============================================================================
"""
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
"""

# ============================================================================
# 4. products/models.py - Модели продуктов
# ============================================================================
"""
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
"""

# ============================================================================
# 5. orders/models.py - Модели заказов
# ============================================================================
"""
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
"""

# ============================================================================
# 6. inventory/models.py - Модели инвентаря
# ============================================================================
"""
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
"""

# ============================================================================
# 7. customers/serializers.py - API Сериализаторы
# ============================================================================
"""
from rest_framework import serializers
from .models import Customer, LoyaltyProgram

class LoyaltyProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyProgram
        fields = ['points', 'tier', 'joined_date']

class CustomerSerializer(serializers.ModelSerializer):
    loyalty = LoyaltyProgramSerializer(read_only=True)
    
    class Meta:
        model = Customer
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone',
            'customer_type', 'registration_date', 'birth_date',
            'address', 'is_active', 'loyalty'
        ]
        read_only_fields = ['id', 'registration_date']
    
    def validate_email(self, value):
        if Customer.objects.filter(email=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("Клиент с таким email уже существует.")
        return value
"""

# ============================================================================
# 8. customers/views.py - API Views
# ============================================================================
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Customer
from .serializers import CustomerSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
    @action(detail=True, methods=['get'])
    def orders(self, request, pk=None):
        customer = self.get_object()
        orders = customer.orders.all()
        return Response({
            'customer': CustomerSerializer(customer).data,
            'orders_count': orders.count(),
            'total_spent': sum(order.final_amount for order in orders)
        })
    
    @action(detail=False, methods=['get'])
    def loyalty_members(self, request):
        members = Customer.objects.filter(customer_type='loyalty')
        serializer = self.get_serializer(members, many=True)
        return Response(serializer.data)
"""

# ============================================================================
# 9. belle_croissant/urls.py - URL Configuration
# ============================================================================
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from customers.views import CustomerViewSet

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""

# ============================================================================
# 10. Команды для запуска проекта
# ============================================================================
"""
# Создание структуры проекта:
django-admin startproject belle_croissant .
python manage.py startapp customers
python manage.py startapp products
python manage.py startapp orders
python manage.py startapp inventory

# Установка зависимостей:
pip install -r requirements.txt

# Миграции:
python manage.py makemigrations
python manage.py migrate

# Создание суперпользователя:
python manage.py createsuperuser

# Запуск сервера:
python manage.py runserver

# API будет доступен по адресу:
# http://localhost:8000/api/customers/
"""