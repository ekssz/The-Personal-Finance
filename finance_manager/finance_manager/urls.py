"""
URL configuration for finance_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from expenses.views import CategoryListView, add_category, edit_category, edit_transaction

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', CategoryListView.as_view(), name='home'),
    path('add_category/', add_category, name='add_category'),
    path('edit_category/<int:category_id>/', edit_category, name='edit_category'),
    path('edit_transaction/<int:transaction_id>/', edit_transaction, name='edit_transaction'),
]

urlpatterns += [
    path('expenses/', include('expenses.urls')),
]
