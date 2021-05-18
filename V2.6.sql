CREATE TABLE mailing_product
(
pk_bint_id BIGSERIAL PRIMARY KEY,
vchr_name VARCHAR(100),
vchr_email VARCHAR(50),
fk_product_id BIGINT REFERENCES PRODUCTS
);



INSERT INTO sub_category(fk_main_category_id,vchr_sub_category_name,vchr_sub_category_value,int_sub_category_order,vchr_icon_name) VALUES((SELECT pk_bint_id from main_category WHERE vchr_main_category_name = 'TRANSACTIONS'),'JOURNAL','journal',20,'mdi mdi-face');

INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_listurl) VALUES('Add Journal',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'JOURNAL'),'addjournal',1,'false','/journal/addjournal');
INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_listurl) VALUES('List Journal',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'JOURNAL'),'listjournal',2,'false','/journal/listjournal');



