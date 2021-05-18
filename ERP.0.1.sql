CREATE TABLE salary_structure(
  pk_bint_id  BIGSERIAL PRIMARY KEY,
  vchr_name VARCHAR(50) NOT NULL,
  dbl_bp_da DOUBLE PRECISION,
  dbl_bp_da_per DOUBLE PRECISION,
  dbl_da DOUBLE PRECISION,
  json_rules JSONB,
  bln_active BOOLEAN DEFAULT TRUE
);

alter table userdetails drop column bint_phone;
alter table userdetails drop column vchr_pssrsttkn;
alter table userdetails drop column bint_passrstflg;
alter table userdetails drop column dat_passrsttime;
alter table userdetails drop column fk_group_id;
alter table userdetails drop column fk_company_id;
alter table userdetails drop column fk_branch_id;
alter table userdetails drop column fk_brand_id;
alter table userdetails drop column bint_usercode;
alter table userdetails drop column vchr_profpic;
alter table userdetails drop column dat_resapp;
alter table userdetails drop column int_areaid;
alter table userdetails drop column dat_created;
alter table userdetails drop column dat_updated;
alter table userdetails drop column fk_created_id;
alter table userdetails drop column fk_updated_id;
alter table userdetails drop column json_product;
alter table userdetails drop column int_guest_user;
alter table userdetails drop column fk_department_id;
alter table userdetails drop column fk_department_id;



alter TABLE  userdetails add column
  vchr_employee_code VARCHAR(50), add column
  fk_category_id BIGINT REFERENCES category(pk_bint_id), add column
  bint_phone BIGINT, add column
  vchr_email VARCHAR(50), add column
  dat_dob DATE, add column
  dat_doj TIMESTAMP, add column
  vchr_gender VARCHAR(15), add column
  vchr_desig VARCHAR(50), add column
  vchr_level VARCHAR(50), add column
  vchr_grade VARCHAR(50), add column
  fk_salary_struct_id BIGINT REFERENCES salary_structure(pk_bint_id), add column
  fk_branch_id BIGINT REFERENCES branch(pk_bint_id), add column
  fk_department_id BIGINT REFERENCES department(pk_bint_id), add column
  fk_company_id BIGINT REFERENCES company(pk_bint_id), add column
  fk_group_id BIGINT REFERENCES groups(pk_bint_id), add column
  fk_created_id BIGINT REFERENCES auth_user(id), add column
  fk_updated_id BIGINT REFERENCES auth_user(id), add column
  dat_created TIMESTAMP,  add column
  dat_updated TIMESTAMP, add column
  json_allowance JSONB;


ALTER TABLE userdetails ADD COLUMN vchr_weekoff_day VARCHAR(10);
ALTER TABLE userdetails ADD COLUMN bint_emergency_phno BIGINT;
ALTER TABLE userdetails ADD COLUMN vchr_father_name VARCHAR(30);
ALTER TABLE userdetails ADD COLUMN vchr_salutation VARCHAR(10);
ALTER TABLE userdetails ADD COLUMN fk_religion_id BIGINT REFERENCES religion_caste(pk_bint_id);
ALTER TABLE userdetails ADD COLUMN vchr_marital_status VARCHAR(30);
ALTER TABLE userdetails ADD COLUMN vchr_blood_group VARCHAR(10);
ALTER TABLE userdetails ADD COLUMN vchr_emergency_person VARCHAR(100);
ALTER TABLE userdetails ADD COLUMN vchr_emergency_relation VARCHAR(30);
ALTER TABLE userdetails ADD COLUMN bln_pass_reset BOOLEAN DEFAULT FALSE;
ALTER TABLE userdetails ALTER COLUMN vchr_father_name TYPE VARCHAR(150);
ALTER TABLE userdetails ADD COLUMN vchr_pf_no VARCHAR(100);
ALTER TABLE userdetails ADD COLUMN int_hierarchy_type INTEGER DEFAULT 0;
ALTER TABLE userdetails ADD vchr_password_reset_token text NULL;
ALTER TABLE userdetails ADD dat_password_reset_timer TIMESTAMP NULL;
ALTER TABLE userdetails ADD COLUMN dbl_gross DOUBLE PRECISION;
ALTER TABLE userdetails DROP COLUMN vchr_desig ;
ALTER TABLE userdetails ADD COLUMN fk_desig_id  BIGINT REFERENCES job_position (pk_bint_id);

