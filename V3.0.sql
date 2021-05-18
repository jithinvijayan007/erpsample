

-- add scheme
-- INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_listurl) VALUES('Add Scheme',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'SCHEME'),'addscheme',1,'false','scheme/addscheme/');

-- SCHEME QUERIES
INSERT INTO sub_category(fk_main_category_id,vchr_sub_category_name,vchr_sub_category_value,int_sub_category_order,vchr_icon_name) VALUES((SELECT pk_bint_id from main_category WHERE vchr_main_category_name = 'MASTER'),'SCHEME','scheme',1,'mdi mdi-home-map-marker');
INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_listurl) VALUES('Scheme List',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'SCHEME'),'listschema',2,'false','/schema/listschema');
INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_listurl) VALUES('Add Scheme',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'SCHEME'),'addscheme',1,'false','/schema/addschema');

--EWAY BILL QUERY
ALTER TABLE stock_Transfer ADD vchr_vehicle_num VARCHAR(20);

-- QUOTATION QUERIES
INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_listurl) VALUES('Add Quotation',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'INVOICE'),'addquotation',2,'false','/invoice/quotationprint');
INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_listurl) VALUES('Quotation List',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'INVOICE'),'quotationlist',2,'false','/invoice/quotationlist');


ALTER TABLE transfer_mode_details ADD fk_courier_id BIGINT REFERENCES courier_master;

update courier_master set vchr_gst_no='32ANIPV5870E1ZS' where vchr_name ilike 'VPM COURIER';


