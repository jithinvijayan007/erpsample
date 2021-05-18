alter table purchase add column int_approve INTEGER;
alter table purchase add column vchr_bill_no VARCHAR(20);
alter table purchase add column dat_bill TIMESTAMP;

ALTER TABLE purchase RENAME TO grn_master;
ALTER TABLE purchase_details RENAME TO grn_details;

ALTER TABLE grn_details ALTER COLUMN jsn_imei TYPE JSONB;
ALTER TABLE grn_details ALTER COLUMN jsn_imei_avail TYPE JSONB;
ALTER TABLE grn_details ALTER COLUMN jsn_imei_dmgd TYPE JSONB;
ALTER TABLE grn_details ALTER COLUMN jsn_tax TYPE JSONB;

ALTER TABLE grn_details add COLUMN int_damaged INTEGER;


CREATE TABLE financial_year(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  int_year INTEGER,
  dat_start DATE,
  dat_end DATE
);

ALTER TABLE sales_master ADD COLUMN dat_updated TIMESTAMP;
ALTER TABLE sales_master DROP COLUMN fk_staff_id;
ALTER TABLE sales_master ADD COLUMN fk_assign_id BIGINT REFERENCES userdetails(user_ptr_id);
ALTER TABLE sales_master ADD COLUMN fk_created_id BIGINT REFERENCES userdetails(user_ptr_id);
ALTER TABLE sales_master ADD COLUMN fk_financial_year_id BIGINT REFERENCES financial_year(pk_bint_id);
ALTER TABLE sales_master ADD COLUMN dbl_supplier_amount DOUBLE PRECISION;
ALTER TABLE sales_master ADD COLUMN dbl_commission DOUBLE PRECISION;
ALTER TABLE sales_master ADD COLUMN dbl_service_fee DOUBLE PRECISION;
ALTER TABLE sales_master ADD COLUMN dbl_agent_commission DOUBLE PRECISION;
ALTER TABLE sales_master ADD COLUMN dbl_tds_deducted DOUBLE PRECISION;
ALTER TABLE sales_master ADD COLUMN dbl_outstanding_amt DOUBLE PRECISION;

ALTER TABLE sales_details ADD COLUMN fk_assign_id BIGINT REFERENCES userdetails(user_ptr_id);
ALTER TABLE sales_details ADD COLUMN fk_created_id BIGINT REFERENCES userdetails(user_ptr_id);
ALTER TABLE sales_details ADD COLUMN int_doc_status INTEGER;
ALTER TABLE sales_details ADD COLUMN dat_created TIMESTAMP;
ALTER TABLE sales_details ADD COLUMN dat_updated TIMESTAMP;
ALTER TABLE sales_details ADD COLUMN dbl_supplier_amount DOUBLE PRECISION;
ALTER TABLE sales_details ADD COLUMN dbl_commission DOUBLE PRECISION;
ALTER TABLE sales_details ADD COLUMN dbl_service_fee DOUBLE PRECISION;
ALTER TABLE sales_details ADD COLUMN dbl_agent_commission DOUBLE PRECISION;
ALTER TABLE sales_details ADD COLUMN dbl_selling_price DOUBLE PRECISION;
ALTER TABLE sales_details ADD COLUMN dbl_tds_deducted DOUBLE PRECISION;
ALTER TABLE sales_details DROP COLUMN txt_imei;
ALTER TABLE sales_details ADD COLUMN json_imei JSONB;

INSERT INTO document(vchr_module_name,vchr_short_code,int_number) VALUES('INVOICE','INV',1);
ALTER TABLE financial_year DROP int_year;
ALTER TABLE financial_year ADD COLUMN vchr_financial_year VARCHAR(20);
create TABLE purchase_voucher(
    pk_bint_id BIGSERIAL PRIMARY KEY,
    vchr_voucher_num VARCHAR(20),
    fk_supplier_id BIGINT REFERENCES supplier(pk_bint_id),
    fk_grn_id BIGINT REFERENCES grn_master(pk_bint_id),
    dbl_voucher_amount DOUBLE PRECISION,
    vchr_voucher_bill_no VARCHAR(20),
    dat_voucher_bill TIMESTAMP,
    fk_created_id BIGINT REFERENCES auth_user(id),
    dat_created TIMESTAMP,
    fk_updated_id BIGINT REFERENCES auth_user(id),
    dat_updated TIMESTAMP,
    vchr_remark TEXT,
    int_doc_status INTEGER
);