ALTER TABLE userdetails ADD COLUMN vchr_middle_name VARCHAR(150);
ALTER TABLE userdetails ADD COLUMN int_payment INT;
ALTER TABLE userdetails ADD COLUMN vchr_pan_no VARCHAR(150);
ALTER TABLE userdetails ADD COLUMN vchr_aadhar_no VARCHAR(150);
ALTER TABLE userdetails ADD COLUMN vchr_img VARCHAR(300);
ALTER TABLE userdetails ADD COLUMN vchr_bank_name VARCHAR(300);
ALTER TABLE userdetails ADD COLUMN vchr_acc_no VARCHAR(150);
ALTER TABLE userdetails ADD COLUMN vchr_ifsc VARCHAR(150);
ALTER TABLE userdetails ADD COLUMN fk_brand_id BIGINT REFERENCES brand (pk_bint_id);
ALTER TABLE userdetails ADD COLUMN json_function JSONB;
ALTER TABLE userdetails ADD COLUMN vchr_file_no VARCHAR(150);
ALTER TABLE userdetails ADD COLUMN vchr_physical_loc VARCHAR(200);
ALTER TABLE userdetails DROP COLUMN fk_group_id;
ALTER TABLE userdetails ADD COLUMN vchr_address TEXT;
ALTER TABLE userdetails ADD COLUMN int_weekoff_type INT;
ALTER TABLE userdetails DROP COLUMN vchr_physical_loc;
ALTER TABLE userdetails ADD COLUMN json_physical_loc JSONB;
ALTER TABLE userdetails ADD COLUMN dat_resignation DATE;
ALTER TABLE userdetails ADD COLUMN txt_resignation_reason TEXT;
ALTER TABLE userdetails ALTER COLUMN vchr_address TYPE VARCHAR(100);
ALTER TABLE userdetails ADD COLUMN vchr_po VARCHAR(75);
ALTER TABLE userdetails ADD COLUMN vchr_land_mark VARCHAR(150);
ALTER TABLE userdetails ADD COLUMN vchr_place VARCHAR(100);
ALTER TABLE userdetails ADD COLUMN int_pincode INTEGER;
ALTER TABLE userdetails ADD COLUMN fk_dist_id BIGINT REFERENCES district(pk_bint_id);
ALTER TABLE userdetails ADD COLUMN vchr_esi_no VARCHAR(100);
ALTER TABLE userdetails ADD COLUMN vchr_uan_no VARCHAR(100);
ALTER TABLE userdetails ADD COLUMN vchr_wwf_no VARCHAR(100);
ALTER TABLE userdetails ADD COLUMN int_act_status INTEGER DEFAULT 1;
ALTER TABLE userdetails ADD COLUMN fk_wps_id BIGINT REFERENCES wps(pk_bint_id);
ALTER TABLE userdetails ADD COLUMN vchr_disease VARCHAR(400);


ALTER TABLE userdetails ADD COLUMN bint_phone BIGINT;
ALTER TABLE userdetails ADD COLUMN fk_branch_id BIGINT REFERENCES branch(pk_bint_id);
ALTER TABLE userdetails ADD COLUMN fk_department_id BIGINT REFERENCES department(pk_bint_id);
ALTER TABLE userdetails ADD COLUMN fk_company_id BIGINT REFERENCES company(pk_bint_id);
ALTER TABLE userdetails ADD COLUMN fk_created_id BIGINT REFERENCES auth_user(id);
ALTER TABLE userdetails ADD COLUMN fk_updated_id BIGINT REFERENCES auth_user(id);
ALTER TABLE userdetails ADD COLUMN dat_created DATE;
ALTER TABLE userdetails ADD COLUMN dat_updated DATE;





CREATE TABLE tax_master(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_name VARCHAR(100),
  int_intra_tax INTEGER DEFAULT 0,
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
    vchr_gstin VARCHAR(50),
    vchr_mail VARCHAR(150),
    vchr_phone VARCHAR(25),
    vchr_logo VARCHAR(350),
    vchr_print_logo VARCHAR(350),
    int_status INTEGER DEFAULT 1
);

CREATE TABLE states(
		pk_bint_id BIGSERIAL PRIMARY KEY,
    vchr_name VARCHAR(50),
    vchr_code VARCHAR(100)
);


-- CREATE TABLE branch(
--   pk_bint_id BIGSERIAL PRIMARY KEY,
--   vchr_code VARCHAR(20),
--   vchr_name VARCHAR(50) NOT NULL,
--   vchr_address VARCHAR(100),
--   vchr_email VARCHAR(50),
--   vchr_phone VARCHAR(20),
--   dat_close TIMESTAMP,
--   bint_stock_limit BIGINT,
--   flt_static_ip FLOAT,
--   flt_latitude FLOAT,
--   flt_longitude FLOAT,
--   dat_inauguration DATE,
--   tim_inauguration TIME WITHOUT TIME ZONE,
--   vchr_inaugurated_by VARCHAR(50),
--   int_status INTEGER DEFAULT 1,
--   fk_category_id BIGINT REFERENCES other_category(pk_bint_id),
--   int_type INTEGER,
--   fk_states_id BIGINT REFERENCES states (pk_bint_id),
--   int_price_template INT
-- );
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


CREATE TABLE groups(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_code VARCHAR(50),
  vchr_name VARCHAR(150),
  int_status INTEGER DEFAULT 1,
  fk_created_id BIGINT REFERENCES auth_user(id),
  dat_created TIMESTAMP,
  fk_updated_id BIGINT REFERENCES auth_user(id),
  fk_company_id BIGINT REFERENCES company(pk_bint_id)
);

CREATE TABLE job_position(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_name VARCHAR(150),
  fk_department_id BIGINT REFERENCES department(pk_bint_id),
  int_area_type INTEGER,
  json_area_id JSONB,
  bln_active BOOLEAN
);

ALTER TABLE job_position ADD COLUMN dbl_experience DOUBLE PRECISION;
ALTER TABLE job_position ADD COLUMN json_qualification JSONB;
ALTER TABLE job_position ADD COLUMN vchr_age_limit VARCHAR (50);
ALTER TABLE job_position ADD COLUMN txt_desc TEXT;
ALTER TABLE job_position ADD COLUMN int_notice_period INTEGER;
alter table job_position add column json_desc JSONB;
ALTER TABLE job_position add column fk_company_id BIGINT REFERENCES company(pk_bint_id);
ALTER TABLE job_position ADD COLUMN bln_admin BOOLEAN;
ALTER TABLE job_position ADD COLUMN int_permission INTEGER;
ALTER TABLE job_position ADD COLUMN bln_brand BOOLEAN DEFAULT FALSE;

CREATE TABLE wps (pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_name TEXT, dat_created TIMESTAMP,
  fk_created_id BIGINT REFERENCES auth_user(id),
  fk_updated_id BIGINT REFERENCES auth_user(id),
  bln_active BOOLEAN
);

CREATE TABLE session_handler(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_user_id BIGINT REFERENCES auth_user(id),
  vchr_session_key VARCHAR(500)
);


alter table branch add column fk_hierarchy_data_id bigint REFERENCES hierarchy_data(pk_bint_id);
create table hierarchy(
  pk_bint_id  BIGSERIAL PRIMARY KEY,
  int_level smallint,
  vchr_name varchar(100)
  );

