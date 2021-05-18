# Create your views here.
from rest_framework.permissions import IsAuthenticated,AllowAny
from dealer.models import Dealer,DealerAddress,DealerContactPerson,DealerLog
from category.models import OtherCategory
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import and_,func ,cast,Date
from sqlalchemy.sql.expression import literal,union_all
from aldjemy.core import get_engine
from django.db.models import Q
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from item_category.models import TaxMaster
from sqlalchemy import case, literal_column
from sqlalchemy import desc
from aldjemy.core import get_engine
from sqlalchemy.orm import mapper, aliased
from sqlalchemy import and_,func ,cast,Date
from POS import ins_logger
import sys, os

DealerSA=Dealer.sa
DealerAddressSA=DealerAddress.sa
DealerContactPersonSA=DealerContactPerson.sa
OtherCategorySA=OtherCategory.sa
TaxMasterSA=TaxMaster.sa

def Session():
    from aldjemy.core import get_engine
    engine=get_engine()
    _Session = sessionmaker(bind=engine)
    return _Session()


class AddDealer(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        #sending values in Taxmaster AND Category as list
        try:
            tax_name = list(TaxMaster.objects.values_list('pk_bint_id','vchr_name'))
            ins_category = list(OtherCategory.objects.filter(int_status = 1).values('pk_bint_id','vchr_name'))
            return Response({'status':1 , 'tax_list' : tax_name ,'dealer_category' : ins_category})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'status':0,'reason':e})

    def post(self,request):
        try:
            dct_addr_data  =  request.data.get('lstaddress')
            dct_contactp_data  = request.data.get('lstcontact')
            strDealerName = request.data.get('strDealerName')
            datDealerFrom = request.data.get('datDealerFrom')
            strDealerCode = request.data.get('strDealerCode')
            intCreditDays = request.data.get('intCreditDays')
            intCreditLimit = request.data.get('intCreditLimit')
            poExpiryDays = request.data.get('poExpiryDays')
            strTINNo = request.data.get('strTINNo')
            strCSTNo = request.data.get('strCSTNo')
            strGSTIN = request.data.get('strGSTIN')
            strGSTStatus = request.data.get('strGSTStatus')
            fk_category = int(request.data.get('fk_category'))
            fk_tax_class = int(request.data.get('fk_tax_class'))
            strGroup = request.data.get('strGroup')
            strAccount = request.data.get('strAccount')
            strPanNo = request.data.get('strPanNo')
            strPanStatus = request.data.get('strPanStatus')
            intActive = request.data.get('intActive')

            ins_item_duplicate = list(Dealer.objects.filter(Q(vchr_code = strDealerCode)|Q(vchr_cst_no = strCSTNo)|Q(vchr_gstin = strGSTIN)|Q(vchr_bank_account= strAccount)|Q(vchr_pan_no = strPanNo)|Q(vchr_tin_no=strTINNo)).values('pk_bint_id'))

            if ins_item_duplicate:
                return Response({'status':0 , 'data' : 'Dealer already exists'})

            else:
                ins_dealer = Dealer.objects.create(
                                        vchr_name = strDealerName,
                                        dat_from = datDealerFrom,
                                        vchr_code = strDealerCode,
                                        int_credit_days = intCreditDays,
                                        bint_credit_limit = intCreditLimit,
                                        int_po_expiry_days = poExpiryDays,
                                        vchr_tin_no = strTINNo,
                                        vchr_cst_no = strCSTNo,
                                        vchr_gstin = strGSTIN,
                                        vchr_gstin_status =strGSTStatus,
                                        fk_category_id = fk_category,
                                        fk_tax_class_id = fk_tax_class,
                                        vchr_account_group = strGroup,
                                        vchr_bank_account = strAccount,
                                        vchr_pan_no = strPanNo,
                                        vchr_pan_status = strPanStatus,
                                        int_is_act_del = intActive,
                                        fk_created_id=request.user.id,
                                        dat_created=datetime.now()
                                        )


                # import pdb; pdb.set_trace()
            #iterating through dictionary
                for dct_sub in range(len(dct_addr_data)):
            #giving front end data to address model one by one
                    ins_addr = DealerAddress.objects.create(
                                vchr_address = dct_addr_data[dct_sub]['strAddress'],
                                vchr_email = dct_addr_data[dct_sub]['strEmail'],
                                bint_phone_no = dct_addr_data[dct_sub]['intContact'],
                                int_pincode = dct_addr_data[dct_sub]['intPinCode'],
                                fk_dealer_id = ins_dealer.pk_bint_id,
                                bln_status=True
                                                                    )




                for dct_sub in range(len(dct_contactp_data)):

                #giving front end data to ContactPerson model one by one
                    ins_cont  =  DealerContactPerson.objects.create(
                                                vchr_name = dct_contactp_data[dct_sub]['strName'],
                                                vchr_designation = dct_contactp_data[dct_sub]['strDesig'],
                                                vchr_department = dct_contactp_data[dct_sub]['strDept'],
                                                vchr_office = dct_contactp_data[dct_sub]['strOffice'],
                                                bint_mobile_no1 = dct_contactp_data[dct_sub]['intPhone1'],
                                                bint_mobile_no2 = dct_contactp_data[dct_sub]['intPhone2'],
                                                fk_dealer_id = ins_dealer.pk_bint_id,
                                                bln_status=True
                                                )

                return Response({'status':1})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'status':0,'reason':e})


