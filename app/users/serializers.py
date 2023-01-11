from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    user_model = get_user_model()

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def validate_password(self, password: str):
        password_validation.validate_password(password, self.instance)
        return password

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = self.user_model(**validated_data)
        user.set_password(password)
        user.save()
        return user
