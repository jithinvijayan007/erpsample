from django.db import models
from customer.models import CustomerDetails as CustomerAppCustomermodel
from userdetails.models import UserDetails as UserAppUsermodel
# Create your models here.
class CustomerRating(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    vchr_feedback = models.TextField(blank=True, null=True)
    dbl_rating = models.FloatField(blank=True, null=True)
    fk_customer = models.ForeignKey(CustomerAppCustomermodel, models.DO_NOTHING)
    fk_user = models.ForeignKey(UserAppUsermodel, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'customer_rating'

    def __str__ (self):
        return self.fk_customer
