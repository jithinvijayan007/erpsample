DROP TABLE JOURNAL;
CREATE TABLE journal(
pk_bint_id BIGSERIAL PRIMARY KEY,
vchr_jv_num VARCHAR(100),
fk_branch_id BIGINT REFERENCES BRANCH(pk_bint_id),
dat_journal DATE,
int_debit_type INTEGER,-- CUST
fk_debit_id INTEGER ,
int_credit_type INTEGER,
fk_credit_id INTEGER,
dbl_amount DOUBLE PRECISION,
vchr_remarks varchar(500),
dat_created TIMESTAMP WITHOUT TIME ZONE,
fk_created_id BIGINT REFERENCES userdetails(user_ptr_id)
);


