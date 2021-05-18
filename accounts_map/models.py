from django.db import models
from sap_api.models import ChartOfAccounts
from branch.models import Branch


# Create your models here.

class AccountsMap(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    vchr_module_name = models.CharField(max_length=50)
    vchr_category = models.CharField(max_length=250, blank=True, null=True)
    fk_coa = models.ForeignKey(ChartOfAccounts, models.DO_NOTHING, blank=True, null=True)
    int_status = models.IntegerField(blank=True, null=True) # 0 ACTIVE  2 DEACTIVE -1 DELETE
    int_type = models.IntegerField(blank=True, null=True) # 1. ADDITIONS 2. DEDUCTIONS
    fk_branch = models.ForeignKey(Branch, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False

        db_table = 'accounts_map'
