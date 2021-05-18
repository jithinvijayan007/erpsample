CREATE TABLE tax_master(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_name VARCHAR(100),
  bln_active BOOLEAN
);

CREATE TABLE brands(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_code VARCHAR(50),
  vchr_name VARCHAR(150),
  int_status INTEGER DEFAULT 1
);

CREATE TABLE company(
    pk_bint_id BIGSERIAL PRIMARY KEY,
    vchr_name VARCHAR(50) NOT NULL,
    vchr_address VARCHAR(250),
    int_gstin BIGINT,
    vchr_mail VARCHAR(150),
    vchr_phone VARCHAR(25),
    vchr_logo VARCHAR(350),
    vchr_print_logo VARCHAR(350),
    int_status INTEGER DEFAULT 1
);

CREATE TABLE states(
		pk_bint_id BIGSERIAL PRIMARY KEY,
    vchr_name VARCHAR(50)
);
INSERT INTO states (vchr_name,vchr_code) VALUES ('JAMMU & KASHMIR','IN-JK'),('HIMACHAL PRADESH','IN-HP'),('PUNJAB','IN-PB'),('CHANDIGARH','IN-CH'),('UTTARANCHAL','IN-UT'),('HARYANA','IN-HR'),('DELHI','IN-DL'),('RAJASTHAN','IN-RJ'),('UTTAR PRADESH','IN-UP'),('BIHAR','IN-BR'),('SIKKIM','IN-SK'),('ARUNACHAL PRADESH','IN-AR'),('NAGALAND','IN-NL'),('MANIPUR','IN-MN'),('MIZORAM','IN-MZ'),('TRIPURA','IN-TR'),('MEGHALAYA','IN-ML'),('ASSAM','IN-AS'),('WEST BENGAL','IN-WB'),('JHARKHAND','IN-JH'),('ORISSA','IN-OR'),('CHHATTISGARH','IN-CT'),('MADHYA PRADESH','IN-MP'),('GUJARAT','IN-GJ'),('DAMAN & DIU','IN-DD'),('DADRA & NAGAR HAVELI','IN-DN'),('MAHARASHTRA','IN-MH'),('ANDHRA PRADESH','IN-AP'),('KARNATAKA','IN-KA'),('GOA','IN-GA'),('LAKSHADWEEP','IN-LD'),('KERALA','IN-KL'),('TAMIL NADU','IN-TN'),('PONDICHERRY','IN-PY'),('ANDAMAN & NICOBAR ISLANDS','IN-AN');

CREATE TABLE branch(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_code VARCHAR(20),
  vchr_name VARCHAR(50) NOT NULL,
  vchr_address VARCHAR(100),
  vchr_email VARCHAR(50),
  vchr_phone VARCHAR(20),
  fk_company BIGINT REFERENCES company(pk_bint_id) NULL,
  vchr_category VARCHAR(50),
  dat_close TIMESTAMP,
  bint_stock_limit BIGINT,
  flt_static_ip FLOAT,
  flt_latitude FLOAT,
  flt_longitude FLOAT,
  dat_inauguration DATE,
  tim_inauguration TIME WITHOUT TIME ZONE,
  vchr_inaugurated_by VARCHAR(50)
);

CREATE TABLE category(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_code VARCHAR(30),
  vchr_name VARCHAR(30),
  int_status INTEGER,
  fk_created_id BIGINT REFERENCES auth_user(id),
  fk_updated_id BIGINT REFERENCES auth_user(id),
  dat_created TIMESTAMP,
  dat_updated TIMESTAMP
);
--
-- ALTER TABLE category RENAME vchr_categorycode to vchr_code;
-- ALTER TABLE category RENAME vchr_categoryname to vchr_name;
-- ALTER TABLE category ADD fk_updated_id BIGINT REFERENCES auth_user(id);
-- ALTER TABLE category ADD fk_created_id BIGINT REFERENCES auth_user(id);
-- ALTER TABLE category ADD dat_created TIMESTAMP;
-- ALTER TABLE category ADD dat_updated TIMESTAMP;



