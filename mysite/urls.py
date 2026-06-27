"""
URL configuration for mysite project.

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
from banksystem.views import signin,dashboard,signup,logout,deposit,withdrawal,term,loan,check_value,loan_rate
from banksystem.views import loan_rate1,final_emi,cut_emi,display_emi
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',signin),
    path('dashboard/',dashboard),
    path('signup/',signup),
    path('logout/',logout),
    path('deposit/',deposit),
    path('withdrawal/',withdrawal),
    path('term/',term),
    path('loan/',loan),
    path('check_value/',check_value),
    path('loan_rate/',loan_rate,name="loan_rate"),
    path('loan_rate1/',loan_rate1),
    path('final_emi/',final_emi),
    path('cut_emi/',cut_emi),
    path('display_emi/',display_emi)
    
]
