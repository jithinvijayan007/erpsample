from django.db import models
from userdetails.models import UserDetails as Userdetails
from branch.models import Branch

# Create your models here.
class DayClosureMaster(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    vchr_name = models.CharField(max_length=50) #note value
    bln_active = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'day_closure_master'

class DayClosureDetails(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    dat_time = models.DateTimeField(blank=True, null=True)#date with time
    fk_staff = models.ForeignKey(Userdetails, models.DO_NOTHING, blank=True, null=True)
    total_amount = models.FloatField(blank=True, null=True)
    json_dayclosure = models.TextField(blank=True, null=True)  # This field type is a guess. #note and its count of numbers
    int_closed = models.IntegerField(blank=True, null=True) #0 for open , 1 for closed, 2 for not tally , 3 for not tally and mail requested to ho ,4 rejected by HO
    fk_branch = models.ForeignKey(Branch, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'day_closure_details'


class DayClosureNotTally(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    fk_day_closure_details = models.ForeignKey(DayClosureDetails, models.DO_NOTHING, blank=True, null=True)
    dat_time = models.DateTimeField(blank=True, null=True)
    fk_staff = models.ForeignKey(Userdetails, models.DO_NOTHING, blank=True, null=True,related_name="day_closure_staff")
    fk_approve = models.ForeignKey(Userdetails, models.DO_NOTHING, blank=True, null=True,related_name="day_closure_approve") #aprove or rejected staff id
    total_amount = models.FloatField(blank=True, null=True)
    json_dayclosure = models.TextField(blank=True, null=True)  # This field type is a guess.
    int_status = models.IntegerField() #1 - not tally, 2-tally by staff 3-approved by HO 4-rejected
    fk_branch = models.ForeignKey(Branch, models.DO_NOTHING)
    vchr_remark = models.CharField(max_length=100, blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'day_closure_not_tally'
