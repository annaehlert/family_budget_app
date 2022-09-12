from rest_framework import generics, status
from .models import Budget, IncomeTransaction, ExpenseTransaction, Family
from django.contrib.auth.models import User
from .serializers import UserSerializer, BudgetSerializer, \
    ExpenseTransactionSerializer, IncomeTransactionSerializer, BudgetListSerializer, FamilySerializer, \
    FamilyCreateSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsOwnerOrReadOnly, IsOwnerOrReadOnlyForBudget
import django_filters.rest_framework
from django_filters.rest_framework import DjangoFilterBackend


# GET list of all users
class UsersList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]


# POST creation of owner
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )


# GET, PUT and DELETE on specific owner
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]


# GET list of all families
class FamiliesList(generics.ListAPIView):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    # def perform_create(self, serializer_class):
    #     serializer_class.save(users=self.request.owner)


# POST creation of family object
class FamilyCreate(generics.CreateAPIView):
    queryset = Family.objects.all()
    serializer_class = FamilyCreateSerializer
    permission_classes = [IsAuthenticated]


# GET, PUT and DELETE on specific family
class FamilyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Family.objects.all()
    serializer_class = FamilyCreateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]


# GET for all budgets
class BudgetList(generics.ListAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    def get_queryset(self):
        queryset = Budget.objects.all()
        username = self.request.user
        if IsAdminUser:
            return queryset
        elif username is not None:
            queryset = queryset.filter(owner__username=username)
            return queryset
        else:
            return None


# POST for budget creation
class BudgetCreate(generics.CreateAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]


# GET, PUT, DELETE for specific budget
class UserBudgetList(generics.RetrieveUpdateDestroyAPIView):
    queryset = Budget
    serializer_class = BudgetListSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyForBudget]
    filter_backends = [DjangoFilterBackend]


# GET and POST for income data
class IncomeTransactionList(generics.CreateAPIView):
    queryset = IncomeTransaction.objects.all()
    serializer_class = IncomeTransactionSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]


# GET and POST for expense data
class ExpenseTransactionList(generics.CreateAPIView):
    queryset = ExpenseTransaction.objects.all()
    serializer_class = ExpenseTransactionSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]