create table hierarchy_data(
  pk_bint_id  BIGSERIAL PRIMARY KEY,
  vchr_name varchar(100),
  vchr_code varchar(5),
  fk_hierarchy_id bigint REFERENCES hierarchy(pk_bint_id),
  fk_hierarchy_data_id bigint REFERENCES hierarchy_data(pk_bint_id)
  );

Alter table department ADD int_status smallint;

alter table department add int_status smallint;
CREATE TABLE country(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_code  VARCHAR(15),
  vchr_name VARCHAR(50)
);




CREATE TABLE religion_caste (
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_name VARCHAR(100),
  bln_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE admin_settings(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_name VARCHAR(50),
  vchr_value VARCHAR ARRAY [50],
  tim_punch_cool TIME,
  fk_company_id BIGINT REFERENCES company(pk_bint_id),
  bln_enabled BOOLEAN DEFAULT true,
  vchr_code VARCHAR(50)
);



CREATE TABLE emp_leave_data(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_employee_id BIGINT REFERENCES auth_user(id),
  dbl_number BIGINT
);
alter table states add fk_country_id bigint REFERENCES country(pk_bint_id);
update states set fk_country_id = 1;
alter table district add vchr_code varchar(10);


ALTER TABLE userdetails ADD COLUMN vchr_weekoff_day VARCHAR(10);
ALTER TABLE userdetails ADD COLUMN fk_religion_id BIGINT REFERENCES religion_caste(pk_bint_id);
ALTER TABLE userdetails ADD COLUMN fk_desig_id  BIGINT REFERENCES job_position (pk_bint_id);
ALTER TABLE userdetails ADD COLUMN fk_brand_id BIGINT REFERENCES brands (pk_bint_id);
ALTER TABLE userdetails ADD COLUMN fk_wps_id BIGINT REFERENCES wps(pk_bint_id);
ALTER TABLE userdetails ADD COLUMN json_documents JSONB;
alter table userdetails add column fk_dist_id bigint REFERENCES district(pk_bint_id);
alter table userdetails ADD COLUMN vchr_emp_remark TEXT;
alter table userdetails ADD COLUMN int_official_num BIGINT;
alter table userdetails ADD COLUMN json_weekoff JSONB;


CREATE TABLE document_hrms(
  	pk_bint_id BIGSERIAL PRIMARY KEY,
  	vchr_module_name VARCHAR(50) NOT NULL,
  	vchr_short_code VARCHAR(5) NOT NULL,
  	int_number INTEGER NOT NULL
);
ALTER TABLE document_hrms ADD COLUMN fk_company_id BIGINT REFERENCES company(pk_bint_id);
ALTER TABLE document_hrms ADD COLUMN chr_num_separate VARCHAR(2);
ALTER TABLE document_hrms ADD COLUMN int_num_length INTEGER DEFAULT 1;

CREATE TABLE emp_references(pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_employee_id BIGINT REFERENCES userdetails(user_ptr_id),
  vchr_name VARCHAR(150),
  vchr_company_name VARCHAR(400),
  vchr_desig VARCHAR(200),
  vchr_phone VARCHAR(200),
  vchr_email VARCHAR(200)
);
ALTER TABLE emp_references ADD COLUMN int_status INTEGER DEFAULT 1;

CREATE TABLE emp_family(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_name VARCHAR(150), vchr_realation VARCHAR(150),
  dat_dob DATE, vchr_occupation VARCHAR(200),
  vchr_alive VARCHAR(50),
  fk_employee_id BIGINT REFERENCES userdetails(user_ptr_id),
  int_status INT
);

CREATE TABLE emp_edu_details(  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_employee_id BIGINT REFERENCES userdetails(user_ptr_id),
  bln_highest_qualif BOOLEAN,
  vchr_course VARCHAR(200),
  vchr_institution VARCHAR(300),
  vchr_university VARCHAR(300),
  int_pass_year INTEGER,
  bln_active BOOLEAN,
  dbl_percentage DOUBLE PRECISION,
  vchr_place VARCHAR (200),
  vchr_qualif VARCHAR(200),
  vchr_specialzation VARCHAR (200)
);

CREATE TABLE emp_exp_details(  pk_bint_id BIGSERIAL PRIMARY KEY,
  	fk_employee_id BIGINT REFERENCES userdetails(user_ptr_id),
  	vchr_employer VARCHAR (300),
  	vchr_designation VARCHAR (200),
  	txt_exp_details TEXT,
  	bln_active BOOLEAN
  );


CREATE TABLE shift_schedule(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_name  VARCHAR(50),
  vchr_code  VARCHAR(25),
  bln_night BOOLEAN,
  time_shift_from TIME,
  time_shift_to TIME,
  time_break_from TIME,
  time_break_to TIME,
  time_break_hrs TIME,
  time_shed_hrs TIME,
  time_full_day TIME,
  time_half_day TIME,
  bln_allowance BOOLEAN,
  dbl_allowance_amt DOUBLE PRECISION,
  vchr_remark TEXT,
  int_status INT,
  fk_created_id BIGINT REFERENCES auth_user(id),
  fk_updated_id BIGINT REFERENCES auth_user(id),
  dat_created TIMESTAMP ,
  dat_updated TIMESTAMP
);
ALTER TABLE shift_schedule ALTER COLUMN time_full_day TYPE INTERVAL;
ALTER TABLE shift_schedule ALTER COLUMN time_half_day TYPE INTERVAL;
ALTER TABLE shift_schedule ALTER COLUMN time_shed_hrs TYPE INTERVAL;
ALTER TABLE shift_schedule ALTER COLUMN time_break_hrs TYPE INTERVAL;
ALTER TABLE shift_schedule ADD COLUMN bln_time_shift BOOLEAN DEFAULT FALSE;
ALTER TABLE shift_schedule ADD COLUMN int_shift_type INTEGER DEFAULT 0;


CREATE TABLE employee_shift(
  pk_bint_id  BIGSERIAL PRIMARY KEY,
  fk_employee_id BIGINT REFERENCES userdetails(user_ptr_id),
  int_shift_type INT,
  json_shift JSONB,
  bln_active BOOLEAN,
  fk_created_id BIGINT REFERENCES auth_user(id),
  fk_updated_id BIGINT REFERENCES auth_user(id),
  dat_created TIMESTAMP,
  dat_updated TIMESTAMP
);

CREATE TABLE user_history(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_user_id BIGINT REFERENCES userdetails(user_ptr_id),
  json_details JSONB,
  int_type INTEGER,
  bln_changed BOOLEAN DEFAULT FALSE,
  fk_created_id BIGINT REFERENCES auth_user(id),
  dat_created TIMESTAMP DEFAULT NOW(),
  fk_approved_id BIGINT REFERENCES auth_user(id),
  dat_approved TIMESTAMP,
  int_status INTEGER
);

alter table group_permissions add column fk_desig_id BIGINT REFERENCES job_position(pk_bint_id);
alter table userdetails add fk_hierarchy_data_id bigint REFERENCES hierarchy_data(pk_bint_id);


CREATE TABLE hierarchy_groups (pk_bint_id BIGSERIAL PRIMARY KEY,fk_hierarchy_id BIGINT REFERENCES hierarchy(pk_bint_id),vchr_name VARCHAR(50),int_status SMALLINT);
alter table hierarchy_groups add column fk_department_id bigint REFERENCES department(pk_bint_id);
alter table hierarchy add fk_department_id bigint REFERENCES department(pk_bint_id);

alter table userdetails add fk_group_id bigint REFERENCES groups(pk_bint_id);
alter table userdetails add column fk_hierarchy_group_id bigint REFERENCES hierarchy_groups(pk_bint_id);

alter table customer_details add column vchr_gender varchar(10) ;
alter table customer_details add COLUMN cust_smsaccess BOOLEAN;









-- insert query#######################################33333
-- INSERT INTO states (vchr_name) VALUES ('JAMMU & KASHMIR'),('HIMACHAL PRADESH'),('PUNJAB'),('CHANDIGARH'),('UTTARANCHAL'),('HARYANA'),('DELHI'),('RAJASTHAN'),('UTTAR PRADESH'),('BIHAR'),('SIKKIM'),('ARUNACHAL PRADESH'),('NAGALAND'),('MANIPUR'),('MIZORAM'),('TRIPURA'),('MEGHALAYA'),('ASSAM'),('WEST BENGAL'),('JHARKHAND'),('ORISSA'),('CHHATTISGARH'),('MADHYA PRADESH'),('GUJARAT'),('DAMAN & DIU'),('DADRA & NAGAR HAVELI'),('MAHARASHTRA'),('ANDHRA PRADESH'),('KARNATAKA'),('GOA'),('LAKSHADWEEP'),('KERALA'),('TAMIL NADU'),('PONDICHERRY'),('ANDAMAN & NICOBAR ISLANDS')

-- insert into brands(vchr_code,vchr_name,int_status) values ('ACER','ACER',0),('AMAZON','AMAZON',0),('APPLE','APPLE',0);

-- insert into other_category (vchr_name, int_status) values ('dealer',1),('supplier',2),('branch',3);

-- insert into hierarchy (vchr_name,int_level) values ('TEAM',1),('FLOOR',2),('BRANCH',3),('DISTRICT',4),('TERIRTORY',5),('STATE',6),('ZONE',7),('COUNTRY',8);

INSERT INTO sub_category(fk_main_category_id,vchr_sub_category_name,vchr_sub_category_value,int_sub_category_order,vchr_icon_name) VALUES ((SELECT pk_bint_id from main_category WHERE vchr_main_category_name = 'MASTER'),'ADD LOCATIONS','add locations',1,'mdi mdi-map-marker');


INSERT INTO country (vchr_name,vchr_code) VALUES ('INDIA','IND');


ALTER TABLE groups ADD COLUMN dbl_experience DOUBLE PRECISION;
ALTER TABLE groups ADD COLUMN json_qualification JSONB;
ALTER TABLE groups ADD COLUMN vchr_age_limit VARCHAR (50);
ALTER TABLE groups ADD COLUMN txt_desc TEXT;
ALTER TABLE groups ADD COLUMN int_notice_period INTEGER;
alter table groups add column json_desc JSONB;
ALTER TABLE groups add column fk_company_id BIGINT REFERENCES company(pk_bint_id);
ALTER TABLE groups ADD COLUMN bln_admin BOOLEAN;
ALTER TABLE groups ADD COLUMN int_permission INTEGER;
ALTER TABLE groups ADD COLUMN bln_brand BOOLEAN DEFAULT FALSE;
ALTER TABLE groups ADD COLUMN fk_department_id BIGINT REFERENCES department(pk_bint_id);
ALTER TABLE groups ADD COLUMN int_area_type INTEGER;
ALTER TABLE groups ADD COLUMN json_area_id JSONB;
ALTER TABLE groups ADD COLUMN bln_active BOOLEAN;

INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_addurl) VALUES('Desiganation Permission',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'GROUP'),'designationpermmison',1,'false','group-permission/addpermission');
CREATE TABLE physical_location(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_physical_loc VARCHAR(150)
);

