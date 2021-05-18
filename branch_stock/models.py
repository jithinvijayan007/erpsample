from django.db import models
from item_category.models import Item
from internal_stock.models import StockTransfer,IstDetails
from branch.models import Branch
from django.contrib.auth.models import User as AuthUser
from django.contrib.postgres.fields import JSONField
from purchase.models import GrnDetails
from userdetails.models import UserDetails as Userdetails

from products.models import Products


# Create your models here.
class BranchStockMaster(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    dat_stock = models.DateTimeField(blank=True, null=True)
    fk_branch = models.ForeignKey(Branch, models.DO_NOTHING, blank=True, null=True)
    fk_created = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    dbl_tax = models.FloatField(blank=True, null=True)
    dbl_amount = models.FloatField(blank=True, null=True)
    jsn_tax = JSONField(blank=True, null=True)  #  {CGST:4,SGST:4} ,tax total amount
    vchr_sap_doc_num = models.CharField(max_length=10, blank=True, null=True)
    dat_sap_doc_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'branch_stock_master'



class BranchStockDetails(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    fk_item = models.ForeignKey(Item, models.DO_NOTHING, blank=True, null=True)
    fk_master = models.ForeignKey(BranchStockMaster, models.DO_NOTHING, blank=True, null=True)
    int_qty = models.IntegerField(blank=True, null=True)
    jsn_imei = JSONField(blank=True, null=True)  # Available IMEI
    jsn_imei_avail = JSONField(blank=True, null=True)  # Available IMEI
    jsn_imei_dmgd = JSONField(blank=True, null=True)  # IMEI of Damaged items
    jsn_batch_no = JSONField(blank=True, null=True)
    fk_transfer_details = models.ForeignKey(IstDetails, models.DO_NOTHING, blank=True, null=True)
    int_received =models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False

        db_table = 'branch_stock_details'


class BranchStockImeiDetails(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    fk_details = models.ForeignKey(BranchStockDetails, models.DO_NOTHING, blank=True, null=True)
    fk_grn_details = models.ForeignKey(GrnDetails, models.DO_NOTHING, blank=True, null=True)
    jsn_imei = JSONField(blank=True, null=True)  # {"imei":[]}
    jsn_batch_no = JSONField(blank=True, null=True)  #  {"batch":[]}
    jsn_imei_reached = JSONField(blank=True, null=True)  #  {"imei":[]}
    jsn_batch_reached = JSONField(blank=True, null=True)  #  {"batch":[]}
    int_qty = models.IntegerField(blank=True, null=True)
    int_received =models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False

        db_table = 'branch_stock_imei_details'


class NonSaleable(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    fk_item = models.ForeignKey(Item, models.DO_NOTHING, blank=True, null=True)
    fk_branch = models.ForeignKey(Branch, models.DO_NOTHING, blank=True, null=True)
    dat_created = models.DateTimeField(blank=True, null=True)
    dat_updated = models.DateTimeField(blank=True, null=True)
    fk_created = models.ForeignKey(Userdetails, models.DO_NOTHING, blank=True, null=True ,related_name='creatednonsaleable')
    fk_updated = models.ForeignKey(Userdetails, models.DO_NOTHING, blank=True, null=True ,related_name='updatednonsaleable')
    int_status = models.IntegerField(blank=True, null=True)  # 0) active 1) not active
    jsn_non_saleable = JSONField(blank=True, null=True)  # List of non saleable imei
    jsn_status_change = JSONField(blank=True, null=True)  # List of imei which is updated to saleable
    vchr_remarks = models.TextField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'non_saleable'


class MailingProduct(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    vchr_name = models.CharField(max_length=100, blank=True, null=True)
    vchr_email = models.CharField(max_length=50, blank=True, null=True)
    fk_product = models.ForeignKey(Products, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mailing_product'