alter table grn_master add column vchr_reject_reason TEXT;

insert into document (vchr_module_name,vchr_short_code,int_number) values ('PURCHASE VOUCHER','PVR',0);

update document SET vchr_module_name='GRN',vchr_short_code='GRN',int_number=0 where vchr_module_name= 'PURCHASE';
update document SET vchr_short_code='PO',int_number=0 where vchr_module_name= 'PURCHASE ORDER';

ALTER TABLE branch_stock_details ADD COLUMN dbl_unitprice DOUBLE PRECISION;-->[price of a single piece without tax and discount]
ALTER TABLE branch_stock_details ADD COLUMN dbl_ppu DOUBLE PRECISION;-->[price of a single piece with tax and discount]
ALTER TABLE branch_stock_master DROP COLUMN fk_pd_id;
ALTER TABLE branch_stock_master ADD COLUMN fk_branch_id BIGINT REFERENCES branch(pk_bint_id);
ALTER TABLE branch_stock_details ADD COLUMN fk_pd_id BIGINT REFERENCES purchase_details(pk_bint_id);
ALTER TABLE branch_stock_details DROP column txt_imei ;
ALTER TABLE branch_stock_details ADD COLUMN jsn_imei jsonb;
ALTER TABLE branch_stock_details ADD COLUMN jsn_imei_avail jsonb;
ALTER TABLE branch_stock_details ADD COLUMN dbl_tax DOUBLE PRECISION;-->[tax amount per piece]
ALTER TABLE branch_stock_details ADD COLUMN jsn_tax JSONB;--> (CGST:4,SGST:4)[per piece]
ALTER TABLE branch_stock_master ADD COLUMN fk_created_id  BIGINT REFERENCES auth_user(id);
ALTER TABLE branch_stock_details ADD COLUMN vchr_batch_no VARCHAR(30);
ALTER TABLE branch_stock_details ADD COLUMN jsn_imei_dmgd jsonb;


ALTER TABLE branch_stock_master DROP COLUMN fk_transfer_id;
ALTER TABLE branch_stock_master ADD COLUMN dbl_tax DOUBLE PRECISION;
ALTER TABLE branch_stock_master ADD COLUMN dbl_amount DOUBLE PRECISION;
ALTER TABLE branch_stock_master ADD COLUMN jsn_tax JSONB;

ALTER TABLE branch_stock_details DROP column fk_pd_id ;
ALTER TABLE branch_stock_details DROP column dbl_unitprice ;
ALTER TABLE branch_stock_details DROP column dbl_ppu ;
ALTER TABLE branch_stock_details DROP column dbl_tax ;
ALTER TABLE branch_stock_details DROP column jsn_tax ;
ALTER TABLE branch_stock_details DROP column vchr_batch_no ;

ALTER TABLE branch_stock_details ADD COLUMN jsn_batch_no jsonb;
ALTER TABLE branch_stock_details ADD COLUMN fk_transfer_details_id BIGINT REFERENCES ist_details(pk_bint_id);


alter table ist_details add column dbl_rate DOUBLE PRECISION null;
alter table ist_details add column jsn_imei jsonb;
alter table ist_details drop column txt_imei;



CREATE TABLE transfer_history (
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_transfer_id BIGINT REFERENCES stock_transfer(pk_bint_id),
  fk_created_id BIGINT REFERENCES auth_user(id),
  dat_created TIMESTAMP,
  fk_updated_id BIGINT REFERENCES auth_user(id),
  dat_updated TIMESTAMP,
  vchr_status VARCHAR(30),
  int_doc_status INTEGER

);

