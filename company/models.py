from django.db import models

# Create your models here.
class Company(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    vchr_name = models.CharField(max_length=50)
    vchr_address = models.CharField(max_length=250, blank=True, null=True)
    vchr_gstin = models.CharField(max_length=50)
    vchr_mail = models.CharField(max_length=150, blank=True, null=True)
    vchr_phone = models.CharField(max_length=25, blank=True, null=True)
    vchr_logo = models.CharField(max_length=350, blank=True, null=True)
    vchr_print_logo = models.CharField(max_length=350, blank=True, null=True)
    int_status = models.IntegerField(default = 0)# 0. Active -1. delete,
    vchr_fin_type = models.CharField(max_length=10,blank=True,null=True)

    class Meta:
        managed = False
        db_table = 'company'

class FinancialYear(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    vchr_type = models.CharField(max_length=20, blank=True, null=True)
    int_year = models.IntegerField(blank=True, null=True)
    dat_start = models.DateTimeField(blank=True, null=True)
    dat_end = models.DateTimeField(blank=True, null=True)
    bln_status = models.NullBooleanField()

    class Meta:
        managed = False

        db_table = 'financial_year'
