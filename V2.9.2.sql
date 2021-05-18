alter table stock_Transfer ADD vchr_eway_bill_no VARCHAR(25);
ALTER TABLE branch ADD int_pincode INTEGER;

CREATE TABLE courier_master (
pk_bint_id BIGSERIAL PRIMARY KEY,
vchr_name VARCHAR(100),
vchr_gst_no VARCHAR(100),
json_vehicle_no JSONB);

ALTER TABLE transfer_mode_details ADD fk_courier_id BIGINT REFERENCES courier_master;

INSERT INTO courier_master (json_vehicle_no,vchr_gst_no,vchr_name) VALUES('["PVC1234","PVC1234","PVC1234","PVC1234","PVC1234"]','2321321323','DHL');
INSERT INTO courier_master (json_vehicle_no,vchr_gst_no,vchr_name) VALUES('["PVC1234","PVC1234","PVC1234","PVC1234","PVC1234"]','2321321323','DTDC');
INSERT INTO courier_master (json_vehicle_no,vchr_gst_no,vchr_name) VALUES('["PVC1234","PVC1234","PVC1234","PVC1234","PVC1234"]','2321321323','BlueDart');

INSERT INTO courier_master (json_vehicle_no,vchr_gst_no,vchr_name) VALUES('["KL11AW5155"]','32AABCC8298E1ZO','TRACKON');
INSERT INTO courier_master (json_vehicle_no,vchr_gst_no,vchr_name) VALUES('["KL11BA6414"]','88AAACD8017H1ZX','DTDC');

INSERT INTO courier_master (json_vehicle_no,vchr_name) VALUES('["KL11AR8515","KL11BJ6331","KL11AQ6232","KL11AE0019","KL59P565"]','VPM COURIER');


ALTER TABLE stock_Transfer ADD bln_direct_transfer BOOLEAN DEFAULT false;
