from django.db import models
from company.models import Company
from category.models import OtherCategory
from states.models import States,LocationMaster
from hierarchy.models import HierarchyData

class Branch(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    vchr_code = models.CharField(max_length=20, blank=True, null=True)
    vchr_name = models.CharField(max_length=50)
    vchr_address = models.CharField(max_length=300, blank=True, null=True)
    vchr_email = models.CharField(max_length=50, blank=True, null=True)
    vchr_phone = models.CharField(max_length=20, blank=True, null=True)
    # vchr_category = models.CharField(max_length=50, blank=True, null=True)
    bint_stock_limit = models.BigIntegerField(blank=True, null=True)
    vchr_ip = models.CharField(max_length=15, blank=True, null=True)
    flt_latitude = models.FloatField(blank=True, null=True)
    flt_longitude = models.FloatField(blank=True, null=True)
    dat_inauguration = models.DateField(blank=True, null=True)
    tim_inauguration = models.TimeField(blank=True, null=True)
    dat_close = models.DateField(blank=True, null=True)
    vchr_inaugurated_by = models.CharField(max_length=50, blank=True, null=True)
    # fk_company = models.ForeignKey(Company, models.DO_NOTHING)
    int_status = models.IntegerField(blank=True, null=True) #0 active 2 deactive -1 delete
    fk_category = models.ForeignKey(OtherCategory, models.DO_NOTHING, blank=True, null=True)
    int_type = models.IntegerField(blank=True, null=True) #1 branch 2 head office 3 ware house
    # bln_active = models.NullBooleanField()
    fk_states = models.ForeignKey(States, models.DO_NOTHING, blank=True, null=True)
    flt_size = models.FloatField(blank=True, null=True)
    int_price_template = models.IntegerField(blank=True, null=True)#0. Cost Price, 1. Dealer, 2. MOP, 3. MYG Price, 4. MRP
    dbl_stock_request_amount = models.FloatField(blank=True, null=True)
    int_stock_request_qty = models.IntegerField(blank=True, null=True)
    fk_location_master = models.ForeignKey(LocationMaster, models.DO_NOTHING, blank=True, null=True)
    vchr_mygcare_no = models.CharField(max_length=50, blank=True, null=True)
    vchr_gstno = models.CharField(max_length=50, blank=True, null=True)
    int_pincode = models.IntegerField(blank=True, null=True)
    fk_hierarchy_data = models.ForeignKey(HierarchyData, models.DO_NOTHING, blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'branch'

    def __str__(self):
        return self.vchr_code + "-" + self.vchr_name


# class Department(models.Model):
#     pk_bint_id = models.BigAutoField(primary_key=True)
#     vchr_code = models.CharField(max_length=50, blank=True, null=True)
#     vchr_name = models.CharField(max_length=150, blank=True, null=True)
#     int_status = models.IntegerField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'department'
