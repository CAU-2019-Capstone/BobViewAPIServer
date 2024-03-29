# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser

class UserInfo(AbstractUser):
    # password = models.CharField(max_length=128)
    # last_login = models.DateTimeField(blank=True, null=True)
    # is_superuser = models.IntegerField()
    # username = models.CharField(unique=True, max_length=150)
    # first_name = models.CharField(max_length=30)
    # last_name = models.CharField(max_length=150)
    # email = models.CharField(max_length=254)
    # is_staff = models.IntegerField()
    # is_active = models.IntegerField()
    # date_joined = models.DateTimeField()
    is_owner = models.IntegerField(default=False)

    class Meta:
        managed = True
        db_table = 'user_info'


class RestaurantInfo(models.Model):
    owner = models.OneToOneField(UserInfo, on_delete=models.CASCADE)     # user_info와 일대일 관계
    # owner = models.ForeignKey(UserInfo, on_delete=models.CASCADE)     # user_info와 일대일 관계
    restaurant_name = models.CharField(primary_key=True, max_length=45)
    restaurant_gps = models.CharField(max_length=45)
    restaraunt_rating = models.FloatField(blank=True, null=True)
    restaurant_image = models.ImageField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'restaurant_info'


class Order(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)    # User와 대대일 관계
    order_id = models.CharField(primary_key=True, max_length=45)
    order_time = models.DateTimeField()
    tot_price = models.IntegerField()
    table_id = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'order'
        unique_together = (('user', 'order_id'),)


class MenuInfo(models.Model):
    restaurant = models.ForeignKey(RestaurantInfo, on_delete=models.CASCADE)    # restaurant_info와 다대일 관계
    menu_id = models.CharField(primary_key=True, max_length=45)
    menu_name = models.CharField(max_length=45)
    menu_price = models.IntegerField()
    menu_desc = models.TextField()
    menu_rating = models.FloatField(blank=True, null=True)
    menu_image = models.CharField(max_length=1024)

    class Meta:
        managed = True
        db_table = 'menu_info'


class OrderMenu(models.Model):
    order = models.ManyToManyField(Order)               # Order와 다대다 관계
    menu = models.ManyToManyField(MenuInfo)             # Menu Info와 다대다 관계
    menu_tot_price = models.IntegerField()
    menu_num = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'order_menu'
