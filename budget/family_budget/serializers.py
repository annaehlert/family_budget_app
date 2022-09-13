from rest_framework import serializers, request
from .models import Budget, ExpenseTransaction, IncomeTransaction, Family
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import json


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

    def validate(self, value):
        username = value.get('username')
        password = value.get('password')
        email = value.get('email')
        if not username or not password or not email:
            raise serializers.ValidationError('Username, password and email cannot be empty.')
        return value


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
        name = json.loads(value.get('name'))
        family_name = self.instance.name if self.instance else None
        users = self.instance.users.all() if self.instance else None
        if not name:
            raise serializers.ValidationError('No name provided.')
        if not isinstance(name, str):
            raise serializers.ValidationError('Name should be text.')
        lower_name = name.lower()
        if Family.objects.filter(name__iexact=lower_name).exists() and not self.instance:
            raise serializers.ValidationError('This name already exists')
        elif lower_name == family_name and value.get('users') == list(users):
            raise serializers.ValidationError('This name already exists')
        value['name'] = lower_name
        return value


class BudgetSerializer(serializers.ModelSerializer):
    family_name = serializers.ReadOnlyField(source='family.name')
    owner = serializers.ReadOnlyField()

    class Meta:
        model = Budget
        fields = ['id', 'name', 'creation_date', 'last_update', 'family', 'family_name', 'users', 'owner']
        extra_kwargs = {
            'users': {'required': False}}

    def create(self, validated_data):
        user = self.context['request'].user
        user = User.objects.get(username=user)
        another_users = validated_data['users']
        another_users.append(user)
        budget = Budget(name=validated_data['name'], owner=user.username, family=validated_data['family'])
        budget.save()
        budget.users.set(another_users)
        return budget

    def validate(self, value):
        name = json.loads(value.get('name'))
        budget_name = self.instance.name if self.instance else None
        users = self.instance.users.all() if self.instance else None
        if not name:
            raise serializers.ValidationError('No name provided.')
        if not isinstance(name, str) and not isinstance(name, int):
            raise serializers.ValidationError('Name should be text or int.')
        if isinstance(name, str):
            lower_name = name.lower()
        else:
            lower_name = name
        if Family.objects.filter(name__iexact=lower_name).exists() and not self.instance:
            raise serializers.ValidationError('This name already exists')
        elif lower_name == budget_name and value.get('users') == list(users):
            raise serializers.ValidationError('This name already exists')
        value['name'] = lower_name
        return value


class BudgetDetailSerializer(serializers.ModelSerializer):
    family_name = serializers.ReadOnlyField(source='family.name')
    users = UserSerializer(many=True)

    class Meta:
        model = Budget
        fields = ['id', 'name', 'creation_date', 'last_update', 'family', 'family_name', 'owner', 'users']


class ExpenseTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseTransaction
        fields = ['id', 'amount', 'category', 'budget', 'creation_date']

    def create(self, validated_data):
        user = self.context['request'].user
        user = User.objects.get(username=user)
        expense = ExpenseTransaction(amount=validated_data['amount'], user=user, budget=validated_data['budget'], category=validated_data['category'])
        expense.save()
        return expense

    def validate(self, value):
        amount = int(value.get('amount'))
        if not amount:
            raise serializers.ValidationError('No amount provided.')
        if not isinstance(amount, int):
            raise serializers.ValidationError('Name should be int.')
        return value


class IncomeTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeTransaction
        fields = ['id', 'amount', 'category', 'budget', 'creation_date']

    def create(self, validated_data):
        user = self.context['request'].user
        user = User.objects.get(username=user)
        income = IncomeTransaction(amount=validated_data['amount'], user=user, budget=validated_data['budget'], category=validated_data['category'])
        income.save()
        return income

    def validate(self, value):
        amount = int(value.get('amount'))
        if not amount:
            raise serializers.ValidationError('No amount provided.')
        if not isinstance(amount, int):
            raise serializers.ValidationError('Name should be int.')
        return value


class BudgetListSerializer(serializers.ModelSerializer):
    income = IncomeTransactionSerializer(many=True, read_only=True)
    expense = ExpenseTransactionSerializer(many=True, read_only=True)
    family_name = serializers.ReadOnlyField(source='family.name')
    owner = serializers.ReadOnlyField()
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Budget
        fields = ['id', 'name', 'creation_date', 'last_update', 'owner', 'users', 'family', 'family_name', 'income', 'expense']


class UpdateBudgetListSerializer(serializers.ModelSerializer):
    income = IncomeTransactionSerializer(many=True, read_only=True)
    expense = ExpenseTransactionSerializer(many=True, read_only=True)
    family_name = serializers.ReadOnlyField(source='family.name')
    owner = serializers.ReadOnlyField()

    class Meta:
        model = Budget
        fields = ['id', 'creation_date', 'last_update', 'owner', 'users', 'family_name', 'income', 'expense']





