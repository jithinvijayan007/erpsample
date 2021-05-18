ALTER TABLE journal ADD fk_debit_branch_id BIGINT REFERENCES branch;
ALTER TABLE journal ADD fk_credit_branch_id BIGINT REFERENCES branch;
ALTER TABLE journal DROP fk_branch_id;

alter table user_permissions add column json_price_perm jsonb;

INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_listurl) VALUES('Emi Sales Report',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'SALES'),'emisalesreport',4,'false','/report/emisalesreport');

INSERT INTO menu_category(vchr_menu_category_name,fk_sub_category_id,vchr_menu_category_value,int_menu_category_order,bln_has_children,vchr_listurl) VALUES('Day Closure Report',(SELECT pk_bint_id from sub_category WHERE vchr_sub_category_name = 'SALES'),'dayclosurereport',5,'false','/report/dayclosurereport');

INSERT INTO chart_of_accounts (vchr_acc_name,vchr_acc_code) VALUES ('ADDITIONS','ADDITIONS');

INSERT INTO chart_of_accounts (vchr_acc_name,vchr_acc_code) VALUES ('DEDUCTIONS','DEDUCTIONS');
