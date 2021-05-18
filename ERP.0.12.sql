CREATE TABLE offers (
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_code VARCHAR(100),
  vchr_details VARCHAR(100)
);
alter table offers add column bln_item boolean;
ALTER TABLE offers add column bln_active BOOL DEFAULT FALSE;
ALTER TABLE offers ADD COLUMN fk_branch_id BIGINT REFERENCES branch(pk_bint_id);


CREATE TABLE enquiry_master (
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_enquiry_num VARCHAR(50) NOT NULL,
  fk_customer_id BIGINT REFERENCES customer_details(pk_bint_id),
  vchr_enquiry_source VARCHAR(50) NOT NULL,
  vchr_customer_type VARCHAR(50) NOT NULL,
  vchr_enquiry_priority VARCHAR(50) NOT NULL,
  fk_assigned_id BIGINT REFERENCES auth_user(id),
  bln_sms BOOLEAN,
  chr_doc_status CHAR NOT NULL,
  fk_created_by_id BIGINT CONSTRAINT enquiry_master_created REFERENCES auth_user(id),
	fk_updated_by_id BIGINT CONSTRAINT enquiry_master_updated REFERENCES auth_user(id) NULL,
	dat_created_at TIMESTAMP without time zone DEFAULT NOW(),
	dat_updated_at TIMESTAMP NULL,
  fk_company_id BIGINT REFERENCES company(pk_bint_id) NOT NULL
);

alter table enquiry_master add column int_customer_type integer;
alter table enquiry_master add column vchr_order_num varchar(30);
alter table enquiry_master add column vchr_reference_num varchar(30);
alter table enquiry_master add column fk_branch_id BIGINT REFERENCES branch(pk_bint_id);
ALTER TABLE enquiry_master ADD COLUMN dbl_partial_amt DOUBLE PRECISION;
alter table enquiry_master add column vchr_remarks TEXT;
alter table enquiry_master add column int_sale_type INTEGER;
alter table enquiry_master add column vchr_hash TEXT;
ALTER TABLE enquiry_master ADD COLUMN fk_offers_id BIGINT REFERENCES offers(pk_bint_id);

CREATE TABLE stockmaster(
    pk_bint_id BIGSERIAL PRIMARY KEY,
    fk_supplier_id BIGINT REFERENCES supplier(pk_bint_id) NOT NULL,
    dat_added  TIMESTAMP NULL,
    vchr_payment_mode VARCHAR(50) NOT NULL,
    dbl_paid_amount DOUBLE PRECISION ,
    fk_branch_id BIGINT REFERENCES branch(pk_bint_id) NOT NULL,
    fk_company_id BIGINT REFERENCES company(pk_bint_id) NOT NULL,
    fk_user_id BIGINT REFERENCES userdetails(user_ptr_id) NOT NULL,
    dat_updated  TIMESTAMP ,
    fk_updated_id BIGINT REFERENCES userdetails(user_ptr_id)
);

CREATE TABLE stockdetails(
    pk_bint_id BIGSERIAL PRIMARY KEY,
    fk_stock_master_id BIGINT REFERENCES stockmaster(pk_bint_id) NOT NULL,
    fk_item_id BIGINT REFERENCES item(pk_bint_id) NOT NULL,
    int_qty INTEGER ,
    int_available INTEGER,
    dbl_cost DOUBLE PRECISION ,
    dbl_min_selling_price DOUBLE PRECISION ,
    dbl_max_selling_price DOUBLE PRECISION
);
ALTER TABLE stockdetails ADD COLUMN dbl_imei_json json;

  CREATE TABLE item_exchange (
   pk_bint_id BIGSERIAL PRIMARY KEY,
   fk_item_id BIGINT REFERENCES item(pk_bint_id),
   vchr_filename_json json
  );
Alter TABLE item_exchange ADD COLUMN dbl_exchange_amt DOUBLE PRECISION;
Alter TABLE item_exchange ADD COLUMN vchr_exc_imei VARCHAR(50);
Alter TABLE item_exchange ADD COLUMN fk_item_enquiry_id BIGINT REFERENCES item_enquiry(pk_bint_id);