class ListDealer(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        try:

            tax_name = list(TaxMaster.objects.values_list('pk_bint_id','vchr_name'))
            ins_category = list(OtherCategory.objects.filter(int_status = 1).values('pk_bint_id','vchr_name'))

            intCreditDays = request.data.get('intCreditDays') #Get's values from front with field name = vchr_name and vchr_code
            intCreditLimit = request.data.get('intCreditLimit')
            fk_category = request.data.get('fk_category')
            intActive = request.data.get('intActive')
            int_dealer_id =request.data.get('dealerId')
            rst_dealer=Dealer.objects.filter(int_is_act_del__in=[0,2]).values('pk_bint_id','vchr_name','dat_from','vchr_code','int_credit_days','bint_credit_limit','vchr_tin_no','vchr_cst_no','vchr_gstin','vchr_gstin_status','fk_tax_class_id','fk_tax_class__vchr_name','vchr_account_group','vchr_bank_account','vchr_pan_no','vchr_pan_status','int_po_expiry_days','int_is_act_del','fk_category_id','fk_category__vchr_name').order_by('-dat_created','-dat_updated')

            #multiple if condition to check all conditions are active or not  and filter values according to it
            if intActive:
                rst_dealer = rst_dealer.filter(int_is_act_del = int(intActive))
            if intCreditDays:
                rst_dealer = rst_dealer.filter(int_credit_days = intCreditDays)
            if intCreditLimit:
                rst_dealer = rst_dealer.filter(bint_credit_limit = intCreditLimit)
            if fk_category:
                rst_dealer = rst_dealer.filter(fk_category_id = fk_category)
            if int_dealer_id:
                rst_dealer = rst_dealer.filter(pk_bint_id = int_dealer_id)


            return Response({'status':1,'list_dealer':list(rst_dealer), 'tax_list' : tax_name ,'dealer_category' : ins_category})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'status':0,'reason':e})



