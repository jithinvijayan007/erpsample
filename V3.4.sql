
ALTER TABLE user_permissions ADD COLUMN jsn_branch_type JSONB;

CREATE TABLE paytm_point_data (pk_bint_id BIGSERIAL PRIMARY KEY,fk_partial_id BIGINT REFERENCES partial_invoice(pk_bint_id),int_status SMALLINT,dat_created TIMESTAMP,fk_created_id BIGINT REFERENCES auth_user(id),dat_updated TIMESTAMP,fk_invoice_id BIGINT REFERENCES sales_master(pk_bint_id),vchr_ref_num VARCHAR(100),dbl_amount DOUBLE PRECISION,dbl_pts DOUBLE PRECISION);

ALTER TABLE item add COLUMN dbl_myg_amount DOUBLE PRECISION;
ALTER TABLE sales_return ADD COLUMN vchr_old_inv_no VARCHAR(20);


INSERT INTO sub_category(fk_main_category_id,vchr_sub_category_name,vchr_sub_category_value,int_sub_category_order,vchr_icon_name) VALUES((SELECT pk_bint_id from main_category WHERE vchr_main_category_name = 'TRANSACTIONS'),'GOODS RETURN','goodsreturn',20,'mdi mdi-group');

INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_listurl) VALUES('Online Sales Order List',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'INVOICE'),'online_sales_order_list',1,'false','/invoice/onlinesaleslist');

INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_listurl) VALUES('Add Goods Return',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'GOODS RETURN'),'add_goods_return',1,'false','/transfer/goodsreturn');

INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_listurl) VALUES('Goods Return List',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'GOODS RETURN'),'goods_return_list',2,'false','/transfer/goodsreturnlist');

ALTER TABLE grnr_master ADD COLUMN vchr_remarks VARCHAR(50);
INSERT INTO document (vchr_module_name,vchr_short_code,int_number) values('GOODS RETURN','GRTN-',1);
INSERT INTO document (vchr_module_name,vchr_short_code,int_number,fk_branch_id) values
    ('GOODS RETURN','GRTN-WHO3-',1,1),
    ('GOODS RETURN','GRTN-WHO1-',1,3),
    ('GOODS RETURN','GRTN-WHO2-',1,4),
    ('GOODS RETURN','GRTN-GPT-',1,7),
    ('GOODS RETURN','GRTN-MPL4-',1,41),
    ('GOODS RETURN','GRTN-MCL3-',1,46),
    ('GOODS RETURN','GRTN-MCL2-',1,47),
    ('GOODS RETURN','GRTN-MCH-',1,48),
    ('GOODS RETURN','GRTN-ACCE-',1,62),
    ('GOODS RETURN','GRTN-DHO-',1,75),
    ('GOODS RETURN','GRTN-DSC-',1,76),
    ('GOODS RETURN','GRTN-ITS-',1,85),
    ('GOODS RETURN','GRTN-SMC-',1,97),
    ('GOODS RETURN','GRTN-ITC-',1,102),
    ('GOODS RETURN','GRTN-ROC-',1,104)
;

INSERT INTO document (vchr_module_name,vchr_short_code,int_number) values('INDIRECT DISCOUNT','JV-',1);
ALTER TABLE grnr_master ADD COLUMN fk_created_id BIGINT REFERENCES auth_user(id);

INSERT INTO document (vchr_module_name,vchr_short_code,int_number,fk_branch_id) values
    ('GOODS RETURN','GRTN-GSR-',1,94),
    ('GOODS RETURN','GRTN-ECO-',1,100),
    ('GOODS RETURN','GRTN-FA-',1,80),
    ('GOODS RETURN','GRTN-MIT-',1,44),
    ('GOODS RETURN','GRTN-3GH-',1,61),
    ('GOODS RETURN','GRTN-MRK-',1,40),
    ('GOODS RETURN','GRTN-OFT-',1,34),
    ('GOODS RETURN','GRTN-GDP-',1,81),
    ('GOODS RETURN','GRTN-VSP-',1,111)
;

INSERT INTO bank (vchr_name,int_status) VALUES ('MYG ECOMMERCE BANK',0);
