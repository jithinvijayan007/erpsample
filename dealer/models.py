from django.db import models
from category.models import Category
from item_category.models import TaxMaster
from django.contrib.auth.models import User
from category.models import OtherCategory

# Create your models here.

class Dealer(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    vchr_name = models.CharField(max_length=50, blank=True, null=True)
    dat_from = models.DateTimeField(blank=True, null=True)
    vchr_code = models.CharField(max_length=50, blank=True, null=True)
    int_credit_days = models.IntegerField(blank=True, null=True)
    bint_credit_limit = models.BigIntegerField(blank=True, null=True)
    int_po_expiry_days = models.IntegerField(blank=True, null=True)
    vchr_tin_no = models.CharField(max_length=50, blank=True, null=True)
    vchr_cst_no = models.CharField(max_length=50, blank=True, null=True)
    vchr_gstin = models.CharField(max_length=50, blank=True, null=True)
    vchr_gstin_status = models.CharField(max_length=50, blank=True, null=True)
    fk_category = models.ForeignKey(OtherCategory, models.DO_NOTHING, blank=True, null=True)
    fk_tax_class = models.ForeignKey(TaxMaster, models.DO_NOTHING, blank=True, null=True)
    vchr_account_group = models.CharField(max_length=50, blank=True, null=True)
    vchr_bank_account = models.CharField(max_length=50, blank=True, null=True)
    vchr_pan_no = models.CharField(max_length=50, blank=True, null=True)
    vchr_pan_status = models.CharField(max_length=50, blank=True, null=True)
    int_is_act_del = models.IntegerField(blank=True, null=True)
    fk_created = models.ForeignKey(User,models.DO_NOTHING, blank=True, null=True,related_name="dealer_created")
    fk_updated = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True,related_name="dealer_updated")
    dat_created = models.DateTimeField(blank=True, null=True)
    dat_updated = models.DateTimeField(blank=True, null=True)
    '''when is_act_del is     0, supplier is active, 2, supplier is de-active,
                          -1, supplier is deleted'''
    def __str__(self):
        return self.vchr_name
    class Meta:
        managed = False
        db_table = 'dealer'

class DealerAddress(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    vchr_address = models.CharField(max_length=180, blank=True, null=True)
    vchr_email = models.CharField(max_length=30, blank=True, null=True)
    bint_phone_no = models.BigIntegerField(blank=True, null=True)
    int_pincode = models.IntegerField(blank=True, null=True)
    fk_dealer = models.ForeignKey(Dealer, models.DO_NOTHING, blank=True, null=True)
    bln_status = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'dealer_address'

class DealerContactPerson(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    vchr_name = models.CharField(max_length=50, blank=True, null=True)
    vchr_designation = models.CharField(max_length=50, blank=True, null=True)
    vchr_department = models.CharField(max_length=50, blank=True, null=True)
    vchr_office = models.CharField(max_length=50, blank=True, null=True)
    bint_mobile_no1 = models.BigIntegerField(blank=True, null=True)
    bint_mobile_no2 = models.BigIntegerField(blank=True, null=True)
    fk_dealer = models.ForeignKey(Dealer, models.DO_NOTHING, blank=True, null=True)
    bln_status = models.NullBooleanField()

    def __str__(self):
        return self.vchr_name

    class Meta:
        managed = False
        db_table = 'dealer_contact_person'



class DealerLog(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    vchr_remarks = models.TextField(blank=True, null=True)
    vchr_status = models.CharField(max_length=20, blank=True, null=True)
    dat_created = models.DateTimeField(blank=True, null=True)
    fk_created = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    fk_dealer = models.ForeignKey(Dealer, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dealer_log'





# class OtherCategory(models.Model):
#     pk_bint_id = models.BigAutoField(primary_key=True)
#     vchr_name = models.CharField(max_length=50, blank=True, null=True)
#     int_status = models.IntegerField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'other_category'
