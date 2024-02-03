from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, View
from django.db.models import Sum
from .models import Category, Transaction
from .forms import CategoryForm, TransactionForm, ReportGeneratorForm
from django.http import JsonResponse

class CategoryListView(ListView):
    model = Category
    template_name = 'expenses/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(is_deleted=False)

class TransactionListView(ListView):
    model = Transaction
    template_name = 'expenses/transactions.html'
    context_object_name = 'transactions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReportGeneratorForm()
        return context

class ConfirmModalView(View):
    template_name = 'expenses/confirm_del_transactions.html'

    def get(self, request, *args, **kwargs):
        transaction_id = kwargs.get('transaction_id')
        transaction = get_object_or_404(Transaction, id=transaction_id)
        context = {'transaction': transaction}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        transaction_id = kwargs.get('transaction_id')
        transaction = get_object_or_404(Transaction, id=transaction_id)
        transaction.delete()
        return redirect('transactions')

class ConfirmCategoryView(View):
    template_name = 'expenses/confirm_del_category.html'

    def get(self, request, *args, **kwargs):
        category_id = kwargs.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        context = {'category': category}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        category_id = kwargs.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        category.delete()
        return redirect('category_list')

# edit & add
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()

    return render(request, 'expenses/add_category.html', {'form': form})

def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'expenses/edit_category.html', {'form': form, 'category': category})

def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transactions')
    else:
        form = TransactionForm()

    return render(request, 'expenses/add_transaction.html', {'form': form})

def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transactions')
    else:
        form = TransactionForm(instance=transaction)

    return render(request, 'expenses/edit_transaction.html', {'form': form, 'transaction': transaction})

# delete
def delete_category(request, category_id):
    if request.method == 'POST':
        try:
            category = get_object_or_404(Category, id=category_id)
            category.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Невірний метод запиту'})

def delete_transaction(request, transaction_id):
    if request.method == 'POST':
        try:
            transaction = get_object_or_404(Transaction, id=transaction_id)
            transaction.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Невірний метод запиту'})

def generate_report_data(request):
    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        operation_type = request.POST.get('operation_type')
        category_id = request.POST.get('category')

        try:
            transactions = Transaction.objects.filter(
                date__range=[date_from, date_to],
                operation_type=operation_type,
            )

            if category_id:
                transactions = transactions.filter(category_id=category_id)

            chart_data = []
            for transaction in transactions:
                chart_data.append({
                    'name': transaction.name,
                    'y': transaction.amount
                })

            return JsonResponse({'success': True, 'chart_data': chart_data})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'error': 'Invalid request method'})

class ReportGeneratorView(View):
    template_name = 'expenses/report_generator.html'

    def get(self, request, *args, **kwargs):
        form = ReportGeneratorForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ReportGeneratorForm(request.POST)
        if form.is_valid():
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            operation_type = form.cleaned_data['operation_type']
            category = form.cleaned_data['category']

            transactions = Transaction.objects.filter(
                date__range=[date_from, date_to],
                operation_type=operation_type,
            )

            if category:
                transactions = transactions.filter(category=category)

            total_amount = transactions.aggregate(Sum('amount'))['amount__sum']

            context = {
                'form': form,
                'date_from': date_from,
                'date_to': date_to,
                'operation_type': operation_type,
                'category': category.id if category else None,
                'transactions': transactions,
                'total_amount': total_amount,
            }

            return render(request, 'expenses/report_template.html', context)

        context = {
            'form': form,
        }
        return render(request, self.template_name, context)



class ReportGeneratorForm(forms.Form):
    date_from = forms.DateField(label='Дата з', widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(label='Дата до', widget=forms.DateInput(attrs={'type': 'date'}))
    operation_type = forms.ChoiceField(label='Тип операції', choices=Transaction.OPERATION_TYPE_CHOICES, required=False)
    category = forms.ModelChoiceField(label='Категорія', queryset=Category.objects.all(), required=False)


def report_generator(request):
    if request.method == 'POST':
        form = ReportGeneratorForm(request.POST)
        if form.is_valid():
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            operation_type = form.cleaned_data['operation_type']
            category = form.cleaned_data['category']

            categories = Category.objects.all()

            transactions = Transaction.objects.filter(
                date__range=[date_from, date_to],
                operation_type=operation_type,
            )

            if category:
                transactions = transactions.filter(category=category)

            context = {
                'form': form,
                'date_from': date_from,
                'date_to': date_to,
                'operation_type': operation_type,
                'category': category,
                'categories': categories,
                'transactions': transactions,
            }

    return render(request, 'expenses/report_generator.html')    
    
def report_template(request, date_from, date_to, operation_type, category_id, total_amount):
    context = {
        'date_from': date_from,
        'date_to': date_to,
        'operation_type': operation_type,
        'category_id': category_id,
        'total_amount': total_amount,
    }

    if request.method == 'POST':
        form = ReportGeneratorForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = ReportGeneratorForm()

    context['form'] = form
    context['category_id'] = category_id if category_id != 'None' else None

    transactions = Transaction.objects.filter(
        date__range=[date_from, date_to],
        operation_type=operation_type,
    )
    context['transactions'] = transactions

    return render(request, 'expenses/report_template.html', context)


def chart_data(request):
    data = [
        {'name': 'Категорія 1', 'y': 100},
        {'name': 'Категорія 2', 'y': 200},
    ]
    
    return JsonResponse(data, safe=False)