-- CREATE TABLE department(
--   pk_bint_id BIGSERIAL PRIMARY KEY,
--   vchr_code VARCHAR(50),
--   vchr_name VARCHAR(150),
--   int_status INTEGER
-- );


CREATE TABLE groups(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_code VARCHAR(50),
  vchr_name VARCHAR(150),
  int_status INTEGER DEFAULT 1
);



CREATE TABLE userdetails(
  user_ptr_id BIGINT REFERENCES auth_user PRIMARY KEY,
  bint_phone BIGINT,
  vchr_pssrsttkn VARCHAR(30),
  bint_passrstflg BIGINT,
  dat_passrsttime TIMESTAMP,
  fk_group_id BIGINT REFERENCES groups(pk_bint_id),
  fk_company_id BIGINT REFERENCES company(pk_bint_id),
  fk_branch_id BIGINT REFERENCES branch(pk_bint_id),
  fk_brand_id BIGINT REFERENCES brands(pk_bint_id),
  bint_usercode INTEGER UNIQUE,
  vchr_profpic VARCHAR(30),
  dat_resapp TIMESTAMP,
  int_areaid INTEGER,
  dat_created TIMESTAMP,
  dat_updated TIMESTAMP,
  fk_created_id BIGINT REFERENCES auth_user(id),
  fk_updated_id BIGINT REFERENCES auth_user(id),
  json_product JSONB
);
-- ALTER TABLE userdetails ADD ;
-- ALTER TABLE userdetails ALTER COLUMN bint_phone TYPE bigint;
-- ALTER TABLE userdetails
-- ADD UNIQUE (bint_usercode);
-- ALTER TABLE userdetails ALTER bint_usercode TYPE bigint;
-- ALTER TABLE userdetails RENAME dat_creaed TO dat_created;
-- alter table userdetails add  fk_updated_id BIGINT REFERENCES auth_user(id);
-- alter table userdetails add  fk_created_id BIGINT REFERENCES auth_user(id);


CREATE TABLE specifications(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_name VARCHAR(50) NOT NULL,
  bln_status boolean DEFAULT true
);

CREATE TABLE products(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_name VARCHAR(50) NOT NULL,
  fk_category_id BIGINT REFERENCES category(pk_bint_id) NOT NULL,
  fk_specification_id BIGINT REFERENCES specifications(pk_bint_id) NOT NULL,
  vchr_hsn_code VARCHAR(50),
  vchr_sac_code VARCHAR(50),
  int_status INTEGER DEFAULT 1,
  bln_sales boolean -- true if sales,false if service
);

CREATE TABLE item_group (
	pk_bint_id BIGSERIAL PRIMARY KEY,
	vchr_item_group VARCHAR(30),
	int_status INTEGER DEFAULT 1,
  fk_created_id BIGINT REFERENCES auth_user(id),
  fk_updated_id BIGINT REFERENCES auth_user(id),
  dat_created TIMESTAMP,
  dat_updated TIMESTAMP
);
-- ALTER TABLE item_group ADD fk_updated_id BIGINT REFERENCES auth_user(id);
-- ALTER TABLE item_group ADD fk_created_id BIGINT REFERENCES auth_user(id);
-- ALTER TABLE item_group ADD dat_created TIMESTAMP;
-- ALTER TABLE item_group ADD dat_updated TIMESTAMP;


ALTER TABLE products DROP COLUMN fk_specification_id;


CREATE TABLE item_category(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_item_category VARCHAR(50) NOT NULL,
  json_tax_master JSONB,
  json_specification_id JSONB,
  int_status INTEGER DEFAULT 1
);



