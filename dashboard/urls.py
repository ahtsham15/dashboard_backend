"""
URL configuration for dashboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from myfinance.views import UserList,LoginView,IncomeList,IncomeDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', UserList.as_view(), name='user-list'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/incomes/', IncomeList.as_view(), name='income-list'),
    path('api/incomes/<int:pk>/', IncomeDetail.as_view(), name='income-detail')
]
