
-- new
CREATE TABLE partial_receipt(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_branchcode VARCHAR(20),
  vchr_item_code VARCHAR(20),
  json_data JSONB,
  fk_enquiry_master_id BIGINT,
  fk_receipt_id BIGINT REFERENCES receipt,
  dat_created TIMESTAMP,
  int_status INTEGER
);
