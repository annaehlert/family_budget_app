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
    path('api/users', views.UsersList.as_view()),
    path('api/user/create', views.UserCreate.as_view()),
    path('api/user/<pk>', views.UserDetail.as_view()),
    # FAMILY
    path('api/families', views.FamiliesList.as_view()),
    path('api/family/create', views.FamilyCreate.as_view()),
    path('api/family/<pk>', views.FamilyDetail.as_view()),
    # BUDGET
    path('api/budget/<pk>', views.UserBudgetList.as_view()),
    path('api/budget', views.BudgetCreate.as_view()),
    path('api/budgets', views.BudgetList.as_view()),
    # INCOME
    path('api/income_transaction', views.IncomeTransactionList.as_view()),
    # EXPENSE
    path('api/expense_transaction', views.ExpenseTransactionList.as_view()),

    path('api-auth/', include('rest_framework.urls')),

]
