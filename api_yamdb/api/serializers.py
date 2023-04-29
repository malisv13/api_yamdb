from rest_framework.serializers import ModelSerializer, CharField

from user.models import User


class ModeratorOrAdminSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'bio', 'role')
        read_only_fields = ('role',)


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class SignUpSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')


class TokenSerializer(ModelSerializer):
    username = CharField(
        required=True)
    confirmation_code = CharField(
        required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )
