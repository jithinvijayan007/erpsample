CREATE TABLE sales_return (
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_sales_id BIGINT REFERENCES sales_master(pk_bint_id),
  fk_item_id BIGINT REFERENCES item(pk_bint_id),
  dbl_amount DOUBLE PRECISION,
  jsn_imei jsonb,
  dat_returned DATE,
  fk_staff_id BIGINT REFERENCES auth_user(id),
  dat_created TIMESTAMP,
  fk_created_id BIGINT REFERENCES auth_user(id),
  dat_updated TIMESTAMP,
  fk_updated_id BIGINT REFERENCES auth_user(id),
  int_doc_status INTEGER
);
alter table sales_details add column int_sales_status INTEGER;
alter table sales_details add column dbl_indirect_discount DOUBLE PRECISION;

ALTER TABLE transfer_mode_details add column dbl_expense DOUBLE PRECISION;
ALTER TABLE branch add column dbl_stock_request_amount DOUBLE PRECISION;
ALTER TABLE branch add column int_stock_request_qty INTEGER;

ALTER TABLE partial_invoice ADD COLUMN int_enq_master_id BIGINT;
ALTER TABLE receipt ADD int_pstatus INT;
ALTER TABLE receipt ADD int_receipt_type INT;
ALTER TABLE receipt ADD fk_item_id BIGINT REFERENCES ITEM;

ALTER TABLE grn_master add column dbl_bill_amount DOUBLE PRECISION;
ALTER TABLE grn_master add column vchr_bill_image VARCHAR(350);
ALTER TABLE sales_return add column vchr_image VARCHAR(350);
ALTER TABLE sales_return add column vchr_remark VARCHAR(500);

ALTER TABLE receipt ADD vchr_bank VARCHAR(50);
ALTER TABLE receipt ADD vchr_transaction_id VARCHAR(50);
ALTER TABLE receipt ADD dat_approval TIMESTAMP;

CREATE TABLE payment(
 pk_bint_id BIGSERIAL PRIMARY KEY,
 vchr_doc_num VARCHAR(50),
 dat_payment TIMESTAMP,
 int_fop INTEGER,
 int_payee_type INTEGER,
 fk_payee_id INTEGER,
 fk_branch_id BIGINT REFERENCES branch(pk_bint_id),
 dbl_amount DOUBLE PRECISION,
 vchr_remarks TEXT,
 fk_created_id BIGINT REFERENCES userdetails(user_ptr_id),
 fk_updated_id BIGINT REFERENCES userdetails(user_ptr_id),
 fk_approved_by_id BIGINT REFERENCES userdetails(user_ptr_id),
 int_doc_status INTEGER,
 dat_created TIMESTAMP,
 dat_updated TIMESTAMP
 );

insert into document (vchr_module_name,vchr_short_code,int_number) values ('DOCUMENT','DOC',0);
CREATE TABLE receipt_invoice_matching(
pk_bint_id BIGSERIAL PRIMARY KEY,
fk_sales_master_id BIGINT REFERENCES sales_master,
fk_receipt_id BIGINT REFERENCES receipt,
dbl_amount DOUBLE PRECISION,
dat_created TIMESTAMP);
INSERT INTO document(vchr_module_name,vchr_short_code,int_number) VALUES('RECEIPT','RV',1);
INSERT INTO document(vchr_module_name,vchr_short_code,int_number) VALUES('DELIVERY CHALLAN','DC',1);
ALTER TABLE receipt ADD vchr_receipt_num VARCHAR(50);

ALTER TABLE loyalty_card_status ADD COLUMN int_status INTEGER DEFAULT 0;
ALTER TABLE payment_details  add column dbl_cc_charge DOUBLE PRECISION;
ALTER TABLE sales_return  add column fk_returned_id BIGINT REFERENCES sales_master(pk_bint_id);
ALTER TABLE sales_return  add column int_qty INTEGER;

ALTER TABLE sales_return  add column bln_damaged boolean DEFAULT False;
ALTER TABLE sales_return ADD COLUMN dbl_selling_price DOUBLE PRECISION;








-- #####################nikhil for partial invoice
 alter table partial_invoice add column int_status INTEGER;
 --#############################
alter table sales_master add column dbl_rounding_off DOUBLE PRECISION;



CREATE TABLE day_closure_not_tally(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_day_closure_details_id BIGINT REFERENCES day_closure_details(pk_bint_id),
  Dat_time TIMESTAMP,
  fk_staff_id BIGINT REFERENCES userdetails(user_ptr_id),
  fk_approve_id BIGINT REFERENCES userdetails(user_ptr_id),
  total_amount DOUBLE PRECISION,
  json_dayclosure json,
  int_status INTEGER NOT NULL,
  fk_branch_id BIGINT REFERENCES branch(pk_bint_id) NOT NULL,
  vchr_remark VARCHAR(100)
);



