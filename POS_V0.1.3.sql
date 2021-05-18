alter table payment add column fk_bank_id BIGINT REFERENCES bank(pk_bint_id);

ALTER TABLE customer_details ADD vchr_code VARCHAR(25);
UPDATE customer_details SET vchr_code = 'CST1';




CREATE TABLE sales_customer_details(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_customer_id BIGINT REFERENCES customer_details(pk_bint_id),
  dat_created TIMESTAMP,
  fk_created_id BIGINT REFERENCES userdetails(user_ptr_id),
  vchr_name VARCHAR(100),
  vchr_email VARCHAR(200),
  int_mobile BIGINT,
  fk_state_id BIGINT REFERENCES states(pk_bint_id),
  int_loyalty_points BIGINT,
  int_redeem_point BIGINT,
  dbl_purchase_amount FLOAT,
  vchr_loyalty_card_number VARCHAR(50),
  txt_address TEXT,
  vchr_gst_no VARCHAR(30),
  int_otp_number BIGINT,
  fk_location_id BIGINT REFERENCES location(pk_bint_id),
  fk_loyalty_id BIGINT REFERENCES loyalty_card(pk_bint_id),
  vchr_code VARCHAR(25)
);


-- change foreign key(fk_customer_id)column point from customer_details to sales_customer_details
-- ========================================================================================================================
alter table sales_master add column fk_sales_customer_id BIGINT REFERENCES sales_customer_details(pk_bint_id);
alter table sales_master_jio add column fk_sales_customer_id BIGINT REFERENCES sales_customer_details(pk_bint_id);

                """ Only After script"""
-- alter table sales_master drop column fk_customer_id ;
-- alter table sales_master_jio  drop column fk_customer_id ;
-- alter table sales_master RENAME fk_sales_customer_id to fk_customer_id;
-- alter table sales_master_jio  RENAME fk_sales_customer_id to fk_customer_id;
-- =============================================================================================================================

-

ALTER TABLE item ADD COLUMN dat_updated TIMESTAMP;

create table tools (￼
    pk_bint_id BIGSERIAL PRIMARY KEY,￼
    vchr_tool_name VARCHAR(40),￼
    vchr_tool_code VARCHAR(40),￼
    jsn_data JSONB,￼
    int_status INTEGER￼
);
￼	insert into tools(vchr_tool_name,vchr_tool_code,int_status)  values('DIRECT DISCOUNT','DIRECT_DISCOUNT',1),('INDIRECT DISCOUNT','INDIRECT_DISCOUNT',1);
￼	insert into tools(vchr_tool_name,vchr_tool_code,int_status)  values('DEDUCTIONS','DEDUCTION',1),('ADDITION','ADDITION',1);


CREATE TABLE contra_details(
pk_bint_id BIGSERIAL PRIMARY KEY,
json_denomination JSONB,
fk_payment_id BIGINT REFERENCES payment);


create table finance_scheme(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_schema VARCHAR(30),
  dat_from DATE,
  dat_to DATE);


INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ('10 BY 0', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ('10 BY 1', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ('10 BY 2', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ('10 BY 3', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '11 BY 2', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '11 BY 3', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '12 BY 0', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '12 BY 2', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '12 BY 3', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '12 BY 4', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '13 BY 2', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '13 BY 3', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '15 BY 0', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '15 BY 3', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '15 BY 4', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '15 BY 5', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '16 BY 4', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '18 BY 0', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '18 BY 3', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '18 BY 4', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '18 BY 6', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '19 BY 6', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '20 BY 4', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '20 BY 5', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '20 BY 6', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '24 BY 6', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '24 BY 8', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '25 BY 5', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '3 BY 0', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '4 BY 0', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '4 BY 1', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '5 BY 0', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '6 BY 0', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '6 BY 1', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '6 BY 2', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '7 BY 0', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '7 BY 1', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '8 BY 0', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '8 BY 2', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '8 BY 3', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '9 BY 0', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '9 BY 2', '2019-05-13', NULL);
INSERT INTO finance_scheme (vchr_schema, dat_from, dat_to) VALUES ( '9 BY 3', '2019-05-13', NULL);



ALTER TABLE receipt ADD COLUMN fk_branch_id BIGINT REFERENCES branch(pk_bint_id);

alter table sales_master add column vchr_journal_num VARCHAR(30) null;

alter table Document alter column vchr_short_code type varchar(10);
alter table sales_master add column jsn_addition jsonb;
alter table sales_master add column jsn_deduction jsonb;
insert into supplier(vchr_name,vchr_code) values('DEFAULT','DEFAULT');


ALTER TABLE supplier ALTER column vchr_name TYPE VARCHAR(100);
ALTER TABLE supplier ALTER column vchr_gstin TYPE VARCHAR(100);
ALTER TABLE contact_person_supplier ALTER column vchr_name TYPE VARCHAR(100);
alter table receipt add column vchr_card_num varchar(30);

ALTER TABLE  receipt_invoice_matching ADD COLUMN fk_payment_id BIGINT REFERENCES payment(pk_bint_id);


-- grn_details_batch_no entry
update grn_details gr set vchr_batch_no = BTRIM(jsn_batch_no->>'batch','[""]') from branch_stock_imei_details bsid where gr.pk_bint_id = bsid.fk_grn_details_id;
select BTRIM(jsn_batch_no->>'batch','[""]'),vchr_batch_no  from branch_stock_imei_details bsid join grn_details gr on gr.pk_bint_id = bsid.fk_grn_details_id where BTRIM(jsn_batch_no->>'batch','[""]') !=vchr_batch_no;


alter table payment add column fk_accounts_map_id BIGINT REFERENCES accounts_map(pk_bint_id);


ALTER TABLE tools ADD dat_from TIMESTAMP;
ALTER TABLE tools ADD dat_to TIMESTAMP;
ALTER  TABLE TOOLS ADD jsn_keys JSONB;
alter table  customer_details add column int_edit_count INTEGER ;
alter table  customer_details add column vchr_otp VARCHAR (10) ;
alter table  customer_details add column dat_exp TIMESTAMP ;
-- alter table customer_details rename column exp_date to dat_exp;


alter table stock_request add column int_automate INTEGER;
create table purchase_request(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_supplier_id  BIGINT REFERENCES supplier(pk_bint_id),
  fk_branch_id BIGINT REFERENCES branch(pk_bint_id),
  dat_request TIMESTAMP,
  dat_expired TIMESTAMP;
  int_status INTEGER,
  fk_created_id BIGINT REFERENCES userdetails(user_ptr_id),
  dat_created TIMESTAMP
);
create table purchase_request_details(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_request_id BIGINT REFERENCES purchase_request(pk_bint_id),
  fk_item_id  BIGINT REFERENCES item(pk_bint_id),
  int_qty INTEGER
);
CREATE TABLE financiers(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_name varchar(50) NOT NULL,
  bln_active BOOLEAN NOT NULL
);


alter table financiers add column vchr_code VARCHAR(10);


CREATE TABLE sap_payment(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_code VARCHAR(50),
  vchr_description VARCHAR(150),
  dbl_amount DOUBLE PRECISION,
  int_tran_id INTEGER,
  int_type INTEGER,
  doc_date TIMESTAMP
);
-- alter table receipt  drop column vchr_bank;
alter table receipt add column fk_bank_id BIGINT REFERENCES bank(pk_bint_id);


CREATE TABLE non_saleable(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_item_id BIGINT REFERENCES item(pk_bint_id),
  fk_branch_id BIGINT REFERENCES branch(pk_bint_id),
  dat_created TIMESTAMP,
  dat_updated TIMESTAMP,
  fk_created_id BIGINT REFERENCES userdetails(user_ptr_id),
  fk_updated_id BIGINT REFERENCES userdetails(user_ptr_id),
  int_status INTEGER,
  jsn_non_saleable JSONB,
  jsn_status_change JSONB
);

ALTER TABLE sales_return ADD vchr_doc_code VARCHAR(50);
ALTER TABLE document ADD fk_branch_id BIGINT REFERENCES branch;

CREATE TABLE exchange_stock(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  JSN_IMEI JSONB,
  jsn_avail JSONB,
  fk_branch_id BIGINT REFERENCES BRANCH,
  fk_item_id BIGINT REFERENCES ITEM,
  fk_sales_details_id BIGINT REFERENCES sales_details,
  int_avail INTEGER,
  dbl_unit_price DOUBLE PRECISION,
  int_status INTEGER DEFAULT 0,
  dat_exchanged TIMESTAMP
);
alter table customer_details add column int_cust_type INTEGER DEFAULT 0;
alter table sales_customer_details add column int_cust_type INTEGER DEFAULT 0;

insert into tools(vchr_tool_name,vchr_tool_code,int_status)  values('ALLOW SERVICER PRINT ','ALLOW_SERVICER_PRINT',1);

alter table products add column int_type INTEGER default 0;
alter table products add column vchr_code VARCHAR(10);
ALTER TABLE branch ADD COLUMN vchr_gstno VARCHAR(50);

ALTER TABLE branch_stock_master add column vchr_sap_doc_num  VARCHAR(10);
ALTER TABLE branch_stock_master add column dat_sap_doc_date  TIMESTAMP;
alter table branch_stock_details add column int_received INTEGER;
alter table branch_stock_imei_details add column int_received INTEGER;
Alter table branch_stock_imei_details add column jsn_imei_reached JSONB;
Alter table branch_stock_imei_details add column jsn_batch_reached JSONB;


alter table customer_details add column dbl_credit_balance DOUBLE PRECISION default 0;
alter table customer_details add column dbl_credit_limit DOUBLE PRECISION default 0;

CREATE TABLE gdp_range (
 pk_bint_id BIGSERIAL PRIMARY KEY,
 dbl_from DOUBLE PRECISION,
 dbl_to DOUBLE PRECISION,
 dbl_amt DOUBLE PRECISION,
 int_type INTEGER NOT NULL
);

INSERT INTO gdp_range (dbl_from,dbl_to,dbl_amt,int_type) VALUES (1,4000,390,1),(4001,10000,890,1);
INSERT INTO gdp_range (dbl_from,dbl_to,dbl_amt,int_type) VALUES (10001,15000,1390,1),(15001,20000,1790,1),(20001,25000,1990,1),
(25001,30000,2490,1),(30001,40000,3290,1),(40001,50000,3990,1),(50001,60000,4690,1),(60001,70000,5390,1);
INSERT INTO gdp_range (dbl_from,dbl_to,dbl_amt,int_type) VALUES (70001,80000,5990,1),(80001,90000,6490,1),(90001,100000,6890,1),
(100001,110000,7890,1),(110001,120000,9990,1),(120001,130000,10990,1),(130001,140000,11990,1),(140001,150000,12990,1),(150001,160000,13990,1);

INSERT INTO gdp_range (dbl_from,dbl_to,dbl_amt,int_type) VALUES (1,2000,199,2),(2001,4000,299,2),(4001,10000,599,2),(10001,15000,899,2),(15001,20000,1199,2),(20001,25000,1499,2),
(25001,30000,1499,2),(30001,40000,1899,2),(40001,50000,2499,2),(50001,60000,2599,2),(60001,70000,2999,2),(70001,80000,2999,2),(80001,90000,2999,2),(90001,100000,3999,2),(100001,110000,3999,2);

CREATE TABLE finance_details(
pk_bint_id BIGSERIAL PRIMARY KEY,
fk_payment_id  BIGINT REFERENCES payment_details (pk_bint_id),
dbl_finance_amt  DOUBLE PRECISION,
dbl_receved_amt DOUBLE PRECISION,
dbl_processing_fee DOUBLE PRECISION,
dbl_margin_fee DOUBLE PRECISION,
dbl_service_amt DOUBLE PRECISION,
dbl_dbd_amt DOUBLE PRECISION
);
ALTER TABLE case_closure_details ADD amount_status INTEGER;


insert into type(vchr_name) values('invoice-A'),('invoice-B'),('invoice-C'),('gdp'),('gdew');

insert into terms(fk_type_id,int_status,jsn_terms) values((select pk_bint_id from type where upper(vchr_name)='INVOICE-A'),0,'{"1":"സുതാര്യത , വിശ്വസ്തത ,സത്യസന്ധത  MYG യുടെ മുഖമുദ്ര ....!","2":"വാറന്റി സംബന്ധമായ ചില മുന്നറിയിപ്പുകൾ:","3":"DOA *യുടെ പരിധിയിൽ വരാത്തതായ അല്ലെങ്കിൽ സർവീസ് സെന്ററിന്റെ അംഗീകാരത്തോടെ മാത്രം","4":"DOA *ലഭിക്കാവുന്ന തകരാറുകൾ താഴെ ചേർത്തിരിക്കുന്നു","5":"(A1)സോഫ്റ്റ്‌വെയർ സംബന്ധമായ പ്രേശ്നങ്ങൾ  ഉദാ : ഓട്ടോമാറ്റിക്കായി സ്വിച്ച് ഓഫ് ആയിപ്പോവുക ,റീസ്റ്റാർട് ആവുക ,ബാറ്ററി ബാക്ക് അപ്പ് ഇല്ലാത്തതായ  പ്രശ്നങ്ങൾ,ഹീറ്റിംഗ്  അനുഭവപ്പെടുക (തുടർച്ചയായ ഉപയോഗവും ചാർജിങ്ങും ആപ്പ്ളിക്കേഷനുകളുടെ അനാരോഗ്യകരമായ ഉപയോഗ രീതി മുതലായ കാരണങ്ങൾ കൊണ്ട് നേരിയ തോതിൽ ഹീറ്റിംഗ് അനുഭവപ്പെടൽ സ്വാഭാവികമാണ് )","6":"(A2)പ്രത്യക്ഷത്തിൽ കാണാത്തതായ നെറ്റ്‌വർക്ക് പ്രശ്നങ്ങൾ ഉദാ :ഉപഭോക്താവ് ഉപയോഗിക്കുന്ന സ്ഥലങ്ങളിൽ നേടി ലഭിക്കുന്നില്ല എന്ന് പറയപ്പെടുക ,പക്ഷെ ഷോറൂമിൽ ഉള്ള സമയത്ത് നെറ്റ്‌വർക്ക് ലഭിക്കുക ,ഇത്തരത്തിലുള്ള തകരാറുകൾ ശ്രെദ്ധയിൽ പെട്ടാൽ അംഗീകൃത സർവീസ് സെന്ററിനെ സമീപിച്ചു doa *സെര്ടിഫിക്കറ് ലഭിച്ചതിനു ശേഷം മാത്രം ഷോറൂമിനെ സമീപിക്കുക .ഈ രീതിയിൽ ലഭ്യമാക്കുന്നതിനുള്ള എല്ലാ വിധ സഹായ സഹകരണങ്ങളും ഞങ്ങളിലൂടെ ലഭ്യവുമാണ്.","7":"(A3) DOA *കാലാവധിക്ക് ശേഷം വരുന്ന തകരുകൾക്ക് കമ്പനികൾ സർവീസ് വാറൻറ്റി മാത്രമേ നൽകപ്പെടുകയുള്ളൂ .ഉപഭോഗക്താക്കൾ സഹകരിക്കണമെന്ന് അഭ്യർത്ഥിക്കുന്നു."}');
insert into terms(fk_type_id,int_status,jsn_terms) values((select pk_bint_id from type where upper(vchr_name)='INVOICE-B'),0,'{"1":"ഷോറുമിൽ നിന്ന് നേരിട്ട് വാങ്ങിക്കാവുന്ന DOA /  WARENTTY POLICY","2":"(B1)നിങ്ങൾ വാങ്ങിയ പ്രൊഡക്ടിന്റെ DOA *കാലാവധി അഥവാ പ്രോഡക്റ്റ് നു ഏതെങ്കിലും തകരാർ ശ്രെദ്ധയിൽ പെട്ടാൽ ഷോറൂമിൽ നിന്നും തന്നെ മാറ്റിവാങ്ങാവുന്ന പരമാവധി കാലാവധി പർച്ചെയ്‌സ് ചെയ്‌ത്‌ (അക്ഷരത്തിൽ ).....................................................................  ദിവസത്തിനുള്ളിൽ മാത്രമായിരിക്കും (പോയിന്റ് NO : A 1 &A 2  എന്നീ തകരാറുകൾക്കു ലഭിക്കുന്നതല്ല കൂടാതെ അംഗീകൃത സർവീസ് സെന്ററിന്റെ അംഗീകാരത്തിനായി പരമാവധി 3 പ്രവൃത്തി ദിവസം കാത്തിരിക്കേണ്ടതാണ് )","3":"(B2)മറ്റുള്ള  ഇലക്ട്രോണിക് ഉപകരണങ്ങളിൽ നിന്നും വ്യത്യസ്തമായി ഞങ്ങൾ വിൽക്കപ്പെടുന്ന ഉത്പന്നം സിം ആക്ടിവേഷനെ അടിസ്ഥാനമാക്കി കമ്പനികൾ നിരീക്ഷിക്കുമെന്നതിനാൽ DOA * കാലാവധിയിൽ ഒരു ദിവസത്തെ പോലും ഇളവ് നൽകുന്നതിൽ ഞങ്ങൾ നിസ്സഹായരാണ് ."}');
insert into terms(fk_type_id,int_status,jsn_terms) values((select pk_bint_id from type where upper(vchr_name)='INVOICE-C'),0,'{"1":"IMPORTANT NOTICE","2":"(C1) ഞങ്ങളുടേത് അംഗീകൃത സെയിൽസ് ഷോറൂം മാത്രമാണ് .വില്പനാനന്തരം  ആവിശ്യം ആയ എല്ലാ സർവീസ് പ്രശ്നങ്ങൾക്കും കമ്പനി സർവീസ് സെന്ററുമായി ബന്ധപ്പെടേണ്ടതാണ് .ഇതിനാവശ്യമായ എല്ലാ വിധ സഹകരണങ്ങളും ഞങ്ങളിലൂടെ ലഭ്യമാണ് .","3":"(C2) നിങ്ങൾ വാങ്ങിയ പ്രോഡക്റ്റ് ഉപയോഗിച്ച് തുടങ്ങിയാൽ യാതൊരു കാരണവശാലും (പ്രൊഡക്ടിന്റെ സവിശേഷത കാരണം ) അംഗീകൃത സർവീസ് സെന്ററിന്റെ അംഗീകാരത്തോടെയല്ലാതെ തിരിച്ചെടുക്കുന്നതിൽ നിന്നും എക്സ്ചേഞ്ച് ചെയ്യുന്നതിൽ നിന്നും ഞങ്ങൾ നിസ്സഹായരാണ് .ഇപ്രകാരം തിരിച്ചെടുക്കേണ്ടി  വന്നേക്കാവുന്ന പ്രോഡക്റ്റ് അതിൻറെ തേയ്മാനം കഴിച്ചു ആ സമയത്തുള്ള കമ്പനി വിലയ് ക്ക്  മാത്രമേ എടുക്കാൻ സാധിക്കുകയുള്ളു .ദയവു ചെയ്‌ത്‌ ഉപഭോക്താക്കൾ സഹകരിക്കണമെന്ന് അഭ്യർത്ഥിക്കുന്നു","4":"(C3) തുടർന്നുള്ള ആവിശ്യങ്ങൾക്കായി നിങ്ങളുടെ ഇൻവോയ്‌സും (നിർബന്ധമായും )വാറൻറ്റി കാർഡും (നല്കിയിട്ടുണ്ടെങ്കിൽ )സൂക്ഷിക്കുക .","5":"(C4) വാട്ടർ എൻട്രി ,ഫിസിക്കൽ ഡാമേജ് തുടങ്ങിയ കാരണങ്ങളാൽ പ്രോഡക്റ്റ് കേടുവന്നാൽ വാറൻറ്റി ലഭിക്കുന്നതല്ല .വിയർപ്പ് ,ഈർപ്പം  മുതലായവ  വാട്ടർ എൻട്രി ആയി കണക്കാക്കുന്നതാണ് .ഇതിനാൽ നിങ്ങളുടെ പ്രൊഡക്ടുകൾ വാട്ടർ എൻട്രിയിൽ  നിന്ന് സംരക്ഷിക്കുക .","6":"(C5) നിങ്ങൾ വാങ്ങിയ പ്രോഡക്റ്റിന്റെ  കാലിയായ ബോക്സും  വാങ്ങുമ്പോൾ  ലഭിച്ചതായ  മറ്റനുബന്ധ സാധന സാമഗ്രികളും (ഉദാ : ബോക്സിനുള്ളിലെ  പ്രോഡക്റ്റ് വയ്ക്കാനുള്ള  ട്രേ  ആണെങ്കിൽ പോലും ) വൃത്തിയായി  ശ്രെദ്ധയോടെ (വരയ്ക്കൽ ,പേരെഴുതൽ എന്നിവ പോലും  പാടുള്ളതല്ല )വാറൻറ്റി കാലാവധി കഴിയുന്നത് വരെ സൂക്ഷിച്ച്  വയ്ക്കേണ്ടതാണ് .അല്ലാത്ത പക്ഷം  ചിലപ്പോൾ നിങ്ങൾ വാങ്ങിയ പ്രൊഡക്ടിന്റെ ചില സവിശേഷമായ  വാറന്റികൾ നക്ഷ്ടമായേക്കാം .","7":"(C6) പല പ്രൊഡക്ടുകൾക്കും അതിൻറെ കൂടെ ലഭ്യമാകുന്ന അനുബന്ധ ആക്‌സസറീസ്സുകൾക്കും പല കമ്പനികളും വ്യത്യസ്തമായ വാറൻറ്റി പോളിസികളാണ് നൽകുന്നത് .അതുകൊണ്ട് തന്നെ വാങ്ങുന്ന പ്രൊഡക്ടുകളുടെ വാറൻറ്റി പോളിസി തീർച്ചയായും വ്യക്തതയോടെ ചോദിച്ചു മനസ്സിലാക്കേണ്ടതാണ്","8":"(C7) എല്ലാ നിയമപരമായ പരാതികളും തർക്കങ്ങളും കോഴിക്കോട് കോടതിയുടെ അധികാര പരിധിയിൽ ആയിരിക്കുന്നതാണ്","9":"(C8) ഇന്ത്യൻ ഗവർമെന്റിന്റെ 2017 ലെ പുതിയ ഫിനാൻസ് ആക്ട് പ്രകാരം (സെക്‌ഷൻ നമ്പർ 269 ST  )ഒരു ഉപഭോക്താവ് ഒരു ദിവസം 2 ലക്ഷത്തിനു മുകളിൽ  പർച്ചെയ്‌സ് ചെയ്യുന്നുണ്ടെങ്കിൽ RTGS/NEFT/REALISED CHEQUE OR DD തുടങ്ങിയ മാർഗ്ഗങ്ങളിലൂടെ സ്ഥാപനത്തിൻറെ  അക്കൗണ്ടിലേക്ക് ഉപഭോക്താവിൻറെ അക്കൗണ്ടിൽ നിന്നും നേരിട്ട് പണം നിക്ഷേപിക്കുന്ന രീതി അവലംബിക്കേണ്ടതാണ് "}');
insert into terms(fk_type_id,int_status,jsn_terms) values((select pk_bint_id from type where upper(vchr_name)='GDEW'),0,'{"1":"GDOT EXTENDED  WARRANTY (GDEW) എന്നത് ഉപഭോക്താക്കളുടെ താല്പര്യം മുൻനിർത്തി കൃത്യമായ നിബന്ധനകൾക്ക് വിധേയമായി കമ്പനികൾ സാധാരണയായി നൽകുന്ന ആദ്യ ഒരു വർഷ വാറന്റിക് ശേഷം അടുത്ത ഒരു വർഷത്തേക്ക് കൂടി (365 ദിവസം )നൽകപ്പെടുന്ന ഒരു വാറന്റി പോളിസി ആണ്. ഇതിൽ കവർ ചെയ്യപ്പെടുന്ന വാറന്റി എന്നത് ആദ്യ വർഷത്തിൽ പ്രൊഡക്ടിന്റെ മാതൃ കമ്പനി സാധാരണയായി കവർ ചെയ്യപ്പെടുന്നതിന് മാത്രമായിരിക്കും (ചില കമ്പനികൾ ഫിസിക്കൽ/ ലിക്വിഡ് ഡാമേജ് & മോഷണം എന്നിവയ്ക്കു വാറൻറ്റി നൽകാറുണ്ട് ,അത് പക്ഷെ GDEWയിൽ ലഭിക്കുന്നതല്ല ) GDEW എന്തെല്ലാം കവർ ചെയ്യും എന്ന് മനസ്സിലാക്കാൻ ANNEXURE 1 നോക്കേണ്ടതാണ് .","2":"പതിനെട്ടു (18) വയസ്സ് പൂർത്തിയായ ഇന്ത്യൻ പൗരന് മാത്രമെ GDEW ൻറെ സേവനം ലഭിക്കുകയുള്ളു. പ്രോഡക്റ്റ് വാങ്ങി 90 ദിവസത്തിനുള്ളിൽ ഷോറൂമിൽ വച്ചുതന്നെ GDEW രജിസ്റ്റർ ചെയ്യേണ്ടതാണ്.MYG/3G DIGITAL WORLD ൽ നിന്നു വാങ്ങിയ പ്രൊഡക്ടിനു മാത്രമേ GDEW ൻറെ സംരക്ഷണം ലഭിക്കുകയുള്ളു. ആയതിനാൽ ഭാവിയിൽ വരുന്ന സേവനങ്ങൾക്ക് പ്രൊഡക്ടിന്റെ ബിൽ നിർബന്ധമായും കൊണ്ടുവരേണ്ടതാണ് .","3":"GDEW ക്ക് വേണ്ടി കൃത്യവും പൂർണവുമായ വിവരങ്ങൾ നൽകേണ്ടതാണ്. ഗവ.അംഗീകൃത തിരിച്ചറിയൽ രേഖയിലുള്ള മുഴുവൻ പേര്, മേൽവിലാസം,ജനനത്തീയതി തന്നെയാണ് GDEW സെർട്ടിഫിക്കറ്റിൽ രേഖപ്പെടുത്തിയിരിക്കുന്നത് എന്ന് ഷോറൂമിൽ വെച്ചു തന്നെ ഉപഭോക്താവ് ഉറപ്പുവരുത്തേണ്ടതാണ്.  വാറന്റി ക്ലെയിം രജിസ്റ്റർ ചെയ്യുമ്പോൾ നൽകുന്ന വിവരങ്ങളും ആദ്യം നൽകിയ മേല്പറഞ്ഞ വിവരങ്ങളും തമ്മിൽ വ്യത്യാസം വന്നാൽ ക്ലെയിം അംഗീകരിക്കുന്നതിൽ ഞങ്ങൾ നിസ്സഹായരാണ്. തെറ്റായ വിവരങ്ങൾ നൽകുന്നതിലൂടെ നഷ്ടപ്പെട്ടേക്കാവുന്ന ക്ലെയിമുകളുടെ പൂർണ ഉത്തരവാദിത്വം ഉപഭോക്താവിൽ നിക്ഷിപ്തമാണ്. അതുകൊണ്ടുതന്നെ വളരെ കൃത്യതപാലിക്കണമെന്ന് അപേക്ഷിക്കുന്നു.","4":"പ്രൊഡക്ടിന്റെ ബോക്സിന്റെ കൂടെ ലഭിക്കുന്ന ഒരു ആക്‌സെസ്സറിസിനും (ഉദാ:- ബാറ്ററി, ഹെഡ്‍ഫോൺ, അഡാപ്‌റ്റർ, ഡാറ്റ കേബിൾ തുടങ്ങിയവ )GDEW വാറന്റി ലഭിക്കുന്നതല്ല","5":"GDEW സർട്ടിഫിക്കറ്റും വാറന്റി ആവശ്യമായ പ്രൊഡക്ടിന്റെ ബില്ലും ഒരാളുടെ പേരിൽ തന്നെ ആയിരിക്കണ്ടതാണ്. കൂടാതെ ആരുടെ പേരിലാണോ GDEW രജിസ്റ്റർ ചെയ്തിരിക്കുന്നത് ആ വ്യക്തിക്ക് മാത്രമേ വാറന്റി ക്ലെയിം ചെയ്യാൻ അധികാരമുണ്ടായിരിക്കുകയുള്ളു. ആ വ്യക്തി തന്നെ ക്ലെയിമിന് വേണ്ടി MYG/3G DIGITAL WORLDഷോറൂമിൽ വരേണ്ടതാണ്. നിർഭാഗ്യവശാൽ നിർദിഷ്ട വ്യക്തിക്ക് വല്ല അസൗകര്യവും ഉണ്ടെങ്കിൽ യഥാർത്ഥ ഉപഭോക്താവിന്റെ തിരിച്ചറിയൽ രേഖയും അധികാരപ്പെടുത്തിയതായ സമ്മതപത്രവും കൂടാതെ ക്ലെയിം റജിസ്റ്റർ ചെയ്യാൻ വരുന്ന വ്യക്തിയുടെ തിരിച്ചറിയൽ രേഖയും ആയി മറ്റൊരാൾക്കു ഷോറൂമിൽ ബന്ധപ്പെടാവുന്നതാണ്.","6":"GDEW യെ അന്വേഷണങ്ങൾ, പരാതികൾ, ക്ലെയിം എന്നിവയുമായി ബന്ധപ്പെട്ട കാര്യങ്ങൾക്ക് അവധി ദിവസങ്ങൾ (ഞായറാഴ്ച, ഗവ.അംഗീകൃത ഒഴിവുകൾ, ഹർത്താൽ) ഒഴികെയുള്ള ദിവസങ്ങളിൽ കസ്റ്റമർ കെയർ നമ്പറായ 9249001001 (പ്രവർത്തിസമയം 9:30 am -5:30 pm ) അല്ലെങ്കിൽ ഷോറൂമുമായി നേരിട്ടോ care@gdot.in എന്ന ഇമെയിൽ അഡ്രസുമായോ ബന്ധപ്പെടാവുന്നതാണ്.","7":"GDEWൻറെ സർവീസിന് വേണ്ടി ഞങ്ങളുടെ തന്നെ സർവീസ് സെന്ററായ MYG CAREനെ മാത്രമേ അംഗീകൃതമായി അധികാരപ്പെടുത്തിയിട്ടുള്ളൂ.. വാറന്റി കാലാവധിക്കുള്ളിൽ അതാത് കമ്പനികളുടെ അംഗീകൃത സർവീസ് സെന്ററിൽ നിന്നല്ലാതെ മറ്റു സർവീസ് സെന്ററിൽ നിന്ന് സർവീസ് ചെയ്ത പ്രൊഡക്ടിനു GDEWന്റെ വാറന്റി ലഭിക്കുന്നതല്ല. കൂടാതെ പൂർത്തീകരണത്തിനായി ഏതെങ്കിലും സ്‌പെയർ പാർട്സ് മാറ്റേണ്ടി വന്നാൽ MYG Care അംഗീകരിച്ച നിലവാരത്തിലുള്ളവ ആയിരിക്കും ഉപയോഗിക്കുക. പൂർണ നാശം സംഭവിച്ചതോ സ്പെയർ പാർട്സ് ലഭ്യമല്ലാത്തതോ ആയ അവസ്ഥയിൽ ഉപഭോകതാവ് അതുവരെ ഉപയോഗിച്ചതിന് അനുസൃതമായ pre-owned ആയ മോഡലോ അ","8":"GDEW ചെയ്ത ഒരു പ്രൊഡക്ട് പിന്നീട് റീപ്ലേസ് ചെയ്യുകയാണെങ്കിൽ അംഗീകൃത സർവീസ് സെന്ററിൽ നിന്നുള്ള സാക്ഷ്യപത്രവുമായി വന്നു MYG/3G DIGITAL WORLD ഷോറൂമിൽ നിന്നും GDEW  പുതിയ പ്രൊഡക്ടിലേക്ക്  നിർബന്ധമായും മാറ്റി രജിസ്റ്റർ ചെയ്യേണ്ടതാണ്. അല്ലാത്ത പക്ഷം മാറ്റി നൽകപ്പെട്ട പ്രൊഡക്ടിന് GDOT EXTENDED  WARRANTY നൽകുന്നതിൽ ഞങ്ങൾ നിസ്സഹായരാണ്.","9":"പ്രൊഡക്ടിന്റെ മാനുഫാക്റ്റർ വാറന്റി കാലയളവിൽ ഉപഭോക്താവിന് അതാത് കമ്പനിയുടെ അംഗീകൃത സർവീസ് സെന്ററിൽ നിന്ന് തന്നെ ക്ലെയിം ചെയ്യാവുന്നതാണ്. പ്രോഡക്റ്റ് വാങ്ങിയ ദിവസത്തിന് ശേഷം 366ആം ദിവസം  മുതൽ 730ആം ദിവസം വരെയാണ് GDEW കാലാവധി ഉണ്ടായിരിക്കുന്നത്. ഈ കാലയളവിൽ ഉപഭോക്താവിന്  MYG/3G DIGITAL WORLD ന്റെ ഏതു ഷോറൂമുമായി ബന്ധപെട്ടു വാറന്റി ക്ലെയിം ചെയ്യാവുന്നതാണ്.","10":"വാറന്റി ക്ലെയിം ചെയ്യാനായി നിർബന്ധമായും GDEW രേഖപ്പെടുത്തിയ ഒറിജിനൽ ഇൻവോയ്‌സും, GDEW സർട്ടിഫിക്കറ്റും, ഉപഭോക്താവിന്റെ ഗവ.അംഗീകൃത തിരിച്ചറിയൽ രേഖയും കൊണ്ടുവരേണ്ടതാണ്. കൂടാതെ ഒന്നാമത്തെ ക്ലെയിമിന് ANNEXURE 2 ൽ  വിവരിക്കുന്നത് പോലെ GDEW ന്റെ പാക്കേജിന് ബാക്കിയുള്ള നിശ്‌ചിത തുകയും ഷോറൂമിൽ അടക്കേണ്ടതാണ്.","11":"ഫിസിക്കൽ/ലിക്വിഡ് ഡാമേജ് ആയ പ്രൊഡക്ടിനു GDEW വാറന്റി ക്ലെയിം രജിസ്റ്റർ ചെയ്യാൻ സാധിക്കുന്നതല്ല. വാറന്റി ക്ലെയിം രജിസ്റ്റർ ചെയ്ത പ്രൊഡക്ടിനു ഫിസിക്കൽ/ലിക്വിഡ് ഡാമേജ് കാണാനിടയായാൽ  വാറന്റി നഷ്ടപ്പെടുന്നതായിക്കും.","12":"GDEW ക്ലെയിം ചെയ്യാൻ വേണ്ടി കസ്റ്റമർ ഷോറൂമിൽ കൊടുക്കുന്ന പ്രൊഡക്ടിന്റെ ഡാറ്റ നഷ്ടപെടുന്നതിനു GDEW മാനേജ്‍മെന്റിൽ ഉത്തരവാദിത്വം ഉണ്ടായിരിക്കുന്നതല്ല. ആപ്‌ളിക്കേഷൻ, സോഫ്റ്റ്‌വെയർ, ഡാറ്റ എന്നിവയുടെ വീണ്ടെടുക്കൽ, പുനഃസ്ഥാപനം എന്നിവ GDEW വിൽ ഉൾപ്പെടുത്തിയിട്ടില്ല.","13":"എല്ലാ നിയമപരമായ പരാതികളും തർക്കങ്ങളും കോഴിക്കോട് അധികാര പരിധിയിൽ ആയിരിക്കുന്നതാണ്."}');
insert into terms(fk_type_id,int_status,jsn_terms) values((select pk_bint_id from type where upper(vchr_name)='GDP'),0,'{"1":"GDOT PROTECTION PLUS (GDP PLUS) എന്നത് 3G DIGITALWORLD/myG , ഉപഭോക്താവിന്റെ താല്പര്യം മുന്‍നിര്‍ത്തി കൃത്യമായ നിബന്ധനകള്‍ക്ക് വിധേയമായി ഒരു വര്‍ഷ കാലത്തേക്ക് ചെയ്യുന്ന ഒരു ബിസ്സിനെസ്സ് പോളിസിയാണ് .","2":"GDP PLUS-ന് വേണ്ടി കൃത്യവും പൂര്‍ണ്ണവുമായ വിവരങ്ങള്‍ നല്‍കേണ്ടതാണ്.ഗവ.അംഗീകൃത തിരിച്ചറിയല്‍ രേഖയിലുള്ള മുഴുവന്‍ പേര് , മേല്‍വിലാസം, ജനനതീയതി തന്നെയാണ് GDP PLUS സെര്‍ട്ടിഫിക്കറ്റില്‍ രേഖപ്പെടുത്തിയിരിക്കുന്നത് എന്ന് ഷോറൂമില്‍ വച്ചു തന്നെ ഉപഭോക്താവ് ഉറപ്പുവരുത്തേണ്ടതാണ്.ക്ലെയിം രജിസ്റ്റര്‍ ചെയ്യുമ്പോള്‍ ആദ്യം നല്‍കിയ മേല്പറഞ്ഞ വിവരങ്ങളും , ക്ലെയിം ഫോമിനൊപ്പം നല്‍കുന്ന രേഖകളിലെ വിവരങ്ങളും തമ്മില്‍ വ്യതാസം വന്നാല്‍ ക്ലെയിം അംഗീകരിക്കുന്നതില്‍ ഞങ്ങള്‍ നിസ്സഹായരാണ്. തെറ്റായ വിവരങ്ങള്‍ നല്‍കുന്നതിലൂടെ നഷ്ടപ്പെട്ടേക്കാവുന്ന ക്ലെയിമുകളുടെ പൂര്‍ണ്ണ ഉത്തരവാദിത്വം ഉപഭോക്താവില്‍ നിക്ഷിപ്തമാണ്.അതുകൊണ്ടു തന്നെ വളരെ കൃത്യത പാലിക്കണമെന്ന് അപേക്ഷിക്കുന്നു.","3":"പതിനെട്ടു (18) വയസ്സ് പൂര്‍ത്തിയായ ഇന്ത്യന്‍ പൗരന് മാത്രമേ GDP PLUS-ന്റെ സേവനം ലഭിക്കുകയുള്ളൂ.","4":"GDP PLUS സെര്‍ട്ടിഫിക്കറ്റും പ്രൊട്ടക്ഷന്‍ ആവശ്യമായ പ്രൊഡക്ടിന്റെ ഇന്‍വോയ്‌സും(ബില്ലും) ഒരാളുടെ പേരില്‍ തന്നെ ആയിരിക്കേണ്ടതാണ്.കൂടാതെ ആരുടെ പേരിലാണോ GDP PLUS രജിസ്റ്റര്‍ ചെയ്തിരിക്കുന്നത്, ആ വ്യക്തിക്ക് മാത്രമേ ക്ലെയിം ചെയ്യാന്‍ അധികാരമുണ്ടാകുകയുള്ളൂ.ആ വ്യക്തി തന്നെ ക്ലെയിമിനുവേണ്ടി myG/3G DIGITALWORLD ഷോറൂമില്‍ വരേണ്ടതാണ്.പക്ഷെ നിര്‍ഭാഗ്യവശാല്‍ നിര്‍ദിഷ്ട വ്യക്തിക് വല്ല അസൗകര്യവും ഉണ്ടെങ്കില്‍ താഴെപറയുന്ന എല്ലാ രേഖകളുമായി ഉപഭോക്താവ് അധികാരപ്പെടുത്തിയ വ്യക്തിക്ക് ഷോറൂമുമായി ബന്ധപ്പെടാവുന്നതാണ്.ക്ലെയിം രജിസ്റ്റര്‍ ചെയ്യാന്‍ വരുന്ന വ്യക്തി ഉപഭോക്താവ് അധികാരപ്പെടുത്തിയ കത്തും സ്വന്തം തിരിച്ചറിയല്‍ രേഖയും കൊണ്ടുവരേണ്ടതാണ്.","5":"GDP PLUS നെ കുറിച്ചുള്ള അന്വേഷണങ്ങള്‍, പരാതികള്‍,ക്ലെയിം എന്നിവയുമായി ബന്ധപ്പെട്ട കാര്യങ്ങള്‍ക്ക് അവധി ദിവസങ്ങള്‍ (ഞായറാഴ്ച,ഗവ. അംഗീകൃത ഒഴിവുകള്‍,ഹര്‍ത്താല്‍) ഒഴികെയുള്ള ദിവസങ്ങളില്‍ കസ്റ്റമര്‍ കെയര്‍ നമ്പറായ 9249001001 (പ്രവര്‍ത്തിസമയം 9:30 am - 5:30 pm) അല്ലെങ്കില്‍ ഷോറൂമുമായി നേരിട്ടോ, care@gdotprotection.in എന്ന ഇമെയില്‍ അഡ്ഡ്രസുമായോ ബന്ധപ്പെടാവുന്നതാണ്.","6":"ക്ലെയിമിനു വേണ്ടി സംഭവം നടന്ന് 48 മണിക്കൂറിനകം myG/3G DIGITALWORLD ഷോറൂമില്‍ വന്നു ക്ലെയിം രജിസ്റ്റര്‍ ചെയ്തു Jobsheet വാങ്ങേണ്ടതാണ്.","7":"ഡ്രൈവിംഗ് ലൈസന്‍സ്,പാസ്‌പോര്‍ട്ട്(ഇതില്‍ ഏതെങ്കിലും ഒന്ന് നിര്‍ബന്ധമായും), കേട് പറ്റിയ പ്രോഡക്ട് എന്നിവ കൊണ്ടവരേണ്ടതാണ് കൂടാതെ 500 രൂപയോ പ്രോഡക്ട് വാല്യൂവിന്റെ 5%, ഏതാണോ കൂടുതല്‍ ആ തുകയും അടക്കേണ്ടതാണ്. അഥവാ റിപ്പയര്‍ ചെയ്യാന്‍ സാധിക്കാത്ത അവസ്ഥയോ അല്ലെങ്കില്‍ പ്രൊഡക്ടിന്റെ വിലയേക്കാളും റിപ്പയര്‍ ചാര്‍ജ് വരുകയോ ആണെങ്കില്‍ നിര്‍ദിഷ്ട ക്ലെയിം total loss (പൂര്‍ണ്ണനാശം) എന്ന വിഭാഗത്തിലേക് മാറുന്നതാണ്.ഈ അവസ്ഥയില്‍ Annexure 1ല്‍ പറയുന്ന തേയ്മാനം(depreciation) കഴിച്ചുള്ള തുകയുടെ തുല്യമൂല്യമുള്ള പ്രോഡക്ട് കൈ പറ്റാവുന്നതാണ്. കൂടുതല്‍ മൂല്യമുള്ള പ്രോഡക്ട് ആണ് താല്പര്യമെങ്കില്‍ ബാക്കി തുകയടച്ചു വാങ്ങാവുന്നതാണ്. ഒരു കാരണവശാലും തുക ക്യാഷായി തിരിച്ചുനല്കുന്നതില്‍ ഞങ്ങള്‍ നിസ്സഹായരാണ്.ഇത് തീര്‍ത്തും GDP PLUS ല്‍ വന്നേക്കാവുന്ന ദുരുപയോഗം തടയുന്നതിന് വേണ്ടിയാണ്. ഇതില്‍ ഉപഭോക്താവിന്റെ നിസ്സീമമായ സഹകരണം പ്രതീക്ഷിക്കുന്നു.","8":"ആകസ്മികമായോ പ്രകൃതിക്ഷോഭം മൂലമോ ഉണ്ടാകുന്ന ഫിസിക്കല്‍/ലിക്വിഡ് ഡാമേജ് കൂടാതെ പിടിച്ചുപറി,കൊള്ള, ലോക്ക് ചെയ്യപ്പെട്ട റൂമില്‍ നിന്നോ, വാഹനത്തില്‍ നിന്നോ,വീട്ടില്‍ നിന്നോ നടക്കുന്ന മോഷണം എന്നിവയ്ക്കു മാത്രമേ GDP PLUS സംരക്ഷണം നല്കുന്നുള്ളൂ.ആയതിനാല്‍ പ്രോഡക്ട് നഷ്ടപ്പെടുന്ന ക്ലെയിം രജിസ്റ്റര്‍ ചെയ്യാന്‍ point no. 7ല്‍ പറഞ്ഞ രേഖകളോടൊപ്പം തന്നെ പോലീസ് നല്‍കുന്ന രേഖകളായ intimation ലെറ്റര്‍ , non traceable സെര്‍ട്ടിഫിക്കറ്റ്( സീല്‍ പതിപ്പിച്ചത്) കൂടി നിര്‍ബന്ധമായും കൊണ്ടുവരേണ്ടതാണ്. കൂടാതെ 100 രൂപ സ്റ്റാമ്പ് പേപ്പറില്‍ ഭാവിയില്‍ പ്രോഡക്ട് തിരിച്ചുകിട്ടുന്ന പക്ഷം ക്ലെയിം തുക തിരിച്ചു നല്‍കാം എന്നു നോട്ടറി അറ്റസ്റ്റ് ചെയ്ത സാക്ഷ്യപത്രം (subrogation letter) കൂടി കൊണ്ട് വരേണ്ടതാണ്. ഉപഭോക്താവിന്റെ ശ്രദ്ധക്കുറവ് കാരണമുണ്ടാകുന്ന നഷ്ടപെടലിന് ക്ലെയിം ലഭിക്കുന്നതല്ല. (കൂടുതല്‍ വിവരങ്ങള്‍ക് Anexure 2 നോക്കുക) മേല്‍പറഞ്ഞ എല്ലാ രേഖകളും സാധുവാണെങ്കില്‍ നിര്‍ദിഷ്ട ക്ലെയിം total loss(പൂര്‍ണ്ണ നാശം) എന്ന വിഭാഗത്തിലേക്ക് മാറുകയും point no.7 ല്‍ പറയുന്ന ആനുകൂല്യങ്ങള്‍ ലഭിക്കുന്നതുമാണ്.","9":"അംഗീകൃത സര്‍വിസ് സെന്ററില്‍ നിന്നല്ലാതെ മറ്റു സര്‍വിസ് സെന്ററില്‍ നിന്നു സര്‍വിസ് ചെയ്ത പ്രൊഡക്ടിന് GDP PLUS ന്റെ സംരക്ഷണം ലഭിക്കുന്നതല്ല. കൂടാതെ സര്‍വീസിന്റെ പൂര്‍ത്തീകരണത്തിനായി ഏതെങ്കിലും സ്‌പെയര്‍ പാര്‍ട്‌സ് മാറ്റേണ്ടി വന്നാല്‍ myG Care അംഗീകരിച്ച നിലവരത്തിലുള്ളവ ആയിരിക്കും ഉപയോഗിക്കുക.പൂര്‍ണ്ണ നാശം സംഭവിച്ചതോ സ്‌പെയര്‍ പാര്‍ട്‌സ് ലഭ്യമല്ലാത്തതോ ആയ അവസ്ഥയില്‍ ഉപഭോക്താവ് അതുവരെ ഉപയോഗിച്ചതിന് അനുസൃതമായ pre-owned ആയ അതേ മോഡലോ അല്ലെങ്കില്‍ ഉപഭോക്താവിന് താത്പര്യമുണ്ടെങ്കില്‍ തത്തുല്യവിലയുള്ള മറ്റു കമ്പനികളുടെ മോഡലോ ലഭ്യമാക്കുന്നതായിരിക്കും.എന്നാല്‍ തത്തുല്യ വിലയുള്ള pre-owned പ്രോഡക്ട് ലഭ്യമല്ലെങ്കിലോ പ്രസ്തുത മോഡല്‍ ഉപയോഗിക്കാന്‍ ഉപഭോക്താവിന് താത്പര്യമില്ലെങ്കിലോ point no.7ല്‍ പറയുന്ന ആനുകൂല്യങ്ങള്‍ ലഭിക്കുന്നതാണ്.","10":"GDP PLUS ന്റെ കാലവധിക്കുള്ളില്‍ പ്രൊഡക്ടിന്റെ വിലയുടെ തത്തുല്യമായ ക്ലെയിം തുക വരുന്നത് വരെ എത്ര തവണ വേണമെങ്കിലും ക്ലെയിം ചെയ്യാവുന്നതാണ്. എന്നാല്‍ GDP PLUS മുഖേന ഒരുതവണ മാറ്റി കിട്ടിയ പ്രൊഡക്ടിന് പിന്നീട് സംരക്ഷണം ഉണ്ടായിരിക്കുന്നതല്ല.അതിനായി ഉപഭോക്താവ് പുതുതായി GDP PLUS വാങ്ങി രജിസ്റ്റര്‍ ചെയ്യേണ്ടതാണ്.GDP PLUS മുഖേന സര്‍വിസ് ചെയ്ത പ്രോഡക്ട് പിന്നീട് total loss എന്ന വിഭാഗത്തില്‍ വരുകയാണെങ്കില്‍ മുന്‍പ് നടന്ന സര്‍വീസിന്റെ ക്ലെയിം തുക കഴിച്ചു ബാക്കി തുക മാത്രമേ പരിഗണിക്കുകയുള്ളൂ.","11":"GDP PLUS ചെയ്ത ഒരു പ്രോഡക്ട് പിന്നീട് GDP PLUS മുഖേനയല്ലാതെ റീപ്ലേസ് ചെയ്യുകയാണെങ്കില്‍ അംഗീകൃത സര്‍വിസ് സെന്ററില്‍ നിന്നുള്ള സാക്ഷ്യപത്രവുമായി വന്നു myG/3G DIGITALWORLD ഷോറൂമില്‍ നിന്നും GDP PLUS പുതിയ പ്രൊഡക്ടിലേക് നിര്‍ബന്ധമായും മാറ്റി രജിസ്റ്റര്‍ ചെയ്യേണ്ടതാണ്.","12":"GDP PLUS-ന്റെ നിബന്ധനകളില്‍ മുന്‍കൂര്‍ അറിയിപ്പോ നോട്ടീസോ കൂടാതെ മാറ്റങ്ങള്‍ വരുത്തുവാനുള്ള പൂര്‍ണ്ണ അധികാരം GDP PLUS മാനേജ്‌മെന്റില്‍ നിക്ഷിപ്തമാണ്."}');












update menu_category set vchr_listurl= '/invoice/listinvoice',vchr_addurl='' where pk_bint_id=29;
update menu_category set vchr_listurl= '/invoice/saleslist',vchr_addurl='' where pk_bint_id=28;
update menu_category set vchr_listurl= '/invoice/offerlist',vchr_addurl='' where pk_bint_id=44;
update menu_category set vchr_listurl= '/invoice/bajaj_list',vchr_addurl='' where pk_bint_id=45;
update menu_category set vchr_listurl= '/invoice/salesreturnlist',vchr_addurl='' where pk_bint_id=50;
update menu_category set vchr_listurl= '/invoice/exchangelist',vchr_addurl='' where pk_bint_id=51;
update menu_category set vchr_listurl= '/invoice/salesreturn',vchr_addurl='' where pk_bint_id=60;
update menu_category set vchr_listurl= '/invoice/servicelist',vchr_addurl='' where pk_bint_id=62;
update menu_category set vchr_listurl= '/group/listgroup',vchr_addurl='' where pk_bint_id=7;
update menu_category set vchr_listurl= '/user/usergroupadd',vchr_addurl='' where pk_bint_id=5;
update menu_category set vchr_listurl= '/customer/editcustomer',vchr_addurl='' where pk_bint_id=47;
update menu_category set vchr_listurl= '/invoice/invoicecustomer',vchr_addurl='' where pk_bint_id=48;
update menu_category set vchr_listurl= '/customer/history',vchr_addurl='' where pk_bint_id=57;
update menu_category set vchr_listurl= '/category/addcategory',vchr_addurl='' where pk_bint_id=13;
update menu_category set vchr_listurl= '/tools/set-tools'  where pk_bint_id=56;
update menu_category set vchr_listurl= '/brand/brandlist'  where pk_bint_id=8;


alter table stock_request add column vchr_rej_remark TEXT;
alter table receipt add column vchr_sap_key VARCHAR(10);
alter table import_files rename COLUMN fk_uploaded_by to fk_uploaded_by_id;
alter table import_files add column int_type INTEGER default 0;


alter table sales_master add column vchr_sap_key VARCHAR(10);
alter table stock_transfer_imei_details add column int_qty INTEGER;


alter table non_saleable add column vchr_remarks TEXT;

ALTER TABLE stock_transfer add column vchr_sap_doc_num  VARCHAR(10);
ALTER TABLE stock_transfer add column dat_sap_doc_date  TIMESTAMP;
alter TABLE receipt add column fk_sales_return_id BIGINT REFERENCES sales_return(pk_bint_id);
alter table sales_master add column dat_sap_doc_date TIMESTAMP;
insert into tools (vchr_tool_name,vchr_tool_code,jsn_data,int_status) values ('MYG CARE NUMBER','MYG_CARE_NUMBER','1800 123 2006',1);

ALTER TABLE receipt ADD int_document_id  DOUBLE PRECISION;

ALTER TABLE partial_invoice ADD COLUMN int_approve INTEGER default 0;

Alter table partial_invoice add column json_updated_data JSONB;

 ALTER TABLE group_permissions ADD COLUMN bln_download BOOLEAN NOT NULL DEFAULT FALSE
CREATE TABLE quotation(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_doc_num VARCHAR(50),
  fk_branch_id  BIGINT REFERENCES branch(pk_bint_id),
  fk_state_id  BIGINT REFERENCES states(pk_bint_id),
  vchr_cust_name VARCHAR(100),
  vchr_email VARCHAR(50),
  bint_mobile BIGINT,
  txt_address TEXT,
  vchr_gst_no VARCHAR(50),
  jsn_data JSONB ,
  fk_location_id  BIGINT REFERENCES location(pk_bint_id),
  dat_created TIMESTAMP,
  fk_created_id BIGINT REFERENCES auth_user,
  int_active INTEGER DEFAULT 0,
  txt_remarks TEXT,
  dat_exp DATE
);
INSERT INTO document(vchr_module_name,vchr_short_code,int_number) VALUES('QUOTATION','QTN',1);
ALTER TABLE branch add column vchr_mygcare_no VARCHAR(50);
-- LG 06-03-2020
ALTER table sales_return ADD COLUMN fk_sales_details_id BIGINT REFERENCES sales_details(pk_bint_id);