CREATE TABLE item(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_product_id BIGINT REFERENCES products(pk_bint_id) NOT NULL,
  fk_brand_id BIGINT REFERENCES brands(pk_bint_id) NOT NULL,
  vchr_item_code VARCHAR(50) NOT NULL UNIQUE,
  fk_item_category_id BIGINT REFERENCES item_category(pk_bint_id) NOT NULL,
  fk_item_group_id BIGINT REFERENCES item_group(pk_bint_id) NOT NULL,
  dbl_supplier_cost DOUBLE PRECISION NOT NULL,
  dbl_dealer_cost DOUBLE PRECISION NOT NULL,
  dbl_mrp DOUBLE PRECISION NOT NULL,
  dbl_mop DOUBLE PRECISION NOT NULL,
  json_specification_id JSONB,
  int_reorder_level INTEGER,
  vchr_prefix VARCHAR(40),
  imei_status BOOLEAN, --true = imei number in serial number ,false if automatic serial number
  sale_status BOOLEAN, -- true saleable ,false not saleable
  int_status INTEGER DEFAULT 1
);

create table supplier (
pk_bint_id BIGSERIAL PRIMARY KEY,
vchr_name VARCHAR(50),
vchr_from VARCHAR(50),
vchr_code VARCHAR(50),
int_credit_days INTEGER,
bint_credit_limit BIGINT,
dat_po_expiry_date TIMESTAMP,
bint_tin_no BIGINT,
bint_cst_no BIGINT,
vchr_gstin VARCHAR(50),
vchr_gstin_status VARCHAR(50),
fk_category_id BIGINT REFERENCES category(pk_bint_id),
fk_tax_class_id BIGINT REFERENCES tax_master(pk_bint_id),
vchr_account_group VARCHAR(50),
vchr_bank_account VARCHAR(50),
vchr_pan_no VARCHAR(50),
vchr_pan_status VARCHAR(50),
fk_created_id BIGINT REFERENCES auth_user(id),
fk_updated_id BIGINT REFERENCES auth_user(id),
dat_created TIMESTAMP,
dat_updated TIMESTAMP
);
-- ALTER TABLE supplier ADD fk_updated_id BIGINT REFERENCES auth_user(id);
-- ALTER TABLE supplier ADD fk_created_id BIGINT REFERENCES auth_user(id);
-- ALTER TABLE supplier ADD dat_created TIMESTAMP;
-- ALTER TABLE supplier ADD dat_updated TIMESTAMP;


CREATE TABLE address_supplier(
pk_bint_id BIGSERIAL PRIMARY KEY,
vchr_address VARCHAR(185),
vchr_email VARCHAR(30),
bint_phone_no BIGINT,
INT_pin_code INT,
fk_supplier_id BIGINT REFERENCES supplier(pk_bint_id)
);
CREATE TABLE contact_person_supplier(
pk_bint_id BIGSERIAL PRIMARY KEY,
vchr_name VARCHAR(30),
vchr_designation VARCHAR(30),
vchr_department VARCHAR(30),
vchr_office VARCHAR(30),
bint_mobile_no BIGINT,
bint_mobile_no2 BIGINT,
fk_supplier_id BIGINT REFERENCES supplier(pk_bint_id)
);

CREATE TABLE dealer(
	pk_bint_id BIGSERIAL PRIMARY KEY,
	vchr_name VARCHAR(50),
	vchr_from VARCHAR(50),
	vchr_code VARCHAR(50),
	int_credit_days INTEGER,
	bint_credit_limit BIGINT,
	dat_po_expiry_date TIMESTAMP,
	bint_tin_no BIGINT,
	bint_cst_no BIGINT,
	vchr_gstin VARCHAR(50),
	vchr_gstin_status VARCHAR(50),
	fk_category_id BIGINT REFERENCES category(pk_bint_id),
	fk_tax_class_id BIGINT REFERENCES tax_master(pk_bint_id),
	vchr_account_group VARCHAR(50),
	vchr_bank_account VARCHAR(50),
	vchr_pan_no VARCHAR(50),
	vchr_pan_status VARCHAR (50)
);


ALTER TABLE dealer DROP COLUMN int_po_expiry_days;
ALTER TABLE dealer ADD COLUMN int_po_expiry_days INTEGER;
ALTER TABLE dealer DROP COLUMN fk_category_id;
ALTER TABLE dealer ADD COLUMN fk_category_id BIGINT REFERENCES other_category(pk_bint_id);
ALTER TABLE dealer ADD COLUMN int_is_act_del INTEGER;
ALTER TABLE dealer ADD COLUMN fk_created_id BIGINT;
ALTER TABLE dealer ADD COLUMN fk_updated_id BIGINT;
ALTER TABLE dealer ADD COLUMN dat_created TIMESTAMP;
ALTER TABLE dealer ADD COLUMN dat_updated TIMESTAMP;




