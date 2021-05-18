CREATE TABLE transaction (
  pk_bint_id BIGSERIAL PRIMARY KEY,
  dat_created TIMESTAMP,
  int_accounts_id INTEGER,
  int_account_type INTEGER,
  dbl_debit DOUBLE PRECISION NOT NULL,
  dbl_credit DOUBLE PRECISION NOT NULL,
  int_document_id INTEGER,
  int_document_type INTEGER,
  fk_created_id BIGINT REFERENCES userdetails(user_ptr_id),
  vchr_status VARCHAR(20),
  fk_updated_id BIGINT REFERENCES userdetails(user_ptr_id),
  dat_updated TIMESTAMP,
  fk_financialyear_id BIGINT REFERENCES financial_year(pk_bint_id),
  int_type INTEGER,
  int_lock INTEGER,
  fk_branch_id BIGINT REFERENCES branch(pk_bint_id)
);

CREATE TABLE department(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_code varchar(10) NOT NULL,
  vchr_name varchar(50) NOT NULL,
  fk_company_id BIGINT REFERENCES company(pk_bint_id) NOT NULL
);

INSERT INTO department(vchr_code,vchr_name,fk_company_id) VALUES ('HOD','Head Of Department',1),('DEP001','sales',1),('dep002','service',1),('mtg','marketing',1),('adt','auditing',1),('dpt003','finance',1),('dep007','purchase',1);
INSERT INTO groups(vchr_name,int_status,fk_created_id,fk_company_id) VALUES ('ASST ACCOUNTS MANAGER',0,6673,1),('FINANCE MANAGER',0,6673,1),('SERVICER',0,6673,1),('STRATEGIC BUSINESS ANALYST',0,6673,1),('TERRITORY MANAGER',0,6673,1),('ZONE MANAGER',0,6673,1);
ALTER TABLE userdetails add column fk_department_id BIGINT REFERENCES department(pk_bint_id);

CREATE TABLE financial_year (
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_type VARCHAR(20),
  int_year INTEGER,
  dat_start TIMESTAMP,
  dat_end TIMESTAMP,
  bln_status BOOLEAN
);
INSERT INTO financial_year (vchr_type,int_year,dat_start,dat_end,bln_status) VALUES('Apr-Mar',2020,'2020-04-01','2021-03-31',1);




#terms of receipt
insert into type(vchr_name) values('receipt');

  
insert into terms(fk_type_id,int_status,jsn_terms) values((select pk_bint_id from type where upper(vchr_name)='RECEIPT'),0,'{"1":"Delivery of the pre booked product is subject to manufacturer’s stock availability.","2":"This pre booking cannot be cancelled or refunded as the order has been placed. ","3":"Customer must purchase the pre-booked product on or before ....... and if not purchased, myG won’t be responsible for stock availability. ","4":"If myG is not able to deliver the pre-booked product, refund will be done only through bank transfer within 2 working days after the refund request.","5":"Cheque/RTGS/NEFT/IMPS payment is subject to realization."}');



create table freight (
    pk_bint_id BIGSERIAL PRIMARY KEY,
    vchr_code VARCHAR(10),
    vchr_category VARCHAR(30),
    vchr_tax_code VARCHAR(10),
    int_status INTEGER
);

alter table sales_master add column int_sale_type INTEGER DEFAULT 0;
alter table sales_master add column vchr_reff_no VARCHAR(30);
alter table sales_master add column int_order_no VARCHAR(30);


create table department(pk_bint_id BIGSERIAL PRIMARY KEY,vchr_code VARCHAR(20),vchr_name VARCHAR(40),fk_company_id BIGINT REFERENCES company(pk_bint_id));

alter table userdetails add column fk_department_id BIGINT REFERENCES department(pk_bint_id);

alter table sales_return add column dbl_discount DOUBLE PRECISION;
alter table sales_return add column dbl_buyback DOUBLE PRECISION;
alter table sales_return add column dbl_indirect_discount DOUBLE PRECISION;

alter table sales_master add column dbl_cust_outstanding DOUBLE PRECISION;
alter table receipt add column fk_sales_master_id BIGINT REFERENCES sales_master(pk_bint_id);

alter table item_group alter COLUMN vchr_item_group type VARCHAR(50);
