from django.db import models
from company.models import Company
from item_category.models import Item
from brands.models import Brands

# Create your models here.
class AddComboMaster(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    int_offer_type = models.IntegerField(blank=True, null=True) #itemwise =1, Brandwise =2 , AMountWise=3
    vchr_offer_name = models.CharField(max_length=100, blank=True, null=True)#name of the offer
    fk_item = models.ForeignKey(Item, models.DO_NOTHING, blank=True, null=True)#if discount based on items
    fk_brand = models.ForeignKey(Brands, models.DO_NOTHING, blank=True, null=True)#if discount based on Brands
    dbl_amt = models.FloatField(blank=True, null=True)#if discount on amount of purchase
    int_status = models.IntegerField(blank=True, null=True, default=0)#if offer created 0 edited 1 deleted -1
    int_quantity = models.IntegerField(blank=True, null=True) #quantity of item or brand
    dat_to = models.DateField(blank=True, null=True)
    dat_from = models.DateField(blank=True, null=True)
    fk_company = models.ForeignKey(Company, models.DO_NOTHING)
    class Meta:
        managed = False
        db_table = 'add_combo_master'

class AddComboDiscount(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    fk_master = models.ForeignKey(AddComboMaster, models.DO_NOTHING, blank=True, null=True)#points to AddComboMaster pk_bint_id
    int_discount_type = models.IntegerField(blank=True, null=True)#how to give discount [percentage=1, amount = 2 , item=3]
    dbl_amt = models.FloatField(blank=True, null=True)#if amount is giving as discount
    dbl_percent = models.FloatField(blank=True, null=True)#if percentage is giving as  discount

    class Meta:
        managed = False
        db_table = 'add_combo_discount'

#if items is giving as discount [AddComboDiscount.int_discount_type==3]
class AddComboDiscountItem(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    fk_master = models.ForeignKey(AddComboDiscount, models.DO_NOTHING, blank=True, null=True)#points to master AddComboDiscount.pk_bint_id
    int_quantity = models.IntegerField(blank=True, null=True)#quatity of item
    fk_item = models.ForeignKey(Item, models.DO_NOTHING, blank=True, null=True)#points to the item id
    dbl_amt = models.FloatField(blank=True, null=True)#if amount the giving item
    dbl_percent = models.FloatField(blank=True, null=True)#if percentage on the giving item

    class Meta:
        managed = False
        db_table = 'add_combo_discount_item'
