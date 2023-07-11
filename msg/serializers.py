from rest_framework import serializers
from django.shortcuts import get_object_or_404

from dbcore.models import User, Expense, ExpenseCategory, ExpenseCategoryProperty


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
    

class BaseExpenseCategoryPropertySerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    expense_category_name = serializers.CharField()
    expense_id = serializers.IntegerField()

    class Meta:
        model = ExpenseCategoryProperty
        fields = ('user_id', 'expense_category_name', 'name', 'expense', 'description', 'raw_string', 'expense_id')

    def create(self, validated_data):
        expense_category_name = validated_data.pop('expense_category_name', None)
        user_id = validated_data.pop('user_id', None)
        expense_category = ExpenseCategory.objects.get(user__id=user_id,  name=expense_category_name)

        inst = self.Meta.model(**validated_data)
        inst.category = expense_category
        inst.save()

        return inst
    


