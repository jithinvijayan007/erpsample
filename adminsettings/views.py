from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from adminsettings.models import AdminSettings

class SaveAdminSettings(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            """ To update adminsettings details
                parameter:Admin setting values and status
                return success response
                """
            # import pdb; pdb.set_trace()
            if not request.data:
                return Response({"status":"0","message":"No admin settings data not found"})
            dct_data = request.data
            for str_code in dct_data:
                lst_value = []
                if not type(str_code['vchr_value']) is list:
                    lst_value.append(str_code['vchr_value'])
                else:
                    lst_value = str_code['vchr_value']
                ins_admin_settings = AdminSettings.objects.filter(vchr_code = str_code['vchr_code'],fk_company = request.user.userdetails.fk_company).update(
                                vchr_value = lst_value,
                                bln_enabled = str_code['bln_enabled']
                )
            return JsonResponse({"status": "success","message":"successfully saved"})
        except Exception as e:
            return JsonResponse({'status':'failed','reason':str(e)})

    def get(self, request,):
        try:
            # import pdb; pdb.set_trace()
            lst_data = list(AdminSettings.objects.filter(fk_company_id = request.user.userdetails.fk_company_id).values('pk_bint_id','vchr_name','vchr_value','bln_enabled','vchr_code').order_by('pk_bint_id'))
            return JsonResponse({'status':'success','data':lst_data})
        except Exception as e:
            return JsonResponse({'status':'failed','reason':str(e)})
