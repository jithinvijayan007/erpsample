from django.db import models
from company.models import Company as CompanyDetails
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class AdminSettings(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    vchr_name = models.CharField(max_length=50, blank=True, null=True)
    vchr_value = ArrayField(models.TextField(blank=True,null=True) ) # This field type is a guess.
    fk_company = models.ForeignKey(CompanyDetails, models.DO_NOTHING, blank=True, null=True,related_name="admin_settings_fk_company")
    bln_enabled = models.NullBooleanField()
    vchr_code = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admin_settings'

    def __str__(self):
            return str(self.vchr_name)
