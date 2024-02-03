from django import forms
from .models import Category, Transaction
from django.forms.widgets import SelectDateWidget

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'operation_type', 'amount', 'date', 'description']

    widgets = {
        'date': forms.SelectDateWidget(empty_label=("Year", "Month", "Day"), attrs={'class': 'date-select'}),
    }

#report_generator
class ReportGeneratorForm(forms.Form):
    date_from = forms.DateField(
        label='Дата з',
        widget=forms.DateInput(attrs={'type': 'date', 'id': 'id_date_from'}),
        input_formats=['%Y-%m-%d'], 
    )
    date_to = forms.DateField(
        label='Дата до',
        widget=forms.DateInput(attrs={'type': 'date', 'id': 'id_date_to'}),
        input_formats=['%Y-%m-%d'],  
    )
    operation_type = forms.ChoiceField(
        label='Тип операції',
        choices=Transaction.OPERATION_TYPE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'id': 'id_operation_type'})
    )
    category = forms.ModelChoiceField(
        label='Категорія',
        queryset=Category.objects.all(),
        required=False,
        widget=forms.Select(attrs={'id_category': 'category'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['date_from'].widget = forms.DateInput(attrs={'type': 'date', 'class': 'date-select'})
        self.fields['date_to'].widget = forms.DateInput(attrs={'type': 'date', 'class': 'date-select'})