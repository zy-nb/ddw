# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class DCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    category_id = models.CharField(max_length=20, blank=True, null=True)
    category_pid = models.CharField(max_length=20, blank=True, null=True)
    book_number = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'd_category'


class DOrderltem(models.Model):
    shop_id = models.CharField(primary_key=True, max_length=50)
    shop_num = models.CharField(max_length=50)
    total_price = models.CharField(max_length=50, blank=True, null=True)
    shop_bookid = models.ForeignKey('TBook', models.DO_NOTHING, db_column='shop_bookid')
    shop_ordlid = models.ForeignKey('TOrder', models.DO_NOTHING, db_column='shop_ordlid',null=True)

    class Meta:
        managed = False
        db_table = 'd_orderltem'




class Shoppingcart(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    book_number = models.CharField(max_length=20, blank=True, null=True)
    bookid = models.ForeignKey('TBook', models.DO_NOTHING, db_column='BookId', blank=True, null=True)  # Field name made lowercase.
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shoppingcart'


class TAddress(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=20)
    site = models.CharField(max_length=100)
    region = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=20, blank=True)
    number = models.CharField(max_length=20, blank=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 't_address'


class TBook(models.Model):
    book_id = models.CharField(primary_key=True, max_length=20)
    book_name = models.CharField(max_length=20)
    book_author = models.CharField(max_length=20)
    book_publish = models.CharField(max_length=20)
    publish_time = models.CharField(max_length=20, blank=True, null=True)
    revision = models.CharField(max_length=20, blank=True, null=True)
    book_isbn = models.CharField(max_length=20, blank=True, null=True)
    word_count = models.CharField(max_length=20, blank=True, null=True)
    page_count = models.CharField(max_length=20, blank=True, null=True)
    open_count = models.CharField(max_length=20, blank=True, null=True)
    book_paper = models.CharField(max_length=20, blank=True, null=True)
    book_wrapper = models.CharField(max_length=20, blank=True, null=True)
    book_category = models.ForeignKey(DCategory, models.DO_NOTHING, db_column='book_category', blank=True, null=True)
    book_price = models.FloatField(blank=True, null=True)
    book_dprice = models.FloatField(blank=True, null=True)
    editor_recomme = models.TextField(blank=True, null=True)
    content_introdu = models.TextField(blank=True, null=True)
    author_introd = models.TextField(blank=True, null=True)
    menu = models.TextField(blank=True, null=True)
    media_review = models.TextField(blank=True, null=True)
    digest_image = models.TextField(blank=True, null=True)
    product_image_path = models.CharField(max_length=200, blank=True, null=True)
    series_name = models.CharField(max_length=20, blank=True, null=True)
    printing_time = models.CharField(max_length=200, blank=True, null=True)
    impression = models.CharField(max_length=20, blank=True, null=True)
    stock = models.CharField(max_length=20, blank=True, null=True)
    customer_socre = models.CharField(max_length=20, blank=True, null=True)
    shelves_date = models.DateField(blank=True, null=True)
    book_status = models.CharField(max_length=20, blank=True, null=True)
    sales = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_book'


class TOrder(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    num = models.CharField(max_length=50, blank=True, null=True)
    create_date = models.CharField(max_length=50, blank=True, null=True)
    price = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    order_addrid = models.ForeignKey(TAddress, models.DO_NOTHING, db_column='order_addrid',null=True)
    order_uid = models.ForeignKey('TUser', models.DO_NOTHING, db_column='order_uid',null=True)

    class Meta:
        managed = False
        db_table = 't_order'


class TUser(models.Model):
    user_id = models.CharField(primary_key=True, max_length=20)
    user_email = models.CharField(max_length=20)
    user_password = models.CharField(max_length=100)
    user_name = models.CharField(max_length=20)
    user_status = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 't_user'