class EditDealer(APIView):
    permission_classes = [AllowAny]
    '''Update'''
    def post(self,request):
        try:

            dct_addr_data  =  request.data.get('lstaddress')
            dct_contactp_data  = request.data.get('lstcontact')
            strDealerName = request.data.get('strDealerName')
            datDealerFrom = request.data.get('datDealerFrom')
            strDealerCode = request.data.get('strDealerCode')
            intCreditDays = request.data.get('intCreditDays')
            intCreditLimit = request.data.get('intCreditLimit')
            poExpiryDays = request.data.get('poExpiryDays')
            strTINNo = request.data.get('strTINNo')
            strCSTNo = request.data.get('strCSTNo')
            strGSTIN = request.data.get('strGSTIN')
            strGSTStatus = request.data.get('strGSTStatus')
            fk_category = int(request.data.get('fk_category'))
            fk_tax_class = int(request.data.get('fk_tax_class'))
            strGroup = request.data.get('strGroup')
            strAccount = request.data.get('strAccount')
            strPanNo = request.data.get('strPanNo')
            strPanStatus = request.data.get('strPanStatus')
            int_dealer_id = request.data.get('pk_bint_id')
            intActive = request.data.get('intActive')
            str_remarks = request.data.get('strRemarks')

            # import pdb; pdb.set_trace()


            # ===================soft deleting address and contact person==================================================================

            lst_avail_addr=DealerAddress.objects.filter(fk_dealer_id = int_dealer_id).values_list('pk_bint_id',flat = True)
            lst_avail_cp=DealerContactPerson.objects.filter(fk_dealer_id = int_dealer_id).values_list('pk_bint_id',flat = True)
            #list of all pk_bint_id values currently in database

            lst_cur_addr = [x.get('Address_id') for x in dct_addr_data] #list comprihenson to take all the values (Address_id) from frontend dct_addr_data
            lst_cur_cp = [x.get('contact_id') for x in dct_contactp_data] #list comprihenson to take all the values (contact_id) from frontend dct_contactp_data


            lst_dlt_addr = list(set(lst_avail_addr)-set(lst_cur_addr))
            lst_dlt_cp = list(set(lst_avail_cp)-set(lst_cur_cp))
            #gives all the deleted (address and contactperson) pk_bint_id which are deleted from from end
            #ie if front-end didnt send address,contactperson and its values it means its deleted so the condition is to check if any adddress or contact persion id is not comming back  to reques.data() , update the corresponding address,contactperson bln status to false.

            if lst_dlt_addr:
                DealerAddress.objects.filter(fk_dealer_id = int_dealer_id,pk_bint_id__in = lst_dlt_addr).update(bln_status = False)
                #if any deleted id is stored in lst_dlt_addr it will update bln_status = False
            if lst_dlt_cp:
                DealerContactPerson.objects.filter(fk_dealer_id = int_dealer_id,pk_bint_id__in = lst_dlt_cp).update(bln_status = False)
            # ===============================================================================================================================


            ins_item_duplicate = list(Dealer.objects.filter(Q(vchr_code = strDealerCode)|Q(vchr_cst_no = strCSTNo)|Q(vchr_gstin = strGSTIN)|Q(vchr_bank_account= strAccount)|Q(vchr_pan_no = strPanNo)|Q(vchr_tin_no=strTINNo)).values('pk_bint_id').exclude(pk_bint_id=int_dealer_id))


            if Dealer.objects.filter(pk_bint_id=int_dealer_id).values('int_is_act_del').first()['int_is_act_del'] != request.data.get('intActive') :
                 DealerLog.objects.create(vchr_remarks=str_remarks,vchr_status=intActive,fk_dealer_id=int_dealer_id,fk_created_id=request.user.id,dat_created=datetime.now())
            #if request.data.get('intActive') is changed ,Dealer Log object is created

            if ins_item_duplicate:
                return Response({'status':0 , 'data' : 'Dealer already exists'})

            else:
                ins_dealer = Dealer.objects.filter(pk_bint_id=int_dealer_id).update(
                                                            vchr_name = strDealerName,
                                                            dat_from = datDealerFrom,
                                                            vchr_code = strDealerCode,
                                                            int_credit_days = intCreditDays,
                                                            bint_credit_limit = intCreditLimit,
                                                            int_po_expiry_days = poExpiryDays,
                                                            vchr_tin_no = strTINNo,
                                                            vchr_cst_no = strCSTNo,
                                                            vchr_gstin = strGSTIN,
                                                            vchr_gstin_status =strGSTStatus,
                                                            fk_category = fk_category,
                                                            fk_tax_class = fk_tax_class,
                                                            vchr_account_group = strGroup,
                                                            vchr_bank_account = strAccount,
                                                            vchr_pan_no = strPanNo,
                                                            vchr_pan_status = strPanStatus,
                                                            int_is_act_del = intActive,
                                                            fk_updated_id=request.user.id,
                                                            dat_updated=datetime.now()
                                                            )



            #iterating through dictionary
                for dct_sub in range(len(dct_addr_data)):
                    if dct_addr_data[dct_sub].get('Address_id'):
                        ins_addr = DealerAddress.objects.filter(fk_dealer_id=int_dealer_id,pk_bint_id=dct_addr_data[dct_sub]['Address_id']).update(
                                                                vchr_address = dct_addr_data[dct_sub]['strAddress'],
                                                                vchr_email = dct_addr_data[dct_sub]['strEmail'],
                                                                bint_phone_no = dct_addr_data[dct_sub]['intContact'],
                                                                int_pincode = dct_addr_data[dct_sub]['intPinCode'],
                                                                bln_status=dct_addr_data[dct_sub]['bln_status'],
                                                                fk_dealer_id = int_dealer_id)
                    else:
                        ins_addr = DealerAddress.objects.create(
                                    vchr_address = dct_addr_data[dct_sub]['strAddress'],
                                    vchr_email = dct_addr_data[dct_sub]['strEmail'],
                                    bint_phone_no = dct_addr_data[dct_sub]['intContact'],
                                    int_pincode = dct_addr_data[dct_sub]['intPinCode'],
                                    fk_dealer_id = int_dealer_id,
                                    bln_status=True)

                #giving front end data to address model one by one


                for dct_sub in range(len(dct_contactp_data)):

                #giving front end data to ContactPerson model one by one
                    if dct_contactp_data[dct_sub].get('contact_id'):
                        ins_cont  =  DealerContactPerson.objects.filter(fk_dealer_id=int_dealer_id,pk_bint_id=dct_contactp_data[dct_sub]['contact_id']).update(
                                                    vchr_name = dct_contactp_data[dct_sub]['strName'],
                                                    vchr_designation = dct_contactp_data[dct_sub]['strDesig'],
                                                    vchr_department = dct_contactp_data[dct_sub]['strDept'],
                                                    vchr_office = dct_contactp_data[dct_sub]['strOffice'],
                                                    bint_mobile_no1 = dct_contactp_data[dct_sub]['intPhone1'],
                                                    bint_mobile_no2 = dct_contactp_data[dct_sub]['intPhone2'],
                                                    bln_status = dct_contactp_data[dct_sub]['bln_status'],
                                                    fk_dealer_id = int_dealer_id
                                                    )
                    else:
                        ins_cont  =  DealerContactPerson.objects.create(
                                                    vchr_name = dct_contactp_data[dct_sub]['strName'],
                                                    vchr_designation = dct_contactp_data[dct_sub]['strDesig'],
                                                    vchr_department = dct_contactp_data[dct_sub]['strDept'],
                                                    vchr_office = dct_contactp_data[dct_sub]['strOffice'],
                                                    bint_mobile_no1 = dct_contactp_data[dct_sub]['intPhone1'],
                                                    bint_mobile_no2 = dct_contactp_data[dct_sub]['intPhone2'],
                                                    fk_dealer_id = int_dealer_id,
                                                    bln_status=True
                                                    )



                return Response({'status':1})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'status':0,'reason':e})




