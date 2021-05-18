from django.db import models
from company.models import Company
# Create your models here.
class Department(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    vchr_code = models.CharField(max_length=10)
    vchr_name = models.CharField(max_length=50)
    int_status = models.IntegerField(blank=True, null=True)#1.active -1.delete
    fk_company = models.ForeignKey(Company, models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
            return str(self.vchr_name)
    class Meta:
        managed = False
        db_table = 'department'
