CREATE TABLE shift_exemption(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  dat_start DATE NOT NULL,
  dat_end DATE,
  int_type INTEGER NOT NULL,
  json_type_ids JSONB NOT NULL,
  json_punch_emps JSONB,
  json_exclude JSONB,
  fk_created_id BIGINT REFERENCES auth_user(id) NOT NULL,
  dat_created TIMESTAMP WITHOUT TIME ZONE NOT NULL,
  int_status INTEGER DEFAULT 1 NOT NULL
);

CREATE TABLE hierarchy_level(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_department_id BIGINT REFERENCES department(pk_bint_id) NOT NULL,
  fk_designation_id BIGINT REFERENCES groups(pk_bint_id),
  fk_reporting_to_id BIGINT REFERENCES groups(pk_bint_id),
  dat_created TIMESTAMP DEFAULT NOW(),
  dat_updated TIMESTAMP DEFAULT NOW(),
  fk_created_id BIGINT REFERENCES auth_user(id),
  fk_updated_id BIGINT REFERENCES auth_user(id),
  int_status SMALLINT DEFAULT 1,
  int_mode SMALLINT DEFAULT 0
);
CREATE TABLE punching_emp(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_user_log_id VARCHAR(256), -- punching machine USER ID for EMPCODE
  fk_user_id BIGINT REFERENCES userdetails(user_ptr_id),
  int_active INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE employees (
    employeeid BIGSERIAL PRIMARY KEY,
    employeename character varying NOT NULL,
    employeecode character varying NOT NULL,
    stringcode character varying NOT NULL,
    numericcode integer NOT NULL,
    gender character varying NOT NULL,
    companyid integer NOT NULL,
    departmentid integer NOT NULL,
    designation character varying,
    categoryid integer NOT NULL,
    doj timestamp without time zone,
    dor timestamp without time zone,
    doc timestamp without time zone,
    employeecodeindevice character varying NOT NULL,
    employeerfidnumber character varying,
    employementtype character varying NOT NULL,
    status character varying NOT NULL,
    employeedevicepassword character varying,
    employeedevicegroup character varying,
    fathername character varying,
    mothername character varying,
    residentialaddress character varying,
    permanentaddress character varying,
    contactno character varying,
    email character varying,
    dob timestamp without time zone,
    placeofbirth character varying,
    nomenee1 character varying,
    nomenee2 character varying,
    remarks text,
    recordstatus integer,
    c1 character varying,
    c2 character varying,
    c3 character varying,
    c4 character varying,
    c5 character varying,
    c6 character varying,
    c7 character varying,
    location character varying,
    bloodgroup character varying,
    workplace character varying,
    extensionno character varying,
    loginname character varying,
    loginpassword character varying,
    grade character varying,
    team character varying,
    isrecievenotification integer,
    holidaygroup integer,
    shiftgroupid integer,
    shiftrosterid integer,
    lastmodifiedby character varying
);

CREATE TABLE punch_log(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_punchingemp_id BIGINT REFERENCES punching_emp(pk_bint_id),
  fk_shift_id BIGINT REFERENCES shift_schedule(pk_bint_id),
  int_start_device_id BIGINT,
  dat_start TIMESTAMP,
  int_end_device_id BIGINT,
  dat_end TIMESTAMP,
  dat_punch DATE,
  dur_active INTERVAL,
  int_ellc INTEGER, -- -1. Early Leavers, 0. Normal, 1. Late Comers, 2. Early Leavers & Late comers
  vchr_direction VARCHAR(5),
  bln_manual BOOLEAN DEFAULT False
);

CREATE TABLE punch_log_detail(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_log_id BIGINT REFERENCES punch_log(pk_bint_id),
  int_start_device_id BIGINT,
  tim_start TIME,
  int_end_device_id BIGINT,
  tim_end TIME
);

ALTER TABLE punch_log ADD COLUMN fk_shift_id BIGINT REFERENCES shift_schedule(pk_bint_id);
ALTER TABLE punch_log ADD COLUMN dur_active INTERVAL;
ALTER TABLE punch_log ADD COLUMN int_ellc INTEGER;
ALTER TABLE punch_log add column bln_manual BOOLEAN default False;
ALTER TABLE punch_log RENAME COLUMN int_device_id TO int_start_device_id;
ALTER TABLE punch_log ADD COLUMN int_end_device_id BIGINT;
ALTER TABLE punch_log_detail ADD COLUMN int_start_device_id BIGINT;
ALTER TABLE punch_log_detail ADD COLUMN int_end_device_id BIGINT;


CREATE TABLE devices (
    deviceid BIGSERIAL PRIMARY KEY,
    devicefname character varying NOT NULL,
    devicesname character varying NOT NULL,
    devicedirection character varying,
    serialnumber character varying NOT NULL,
    connectiontype character varying,
    ipaddress character varying,
    baudrate character varying,
    commkey character varying NOT NULL,
    comport character varying,
    lastlogdownloaddate timestamp without time zone,
    c1 character varying,
    c2 character varying,
    c3 character varying,
    c4 character varying,
    c5 character varying,
    c6 character varying,
    c7 character varying,
    transactionstamp character varying,
    lastping timestamp without time zone,
    devicetype character varying,
    opstamp character varying,
    downloadtype integer,
    timezone character varying,
    devicelocation character varying,
    timeout character varying
);

CREATE TABLE holiday(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_name VARCHAR(100),
  dat_holiday DATE,
  int_year INT,
  fk_created_id BIGINT REFERENCES auth_user(id),
  fk_updated_id BIGINT REFERENCES auth_user(id),
  dat_created TIMESTAMP,
  dat_updated TIMESTAMP,
  bln_active BOOLEAN
);

CREATE TABLE duty_roster(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_employee_id BIGINT REFERENCES userdetails(user_ptr_id),
  json_dates JSONB,
  int_month INTEGER,
  int_year INTEGER,
  bln_active BOOLEAN,
  fk_created_id BIGINT REFERENCES auth_user(id),
  fk_updated_id BIGINT REFERENCES auth_user(id),
  dat_created TIMESTAMP ,
  dat_updated TIMESTAMP

);

CREATE TABLE weekoff_leave(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_employee_id BIGINT REFERENCES userdetails(user_ptr_id) NOT NULL,
  dat_from DATE NOT NULL,
  dat_to DATE NOT NULL,
  dat_created TIMESTAMP NOT NULL DEFAULT NOW(),
  int_status INTEGER DEFAULT 1,
  fk_approved_id BIGINT REFERENCES auth_user(id),
  dat_approve TIMESTAMP,
  fk_verified_id BIGINT REFERENCES auth_user(id),
  dat_verified TIMESTAMP
);

 CREATE TABLE leavetype (
     id BIGSERIAL PRIMARY KEY,
     vchr_type VARCHAR(100) NOT NULL,
     bln_active boolean NOT NULL,
     int_count INTEGER NOT NULL,
     int_year INTEGER NOT NULL,
     fk_desig_id BIGINT REFERENCES job_position(pk_bint_id),
     fk_company_id BIGINT REFERENCES company(pk_bint_id) NULL
 );

 CREATE TABLE leave (
     id BIGSERIAL PRIMARY KEY,
     dat_from TIMESTAMP WITHOUT TIME ZONE,
     dat_to TIMESTAMP WITHOUT TIME ZONE,
     dbl_days  DOUBLE PRECISION,
     chr_leave_mode VARCHAR(2) NOT NULL DEFAULT 'F',
     vchr_reason text NOT NULL,
     int_status integer NOT NULL,
     dat_approved TIMESTAMP,
     dat_applied TIMESTAMP WITHOUT TIME ZONE NOT NULL,
     fk_approved_id BIGINT REFERENCES userdetails(user_ptr_id),
     fk_leave_type_id BIGINT REFERENCES leavetype(id),
     fk_user_id BIGINT REFERENCES userdetails(user_ptr_id),
     vchr_approve text,
     vchr_reject text
 );

CREATE TABLE combo_off(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  dat_worked DATE,
  vchr_reason TEXT,
  dat_expiry DATE
);
ALTER TABLE combo_off ADD COLUMN bln_auto_add BOOLEAN DEFAULT FALSE;


CREATE TABLE combo_off_users(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_user_id BIGINT REFERENCES userdetails(user_ptr_id),
  fk_combo_off_id BIGINT REFERENCES combo_off(pk_bint_id),
  dat_leave DATE,
  fk_approved_id BIGINT REFERENCES userdetails(user_ptr_id),
  dat_approved DATE,
  int_status INT  DEFAULT 0,
  vchr_reason TEXT
);
ALTER TABLE combo_off_users ADD COLUMN bln_auto_add BOOLEAN DEFAULT FALSE;

CREATE TABLE leave_type (
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_name VARCHAR(100) NOT NULL,
  int_leaves_per_month INTEGER NOT NULL,
  int_leaves_per_year INTEGER NOT NULL,
  int_year INTEGER NOT NULL,
  fk_desig_id BIGINT REFERENCES job_position(pk_bint_id),
  fk_company_id BIGINT REFERENCES company(pk_bint_id) NULL,
  vchr_remarks VARCHAR(300),
  bln_active BOOLEAN NOT NULL
);
ALTER TABLE leave_type drop column int_leaves_per_month;
ALTER TABLE leave_type drop column int_leaves_per_year;

ALTER TABLE leave_type add column dbl_leaves_per_month DOUBLE PRECISION;
ALTER TABLE leave_type add column dbl_leaves_per_year DOUBLE PRECISION;
ALTER TABLE leave_type ADD COLUMN bln_exclude_count BOOLEAN NOT NULL default FALSE;

  CREATE TABLE less_hour_policy(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  dur_from INTERVAL,
  dur_to INTERVAL,
  dbl_days DOUBLE PRECISION
);
 ALTER TABLE less_hour_policy ADD COLUMN fk_company_id BIGINT REFERENCES company(pk_bint_id);
ALTER TABLE less_hour_policy ADD COLUMN bln_auto BOOLEAN;
INSERT INTO less_hour_policy (dur_from,dur_to,dbl_days,bln_auto) VALUES
  ('00:00:00','00:44:59',0.5,true),
  ('00:00:00','00:44:59',0,false);
 
 
 CREATE TABLE less_hour_deduction(
 pk_bint_id BIGSERIAL PRIMARY KEY,
 fk_employee_id BIGINT REFERENCES userdetails (user_ptr_id),
 int_year INTEGER,
 int_month INTEGER,
 fk_policy_id BIGINT REFERENCES less_hour_policy (pk_bint_id),
 dur_time INTERVAL,
 int_status INTEGER
 );
 ALTER TABLE less_hour_deduction ADD COLUMN dur_aftr_deduct INTERVAL;
ALTER TABLE less_hour_deduction ADD COLUMN bln_regularize BOOLEAN DEFAULT false;
ALTER TABLE less_hour_deduction ADD COLUMN  fk_policy_id BIGINT REFERENCES less_hour_policy (pk_bint_id);


CREATE TABLE less_hour_leave(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_employee_id BIGINT REFERENCES userdetails(user_ptr_id),
  fk_deduction_id BIGINT REFERENCES less_hour_deduction(pk_bint_id),
  dat_leave DATE,
  dbl_days DOUBLE PRECISION,
  int_month INTEGER,
  int_year INTEGER
);

CREATE TABLE on_duty_request (
    pk_bint_id BIGSERIAL PRIMARY key,
    dat_request timestamp without time zone,
    fk_requested_id bigint REFERENCES userdetails(user_ptr_id),
    vchr_remarks text,
    chr_day_type character varying(2) DEFAULT 'F'::character varying NOT NULL,
    dat_created bigint REFERENCES auth_user(id),
    fk_approved_id bigint REFERENCES auth_user(id),
    dat_approved timestamp without time zone,
    fk_verified_id bigint REFERENCES userdetails(user_ptr_id),
    dat_verified timestamp without time zone,
    int_status integer DEFAULT 0
);


CREATE TABLE late_hours_policy(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_name VARCHAR(50),
  dbl_hours DOUBLE PRECISION
);

CREATE TABLE late_hours_request(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_employee_id BIGINT REFERENCES userdetails(user_ptr_id),
  fk_late_hours_policy_id BIGINT REFERENCES late_hours_policy(pk_bint_id),
  dat_requested TIMESTAMP ,
  fk_created_id BIGINT REFERENCES auth_user(id),
  fk_approved_id BIGINT REFERENCES auth_user(id),
  dat_created TIMESTAMP ,
  dat_approved TIMESTAMP ,
  int_status INTEGER ,
  vchr_remarks VARCHAR(300),
  int_month INTEGER,
  int_year INTEGER
);

-- /report/mobilesalesreport

INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_addurl) VALUES('Sales Product Report',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'SALES REPORTS'),'Sales Product Report',1,'false','report/mobilesalesreport');

INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_addurl) VALUES('Sales Productvity Report',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'SALES REPORTS'),'Sales Productvity Report',1,'false','report/productivityreport');

INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_addurl) VALUES('Branch Wise Report',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'SALES REPORTS'),'Branch Wise Report',1,'false','report/mobilebranchreport');