CREATE TABLE salary_details(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_user_id BIGINT REFERENCES userdetails(user_ptr_id),
  dbl_bp DOUBLE PRECISION,
  dbl_da DOUBLE PRECISION,
  dbl_hra DOUBLE PRECISION,
  dbl_cca DOUBLE PRECISION,
  dbl_sa DOUBLE PRECISION,
  dbl_wa DOUBLE PRECISION,
  json_deduction JSONB,
  json_allowance JSONB,
  int_status INTEGER);

alter table salary_details rename column fk_user_id to fk_employee_id;

ALTER TABLE salary_details ADD COLUMN fk_updated_id BIGINT REFERENCES userdetails(user_ptr_id);
ALTER TABLE salary_details ADD COLUMN dat_updated TIMESTAMP;
ALTER TABLE salary_details ADD COLUMN dbl_gross DOUBLE PRECISION DEFAULT 0.0;
ALTER TABLE salary_details ADD COLUMN fk_created_id BIGINT REFERENCES auth_user(id);
ALTER TABLE salary_details ADD COLUMN dat_created TIMESTAMP DEFAULT NOW();


alter table company add vchr_code varchar(50);
alter table company add vchr_plan varchar(50);
alter table company add dat_created_at DATE;
alter table company add dat_updated_at DATE;
alter table company add time_from INTEGER;
alter table company add time_to INTEGER;
alter table company add int_user_count INTEGER;
alter table company add fk_company_type_id BIGINT;
alter table branch add fk_hierarchy_data_id BIGINT REFERENCES hierarchy_data(pk_bint_id);
alter table branch add fk_territory_id BIGINT;

