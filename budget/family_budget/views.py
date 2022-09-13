from rest_framework import generics, status
from .models import Budget, IncomeTransaction, ExpenseTransaction, Family
from django.contrib.auth.models import User
from .serializers import UserSerializer, BudgetSerializer, \
    ExpenseTransactionSerializer, IncomeTransactionSerializer, BudgetListSerializer, FamilySerializer, \
    FamilyCreateSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsOwnerOrReadOnly, IsOwnerOrReadOnlyForBudget
from django_filters.rest_framework import DjangoFilterBackend


# GET list of all users
class UsersList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [DjangoFilterBackend]


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
    filter_backends = [DjangoFilterBackend]


# GET list of all families
class FamiliesList(generics.ListAPIView):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [DjangoFilterBackend]


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
    filter_backends = [DjangoFilterBackend]


# GET for all budgets
class BudgetList(generics.ListAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        queryset = Budget.objects.all()
        user = self.request.user
        if self.request.user.is_staff:
            return queryset
        elif user:
            queryset = queryset.filter(users__id__in=[user.id])
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


# POST for income data
class IncomeTransactionList(generics.CreateAPIView):
    queryset = IncomeTransaction.objects.all()
    serializer_class = IncomeTransactionSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]


# POST for expense data
class ExpenseTransactionList(generics.CreateAPIView):
    queryset = ExpenseTransaction.objects.all()
    serializer_class = ExpenseTransactionSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


# GET specific budget income list
class SpecificBudgetIncomeList(generics.ListAPIView):
    queryset = Budget
    serializer_class = IncomeTransactionSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyForBudget]
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        queryset = IncomeTransaction.objects.all()
        budget_id = self.kwargs['pk']
        queryset = queryset.filter(budget_id=budget_id)
        if queryset:
            category = self.request.query_params.get('category')
            if category:
                queryset = queryset.filter(category=category)
            return queryset
        else:
            return None


# GET specific budget income list
class SpecificBudgetExpenseList(generics.ListAPIView):
    queryset = Budget
    serializer_class = IncomeTransactionSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyForBudget]
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        queryset = ExpenseTransaction.objects.all()
        budget_id = self.kwargs['pk']
        queryset = queryset.filter(budget_id=budget_id)
        if queryset:
            category = self.request.query_params.get('category')
            if category:
                queryset = queryset.filter(category=category)
            return queryset
        else:
            return None