CREATE TABLE dealer_address(
	pk_bint_id BIGSERIAL PRIMARY KEY,
	vchr_address VARCHAR(180),
	vchr_email VARCHAR(30),
	bint_phone_no BIGINT,
	int_pincode INTEGER,
	fk_dealer_id BIGINT REFERENCES dealer (pk_bint_id)
);
ALTER TABLE dealer_address ADD COLUMN bln_status BOOLEAN default True;

CREATE TABLE dealer_contact_person(
	pk_bint_id BIGSERIAL PRIMARY KEY,
	vchr_name VARCHAR(50),
	vchr_desigination VARCHAR(50),
	vchr_department VARCHAR (50),
	vchr_office VARCHAR(50),
	bint_mobile_no1 BIGINT,
	bint_mobile_no2 BIGINT,
	fk_dealer_id BIGINT REFERENCES dealer(pk_bint_id)
);
ALTER TABLE dealer_contact_person RENAME vchr_desigination to vchr_designation;
ALTER TABLE dealer_contact_person ADD COLUMN bln_status BOOLEAN default True;

CREATE TABLE dealer_log(
 pk_bint_id BIGSERIAL PRIMARY KEY,
 vchr_remarks TEXT,
 vchr_status VARCHAR(20),
 dat_created TIMESTAMP,
 fk_created_id BIGINT REFERENCES auth_user(id),
 fk_dealer_id BIGINT REFERENCES dealer
);

ALTER TABLE item ADD COLUMN dat_created  TIMESTAMP DEFAULT now();
ALTER TABLE item ADD COLUMN fk_created_id BIGINT REFERENCES userdetails(user_ptr_id);
ALTER TABLE item ADD COLUMN fk_updated_id BIGINT REFERENCES userdetails(user_ptr_id);
ALTER TABLE item_category ADD COLUMN dat_created  TIMESTAMP DEFAULT now();
ALTER TABLE item_category ADD COLUMN fk_created_id BIGINT REFERENCES userdetails(user_ptr_id);
ALTER TABLE item_category ADD COLUMN fk_updated_id BIGINT REFERENCES userdetails(user_ptr_id);
ALTER TABLE products ADD COLUMN dat_created  TIMESTAMP DEFAULT now();
ALTER TABLE products ADD COLUMN fk_created_id BIGINT REFERENCES userdetails(user_ptr_id);
ALTER TABLE products ADD COLUMN fk_updated_id BIGINT REFERENCES userdetails(user_ptr_id);
ALTER TABLE branch DROP COLUMN fk_company;
-- insert into tax_master (vchr_name,bln_active) values ('CGST','t');
-- insert into specifications (vchr_name) values ('colour');
alter table branch add column bln_active BOOLEAN default True;

create table po_master(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_po_num VARCHAR(20),
  dat_po TIMESTAMP,
  dat_po_expiry TIMESTAMP,-->dat_po + expiry days for supplier
  fk_supplier_id BIGINT REFERENCES supplier(pk_bint_id),
  fk_branch_id BIGINT REFERENCES branch(pk_bint_id),-->[warehouses or head office only]
  vchr_notes TEXT,
  fk_created_id BIGINT REFERENCES auth_user(id),
  dat_created TIMESTAMP,
  fk_updated_id BIGINT REFERENCES auth_user(id),
  dat_updated TIMESTAMP,
  int_doc_status INTEGER -->[-1,0,1]
);


create table po_details(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_item_id BIGINT REFERENCES item(pk_bint_id),
  fk_po_master_id BIGINT REFERENCES po_master(pk_bint_id),
  int_qty INTEGER
  );


