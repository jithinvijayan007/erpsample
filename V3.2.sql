INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_listurl) VALUES('Stock Transfer Batch & IMEI',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'STOCK TRANSFER'),'stock_transfer_batch_&_imei',4,'false','/transfer/stocktransfer');
UPDATE menu_category set vchr_menu_category_name = 'Stock Transfer' WHERE pk_bint_id in (select pk_bint_id from menu_category where vchr_menu_category_value = 'stock_transfer_batch_&_imei');
INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_listurl,vchr_viewurl) VALUES('Price List Report',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'STOCK'),'pricelistreport',3,'false','/price/price-list-report','/price/price-list-report');


alter table partial_invoice add column int_sale_type INTEGER;
