from django.contrib import admin
from django.urls import path
from myfinance.views.userView import UserList, LoginView
from myfinance.views.incomeView import IncomeList, IncomeDetail
from myfinance.views.savingView import SavingList, SavingDetail
from myfinance.views.expenseView import ExpenseList,ExpenseDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', UserList.as_view(), name='user-list'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/incomes/', IncomeList.as_view(), name='income-list'),
    path('api/incomes/<int:pk>/', IncomeDetail.as_view(), name='income-detail'),
    path('api/savings/', SavingList.as_view(), name='saving-list'),
    path('api/savings/<int:pk>/', SavingDetail.as_view(), name='saving-detail'),
    path('api/expenses/', ExpenseList.as_view(), name='expense-list'),
    path('api/expenses/<int:pk>/', ExpenseDetail.as_view(), name='expense-detail')
]