CREATE TABLE document(
	pk_bint_id BIGSERIAL PRIMARY KEY,
	vchr_module_name VARCHAR(50) NOT NULL,
	vchr_short_code VARCHAR(5) NOT NULL,
	int_number INTEGER NOT NULL
);
ALTER TABLE branch ADD vchr_category VARCHAR(50);
ALTER TABLE branch ADD dat_close TIMESTAMP;
ALTER TABLE branch ADD bint_stock_limit BIGINT;
ALTER TABLE branch ADD flt_static_ip FLOAT;
ALTER TABLE branch ADD flt_latitude FLOAT;
ALTER TABLE branch ADD flt_longitude FLOAT;
ALTER TABLE branch ADD dat_inauguration DATE;
ALTER TABLE branch ADD tim_inauguration TIME WITHOUT TIME ZONE;
ALTER TABLE branch ADD vchr_inaugurated_by VARCHAR(50);

ALTER TABLE item ADD COLUMN  image1 VARCHAR(350);
ALTER TABLE item ADD COLUMN  image2 VARCHAR(350);
ALTER TABLE item ADD COLUMN  image3 VARCHAR(350);

ALTER TABLE supplier DROP dat_po_expiry_date;
ALTER TABLE supplier ADD int_po_expiry_days INT;



ALTER TABLE item ADD COLUMN  vchr_name VARCHAR(100);
ALTER TABLE branch DROP COLUMN bln_active;
ALTER TABLE branch ADD COLUMN int_status INTEGER DEFAULT 1;


ALTER TABLE branch DROP COLUMN vchr_category;
ALTER TABLE branch ADD COLUMN fk_category_id BIGINT REFERENCES other_category(pk_bint_id);
ALTER TABLE branch ADD COLUMN int_type INTEGER;


ALTER TABLE supplier DROP fk_category_id;
ALTER TABLE supplier ADD fk_category_id BIGINT REFERENCES other_category;



create table purchase(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_purchase_num VARCHAR(20),
  dat_purchase TIMESTAMP,
  fk_supplier_id BIGINT REFERENCES supplier(pk_bint_id),
  fk_branch_id BIGINT REFERENCES branch(pk_bint_id),-->[warehouses or head office only]
  fk_po_id BIGINT REFERENCES po_master(pk_bint_id),
  int_fop INTEGER,
  dat_pay_before TIMESTAMP,
  dbl_total DOUBLE PRECISION,
  vchr_notes TEXT,
  fk_created_id BIGINT REFERENCES auth_user(id),
  dat_created TIMESTAMP,
  fk_updated_id BIGINT REFERENCES auth_user(id),
  dat_updated TIMESTAMP,
  int_doc_status INTEGER -->[-1,0,1]
);

create table purchase_details(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_item_id BIGINT REFERENCES item(pk_bint_id),
  fk_purchase_id BIGINT REFERENCES purchase(pk_bint_id),
  int_qty INTEGER,
  int_free INTEGER,
  int_avail INTEGER,
  dbl_unitprice DOUBLE PRECISION,-->[price of a single piece without tax and discount]
  dbl_dscnt_percent DOUBLE PRECISION,-->[total discount percent]
  dbl_dscnt_perunit DOUBLE PRECISION,-->[per single piece]
  dbl_discount DOUBLE PRECISION,-->[total amount]
  jsn_tax JSONB,--> (CGST:4,SGST:4)[per piece]
  dbl_tax DOUBLE PRECISION,-->[tax amount per piece]
  dbl_ppu DOUBLE PRECISION,-->[price of a single piece with tax and discount]
  dbl_total_amount DOUBLE PRECISION,-->[dbl_ppu * int_qty]
  txt_imei TEXT,-->text
  txt_imei_avail TEXT,
  txt_imei_dmgd TEXT,-->damaged item
  vchr_batch_no VARCHAR(30)
);
CREATE TABLE customer_details(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_name VARCHAR(100),
  vchr_email VARCHAR(200),
  int_mobile BIGINT
);

CREATE TABLE sales_master(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_customer_id BIGINT REFERENCES customer_details(pk_bint_id),
  fk_staff_id BIGINT REFERENCES auth_user(id),
  fk_branch_id BIGINT REFERENCES branch(pk_bint_id),
  dat_invoice TIMESTAMP,
  vchr_invoice_num VARCHAR(50),
  vchr_remarks VARCHAR(500),
  dat_created TIMESTAMP,
  int_doc_status INTEGER,
  dbl_total_amt DOUBLE PRECISION,
  dbl_total_tax DOUBLE PRECISION,
  dbl_discount DOUBLE PRECISION,
  json_tax JSONB,
  dbl_loyalty DOUBLE PRECISION,
  dbl_buyback DOUBLE PRECISION
);

CREATE TABLE sales_details(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_master_id BIGINT REFERENCES sales_master(pk_bint_id),
  fk_item_id BIGINT REFERENCES item(pk_bint_id),
  int_qty INTEGER,
  dbl_amount DOUBLE PRECISION,
  dbl_tax DOUBLE PRECISION,
  dbl_discount DOUBLE PRECISION,
  dbl_buyback DOUBLE PRECISION,
  json_tax JSONB,
  txt_imei TEXT,
  vchr_batch VARCHAR(50)
);

CREATE TABLE partial_invoice (
  pk_bint_id BIGSERIAL PRIMARY KEY,
  json_data JSONB,
  int_active INTEGER DEFAULT 0,
  dat_created TIMESTAMP,
  dat_invoice TIMESTAMP,
  fk_invoice_id BIGINT REFERENCES sales_master(pk_bint_id)
);





create table stock_request(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_from_id BIGINT REFERENCES branch(pk_bint_id),
  fk_to_id BIGINT REFERENCES branch(pk_bint_id),
  dat_request TIMESTAMP,
  dat_expected TIMESTAMP,
  vchr_remarks TEXT,
  fk_created_id BIGINT REFERENCES auth_user(id),
  dat_created TIMESTAMP,
  fk_updated_id BIGINT REFERENCES auth_user(id),
  dat_updated TIMESTAMP,
  int_doc_status INTEGER, -->[-1,0,1]
  bln_approved INTEGER -->[]
);
create table isr_details(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_request_id BIGINT REFERENCES stock_request(pk_bint_id),
  fk_item_id BIGINT REFERENCES item(pk_bint_id),
  int_qty INTEGER
);

create table stock_transfer(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_request_id  BIGINT REFERENCES stock_request(pk_bint_id),
  fk_pd_id BIGINT REFERENCES purchase_details(pk_bint_id),
  fk_from_id BIGINT REFERENCES branch(pk_bint_id),
  fk_to_id BIGINT REFERENCES branch(pk_bint_id),
  dat_transfer TIMESTAMP,
  dat_expected TIMESTAMP,
  dat_acknowledge TIMESTAMP,
  fk_created_id BIGINT REFERENCES auth_user(id),
  dat_created TIMESTAMP,
  fk_updated_id BIGINT REFERENCES auth_user(id),
  dat_updated TIMESTAMP,
  int_doc_status INTEGER, -->[-1,0,1]
  int_acknowledge INTEGER,
  int_status INTEGER -->transit-0,received-1
);
create table ist_details(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_transfer_id BIGINT REFERENCES stock_transfer(pk_bint_id),
  fk_item_id BIGINT REFERENCES item(pk_bint_id),
  int_qty INTEGER,
  txt_imei TEXT
);


CREATE TABLE branch_stock_master (
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_transfer_id BIGINT REFERENCES stock_transfer(pk_bint_id),
  fk_pd_id BIGINT REFERENCES purchase(pk_bint_id),
  dat_stock TIMESTAMP
);

CREATE TABLE branch_stock_details (
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_item_id BIGINT REFERENCES item(pk_bint_id),
  fk_master_id BIGINT REFERENCES branch_stock_master(pk_bint_id),
  int_qty INTEGER,
  txt_imei TEXT
);


alter table po_details add COLUMN dbl_prate DOUBLE PRECISION;
alter table purchase add column dbl_addition DOUBLE PRECISION;
alter table purchase add column dbl_deduction DOUBLE PRECISION;

