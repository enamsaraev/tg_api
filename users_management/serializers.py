from rest_framework import serializers

from dbcore.models import User


class BaseUserSerializer(serializers.ModelSerializer):
    """Appears a base user model"""

    class Meta:
        model = User
        fields = ('id', 'email', 'chat_id', 'password',)
        extra_kwargs = {
           'password': {'write_only': True} 
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        inst = self.Meta.model(**validated_data)

        if password:
            inst.set_password(password)
        
        inst.save()
        return inst
    

class BaseUserLoginSerializer(serializers.Serializer):
    """User serializer for login"""
    
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
        