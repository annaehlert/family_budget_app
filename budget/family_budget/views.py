from rest_framework import generics, status
from .models import Budget, BudgetShare, IncomeTransaction, ExpenseTransaction, Family
from django.contrib.auth.models import User
from .serializers import UserSerializer, BudgetSerializer, BudgetShareSerializer, \
    ExpenseTransactionSerializer, IncomeTransactionSerializer, BudgetListSerializer, FamilySerializer, \
    FamilyCreateSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsOwnerOrReadOnly


# GET list of all users
class UsersList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


# POST creation of user
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )


# GET list of all families
class FamiliesList(generics.ListAPIView):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer_class):
        serializer_class.save(users=self.request.user)


# POST creation of user
class FamilyCreate(generics.CreateAPIView):
    queryset = Family.objects.all()
    serializer_class = FamilyCreateSerializer
    permission_classes = [IsAuthenticated]


# GET, PUT and DELETE on specific family
class FamilyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Family.objects.all()
    serializer_class = FamilyCreateSerializer
    permission_classes = [IsAuthenticated]


# GET, PUT and DELETE on specific user
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


# GET and POST for budget
class BudgetList(generics.ListAPIView, generics.CreateAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


# POST for budget creation
class BudgetCreate(generics.CreateAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]


# GET, PUT, DELETE for specific budget
class UserBudgetList(generics.RetrieveUpdateDestroyAPIView):
    queryset = Budget
    serializer_class = BudgetListSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


# GET and POST for income data
class IncomeTransactionList(generics.CreateAPIView):
    queryset = IncomeTransaction.objects.all()
    serializer_class = IncomeTransactionSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]








