CREATE TABLE partial_receipt(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  json_data JSONB,
  fk_enquiry_master_id BIGINT,
  fk_receipt_id BIGINT REFERENCES receipt,
  int_status INTEGER
);
