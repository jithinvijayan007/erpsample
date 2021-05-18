from django.contrib import admin

from category.models import Category,OtherCategory
# Register your models here.
admin.site.register(Category)
admin.site.register(OtherCategory)