alter table customer_details add fk_company_id BIGINT REFERENCES company(pk_bint_id);


create table source(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_source_name varchar(15),
  bln_status boolean,
  bln_is_campaign boolean,
  fk_company_id bigint REFERENCES company(pk_bint_id),
  fk_category_id bigint REFERENCES category(pk_bint_id);
alter table enquiry_master add column fk_priority_id bigint REFERENCES priority(pk_bint_id);


INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_addurl) VALUES('Group Permission',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'GROUP'),'designationpermmison',1,'false','group-permission/addpermission');

-- CREATE TABLE accounts_map( 
--   pk_bint_id BIGSERIAL PRIMARY KEY,
--   vchr_module_name varchar(50),
--   vchr_category varchar(250),
--   fk_coa_id bigint REFERENCES chart_of_accounts(pk_bint_id),
--   int_status smallint,
--   int_type smallint,
--   fk_branch_id bigint REFERENCES branch(pk_bint_id)
-- );

ALTER TABLE item ADD column fk_company_id BIGINT REFERENCES company(pk_bint_id);
ALTER TABLE item ALTER COLUMN fk_company_id SET DEFAULT 1;
ALTER TABLE brands ALTER COLUMN fk_company_id SET DEFAULT 1;


-- INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_addurl) VALUES('Add Brand',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'BRAND'),'Add Brand',1,'false','brand/addbrand');
-- INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_addurl) VALUES('Brand List',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'BRAND'),'Brand List',1,'false','brand/brandlist');