class ViewDealer(APIView):
        permission_classes=[AllowAny]
        '''View'''
        def get(self,request):
            try:
                tax_name = list(TaxMaster.objects.values_list('pk_bint_id','vchr_name'))
                ins_category = list(OtherCategory.objects.filter(int_status = 1).values('pk_bint_id','vchr_name'))
                int_dealer_id = request.GET.get('id')
                session=Session()


                if int_dealer_id:

                    rst_enquiry = session.query(DealerSA.pk_bint_id.label("int_id_dealer"),DealerSA.vchr_name.label("dealer_name"),DealerSA.dat_from.label("dat_from"),\
                    DealerSA.vchr_code.label("vchr_code"),DealerSA.int_credit_days.label("int_credit_days"),DealerSA.bint_credit_limit.label("bint_credit_limit"),DealerSA.int_po_expiry_days.label("int_po_expiry_days")\
                    ,DealerSA.vchr_tin_no.label("vchr_tin_no") ,DealerSA.vchr_cst_no.label("vchr_cst_no"),DealerSA.vchr_gstin.label("vchr_gstin") ,DealerSA.vchr_gstin_status.label("vchr_gstin_status"),\
                    DealerSA.fk_category_id.label("fk_category_id"),DealerSA.vchr_account_group.label("vchr_account_group"),\
                    DealerSA.vchr_bank_account.label("vchr_bank_account"),DealerSA.vchr_pan_no.label("vchr_pan_no"),DealerSA.vchr_pan_status.label("vchr_pan_status"),DealerSA.int_is_act_del.label("int_is_act_del")\
                    ,OtherCategorySA.vchr_name.label("vchr_category_name"),TaxMasterSA.vchr_name.label("vchr_taxmaster_name"),TaxMasterSA.pk_bint_id.label("int_id_taxmaster"),DealerAddressSA.pk_bint_id.label("Address_id"),DealerAddressSA.vchr_address.label("vchr_address"),DealerAddressSA.vchr_email.label("vchr_email"),DealerAddressSA.bint_phone_no.label("bint_phone_no"),DealerAddressSA.bln_status.label("bln_addr_status"),\
                    DealerAddressSA.int_pincode.label("int_pincode"),DealerContactPersonSA.pk_bint_id.label("contact_id"),DealerContactPersonSA.vchr_name.label("contact_name"),DealerContactPersonSA.vchr_designation.label("vchr_designation"),\
                    DealerContactPersonSA.vchr_department.label("vchr_department"),DealerContactPersonSA.vchr_office.label("vchr_office"),DealerContactPersonSA.bint_mobile_no1.label("bint_mobile_no1"),\
                    DealerContactPersonSA.bint_mobile_no2.label("bint_mobile_no2"),DealerContactPersonSA.bln_status.label("bln_cp_status")).filter(DealerSA.pk_bint_id==int_dealer_id).\
                    outerjoin(DealerAddressSA,DealerSA.pk_bint_id==DealerAddressSA.fk_dealer_id).\
                    outerjoin(DealerContactPersonSA,DealerSA.pk_bint_id==DealerContactPersonSA.fk_dealer_id).\
                    outerjoin(OtherCategorySA,DealerSA.fk_category_id==OtherCategorySA.pk_bint_id).\
                    outerjoin(TaxMasterSA,DealerSA.fk_tax_class_id==TaxMasterSA.pk_bint_id).filter(DealerAddressSA.bln_status==True,DealerContactPersonSA.bln_status==True)

                    dct_enquiry ={}
                    # import pdb; pdb.set_trace()
                    for ins_enquiry in rst_enquiry.all():

                        if ins_enquiry.int_id_dealer not in dct_enquiry:
                            dct_enquiry[ins_enquiry.int_id_dealer] = {}
                            dct_enquiry[ins_enquiry.int_id_dealer]['dealer_name'] = ins_enquiry.dealer_name
                            dct_enquiry[ins_enquiry.int_id_dealer]['dat_from'] = ins_enquiry.dat_from
                            dct_enquiry[ins_enquiry.int_id_dealer]['vchr_code'] = ins_enquiry.vchr_code
                            dct_enquiry[ins_enquiry.int_id_dealer]['int_credit_days'] = ins_enquiry.int_credit_days
                            dct_enquiry[ins_enquiry.int_id_dealer]['bint_credit_limit'] = ins_enquiry.bint_credit_limit
                            dct_enquiry[ins_enquiry.int_id_dealer]['int_po_expiry_days'] = ins_enquiry.int_po_expiry_days
                            dct_enquiry[ins_enquiry.int_id_dealer]['vchr_tin_no'] = ins_enquiry.vchr_tin_no
                            dct_enquiry[ins_enquiry.int_id_dealer]['vchr_cst_no'] = ins_enquiry.vchr_cst_no
                            dct_enquiry[ins_enquiry.int_id_dealer]['vchr_gstin'] = ins_enquiry.vchr_gstin
                            dct_enquiry[ins_enquiry.int_id_dealer]['vchr_gstin_status'] = ins_enquiry.vchr_gstin_status
                            dct_enquiry[ins_enquiry.int_id_dealer]['fk_category_id'] = ins_enquiry.fk_category_id
                            dct_enquiry[ins_enquiry.int_id_dealer]['vchr_account_group'] = ins_enquiry.vchr_account_group
                            dct_enquiry[ins_enquiry.int_id_dealer]['vchr_bank_account'] = ins_enquiry.vchr_bank_account
                            dct_enquiry[ins_enquiry.int_id_dealer]['vchr_pan_no'] = ins_enquiry.vchr_pan_no
                            dct_enquiry[ins_enquiry.int_id_dealer]['vchr_pan_status'] = ins_enquiry.vchr_pan_status
                            dct_enquiry[ins_enquiry.int_id_dealer]['int_is_act_del'] = ins_enquiry.int_is_act_del
                            dct_enquiry[ins_enquiry.int_id_dealer]['vchr_category_name'] = ins_enquiry.vchr_category_name
                            dct_enquiry[ins_enquiry.int_id_dealer]['int_id_taxmaster'] = ins_enquiry.int_id_taxmaster
                            dct_enquiry[ins_enquiry.int_id_dealer]['vchr_taxmaster_name'] = ins_enquiry.vchr_taxmaster_name

                            dct_address={}
                            dct_contact={}
                            dct_enquiry[ins_enquiry.int_id_dealer]['lst_address']=[]
                            dct_enquiry[ins_enquiry.int_id_dealer]['lst_contact']=[]


                        if ins_enquiry.Address_id not in dct_address:
                                dct_address[ins_enquiry.Address_id]={}
                                dct_address[ins_enquiry.Address_id]['Address_id']=ins_enquiry.Address_id
                                dct_address[ins_enquiry.Address_id]['strAddress']=ins_enquiry.vchr_address
                                dct_address[ins_enquiry.Address_id]['strEmail']=ins_enquiry.vchr_email
                                dct_address[ins_enquiry.Address_id]['intContact']=ins_enquiry.bint_phone_no
                                dct_address[ins_enquiry.Address_id]['intPinCode']=ins_enquiry.int_pincode
                                dct_address[ins_enquiry.Address_id]['bln_status']=ins_enquiry.bln_addr_status
                                dct_enquiry[ins_enquiry.int_id_dealer]['lst_address'].append(dct_address[ins_enquiry.Address_id])
                                dct_address[ins_enquiry.Address_id]=None
                        if ins_enquiry.contact_id not in dct_contact:
                                dct_contact[ins_enquiry.contact_id]={}
                                dct_contact[ins_enquiry.contact_id]['contact_id']=ins_enquiry.contact_id
                                dct_contact[ins_enquiry.contact_id]['strName']=ins_enquiry.contact_name
                                dct_contact[ins_enquiry.contact_id]['strDesig']=ins_enquiry.vchr_designation
                                dct_contact[ins_enquiry.contact_id]['strDept']=ins_enquiry.vchr_department
                                dct_contact[ins_enquiry.contact_id]['strOffice']=ins_enquiry.vchr_office
                                dct_contact[ins_enquiry.contact_id]['intPhone1']=ins_enquiry.bint_mobile_no1
                                dct_contact[ins_enquiry.contact_id]['intPhone2']=ins_enquiry.bint_mobile_no2
                                dct_contact[ins_enquiry.contact_id]['bln_status']=ins_enquiry.bln_cp_status
                                dct_enquiry[ins_enquiry.int_id_dealer]['lst_contact'].append(dct_contact[ins_enquiry.contact_id])
                                dct_contact[ins_enquiry.contact_id]=None

                    session.close()
                    return Response({'status':1,'lst_userdetailsview':dct_enquiry,'tax_list' : tax_name ,'dealer_category' : ins_category})

                else:
                        session.close()
                        return Response({'status':0,'reason':"User deleted or doesn't exist"})

            except Exception as e:
                session.close()
                exc_type, exc_obj, exc_tb = sys.exc_info()
                ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
                return Response({'status':0,'reason':e})


