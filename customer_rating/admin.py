from django.contrib import admin
from customer_rating.models import CustomerRating
# Register your models here.

class CustomerRatingAdmin(admin.ModelAdmin):
    list_display = ['fk_customer','dbl_rating','vchr_feedback']
    list_filter = ['dbl_rating']
    search_fields = ['dbl_rating','vchr_feedback']

admin.site.register(CustomerRating,CustomerRatingAdmin)