CREATE TABLE transfer_mode_details (
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_transfer_id BIGINT REFERENCES stock_transfer(pk_bint_id),
  int_medium INTEGER,
  vchr_name_responsible VARCHAR(30),
  bnt_contact_number BIGINT,
  bnt_number BIGINT,
  fk_created_id BIGINT REFERENCES auth_user(id),
  dat_created TIMESTAMP,
  fk_updated_id BIGINT REFERENCES auth_user(id),
  dat_updated TIMESTAMP,
  int_packet_no INTEGER,
  int_packet_received INTEGER,
  int_doc_status INTEGER
);
alter table po_master add column int_total_qty INTEGER;
alter table po_master add column dbl_total_amount DOUBLE PRECISION;

alter table po_details add column dbl_total_amount DOUBLE PRECISION;

CREATE TABLE branch_stock_imei_details(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_details_id BIGINT REFERENCES branch_stock_details(pk_bint_id),
  fk_grn_details_id BIGINT REFERENCES grn_details(pk_bint_id),
  jsn_imei JSONB,
  jsn_batch_no JSONB
);


ALTER TABLE ist_details ADD COLUMN jsn_batch_no JSONB;
ALTER TABLE ist_details drop column
ALTER TABLE products DROP column vchr_hsn_code ;
ALTER TABLE products DROP column vchr_sac_code ;

ALTER TABLE item_category add column vchr_hsn_code VARCHAR(50);
ALTER TABLE item_category add column vchr_sac_code VARCHAR(50);

ALTER TABLE supplier DROP bint_tin_no;
ALTER TABLE supplier DROP bint_cst_no;
ALTER TABLE supplier ADD vchr_tin_no VARCHAR(50);
ALTER TABLE supplier ADD vchr_cst_no VARCHAR(50);

ALTER TABLE dealer DROP COLUMN vchr_from;
ALTER TABLE dealer ADD COLUMN dat_from TIMESTAMP;

ALTER TABLE supplier DROP COLUMN vchr_from;
ALTER TABLE supplier ADD COLUMN dat_from TIMESTAMP;

ALTER TABLE supplier DROP COLUMN int_gstin;
ALTER TABLE supplier ADD COLUMN vchr_gstin VARCHAR(50);

ALTER TABLE company DROP COLUMN int_gstin;
ALTER TABLE company ADD COLUMN vchr_gstin VARCHAR(50);

ALTER TABLE branch_stock_imei_details ADD COLUMN int_qty INTEGER;

ALTER TABLE address_supplier ADD COLUMN bln_status BOOLEAN default True;
ALTER TABLE contact_person_supplier ADD COLUMN bln_status BOOLEAN default True;

CREATE TABLE district(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_name VARCHAR(100),
  fk_state_id BIGINT REFERENCES states(pk_bint_id)
);

CREATE TABLE location(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_name VARCHAR(100),
  vchr_pin_code VARCHAR(10),
  fk_state_id BIGINT REFERENCES states(pk_bint_id)
);
ALTER TABLE location DROP COLUMN fk_state_id;
ALTER TABLE location ADD COLUMN fk_district_id BIGINT REFERENCES district(pk_bint_id);

ALTER TABLE customer_details ADD COLUMN fk_location_id BIGINT REFERENCES location(pk_bint_id);
ALTER TABLE customer_details ADD COLUMN vchr_gst_no VARCHAR(30);
ALTER TABLE customer_details ADD COLUMN txt_address TEXT;


alter table transfer_mode_details alter column bnt_number TYPE VARCHAR(50);


CREATE TABLE supplier_log(
 pk_bint_id BIGSERIAL PRIMARY KEY,
 vchr_remarks TEXT,
 vchr_status VARCHAR(20),
 dat_created TIMESTAMP DEFAULT now(),
 fk_created_id BIGINT REFERENCES auth_user(id),
 fk_supplier_id BIGINT REFERENCES supplier
);

