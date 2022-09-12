from rest_framework import serializers, request
from .models import Budget, BudgetShare, ExpenseTransaction, IncomeTransaction, Family
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        user = User(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user

    def validate_email(self, value):
        lower_email = value.lower()
        if User.objects.filter(username__iexact=lower_email).exists():
            raise serializers.ValidationError('This email already exists')
        return lower_email


class FamilySerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)

    class Meta:
        model = Family
        fields = ['id', 'name', 'creation_date', 'users']
        extra_kwargs = {
            'users': {'required': False}}


class FamilyCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Family
        fields = ['id', 'name', 'creation_date', 'users']
        extra_kwargs = {
            'users': {'required': False}}

    def create(self, validated_data):
        user_username = self.context['request'].user
        user = User.objects.get(username=user_username)
        another_users = validated_data['users']
        another_users.append(user)
        family = Family(name=validated_data['name'])
        family.save()
        family.users.set(another_users)
        return family

    def validate(self, value):
        name = value.get('name')
        family_name = self.instance.name if self.instance else None
        users = self.instance.users.all() if self.instance else None
        if name:
            lower_name = name.lower()
            if Family.objects.filter(name__iexact=lower_name).exists() and not self.instance:
                raise serializers.ValidationError('This name already exists')
            elif lower_name == family_name and value.get('users') == list(users):
                raise serializers.ValidationError('This name already exists')
            value['name'] = lower_name
            return value


class BudgetSerializer(serializers.ModelSerializer):
    family_name = serializers.ReadOnlyField(source='family.name')

    class Meta:
        model = Budget
        fields = ['id', 'name', 'creation_date', 'last_update', 'family', 'family_name']

    def create(self, validated_data):
        user = self.context['request'].user
        user = User.objects.get(username=user)
        budget = Budget(name=validated_data['name'], user=user, family=validated_data['family'])
        budget.save()
        return budget


class BudgetDetailSerializer(serializers.ModelSerializer):
    family_name = serializers.ReadOnlyField(source='family.name')
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Budget
        fields = ['id', 'name', 'creation_date', 'last_update', 'family', 'family_name', 'user', 'username']


class ExpenseTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseTransaction
        fields = ['id', 'amount', 'category', 'budget', 'creation_date']


class IncomeTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeTransaction
        fields = ['id', 'amount', 'category', 'budget', 'creation_date']


class BudgetShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetShare
        fields = ['id', 'budget', 'user']


class BudgetListSerializer(serializers.ModelSerializer):
    income = IncomeTransactionSerializer(many=True, read_only=True)
    expense = ExpenseTransactionSerializer(many=True, read_only=True)
    family_name = serializers.ReadOnlyField(source='family.name')
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Budget
        fields = ['id', 'name', 'creation_date', 'last_update', 'username', 'family', 'family_name', 'income', 'expense']






