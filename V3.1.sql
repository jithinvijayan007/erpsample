alter table partial_receipt add column  bln_service BOOLEAN;
INSERT INTO accounts_map (vchr_module_name,vchr_category,fk_coa_id,int_status,int_type) VALUES ('DEDUCTIONS','CUSTOMER LOYALTY',(select pk_bint_id from chart_of_accounts where vchr_acc_name='DEDUCTIONS'),0,1);

-- LG
-- Good retrun saving
create table grnr_master(
    pk_bint_id BIGSERIAL PRIMARY KEY,
    vchr_purchase_return_num VARCHAR(80),
    dat_purchase_return TIMESTAMP,
    fk_branch_id BIGINT REFERENCES branch(pk_bint_id),-->[warehouses or head office only]
    dat_created TIMESTAMP
);
create table grnr_details(
    pk_bint_id BIGSERIAL PRIMARY KEY,
    fk_item_id BIGINT REFERENCES item(pk_bint_id),
    fk_master_id BIGINT REFERENCES grnr_master(pk_bint_id),
    int_qty INTEGER,
    dbl_tax_rate DOUBLE PRECISION,
    jsn_imei JSONB,-->text,
    vchr_batch_no VARCHAR(80)
);
create table grnr_imei_details(
    pk_bint_id BIGSERIAL PRIMARY KEY,
    fk_details_id BIGINT REFERENCES grnr_details(pk_bint_id),
    fk_grn_details_id BIGINT REFERENCES grn_details(pk_bint_id),
    jsn_imei JSONB,
    jsn_batch_no JSONB,
    int_qty INTEGER
);

-- special sales side bar

INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_listurl) VALUES('SPECIAL SALES',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'INVOICE'),'special_sales',4,'false','/invoice/specialsaleslist');


-- stock transfer report
INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_listurl) VALUES('Stock Transfer Report',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name ilike 'STOCK'),'stock_transfer_report',4,'false','/stocktransfer/stock_transfer_report');

UPDATE menu_category set vchr_menu_category_name = 'Online Sales' where vchr_menu_category_value = 'bajajlist';

ALTER TABLE sales_master ADD COLUMN vchr_irn_no VARCHAR(100);
ALTER TABLE sales_master ADD COLUMN txt_qr_code TEXT;


ALTER TABLE stock_transfer ADD COLUMN vchr_irn_no VARCHAR(100);
ALTER TABLE stock_transfer ADD COLUMN txt_qr_code TEXT;
