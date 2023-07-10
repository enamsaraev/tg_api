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
    category_name = serializers.CharField(max_length=255)

    class Meta:
        model = Expense
        fields = ('user_id', 'category_name', 'date', 'deleted')

    
    def create(self, validated_data):
        user_id = validated_data.pop('user_id', None)
        category_name = validated_data.pop('category_name', None)

        user = get_object_or_404(User, id=user_id)
        user_category = get_object_or_404(ExpenseCategory, user=user, name=category_name)

        inst = self.Meta.model(**validated_data)
        inst.user = user
        inst.category  = user_category
        inst.save()
    
        return inst