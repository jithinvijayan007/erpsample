from django.db import models
from userdetails.models import UserDetails as Userdetails
from branch.models import Branch


# Create your models here.
class CaseClosureMaster(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    vchr_name = models.CharField(max_length=50)
    bln_active = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'case_closure_master'


class CaseClosureDetails(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    dat_created = models.DateTimeField(blank=True, null=True)
    dat_updated  = models.DateTimeField(blank=True, null=True)
    fk_created = models.ForeignKey(Userdetails, models.DO_NOTHING, blank=True, null=True,related_name="case_closure_fk_updated")
    fk_updated = models.ForeignKey(Userdetails, models.DO_NOTHING, blank=True, null=True,related_name="case_closure_fk_created")
    dbl_total_amount = models.FloatField(blank=True, null=True)
    json_case_closure = models.TextField(blank=True, null=True)  # This field type is a guess.
    int_status = models.IntegerField(blank=True, null=True) #1. open,2.confirm,3.rejects
    fk_branch = models.ForeignKey(Branch, models.DO_NOTHING)
    vchr_remark = models.CharField(max_length=100, blank=True, null=True)
    amount_status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'case_closure_details'
