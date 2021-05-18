-- LG
ALTER TABLE sales_details ADD COLUMN dbl_dealer_price DOUBLE PRECISION, ADD COLUMN dbl_cost_price DOUBLE PRECISION, ADD COLUMN dbl_mrp DOUBLE PRECISION, ADD COLUMN dbl_mop DOUBLE PRECISION, ADD COLUMN dbl_tax_percentage DOUBLE PRECISION;

INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_listurl) VALUES('Detailed Model Sales Report',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'SALES'),'detailed_model_wise_sales_report',4,'false','/report/detailed_model_wise_sales_report');

INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_listurl) VALUES('Credit Sales Report',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'SALES'),'credit_sales_Report',4,'false','/report/creditsalesreport');




INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_addurl) VALUES('Cash Book',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'LEDGER'),'cashbook',2,'false','/ledger/cashbook');
