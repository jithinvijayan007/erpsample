from django.db import models
from department.models import Department
from job_position.models import JobPosition
from userdetails.models import ReligionCaste,UserDetails
from django.contrib.auth.models import User
# from user_model.models import UserDetails
from django.contrib.postgres.fields import JSONField
# Create your models here.


class BonusDetails(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    dbl_gross_from = models.FloatField(blank=True, null=True)
    dbl_gross_to = models.FloatField(blank=True, null=True)
    fk_dept = models.ForeignKey(Department, models.DO_NOTHING, blank=True, null=True)
    fk_desig = models.ForeignKey(JobPosition, models.DO_NOTHING, blank=True, null=True)
    fk_religion = models.ForeignKey(ReligionCaste, models.DO_NOTHING, blank=True, null=True)
    int_month = models.IntegerField(blank=True, null=True)
    int_year = models.IntegerField(blank=True, null=True)
    dbl_bonus_percent = models.FloatField(blank=True, null=True)
    int_bonus_over_type = models.IntegerField(blank=True, null=True)  #1.Gross Pay,2.Basic Pay+DA ,3.CTC
    int_consider_months = models.IntegerField(blank=True, null=True)
    int_eligibility_months = models.IntegerField(blank=True, null=True)
    vchr_bonus_name = models.CharField(max_length=200, blank=True, null=True)
    json_hold = JSONField(blank=True, null=True)
    json_employee = JSONField(blank=True, null=True)
    fk_created = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True,related_name = 'bonus_details_fk_created')
    fk_updated = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True,related_name = 'bonus_details_fk_updated')
    dat_created = models.DateTimeField(blank=True, null=True)
    dat_updated = models.DateTimeField(blank=True, null=True)
    int_status = models.IntegerField(blank=True, null=True)  # 1 if created, 0 if updated, -1 if deleted

    class Meta:
        managed = False
        db_table = 'bonus_details'
    def __str__(self):
        return self.vchr_bonus_name


class BonusPaid(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    fk_bonus = models.ForeignKey(BonusDetails, models.DO_NOTHING, blank=True, null=True)
    dat_paid = models.DateTimeField(blank=True, null=True)
    json_paid = JSONField(blank=True, null=True)
    fk_created = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    dat_created = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'bonus_paid'
    def __str__(self):
        return self.fk_bonus
