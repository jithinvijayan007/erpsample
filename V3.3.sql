UPDATE sub_category SET vchr_sub_category_name = 'SALES REPORTS' WHERE vchr_sub_category_name = 'SALES';

-- Goods Return Side Query
-- INSERT INTO sub_category(fk_main_category_id,vchr_sub_category_name,vchr_sub_category_value,int_sub_category_order,vchr_icon_name) VALUES((SELECT pk_bint_id from main_category WHERE vchr_main_category_name = 'transactions'),'GOODS RETURN','goods_return',20,'mdi mdi-face');

INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_listurl) VALUES('Goods Return',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'STOCK TRANSFER'),'goods_return_list',4,'false','/transfer/goodsreturnlist');

alter table partial_invoice add column int_sale_type INTEGER;
