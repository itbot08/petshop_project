from django.db import models
from django.contrib.auth.models import User

class Items(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование")
    about = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=999999999, decimal_places=2, verbose_name="Цена")
    photo = models.ImageField(upload_to="photos", verbose_name="Фото", blank=True, null=True)
    is_published = models.BooleanField(default=True, verbose_name="Наличие")
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категория")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Категория")
    about = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

class User(User):
    class Meta:
        proxy = True
        verbose_name = u'Пользователи'
        verbose_name_plural = u'Пользователи'

class Reviews(models.Model):
    id_item = models.ForeignKey('Items', on_delete=models.PROTECT, verbose_name="ID_товара")
    id_user = models.ForeignKey('User', on_delete=models.PROTECT, verbose_name="ID_пользователя")

