from django.db import models
from userdetails.models import UserDetails
# Create your models here.
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User

class PunchingEmp(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    vchr_user_log_id = models.CharField(max_length=256, blank=True, null=True)
    fk_user = models.ForeignKey(UserDetails, models.DO_NOTHING, blank=True, null=True)
    int_active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'punching_emp'

    def __str__(self):
        if self.fk_user_id:
            return self.fk_user.first_name+' '+self.fk_user.last_name
        else:
            return self.vchr_user_log_id


class PunchLog(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    fk_punchingemp = models.ForeignKey('PunchingEmp', models.DO_NOTHING, blank=True, null=True)
    fk_shift = models.ForeignKey('shift_schedule.ShiftSchedule', models.DO_NOTHING, blank=True, null=True)
    int_start_device_id = models.IntegerField(blank=True, null=True)
    dat_start = models.DateTimeField(blank=True, null=True)
    int_end_device_id = models.IntegerField(blank=True, null=True)
    dat_end = models.DateTimeField(blank=True, null=True)
    dat_punch = models.DateField(blank=True, null=True)
    dur_active = models.DurationField(blank=True, null=True)
    vchr_direction = models.CharField(max_length=5, blank=True, null=True)
    int_ellc = models.IntegerField(blank=True, null=True)
    bln_manual = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'punch_log'

    def __str__(self):
        if self.fk_punchingemp.fk_user:
            return self.fk_punchingemp.fk_user.first_name+' '+self.fk_punchingemp.fk_user.last_name
        else:
            self.fk_punchingemp.vchr_user_log_id


class PunchLogDetail(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    fk_log = models.ForeignKey('PunchLog', models.DO_NOTHING, blank=True, null=True)
    int_start_device_id = models.IntegerField(blank=True, null=True)
    tim_start = models.TimeField(blank=True, null=True)
    int_end_device_id = models.IntegerField(blank=True, null=True)
    tim_end = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'punch_log_detail'

    def __str__(self):
        if self.fk_log.fk_punchingemp.fk_user:
            return self.fk_log.fk_punchingemp.fk_user.first_name+' '+self.fk_log.fk_punchingemp.fk_user.last_name
        else:
            self.fk_log.fk_punchingemp.vchr_user_log_id


class TriggerErrorLog(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    int_device_id = models.BigIntegerField(blank=True, null=True)
    vchr_user_id = models.CharField(max_length=256, blank=True, null=True)
    dat_time_punch = models.DateTimeField(blank=True, null=True)
    txt_error = models.TextField(blank=True, null=True)
    dat_error = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'trigger_error_log'

    def __str__(self):
        return self.dat_error


# iclock DATABASE TABLE
from datetime import datetime
class Employees(models.Model):
    employeeid = models.AutoField(primary_key=True)
    employeename = models.CharField(max_length=256)
    employeecode = models.CharField(primary_key=True, max_length=50)
    stringcode = models.CharField(max_length=50)
    numericcode = models.IntegerField()
    gender = models.CharField(max_length=10, default='Male')
    companyid = models.IntegerField(default=1)
    doj = models.DateTimeField(blank=True, null=True, default=datetime.strptime('1900-01-01','%Y-%m-%d'))
    dor = models.DateTimeField(blank=True, null=True, default=datetime.strptime('3000-01-01','%Y-%m-%d'))
    doc = models.DateTimeField(blank=True, null=True, default=datetime.strptime('1900-01-01','%Y-%m-%d'))
    departmentid = models.IntegerField(default=1)
    categoryid = models.IntegerField(default=1)
    employeecodeindevice = models.CharField(unique=True, max_length=50)
    employementtype = models.CharField(max_length=50, default='Permanent')
    status = models.CharField(max_length=50, default='Working')
    recordstatus = models.IntegerField(blank=True, null=True, default=1)
    holidaygroup = models.IntegerField(blank=True, null=True, default=-1)
    shiftgroupid = models.IntegerField(blank=True, null=True, default=0)
    shiftrosterid = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        managed = False
        db_table = 'employees'
    def __str__(self):
        return self.employeename


class Devices(models.Model):
    deviceid = models.AutoField(primary_key=True)
    devicefname = models.CharField(max_length=256)
    devicesname = models.CharField(max_length=256)
    devicelocation = models.CharField(max_length=256, blank=True, null=True)
    serialnumber = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'devices'
    def __str__(self):
        return self.devicefname


# class ShiftExemption(models.Model):
#     pk_bint_id = models.BigAutoField(primary_key=True)
#     json_emp_id = JSONField(blank=True, null=True)  # This field type is a guess.
#     dat_created = models.DateTimeField(blank=True, null=True)
#     fk_created = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True,related_name = 'exempt_fk_created')
#     int_status = models.IntegerField(blank=True, null=True)#  1 Created,0 Updated
#     dat_updated = models.DateTimeField(blank=True, null=True)
#     fk_updated = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True,related_name = 'exempt_fk_updated')
#
#     class Meta:
#         managed = False
#
#         db_table = 'shift_exemption'
