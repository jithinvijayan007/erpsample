
CREATE TABLE backend_urls(
pk_bint_id BIGSERIAL PRIMARY KEY,
vchr_backend_url VARCHAR(100),
vchr_module_name VARCHAR(100));

CREATE TABLE user_log_details
(pk_bint_id BIGSERIAL PRIMARY KEY,
fk_user_id BIGINT REFERENCES auth_user(id), 
fk_module_id BIGINT REFERENCES backend_urls(pk_bint_id),
int_count INTEGER,
json_ip JSON,
dat_start_active TIMESTAMP,
dat_last_active TIMESTAMP);



INSERT INTO backend_urls(vchr_backend_url,vchr_module_name) VALUES('/user/login/','USER LOGIN') ,('/payment/payment_list/','PAYMENT LIST' ),('/invoice/add_invoice/','ADD INVOICE' ),('/invoice/sales_list/','SALES LIST' ),('/invoice/invoice_list/','INVOICE LIST' ),('/salesreturn/get_return_details/' ,'SALES RETURN DETAILS' ),('/invoice/save_returned_sales/' ,'SAVE SALES RETURN' ),('/exchange_sales/exchange_sales/' ,'EXCHANGE SALES' ),('/internalstock/gettransferlist/' ,'STOCK TRANSFER LIST' ),('/internalstock/getrequestlist/','STOCK REQUEST LIST' ),('/case_closure/case_closure_notification/' ,'CASE CLOSURE' ),('/payment/payment_list/' ,'PAYMENT LIST' ),('/receipt/list_receipt/' ,'RECEIPT LIST' ),('/receipt/receipt_order_list/' ,'RECEIPT ORDER LIST' ),('/receipt/add/' ,'RECEIPT ADD' ),('/dayclosure/dayclosure_list/' ,'DAY CLOSURE' ),('/dayclosure/lst_dayclosure/' ,'DAY CLOSURE');


INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_listurl) VALUES('List Direct Transfer',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'STOCK TRANSFER'),'listdirecttransfer',11,'false','/stocktransfer/directtransferlist');
 
 
INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_listurl) VALUES('Client Outstanding Report',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'SALES'),'clientoutstanding',11,'false','/report/clientoutstanding');

CREATE TABLE journal(
vchr_jvu VARCHAR(100),
fk_branch_id BIGINT REFERENCES BRANCH(pk_bint_id),
dat_journal TIMESTAMP,
int_debit_type INTEGER,
int_credit_type INTEGER,
bint_debit_id BIGINT ,
bint_credit_id BIGINT,
dbl_amount BIGINT,
bint_payee_debit_id BIGINT,
bint_payee_credit_id BIGINT);

