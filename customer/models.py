from django.db import models
from states.models import States, Location
from userdetails.models import UserDetails as Userdetails
# from customer.models import CustomerModel 
# from user.models import UserModel as UserAppUsermodel
# Create your models here.
# from loyalty_card.models import LoyaltyCard

# Create your models here.
class CustomerDetails(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    vchr_name = models.CharField(max_length=100, blank=True, null=True)
    vchr_email = models.CharField(max_length=200, blank=True, null=True)
    int_mobile = models.BigIntegerField(blank=True, null=True)
    txt_address = models.TextField(blank=True, null=True)
    vchr_gst_no = models.CharField(max_length=30, blank=True, null=True)
    int_otp_number = models.BigIntegerField(blank=True, null=True)
    fk_location = models.ForeignKey(Location, models.DO_NOTHING, blank=True, null=True)
    fk_state = models.ForeignKey(States, models.DO_NOTHING, blank=True, null=True)
    fk_loyalty = models.ForeignKey('loyalty_card.LoyaltyCard', models.DO_NOTHING, blank=True, null=True)
    int_loyalty_points = models.BigIntegerField(blank=True, null=True, default=0)
    int_redeem_point = models.BigIntegerField(blank=True, null=True, default=0)
    dbl_purchase_amount = models.FloatField(blank=True, null=True, default=0.0)
    vchr_loyalty_card_number = models.CharField(max_length=50, blank=True, null=True)
    vchr_code = models.CharField(max_length=25, blank=True, null=True)
    int_edit_count = models.IntegerField(blank=True, null=True)
    vchr_otp = models.CharField(max_length=10, blank=True, null=True)
    dat_exp = models.DateTimeField(blank=True, null=True)
    int_cust_type = models.IntegerField(blank=True, null=True,default=0) #1 - corporate customer 2 - credit customer 3 - sez customer 4 - cash customer
    dbl_credit_balance = models.FloatField(blank=True, null=True,default=0)
    dbl_credit_limit = models.FloatField(blank=True, null=True,default=0)
    cust_smsaccess = models.NullBooleanField()
    cust_salutation = models.CharField(max_length=10, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'customer_details'

    def __str__(self):
        return str(self.vchr_name)

class SalesCustomerDetails(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    fk_customer = models.ForeignKey(CustomerDetails, models.DO_NOTHING)
    dat_created = models.DateTimeField(blank=True, null=True)
    fk_created = models.ForeignKey(Userdetails, models.DO_NOTHING, blank=True, null=True)
    vchr_name = models.CharField(max_length=100, blank=True, null=True)
    vchr_email = models.CharField(max_length=200, blank=True, null=True)
    int_mobile = models.BigIntegerField(blank=True, null=True)
    fk_state = models.ForeignKey(States, models.DO_NOTHING, blank=True, null=True)
    int_loyalty_points = models.BigIntegerField(blank=True, null=True)
    int_redeem_point = models.BigIntegerField(blank=True, null=True)
    dbl_purchase_amount = models.FloatField(blank=True, null=True)
    vchr_loyalty_card_number = models.CharField(max_length=50, blank=True, null=True)
    txt_address = models.TextField(blank=True, null=True)
    vchr_gst_no = models.CharField(max_length=30, blank=True, null=True)
    int_otp_number = models.BigIntegerField(blank=True, null=True)
    fk_location = models.ForeignKey(Location, models.DO_NOTHING, blank=True, null=True)
    fk_loyalty = models.ForeignKey('loyalty_card.LoyaltyCard', models.DO_NOTHING, blank=True, null=True)
    vchr_code = models.CharField(max_length=25, blank=True, null=True)
    int_cust_type = models.IntegerField(blank=True, null=True,default=0)
    class Meta:
        managed = False
        db_table = 'sales_customer_details'

class CustomerOccasionsModel(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    int_cust = models.ForeignKey(CustomerDetails, null=True,on_delete = models.SET_NULL)
    vchr_occasion_name = models.CharField(max_length = 40)
    dat_occasion_date = models.DateField()

    def __str__(self):
        return str(self.cust_id)
    class Meta:
        managed = False
        db_table = 'customer_app_customeroccasionsmodel'


class CustomerRating(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    vchr_feedback = models.TextField(blank=True, null=True)
    dbl_rating = models.FloatField(blank=True, null=True)
    fk_customer = models.ForeignKey(CustomerDetails, models.DO_NOTHING, related_name='customer_customerRating_customertable')
    fk_user = models.ForeignKey(Userdetails, models.DO_NOTHING,related_name='customer_customerRating_usertable')

    class Meta:
        managed = False
        db_table = 'customer_rating'

    def __str__ (self):
        return self.fk_customer
