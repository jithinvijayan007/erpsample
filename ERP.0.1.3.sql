CREATE TABLE customer_rating (
    pk_bint_id BIGSERIAL PRIMARY KEY,
    vchr_feedback TEXT NULL,
    dbl_rating DOUBLE PRECISION ,
    fk_customer_id BIGINT REFERENCES customer_details (pk_bint_id) NOT NULL,
    fk_user_id BIGINT REFERENCES userdetails ( user_ptr_id) NOT NULL
);
CREATE TABLE emp_category(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_code VARCHAR(10),
  vchr_name VARCHAR(150),
  int_status INTEGER ,
  fk_created_id BIGINT REFERENCES auth_user(id),
  fk_updated_id BIGINT REFERENCES auth_user(id),
  dat_created TIMESTAMP ,
  dat_updated TIMESTAMP
);

ALTER TABLE userdetails
DROP COLUMN fk_category_id;

ALTER TABLE userdetails
ADD COLUMN fk_category_id BIGINT REFERENCES emp_category(pk_bint_id);


CREATE TABLE Target_Master(

  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_fin_type VARCHAR(50) NOT NULL,
  int_year INTEGER NOT NULL,
  dbl_target DOUBLE PRECISION,
  int_target_type INTEGER NOT NULL,
  fk_created_id BIGINT REFERENCES userdetails(user_ptr_id),
  dat_created TIMESTAMP NOT NULL,
  fk_updated_id BIGINT REFERENCES userdetails(user_ptr_id),
  dat_updated TIMESTAMP ,
  bln_active boolean,
  bln_all boolean,
  fk_user_id BIGINT REFERENCES userdetails(user_ptr_id) NOT NULL

);


CREATE TABLE Target_Details(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  fk_master_id  BIGINT REFERENCES Target_Master(pk_bint_id) NOT NULL,
  int_target_type INTEGER NOT NULL,
  int_month INTEGER NOT NULL,
  vchr_month VARCHAR(50) NOT NULL,
  int_year INTEGER NOT NULL,
  dbl_target DOUBLE PRECISION,
  fk_user_id BIGINT REFERENCES userdetails(user_ptr_id) NOT NULL,
 fk_brand_id BIGINT REFERENCES brands(pk_bint_id)
);

alter table company add vchr_fin_type varchar(10);
update company set  vchr_fin_type = 'JAN-DEC';

