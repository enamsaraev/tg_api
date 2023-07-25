from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.exceptions import APIException
from django.db.models import Count

from dbcore.models import Expense, ExpenseCategory, ExpenseProperty
from msg.serializers import (
    BaseExpenseCategorySerializer, BaseExpenseCreationSerializer, 
    BaseExpensePropertySerializer, GetExpensesInfoSerializer
)
from msg.helpers import ExpenseCreationHelper


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
        ser = BaseExpenseCreationSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()

        return Response(status=status.HTTP_201_CREATED)
    

class CreateNewExpenseProps(APIView):
    def post(self, request):
        ser = BaseExpensePropertySerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()

        return Response(status=status.HTTP_201_CREATED)


class CreateFullExpense(APIView):
    def post(self, request):
        helper = ExpenseCreationHelper(data=request.data)()
        if not helper:
            raise APIException('Invalid data!')
        
        return Response(status=status.HTTP_201_CREATED)
    

class GetUserExpenseCategories(APIView):
    def get(self, request):
        categories = ExpenseCategory.objects.filter(user__id=request.data['id'])
        ser = BaseExpenseCategorySerializer(categories, many=True)

        return Response(ser.data)
    

class GetAllUserExpenses(APIView):
    def get(self, request):
        all_user_expenses = ExpenseProperty.objects.filter(expense_obj__user__id=request.data['user_id']).select_related('expense_obj').prefetch_related('expense_obj__category')
        ser = GetExpensesInfoSerializer(all_user_expenses, many=True)
        
        return Response(ser.data)