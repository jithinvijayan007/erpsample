from django.shortcuts import render
from django.views import generic
from rest_framework import generics
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework.response import Response
from user_app.models import UserModel
from customer_app.models import CustomerModel
from customer_rating.models import CustomerRating
from django.views.generic import View,TemplateView,CreateView
from rest_framework.views import APIView

# Create your views here.

class CustomerRatingView(APIView):
    def post(self,request):
        try:
            dct_rating = request.data.get('customerRating')
            vchr_feedback = dct_rating['vchr_feedback']
            dbl_rating = dct_rating['dbl_rating']
            fk_customer = dct_rating['fk_customer_id']
            fk_user = dct_rating['fk_user_id']
            ins_rating =  CustomerRating(vchr_feedback = vchr_feedback, dbl_rating = dbl_rating,fk_customer = CustomerModel.objects.get(id= fk_customer), fk_user = UserModel.objects.get(user_ptr_id = fk_user))
            ins_rating.save()
            return JsonResponse({'status':'successfully created'})

        except Exception as e:
            return JsonResponse({'status':'failed','reason':e})
