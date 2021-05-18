# -*- coding: utf-8 -*-
from django.db import models
from products.models import Products
from brands.models import Brands
from item_category.models import ItemCategory
from item_group.models import ItemGroup
from item_category.models import Item
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField


# Create your models here.
class Coupon(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    vchr_coupon_code = models.CharField(max_length=30, blank=True, null=True)
    dat_expiry = models.DateField(blank=True, null=True)
    fk_product = models.ForeignKey(Products, models.DO_NOTHING, blank=True, null=True)
    fk_brand = models.ForeignKey(Brands, models.DO_NOTHING, blank=True, null=True)
    fk_item_category = models.ForeignKey(ItemCategory, models.DO_NOTHING, blank=True, null=True)
    fk_item_group = models.ForeignKey(ItemGroup, models.DO_NOTHING, blank=True, null=True)
    fk_item = models.ForeignKey(Item, models.DO_NOTHING, blank=True, null=True)
    int_discount_percentage = models.IntegerField(blank=True, null=True)
    bint_max_discount_amt = models.BigIntegerField(blank=True, null=True)
    bint_min_purchase_amt = models.BigIntegerField(blank=True, null=True)
    int_max_usage_no = models.IntegerField(blank=True, null=True)
    fk_updated = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True,related_name="coupon_user_created")
    fk_created = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True,related_name="coupon_user_updated")
    dat_created = models.DateTimeField(blank=True, null=True)
    dat_updated = models.DateTimeField(blank=True, null=True)
    int_which = models.IntegerField(blank=True, null=True)

    '''
        int_which denotes:

        0 - All
        1 - Product
        2 - Brand
        3 - ItemCategory
        4 - ItemGroup
        5 - Item

                    '''

    class Meta:
        managed = False
        db_table = 'coupon'


class StaffCouponMaster(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    fk_product = models.ForeignKey(Products, models.DO_NOTHING, blank=True, null=True)
    int_employee = models.SmallIntegerField(blank=True, null=True)
    int_not_employee = models.SmallIntegerField(blank=True, null=True)
    fk_created = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True,related_name='coupon_created')
    dat_created = models.DateTimeField(blank=True, null=True)
    fk_updated = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True,related_name='coupon_updated')
    dat_updated = models.DateTimeField(blank=True, null=True)
    int_status = models.SmallIntegerField(blank=True, null=True) # 1 active 0  inactive -1 deleted

    class Meta:
        managed = False
        db_table = 'staff_coupon_master'

class StaffCouponDetails(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    fk_master = models.ForeignKey(StaffCouponMaster, models.DO_NOTHING, blank=True, null=True)
    json_brand = JSONField(blank=True, null=True)  # This field type is a guess.
    json_item_category = JSONField(blank=True, null=True)  # This field type is a guess.
    json_item_group = JSONField(blank=True, null=True)  # This field type is a guess.
    dbl_discount_percent = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'staff_coupon_details'