CREATE TABLE coupon(
pk_bint_id BIGSERIAL PRIMARY KEY,
vchr_coupon_code VARCHAR(30),
dat_expiry DATE,
fk_product_id BIGINT REFERENCES products,
fk_brand_id BIGINT REFERENCES brands,
fk_item_category_id BIGINT REFERENCES  item_category,
fk_item_group_id BIGINT REFERENCES item_group,
fk_item_id BIGINT REFERENCES item,
int_discount_percentage INT,
bint_max_discount_amt BIGINT,
bint_min_purchase_amt BIGINT,
int_max_usage_no INT,
fk_updated_id BIGINT REFERENCES auth_user(id),
fk_created_id BIGINT REFERENCES auth_user(id),
dat_created TIMESTAMP,
dat_updated TIMESTAMP,
int_which INT
);
CREATE TABLE type(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_name VARCHAR(30)
);
CREATE TABLE terms(
pk_bint_id BIGSERIAL PRIMARY KEY,
jsn_terms JSON,
fk_type_id BIGINT REFERENCES type,
int_status INTEGER,
fk_created_id BIGINT REFERENCES auth_user,
dat_created TIMESTAMP without time zone,
fk_updated_id BIGINT REFERENCES auth_user,
dat_updated TIMESTAMP without time zone);

CREATE TABLE price_list(
pk_bint_id BIGSERIAL PRIMARY KEY,
fk_item_id BIGINT REFERENCES item,
bint_supp_amnt BIGINT,
bint_cost_amnt BIGINT,
bint_mop BIGINT,
bint_mrp BIGINT,
dat_efct_from TIMESTAMP,
fk_created_id BIGINT REFERENCES auth_user,
dat_created TIMESTAMP,
fk_updated_id BIGINT REFERENCES auth_user,
dat_updated TIMESTAMP);

alter table branch drop column flt_static_ip;
alter table branch add column vchr_ip varchar(15);
CREATE TABLE loyalty_card(
pk_bint_id BIGSERIAL PRIMARY KEY,
vchr_card_name VARCHAR(50),
int_price_range_from BIGINT,
int_price_range_to BIGINT,
dbl_loyalty_percentage FLOAT,
dbl_min_purchase_amount FLOAT,
int_min_redeem_days INTEGER,
int_min_redeem_point BIGINT,
bln_status BOOLEAN);


CREATE TABLE cust_service_delivery(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_sales_master_id BIGINT REFERENCES sales_master(pk_bint_id),
  fk_customer_id BIGINT REFERENCES customer_details(pk_bint_id),
  vchr_cust_name VARCHAR(100),
  int_mobile BIGINT,
  txt_address TEXT,
  vchr_landmark VARCHAR(200),
  vchr_gst_no VARCHAR(30),
  fk_location_id BIGINT REFERENCES location(pk_bint_id),
  fk_state_id BIGINT REFERENCES states(pk_bint_id)
);


ALTER TABLE sales_master RENAME fk_assign_id to fk_staff_id;
ALTER TABLE sales_master DROP COLUMN dbl_commission;
ALTER TABLE sales_master DROP COLUMN dbl_service_fee;
ALTER TABLE sales_master DROP COLUMN dbl_agent_commission;
ALTER TABLE sales_master DROP COLUMN dbl_tds_deducted;
ALTER TABLE sales_master DROP COLUMN dbl_outstanding_amt;
ALTER TABLE sales_master ALTER COLUMN dat_invoice TYPE DATE;
ALTER TABLE sales_master ADD COLUMN vchr_delete_remark VARCHAR(500);
ALTER TABLE sales_master ADD COLUMN fk_updated_id BIGINT REFERENCES userdetails(user_ptr_id);
ALTER TABLE sales_master ADD COLUMN fk_loyalty_id BIGINT REFERENCES loyalty_card(pk_bint_id);
ALTER TABLE sales_master ADD COLUMN fk_coupon_id BIGINT REFERENCES coupon(pk_bint_id);
ALTER TABLE sales_master ADD COLUMN dbl_coupon_amt DOUBLE PRECISION;

ALTER TABLE sales_details DROP COLUMN fk_assign_id;
ALTER TABLE sales_details DROP COLUMN fk_created_id;
ALTER TABLE sales_details DROP COLUMN dat_created;
ALTER TABLE sales_details DROP COLUMN dat_updated;
ALTER TABLE sales_details DROP COLUMN dbl_commission;
ALTER TABLE sales_details DROP COLUMN dbl_service_fee;
ALTER TABLE sales_details DROP COLUMN dbl_agent_commission;
ALTER TABLE sales_details DROP COLUMN dbl_tds_deducted;
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- #day_closure table

CREATE TABLE day_closure_master (
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_name VARCHAR(50) NOT NULL,
  bln_active BOOLEAN
);

