from django.db import models
from company.models import Company
# Create your models here.
class Brands(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    vchr_code = models.CharField(max_length=50, blank=True, null=True)
    vchr_name = models.CharField(max_length=150, blank=True, null=True)
    int_status = models.IntegerField(default=1,blank=True, null=True) # 0. Active -1. delete,
    fk_company = models.ForeignKey(Company, models.DO_NOTHING, blank=True, null=True, default=1)

    class Meta:
        managed = False
        db_table = 'brands'
