from django.db import models
from groups.models import Groups
from company.models import Company
from job_position.models import JobPosition
# Create your models here.
class MainCategory(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    vchr_main_category_name = models.CharField(max_length=50)
    vchr_main_category_value = models.CharField(max_length=50, blank=True, null=True)
    int_main_category_order = models.IntegerField(blank=True, null=True)
    vchr_icon_name = models.CharField(max_length=50, blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'main_category'

class SubCategory(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    fk_main_category = models.ForeignKey(MainCategory, models.DO_NOTHING)
    vchr_sub_category_name = models.CharField(max_length=50)
    vchr_sub_category_value = models.CharField(max_length=50, blank=True, null=True)
    int_sub_category_order = models.IntegerField(blank=True, null=True)
    vchr_icon_name = models.CharField(max_length=50, blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'sub_category'

class MenuCategory(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    vchr_menu_category_name = models.CharField(max_length=50)
    fk_sub_category = models.ForeignKey(SubCategory, models.DO_NOTHING)
    vchr_menu_category_value = models.CharField(max_length=50, blank=True, null=True)
    int_menu_category_order = models.IntegerField(blank=True, null=True)
    bln_has_children = models.NullBooleanField()
    vchr_addurl = models.CharField(max_length=50, blank=True, null=True)
    vchr_viewurl = models.CharField(max_length=50, blank=True, null=True)
    vchr_editurl = models.CharField(max_length=50, blank=True, null=True)
    vchr_listurl = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.vchr_menu_category_name +" "+str(self.pk_bint_id)

    class Meta:
        managed = False
        db_table = 'menu_category'

class CategoryItems(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    fk_main_category = models.ForeignKey(MainCategory, models.DO_NOTHING)
    fk_sub_category = models.ForeignKey(SubCategory, models.DO_NOTHING)
    fk_menu_category = models.ForeignKey(MenuCategory, models.DO_NOTHING)
    fk_company = models.ForeignKey(Company, models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.fk_menu_category.vchr_menu_category_name

    class Meta:
        managed = False
        db_table = 'category_items'



class GroupPermissions(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    fk_groups = models.ForeignKey(Groups, models.DO_NOTHING)
    fk_category_items = models.ForeignKey(CategoryItems, models.DO_NOTHING)
    bln_view = models.BooleanField()
    bln_add = models.BooleanField()
    bln_delete = models.BooleanField()
    bln_edit = models.BooleanField()
    bln_download = models.BooleanField()
    fk_desig = models.ForeignKey(JobPosition, models.DO_NOTHING, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'group_permissions'