insert into day_closure_master(vchr_name,bln_active) VALUES('2000',True);
insert into day_closure_master(vchr_name,bln_active) VALUES('1000',True);
insert into day_closure_master(vchr_name,bln_active) VALUES('500',True);
insert into day_closure_master(vchr_name,bln_active) VALUES('200',True);
insert into day_closure_master(vchr_name,bln_active) VALUES('100',True);
insert into day_closure_master(vchr_name,bln_active) VALUES('50',True);
insert into day_closure_master(vchr_name,bln_active) VALUES('20',True);
insert into day_closure_master(vchr_name,bln_active) VALUES('10',True);
insert into day_closure_master(vchr_name,bln_active) VALUES('5',True);
insert into day_closure_master(vchr_name,bln_active) VALUES('1',True);

CREATE TABLE day_closure_details(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  Dat_time TIMESTAMP,
  fk_staff_id BIGINT REFERENCES userdetails(user_ptr_id),
  total_amount DOUBLE PRECISION,
  json_dayclosure json,
  int_closed INTEGER,
  fk_branch_id BIGINT REFERENCES branch(pk_bint_id) NOT NULL
);
ALTER TABLE price_list ADD int_status INTEGER DEFAULT 1
;
 --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

 ALTER TABLE groups ADD COLUMN fk_created_id BIGINT REFERENCES auth_user(id);
 ALTER TABLE groups ADD COLUMN dat_created TIMESTAMP;
 ALTER TABLE groups ADD COLUMN fk_updated_id BIGINT REFERENCES auth_user(id);

ALTER TABLE products ADD COLUMN json_sales jsonb;
ALTER TABLE products DROP COLUMN bln_sales;




---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- """company Permissions"""
CREATE TABLE main_category(
    pk_bint_id BIGSERIAL PRIMARY KEY,
    vchr_main_category_name VARCHAR(50) NOT NULL,
    vchr_main_category_value VARCHAR(50),
    int_main_category_order INTEGER,
    vchr_icon_name varchar(50)
);

CREATE TABLE sub_category(
    pk_bint_id BIGSERIAL PRIMARY KEY,
    fk_main_category_id BIGINT REFERENCES main_category(pk_bint_id) NOT NULL,
    vchr_sub_category_name VARCHAR(50) NOT NULL,
    vchr_sub_category_value VARCHAR(50),
    int_sub_category_order INTEGER,
    vchr_icon_name varchar(50)
);

CREATE TABLE menu_category(
    pk_bint_id BIGSERIAL PRIMARY KEY,
    vchr_menu_category_name VARCHAR(50) NOT NULL,
    fk_sub_category_id BIGINT REFERENCES sub_category(pk_bint_id) NOT NULL,
    vchr_menu_category_value VARCHAR(50),
    int_menu_category_order INTEGER,
    bln_has_children BOOLEAN,
    vchr_addurl varchar(50),
    vchr_viewurl varchar(50),
    vchr_editurl varchar(50),
    vchr_listurl varchar(50)
);


CREATE TABLE category_items(
    pk_bint_id BIGSERIAL PRIMARY KEY,
    fk_main_category_id BIGINT REFERENCES main_category(pk_bint_id) NOT NULL,
    fk_sub_category_id BIGINT REFERENCES sub_category(pk_bint_id) NOT NULL,
    fk_menu_category_id BIGINT REFERENCES menu_category(pk_bint_id) NOT NULL,
    fk_company_id BIGINT REFERENCES company(pk_bint_id) NULL
);


CREATE TABLE group_permissions(
    pk_bint_id BIGSERIAL PRIMARY KEY,
    fk_groups_id BIGINT REFERENCES groups(pk_bint_id) NOT NULL,
    fk_category_items_id BIGINT REFERENCES category_items(pk_bint_id) NOT NULL,
    bln_view BOOLEAN NOT NULL DEFAULT FALSE,
    bln_add BOOLEAN NOT NULL DEFAULT FALSE,
    bln_delete BOOLEAN NOT NULL DEFAULT FALSE,
    bln_edit BOOLEAN NOT NULL DEFAULT FALSE
);



---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

ALTER TABLE supplier add column int_batch_no_offset INTEGER default 0;


