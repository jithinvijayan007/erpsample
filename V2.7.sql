
INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_listurl) VALUES('Detailed Sales Report',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'SALES'),'sales_report',4,'false','/report/details-salesreport');


alter table customer_details alter COLUMN int_cust_type set default 4;
alter table sales_customer_details alter COLUMN int_cust_type set default 4;

CREATE TABLE user_permissions(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_user_id BIGINT REFERENCES auth_user(id) NOT NULL,
  jsn_branch JSONB,
  jsn_product JSONB,
  jsn_item_group JSONB,
  dat_created TIMESTAMP NOT NULL DEFAULT NOW(),
  bln_active BOOLEAN NOT NULL DEFAULT TRUE
);
INSERT INTO sub_category(fk_main_category_id,vchr_sub_category_name,vchr_sub_category_value,int_sub_category_order,vchr_icon_name) VALUES((SELECT pk_bint_id from main_category WHERE vchr_main_category_name = 'Reports'),'PROFIT REPORT','profit_report',20,'mdi mdi-face');
INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_listurl) VALUES('GDOT-GDEW',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'PROFIT REPORT'),'gdotprofitreport',4,'false','/report/gdp-gdew-report');
INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_listurl) VALUES('Recharge',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'PROFIT REPORT'),'rechargereport',4,'false','/report/recharge-profit-report');
INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_listurl) VALUES('Product',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'PROFIT REPORT'),'productreport',4,'false','/report/product-profit-report');
INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_listurl) VALUES('Smart Choice',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'PROFIT REPORT'),'smartchoicereport',4,'false','/report/smart-choice-report');

INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_listurl) VALUES('Smart Choice Sales Report',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'SALES'),'smartchoice_sales_report',4,'false','/report/smart-choice-sale');
ALTER TABLE userdetails ALTER COLUMN vchr_profpic TYPE VARCHAR(150);


INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_listurl) VALUES('Purchase Report',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name ilike 'STOCK'),'purchasereport',4,'false','/report/purchasereport');


INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_listurl) VALUES('STOCK HISTORY',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'SALES'),'sales_report',4,'false','/report/stock-history');


INSERT INTO chart_of_accounts (vchr_acc_name,vchr_acc_code) VALUES ('FINANCE_CHARGES','FINANCE_CHARGES');
-- LG
ALTER TABLE sales_details ADD COLUMN dbl_dealer_price DOUBLE PRECISION, ADD COLUMN dbl_cost_price DOUBLE PRECISION, ADD COLUMN dbl_mrp DOUBLE PRECISION, ADD COLUMN dbl_mop DOUBLE PRECISION, ADD COLUMN dbl_tax_percentage DOUBLE PRECISION;