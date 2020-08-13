from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(username=attrs['email'], password=attrs['password'])

        if not user:
            raise serializers.ValidationError('Incorrect email or password.')

        if not user.is_active:
            raise serializers.ValidationError('User is disabled.')

        return {'user': user}



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'is_active',
            'joined_at',
            'password',
            'is_superuser',
            'last_login'
        )
        read_only_fields = ('is_active', 'joined_at')
        extra_kwargs = {
            'password': {
                'required': True,
                'write_only': True
            },
            'name': {
                'required': True
            }
        }

    @staticmethod
    def validate_email(value):
        return validate_username(value)

    def create(self, validated_data):
        return User.objects.create_user(
            validated_data.pop('email'),
            validated_data.pop('password'),
            **validated_data
        )



def validate_username(username):
    if User.objects.filter(**{'{}__iexact'.format(User.USERNAME_FIELD): username}).exists():
        raise ValidationError('User with this {} already exists'.format(User.USERNAME_FIELD))
    return username
