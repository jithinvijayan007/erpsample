from django.contrib import admin
from company_permissions.models import MainCategory,SubCategory,MenuCategory,CategoryItems,GroupPermissions
# Register your models here.
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ['vchr_main_category_name','vchr_main_category_value','int_main_category_order']
    list_filter = ['vchr_main_category_name']
    search_fields = ['vchr_main_category_name','vchr_main_category_value','pk_bint_id']
admin.site.register(MainCategory,MainCategoryAdmin)

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['fk_main_category','vchr_sub_category_name','int_sub_category_order']
    list_filter = ['vchr_sub_category_name']
    search_fields = ['vchr_sub_category_name','vchr_sub_category_value','pk_bint_id']
admin.site.register(SubCategory,SubCategoryAdmin)

class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ['fk_sub_category','vchr_menu_category_name','int_menu_category_order','vchr_addurl','vchr_viewurl','vchr_editurl','vchr_listurl']
    list_filter = ['vchr_menu_category_name']
    search_fields = ['vchr_menu_category_name','vchr_menu_category_value','pk_bint_id']
admin.site.register(MenuCategory,MenuCategoryAdmin)

class CategoryItemsAdmin(admin.ModelAdmin):
    list_display = ['fk_main_category','fk_sub_category','fk_menu_category']
    list_filter = ['pk_bint_id']
    search_fields = ['pk_bint_id','fk_main_category','fk_sub_category','fk_menu_category']
admin.site.register(CategoryItems,CategoryItemsAdmin)

class GroupPermissionsAdmin(admin.ModelAdmin):
    list_display = ['fk_groups','fk_category_items','bln_view','bln_add','bln_delete','bln_edit']
    list_filter = ['pk_bint_id']
    search_fields = ['pk_bint_id','fk_groups','fk_category_items']
admin.site.register(GroupPermissions,GroupPermissionsAdmin)