ALTER TABLE grn_details RENAME COLUMN dbl_unitprice TO dbl_costprice;
ALTER TABLE groups ADD COLUMN fk_company_id BIGINT REFERENCES company(pk_bint_id);

ALTER TABLE customer_details ADD COLUMN int_otp_number BIGINT;
------------------------------------------------------------------------------------------------------------------------------------

--add_combo

CREATE TABLE add_combo_master(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  int_offer_type INTEGER,
  vchr_offer_name VARCHAR(100),
  fk_item_id BIGINT REFERENCES item(pk_bint_id),
  fk_brand_id BIGINT REFERENCES brands(pk_bint_id),
  dbl_amt DOUBLE PRECISION,
  int_status INTEGER default(1),
  int_quantity INTEGER,
  dat_from DATE,
  dat_to DATE,
  fk_company_id BIGINT REFERENCES company(pk_bint_id) NOT NULL
);


ALTER TABLE loyalty_card ADD fk_created_id BIGINT REFERENCES AUTH_USER;
ALTER TABLE loyalty_card ADD fk_updated_id BIGINT REFERENCES AUTH_USER;
ALTER TABLE loyalty_card ADD dat_created TIMESTAMP;
ALTER TABLE loyalty_card ADD dat_updated TIMESTAMP;

CREATE TABLE add_combo_discount(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_master_id BIGINT REFERENCES add_combo_master(pk_bint_id),
  int_discount_type INTEGER,
  dbl_amt DOUBLE PRECISION,
  dbl_percent DOUBLE PRECISION
);

CREATE TABLE add_combo_discount_item(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_master_id BIGINT REFERENCES add_combo_discount(pk_bint_id),
  int_quantity INTEGER,
  fk_item_id BIGINT REFERENCES item(pk_bint_id),
  dbl_amt DOUBLE PRECISION,
  dbl_percent DOUBLE PRECISION
);
------------------------------------------------------------------------------------------------------------------------------------
ALTER TABLE price_list ADD int_myg_amt BIGINT;
ALTER TABLE price_list ADD int_dealer_amt BIGINT;

ALTER TABLE customer_details ADD cust_points BIGINT;
ALTER TABLE customer_details ADD cust_redeem BIGINT;
ALTER TABLE customer_details ADD cust_purchase_amount DOUBLE PRECISION NULL;
ALTER TABLE customer_details ADD cust_card_number VARCHAR(50);
ALTER TABLE customer_details ADD COLUMN fk_state_id BIGINT REFERENCES states(pk_bint_id);


ALTER TABLE stock_request add column int_status INTEGER;
ALTER TABLE stock_request drop column bln_approved;
alter table stock_request add column vchr_reject TEXT;
alter table stock_request add column vchr_approve TEXT;

ALTER TABLE price_list ALTER bint_supp_amnt type DOUBLE PRECISION;
ALTER TABLE price_list ALTER bint_cost_amnt type DOUBLE PRECISION;
ALTER TABLE price_list ALTER bint_mop type DOUBLE PRECISION;
ALTER TABLE price_list ALTER bint_mrp type DOUBLE PRECISION;
ALTER TABLE price_list ALTER int_myg_amt type DOUBLE PRECISION;
ALTER TABLE price_list ALTER int_dealer_amt type DOUBLE PRECISION;

ALTER TABLE price_list  RENAME bint_supp_amnt  to dbl_supp_amnt;
ALTER TABLE price_list  RENAME bint_cost_amnt  TO dbl_cost_amnt;
ALTER TABLE price_list  RENAME bint_mop   TO dbl_mop;
ALTER TABLE price_list  RENAME bint_mrp  TO dbl_mrp;
ALTER TABLE price_list  RENAME int_myg_amt  TO dbl_my_amt;
ALTER TABLE price_list  RENAME int_dealer_amt  TO dbl_dealer_amt;
=======
ALTER TABLE customer_details ADD int_loyalty_points BIGINT DEFAULT 0;
ALTER TABLE customer_details ADD int_redeem_point BIGINT DEFAULT 0;
ALTER TABLE customer_details ADD dbl_purchase_amount DOUBLE PRECISION DEFAULT 0.0;
ALTER TABLE customer_details ADD vchr_loyalty_card_number VARCHAR(50);
ALTER TABLE customer_details ADD fk_loyalty_id BIGINT REFERENCES loyalty_card(pk_bint_id);