alter table purchase_details add column dbl_perpie_aditn DOUBLE PRECISION;
alter table purchase_details add column dbl_perpie_dedctn DOUBLE PRECISION;
ALTER TABLE stock_request RENAME COLUMN vchr_notes TO vchr_remarks;
ALTER TABLE stock_request ADD COLUMN vchr_stkrqst_num VARCHAR(20);
ALTER TABLE stock_transfer ADD COLUMN vchr_stktransfer_num VARCHAR(20);
ALTER TABLE stock_transfer DROP COLUMN fk_pd_id;
ALTER TABLE ist_details ADD COLUMN fk_pd_id BIGINT REFERENCES purchase_details(pk_bint_id);

insert into document (vchr_module_name,vchr_short_code,int_number) values ('STOCK REQUEST','STRQ',0);
insert into document (vchr_module_name,vchr_short_code,int_number) values ('STOCK TRANSFER','STFR',0);
insert into document (vchr_module_name,vchr_short_code,int_number) values ('PURCHASE','PUR',0);
insert into document (vchr_module_name,vchr_short_code,int_number) values ('PURCHASE ORDER','PRO',0);

-- ALTER TABLE item_group ALTER dat_created SET DEFAULT now();
--
--
-- ALTER TABLE item_group ALTER dat_created SET DEFAULT now();
-- ALTER TABLE item_group ALTER dat_updated SET DEFAULT now();
--
-- ALTER TABLE supplier ALTER dat_created SET DEFAULT now();
-- ALTER TABLE supplier ALTER dat_updated SET DEFAULT now();
--
-- ALTER TABLE supplier_log ALTER dat_created SET DEFAULT now();
--
-- ALTER TABLE supplier_log ADD pk_bint_id BIGSERIAL PRIMARY KEY;
--
-- ALTER TABLE supplier ADD is_act_del INTEGER;


ALTER TABLE supplier ADD COLUMN fk_states_id BIGINT REFERENCES states (pk_bint_id);

ALTER TABLE branch ADD COLUMN fk_states_id BIGINT REFERENCES states (pk_bint_id);


alter table purchase add column dbl_roundoff_value DOUBLE PRECISION null;
alter table purchase_details drop column txt_imei_dmgd ;
alter table purchase_details drop column txt_imei_avail ;
alter table purchase_details drop column txt_imei;

alter table purchase_details add column jsn_imei json;
alter table purchase_details add column jsn_imei_avail json;
alter table purchase_details add column jsn_imei_dmgd json;

alter table po_master add column int_status integer;
ALTER TABLE stock_transfer ADD COLUMN vchr_remarks TEXT;
ALTER TABLE address_supplier ADD COLUMN fk_states_id BIGINT REFERENCES states(pk_bint_id);


ALTER TABLE customer_details ADD COLUMN fk_state_id BIGINT REFERENCES states(pk_bint_id);
ALTER TABLE states ADD COLUMN vchr_code VARCHAR(100);


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


ALTER TABLE coupon ADD fk_updated_id BIGINT REFERENCES auth_user(id);
ALTER TABLE coupon ADD fk_created_id BIGINT REFERENCES auth_user(id);
ALTER TABLE coupon ADD dat_created TIMESTAMP;
ALTER TABLE coupon ADD dat_updated TIMESTAMP;


ALTER TABLE supplier DROP bint_tin_no;
ALTER TABLE supplier DROP bint_cst_no;
ALTER TABLE supplier ADD vchr_tin_no VARCHAR(50);
ALTER TABLE supplier ADD vchr_cst_no VARCHAR(50);

ALTER TABLE dealer DROP bint_tin_no;
ALTER TABLE dealer DROP bint_cst_no;
ALTER TABLE dealer ADD vchr_tin_no VARCHAR(50);
ALTER TABLE dealer ADD vchr_cst_no VARCHAR(50);

ALTER TABLE branch_stock_details ADD COLUMN vchr_batch_no VARCHAR(30);
ALTER TABLE branch_stock_details ADD COLUMN jsn_imei_dmgd jsonb;
