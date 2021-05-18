CREATE TABLE theft_details (
pk_bint_id BIGSERIAL PRIMARY KEY,
dat_purchase DATE,
int_days_missing INTEGER,
int_depreciation_amt BIGINT,
fk_purchase_branch_id BIGINT REFERENCES branch,
fk_partial_invoice_id BIGINT REFERENCES partial_invoice,
fk_created_id BIGINT REFERENCES AUTH_USER,
dat_created TIMESTAMP
)
CREATE TABLE depreciation(
pk_bint_id BIGSERIAL PRIMARY KEY,
int_days_upto INTEGER,
int_dep_percentage INTEGER);