ALTER TABLE brands ADD column fk_company_id BIGINT REFERENCES company(pk_bint_id);
ALTER TABLE brands ALTER COLUMN fk_company_id SET DEFAULT 1;

ALTER TABLE supplier ADD column fk_company_id BIGINT REFERENCES company(pk_bint_id);
ALTER TABLE supplier ALTER COLUMN fk_company_id SET DEFAULT 1;

ALTER TABLE products ADD column fk_company_id BIGINT REFERENCES company(pk_bint_id);
ALTER TABLE products ALTER COLUMN fk_company_id SET DEFAULT 1;

ALTER TABLE dealer ADD column fk_company_id BIGINT REFERENCES company(pk_bint_id);
ALTER TABLE dealer ALTER COLUMN fk_company_id SET DEFAULT 1;

ALTER TABLE item_category ADD column fk_company_id BIGINT REFERENCES company(pk_bint_id);
ALTER TABLE item_category ALTER COLUMN fk_company_id SET DEFAULT 1;

INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_addurl) VALUES('Enquiry List',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'INVOICE'),'Enquiry List',1,'false','lead/lead-list');

INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_addurl) VALUES('Add Brand',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'BRAND'),'Add Brand',1,'false','brand/addbrand');
INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_addurl) VALUES('Brand List',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'BRAND'),'Brand List',1,'false','brand/brandlist');
 