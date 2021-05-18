from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    vchr_code = models.CharField(unique=True, max_length=30, blank=True,null=True)
    vchr_name = models.CharField(max_length=30, blank=True, null=True)
    int_status = models.IntegerField(blank=True, null=True)# 0. Active -1. delete,
    fk_created = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True,related_name='category_fk_created')
    fk_updated = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True,related_name='category_fk_updated')
    dat_created = models.DateTimeField(blank=True, null=True)
    dat_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'

class EmpCategory(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    vchr_code = models.CharField(unique=True, max_length=30, blank=True,null=True)
    vchr_name = models.CharField(max_length=30, blank=True, null=True)
    int_status = models.IntegerField(blank=True, null=True)# 0. Active -1. delete,
    fk_created = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True,related_name='emp_category_fk_created')
    fk_updated = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True,related_name='emp_category_fk_updated')
    dat_created = models.DateTimeField(blank=True, null=True)
    dat_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'emp_category'


class OtherCategory(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    vchr_name = models.CharField(max_length=50, blank=True, null=True)
    int_status = models.IntegerField(blank=True, null=True) #1 dealer  2 supplier 3 branch

    class Meta:
        managed = False
        db_table = 'other_category'