CREATE TABLE item_enquiry (
    pk_bint_id BIGSERIAL PRIMARY KEY,
    fk_enquiry_master_id BIGINT REFERENCES enquiry_master(pk_bint_id) NOT NULL,
    fk_product_id BIGINT REFERENCES products(pk_bint_id) NOT NULL,
    fk_brand_id BIGINT REFERENCES brands(pk_bint_id) NOT NULL,
    fk_item_id BIGINT REFERENCES item(pk_bint_id) NOT NULL,
    int_quantity INTEGER NOT NULL,
    dbl_amount DOUBLE PRECISION,
    vchr_enquiry_status VARCHAR(50) NOT NULL,
    vchr_remarks TEXT,
    fk_stockdetails_id BIGINT REFERENCES stockdetails(pk_bint_id),
    int_sold INTEGER,
    dbl_sup_amount INTEGER,
    dbl_buyback INTEGER,
    dbl_discount INTEGER,
    dbl_min_price INTEGER,
    dbl_max_price INTEGER,
    dbl_imei_json json
);
alter table item_enquiry add column int_fop INTEGER default 0;
ALTER TABLE item_enquiry ADD dbl_buy_back_amount DOUBLE PRECISION;
ALTER TABLE item_enquiry ADD dbl_discount_amount DOUBLE PRECISION;
ALTER TABLE item_enquiry ADD COLUMN dbl_gdp_amount DOUBLE PRECISION default 0.0;
ALTER TABLE item_enquiry ADD COLUMN dbl_gdew_amount DOUBLE PRECISION default 0.0;
ALTER TABLE item_enquiry ADD COLUMN int_type INTEGER default 0;
ALTER TABLE item_enquiry ADD COLUMN  vchr_exc_imei VARCHAR(50);
ALTER TABLE item_enquiry ADD  dbl_actual_gdp DOUBLE PRECISION;
ALTER TABLE item_enquiry ADD  dbl_actual_gdew DOUBLE PRECISION;
ALTER TABLE item_enquiry ADD  dbl_actual_est_amt DOUBLE PRECISION;
ALTER TABLE item_enquiry ADD COLUMN  dbl_exchange_amt DOUBLE PRECISION;
ALTER TABLE item_enquiry ADD COLUMN bln_smart_choice BOOLEAN DEFAULT False;
alter table item_enquiry add column dat_gdp TIMESTAMP;
alter table item_enquiry add column dat_gdew TIMESTAMP;
alter table item_enquiry add column dat_sale TIMESTAMP;
ALTER TABLE item_enquiry alter dbl_imei_json type jsonb;
ALTER TABLE item_enquiry ADD COLUMN dbl_indirect_discount_amount DOUBLE PRECISION;
ALTER TABLE item_enquiry ADD COLUMN dbl_tax DOUBLE PRECISION;
ALTER TABLE item_enquiry ADD COLUMN json_tax JSONB;
ALTER TABLE item_enquiry ADD COLUMN dbl_mrp_price DOUBLE PRECISION;
ALTER TABLE item_enquiry ADD COLUMN dbl_myg_price DOUBLE PRECISION;
ALTER TABLE item_enquiry ADD COLUMN dbl_mop_price DOUBLE PRECISION;
ALTER TABLE item_enquiry ADD COLUMN dbl_dealer_price DOUBLE PRECISION;
ALTER TABLE item_enquiry ADD COLUMN dbl_cost_price DOUBLE PRECISION;
alter table item_enquiry add column int_sale_type INTEGER;


alter table item_enquiry  drop column int_sale_type  ;
ALTER TABLE item_enquiry DROP dbl_buyback;
ALTER TABLE item_enquiry DROP dbl_discount;
Alter TABLE item_enquiry DROP COLUMN vchr_exc_imei ;
Alter TABLE item_enquiry DROP COLUMN fk_item_exchange_id;
Alter TABLE item_enquiry DROP COLUMN dbl_exchange_amt;

ALTER TABLE item_enquiry ADD COLUMN  fk_item_exchange_id BIGINT REFERENCES item_exchange(pk_bint_id);

ALTER TABLE stockmaster ADD vchr_purchase_order_number varchar(50);

create table priority (pk_bint_id BIGSERIAL PRIMARY KEY,vchr_priority_name varchar(50),bln_status boolean, fk_company_id BIGINT REFERENCES company(pk_bint_id));
alter table products add fk_company_id BIGINT REFERENCES company(pk_bint_id);
alter table products add dct_product_spec jsonb;
alter table products add bln_visible boolean;

-- alter table products add column vchr_product_img varchar(300);

CREATE TABLE item_details (pk_bint_id BIGSERIAL PRIMARY KEY,fk_item_id BIGINT REFERENCES item(pk_bint_id),json_spec JSONB,vchr_item_img VARCHAR(300));
alter table brands add fk_company_id BIGINT REFERENCES company(pk_bint_id);
alter table item add dbl_myg_amount DOUBLE PRECISION;

ALTER TABLE products add vchr_product_img VARCHAR(300);