CREATE TABLE loyalty_card_invoice(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_loyalty_id BIGINT REFERENCES loyalty_card(pk_bint_id),
  fk_customer_id BIGINT REFERENCES customer_details,
  int_points BIGINT NULL DEFAULT 0,
  dbl_amount DOUBLE PRECISION,
  fk_invoice_id BIGINT REFERENCES sales_master(pk_bint_id),
  dat_invoice TIMESTAMP);

CREATE TABLE loyalty_card_status(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_customer_id BIGINT REFERENCES customer_details,
  fk_old_card_id BIGINT REFERENCES loyalty_card(pk_bint_id),
  fk_new_card_id BIGINT REFERENCES loyalty_card(pk_bint_id),
  vchr_status VARCHAR(50),
  fk_staff_id  BIGINT REFERENCES auth_user,
  dat_eligible DATE,
  dat_given DATE,
  vchr_remark VARCHAR(500));

-- ALTER TABLE customer_details RENAME COLUMN cust_points to int_loyalty_points;
-- ALTER TABLE customer_details RENAME COLUMN cust_redeem TO int_redeem_point;
-- ALTER TABLE customer_details RENAME COLUMN cust_purchase_amount TO dbl_purchase_amount;
-- ALTER TABLE customer_details RENAME COLUMN cust_card_number TO vchr_loyalty_card_number;

ALTER TABLE branch ADD COLUMN flt_size DOUBLE PRECISION;
ALTER TABLE branch ADD COLUMN int_price_template INT;
ALTER TABLE tax_master ADD COLUMN int_intra_tax INTEGER DEFAULT 0;

-- CREATE TABLE financiers (
--   pk_bint_id BIGSERIAL PRIMARY KEY,
--   vchr_name VARCHAR(100) NOT NULL,
--   bln_active BOOLEAN NOT NULL DEFAULT TRUE,
--   fk_company_id BIGINT REFERENCES company(pk_bint_id)
-- );
--
-- CREATE TABLE finance_schema(
--   pk_bint_id BIGSERIAL PRIMARY KEY,
--   vchr_schema VARCHAR(50),
--   dat_from DATE,
--   dat_to DATE,
--   fk_financier_id BIGINT REFERENCES financiers(pk_bint_id),
--
-- );
ALTER TABLE branch ADD COLUMN int_price_template INT;

ALTER TABLE Products ADD COLUMN int_sales INT;
ALTER TABLE Products DROP COLUMN json_sales;


ALTER TABLE item ALTER COLUMN dbl_supplier_cost DROP NOT  NULL;
ALTER TABLE item ALTER COLUMN dbl_dealer_cost DROP NOT  NULL;
ALTER TABLE item ALTER COLUMN dbl_mrp DROP NOT  NULL;
ALTER TABLE item ALTER COLUMN dbl_mop DROP NOT  NULL;



CREATE TABLE receipt(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  dat_issue TIMESTAMP,
  fk_customer_id BIGINT REFERENCES customer_details(pk_bint_id),
  int_fop INT,
  dbl_amount DOUBLE PRECISION,
  vchr_remarks TEXT,
  fk_created_id BIGINT REFERENCES userdetails(user_ptr_id),
  fk_updated_id BIGINT REFERENCES userdetails(user_ptr_id),
  int_doc_status INTEGER,
  dat_created TIMESTAMP,
  dat_updated TIMESTAMP
);


CREATE TABLE payment_details(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_sales_master_id BIGINT REFERENCES sales_master(pk_bint_id) NOT NULL,
  int_fop INTEGER NOT NULL,
  vchr_card_number VARCHAR(20),
  vchr_name VARCHAR(100),
  vchr_finance_schema VARCHAR(20),
  vchr_reff_number VARCHAR(100),
  dbl_receved_amt DOUBLE PRECISION,
  dbl_finance_amt DOUBLE PRECISION,
  dat_created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

alter table address_supplier add column bln_primary BOOLEAN;