class DealerHistory(APIView):
        permission_classes=[AllowAny]
        '''View'''
        def get(self,request):
            try:
                int_dealer_id = request.GET.get('id')


                history_list=list(DealerLog.objects.filter(fk_dealer_id=int_dealer_id).values('pk_bint_id','vchr_remarks','vchr_status','dat_created','fk_created','fk_dealer').order_by('-dat_created'))
                # history_list = []

                # for values in range(len(data_list)):
                #     dict={}
                #     dict['pk_bint_id']=data_list[values]['pk_bint_id']
                #     dict['vchr_remarks']=data_list[values]['vchr_remarks']
                #     dict['vchr_status']=data_list[values]['vchr_status']
                #     dict['fk_created']=data_list[values]['fk_created']
                #     dict['fk_dealer']=data_list[values]['fk_dealer']
                #
                #     history_list.append(dict)


                return Response({'status':1,'history_list':history_list})

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
                return Response({'status':0,'reason':e})

class DeleteDealer(APIView):
        permission_classes=[AllowAny]
        def post(self,request):
            try:
                int_dealer_id = request.data.get('pk_bint_id')
                str_remarks=request.data.get('strRemarks')

                ins_dealer = Dealer.objects.filter(pk_bint_id=int_dealer_id).update(int_is_act_del = -1)
                DealerLog.objects.create(vchr_remarks=str_remarks,vchr_status=3,fk_dealer_id=int_dealer_id,fk_created_id=request.user.id,dat_created=datetime.now())
                return Response({'status':1})

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
                return Response({'status':0,'reason':e})
