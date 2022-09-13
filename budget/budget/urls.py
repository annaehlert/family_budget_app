"""budget URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from family_budget import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # USER
    path('api/users', views.UsersList.as_view(), name='users_list'),
    path('api/user/create', views.UserCreate.as_view(), name='user_create'),
    path('api/user/<pk>', views.UserDetail.as_view(), name='user_details'),
    # FAMILY
    path('api/families', views.FamiliesList.as_view(), name='families_list'),
    path('api/family/create', views.FamilyCreate.as_view(), name='family_create'),
    path('api/family/<pk>', views.FamilyDetail.as_view(), name='family_details'),
    # BUDGET
    path('api/budget/<pk>', views.UserBudgetList.as_view(), name='budget_details'),
    path('api/budget', views.BudgetCreate.as_view(), name='budget_create'),
    path('api/budgets', views.BudgetList.as_view(), name='budgets_list'),
    path('api/budget/<pk>/income', views.SpecificBudgetIncomeList.as_view(), name='income-budget'),
    path('api/budget/<pk>/expense', views.SpecificBudgetExpenseList.as_view(), name='expense-budget'),
    path('api/budget/<pk>/update', views.UpdateBudgetListUser.as_view(), name='update-budget'),
    # INCOME
    path('api/income_transaction', views.IncomeTransactionList.as_view(), name='income_create'),
    # EXPENSE
    path('api/expense_transaction', views.ExpenseTransactionList.as_view(), name='expense_create'),

    path('api-auth/', include('rest_framework.urls')),

]