CREATE TABLE sales_master_jio(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_customer_id BIGINT REFERENCES customer_details(pk_bint_id),
  fk_branch_id BIGINT REFERENCES branch(pk_bint_id),
  dat_invoice DATE,
  fk_staff_id BIGINT REFERENCES userdetails(user_ptr_id),
  vchr_invoice_num VARCHAR(50),
  vchr_remarks VARCHAR(500),
  fk_item_id BIGINT REFERENCES item(pk_bint_id),
  int_qty INTEGER,
  vchr_batch VARCHAR(50),
  json_imei JSONB,
  dbl_total_amt DOUBLE PRECISION,
  dbl_rounding_off DOUBLE PRECISION,
  int_doc_status INTEGER,
  dat_created TIMESTAMP,
  dat_updated TIMESTAMP,
  fk_created_id BIGINT REFERENCES userdetails(user_ptr_id),
  fk_updated_id BIGINT REFERENCES userdetails(user_ptr_id),
  int_fop INTEGER NOT NULL,
  vchr_card_number VARCHAR(20),
  vchr_name VARCHAR(100),
  vchr_reff_number VARCHAR(100),
  dbl_receved_amt DOUBLE PRECISION,
  fk_financial_year_id BIGINT REFERENCES financial_year(pk_bint_id)
);

ALTER TABLE payment ADD COLUMN int_approved INT ;



CREATE TABLE bank(
pk_bint_id BIGSERIAL PRIMARY KEY,
vchr_name VARCHAR(50) NOT NULL,
int_status INTEGER
);
alter table payment_details add column fk_bank_id BIGINT REFERENCES bank(pk_bint_id);
alter table sales_master_jio add column fk_bank_id BIGINT REFERENCES bank(pk_bint_id);



CREATE TABLE case_closure_master (
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_name VARCHAR(50) NOT NULL,
  bln_active BOOLEAN
);

insert into case_closure_master(vchr_name,bln_active) VALUES('2000',True);
insert into case_closure_master(vchr_name,bln_active) VALUES('500',True);
insert into case_closure_master(vchr_name,bln_active) VALUES('200',True);
insert into case_closure_master(vchr_name,bln_active) VALUES('100',True);
insert into case_closure_master(vchr_name,bln_active) VALUES('50',True);
insert into case_closure_master(vchr_name,bln_active) VALUES('20',True);
insert into case_closure_master(vchr_name,bln_active) VALUES('10',True);
insert into case_closure_master(vchr_name,bln_active) VALUES('5',True);
insert into case_closure_master(vchr_name,bln_active) VALUES('1',True);

  CREATE TABLE case_closure_details(
    pk_bint_id BIGSERIAL PRIMARY KEY,
    dat_created TIMESTAMP,
    dat_updated TIMESTAMP,
    fk_created_id BIGINT REFERENCES userdetails(user_ptr_id),
    fk_updated_id BIGINT REFERENCES userdetails(user_ptr_id),
    dbl_total_amount DOUBLE PRECISION,
    json_case_closure json,
    int_status INTEGER,
    fk_branch_id BIGINT REFERENCES branch(pk_bint_id) NOT NULL,
    vchr_remark VARCHAR(350)
  );



CREATE TABLE guest_user_details(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_user_id BIGINT REFERENCES userdetails(user_ptr_id),
  session_expiry_time TIMESTAMP,
  fk_group_id BIGINT REFERENCES groups(pk_bint_id),
  fk_company_id BIGINT REFERENCES company(pk_bint_id),
  fk_branch_id BIGINT REFERENCES branch(pk_bint_id),
  dat_created TIMESTAMP,
  dat_updated TIMESTAMP,
  fk_created_id BIGINT REFERENCES auth_user(id),
  fk_updated_id BIGINT REFERENCES auth_user(id)
);

ALTER TABLE userdetails ADD COLUMN int_guest_user INT DEFAULT 0;

ALTER TABLE add_combo_master ALTER int_status SET DEFAULT (0) ;
ALTER TABLE company ALTER int_status SET DEFAULT (0) ;
ALTER TABLE item_category ALTER int_status SET DEFAULT (0) ;
ALTER TABLE item ALTER int_status SET DEFAULT (0) ;
ALTER TABLE item_group ALTER int_status SET DEFAULT (0) ;
ALTER TABLE loyalty_card_status ALTER int_status SET DEFAULT (2);
ALTER TABLE products ALTER int_status SET DEFAULT (0);
ALTER TABLE brands ALTER int_status SET DEFAULT (0);