CREATE TABLE buy_back(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  dat_start TIMESTAMP WITHOUT TIME ZONE,
  dat_end TIMESTAMP WITHOUT TIME ZONE,
  fk_item_id BIGINT REFERENCES item(pk_bint_id),
  int_quantity INTEGER,
  dbl_amount DOUBLE PRECISION,
  int_status INTEGER DEFAULT 1
);
ALTER TABLE customer_details add cust_salutation varchar(10);

INSERT INTO document (vchr_module_name,vchr_short_code,int_number,fk_company_id) values ('ENQUIRY','ENQ',847919,1);

ALTER TABLE enquiry_master add fk_source_id BIGINT REFERENCES source(pk_bint_id);

ALTER TABLE enquiry_master add fk_priority_id BIGINT REFERENCES priority(pk_bint_id);

ALTER TABLE source add fk_category_id BIGINT REFERENCES category(pk_bint_id);

ALTER TABLE enquiry_master alter vchr_customer_type drop not null;

ALTER TABLE enquiry_master alter  vchr_enquiry_priority drop not null;

ALTER TABLE enquiry_master alter  vchr_enquiry_source drop not null;

ALTER TABLE enquiry_master add  vchr_item_name varchar(10);

CREATE TABLE item_followup (
    pk_bint_id BIGSERIAL PRIMARY KEY,
    fk_item_enquiry_id BIGINT REFERENCES item_enquiry(pk_bint_id) NOT NULL,
    dat_followup TIMESTAMP DEFAULT NOW(),
    fk_user_id BIGINT REFERENCES user_details(user_ptr_id),
    vchr_notes VARCHAR(250),
    vchr_enquiry_status VARCHAR(50) NOT NULL,
    int_status INTEGER,
    dbl_amount DOUBLE PRECISION,
    fk_updated_id BIGINT REFERENCES user_details(user_ptr_id) NULL,
    dat_updated TIMESTAMP NULL,
    int_quantity INTEGER
);

-- ALTER TABLE products drop column fk_created_id;
-- ALTER TABLE products drop column fk_updated_id;
-- ALTER TABLE products add column fk_created_id bigint REFERENCES user_details(user_ptr_id);
-- ALTER TABLE products add column fk_updated_id bigint REFERENCES user_details(user_ptr_id);

ALTER TABLE brands add column fk_company_id bigint REFERENCES company(pk_bint_id);
-- ALTER TABLE item_category  drop column fk_created_id;
-- ALTER TABLE item_category add column fk_created_id bigint REFERENCES user_details(user_ptr_id);
-- ALTER TABLE item_category  drop column fk_updated_id;
-- ALTER TABLE item_category add column fk_updated_id bigint REFERENCES user_details(user_ptr_id);
alter TABLE customer_details add cust_activestate boolean;

alter TABLE customer_details add cust_salutation varchar(10);
CREATE TABLE item_followup (
    pk_bint_id BIGSERIAL PRIMARY KEY,
    fk_item_enquiry_id BIGINT REFERENCES item_enquiry(pk_bint_id) NOT NULL,
    dat_followup TIMESTAMP DEFAULT NOW(),
    fk_user_id BIGINT REFERENCES userdetails(user_ptr_id),
    vchr_notes VARCHAR(250),
    vchr_enquiry_status VARCHAR(50) NOT NULL,
    int_status INTEGER,
    dbl_amount DOUBLE PRECISION,
    fk_updated_id BIGINT REFERENCES userdetails(user_ptr_id) NULL,
    dat_updated TIMESTAMP NULL,
    int_quantity INTEGER
);

ALTER TABLE customer_details add fk_created_id bigint REFERENCES auth_user(id);
ALTER TABLE customer_details add dat_created date;
ALTER TABLE customer_details add alternate_mobile bigint;

CREATE TABLE enquiry_finance_images (
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_bill_image VARCHAR(350),
  vchr_delivery_image VARCHAR(350),
  vchr_proof1 VARCHAR(350),
  vchr_proof2 VARCHAR(350),
  fk_enquiry_master_id BIGINT REFERENCES enquiry_master(pk_bint_id)
);

alter table products add json_sales jsonb;


alter table item_group add fk_company_id bigint REFERENCES company(pk_bint_id);

ALTER TABLE userdetails add dat_resignation_applied date;


CREATE TABLE user_download_log(
                    pk_bint_id BIGSERIAL PRIMARY KEY,
                    fk_user_id BIGINT REFERENCES userdetails(user_ptr_id) NOT NULL,
                    fk_sub_category_id BIGINT REFERENCES sub_category(pk_bint_id),
                    dat_download TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
                    vchr_dat_filter Text,
                    vchr_filter TEXT,
                    vchr_chart TEXT,
                    fk_company_id BIGINT REFERENCES company(pk_bint_id) NOT NULL DEFAULT 1
                  );
