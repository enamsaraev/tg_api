from rest_framework import serializers
from django.shortcuts import get_object_or_404
from drf_writable_nested.serializers import WritableNestedModelSerializer

from dbcore.models import User, Expense, ExpenseCategory, ExpenseProperty


class BaseExpenseCategorySerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = ExpenseCategory
        fields = ('user_id', 'name', 'description')
        extra_kwargs = {
            'user_id': {'write_only': True}
        }


    def create(self, validated_data):
        user_id = validated_data.pop('user_id', None)
        inst = self.Meta.model(**validated_data)

        user = get_object_or_404(User, id=user_id)
        inst.user = user
        
        inst.save()
        return inst
    

class BaseExpenseCreationSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    expense_category_name = serializers.CharField(max_length=255)

    class Meta:
        model = Expense
        fields = ('user_id', 'expense_category_name', 'date', 'deleted')

    
    def create(self, validated_data):
        user_id = validated_data.pop('user_id', None)
        expense_category_name = validated_data.pop('expense_category_name', None)

        user = get_object_or_404(User, id=user_id)
        user_category = get_object_or_404(ExpenseCategory, user=user, name=expense_category_name)

        inst = self.Meta.model(**validated_data)
        inst.user = user
        inst.category  = user_category
        inst.save()
    
        return inst
    

class BaseExpensePropertySerializer(serializers.ModelSerializer):
    expense_id = serializers.IntegerField()

    class Meta:
        model = ExpenseProperty
        fields = ('name', 'expense', 'description', 'raw_string', 'expense_id')

    def create(self, validated_data):
        expense_id = validated_data.pop('expense_id', None)
        expense_inst = Expense.objects.get(id=expense_id)

        inst = self.Meta.model(**validated_data)
        inst.expense_obj = expense_inst
        inst.save()

        return inst


class GetExpensesInfoSerializer(serializers.ModelSerializer):
    expense_date = serializers.StringRelatedField(source='expense_obj.date')
    expense_category = serializers.StringRelatedField(source='expense_obj.category.name')

    class Meta:
        model = ExpenseProperty
        fields = ('expense_date', 'expense_category', 'name', 'expense', 'description')
