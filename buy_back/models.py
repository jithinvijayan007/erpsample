from django.db import models
from item_category.models import Item as Items

# Create your models here.
class BuyBack(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    dat_start = models.DateTimeField(blank=True, null=True)
    dat_end = models.DateTimeField(blank=True, null=True)
    fk_item = models.ForeignKey(Items, models.DO_NOTHING, blank=True, null=True)
    # int_quantity = models.IntegerField(blank=True, null=True)
    dbl_amount = models.FloatField(blank=True, null=True)
    int_status = models.IntegerField(blank=True, null=True,default=1)

    class Meta:
        managed = False
        db_table = 'buy_back'
        # unique_together = (('dat_start', 'dat_end', 'fk_item'),)
    def __str__(self):
        return str(self.fk_item.vchr_item_name)
