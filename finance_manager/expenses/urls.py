from django.urls import path
from .views import CategoryListView, add_category, edit_category, TransactionListView, add_transaction, edit_transaction, delete_category, delete_transaction, ConfirmModalView, ConfirmCategoryView, ReportGeneratorView, report_template, generate_report_data
from . import views
urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('add_category/', add_category, name='add_category'),
    path('edit_category/<int:category_id>/', edit_category, name='edit_category'),
    path('delete_category/<int:category_id>/', delete_category, name='delete_category'),
    path('transactions/', TransactionListView.as_view(), name='transactions'),
    path('add_transaction/', add_transaction, name='add_transaction'),
    path('edit_transaction/<int:transaction_id>/', edit_transaction, name='edit_transaction'),
    path('delete_transaction/<int:transaction_id>/', delete_transaction, name='delete_transaction'),
    path('confirm_del_transactions/<int:transaction_id>/', ConfirmModalView.as_view(), name='confirm_del_transactions'),
    path('confirm_del_category/<int:category_id>/', ConfirmCategoryView.as_view(), name='confirm_del_category'),
    path('report_generator/', ReportGeneratorView.as_view(), name='report_generator'),
    path('expenses/report_template/<str:date_from>/<str:date_to>/<str:operation_type>/<int:category>/', views.report_template, name='report_template'),
    path('generate_report_data/', generate_report_data, name='generate_report_data'),
]
