from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.exceptions import APIException

from django.shortcuts import get_object_or_404

from dbcore.models import User, Expense, ExpenseCategory, ExpenseCategoryProperty
from msg.serializers import BaseExpenseCategorySerializer, BaseExpenseCreationSerializer


class GetUserExpenseCategories(APIView):
    def get(self, request):
        categories = ExpenseCategory.objects.filter(user__id=request.data['id'])
        ser = BaseExpenseCategorySerializer(categories, many=True)

        return Response(ser.data)
    

class CreateNewUserExpenseCategory(APIView):
    def post(self, request):
        ser_create_category = BaseExpenseCategorySerializer(data=request.data)
        ser_create_category.is_valid(raise_exception=True)
        new_category = ser_create_category.save()

        category = ExpenseCategory.objects.get(user__id=request.data['user_id'], id=new_category.id)
        ser_get_categories = BaseExpenseCategorySerializer(category)

        return Response(ser_get_categories.data)
    

class CreateNewExpense(APIView):
    def post(self, request):
        print(request.data)
        ser = BaseExpenseCreationSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()

        return Response(status=status.HTTP_201_CREATED)