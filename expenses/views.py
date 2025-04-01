from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta
from .models import Category, Expense
from .serializers import CategorySerializer, ExpenseSerializer
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

# Template Views
def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    # Get user's expenses
    expenses = Expense.objects.filter(user=request.user)
    
    # Calculate statistics
    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
    monthly_expenses = expenses.filter(
        date__year=datetime.now().year,
        date__month=datetime.now().month
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Get recent expenses
    recent_expenses = expenses.order_by('-date')[:5]
    
    # Get expenses by category for chart
    category_data = expenses.values('category__name').annotate(total=Sum('amount'))
    category_labels = [item['category__name'] for item in category_data]
    category_amounts = [float(item['total']) for item in category_data]
    
    # Get monthly trend data
    monthly_data = expenses.annotate(
        month=TruncMonth('date')
    ).values('month').annotate(total=Sum('amount')).order_by('month')
    
    monthly_labels = [item['month'].strftime('%B %Y') for item in monthly_data]
    monthly_amounts = [float(item['total']) for item in monthly_data]
    
    context = {
        'total_expenses': total_expenses,
        'monthly_expenses': monthly_expenses,
        'total_categories': Category.objects.count(),
        'total_transactions': expenses.count(),
        'recent_expenses': recent_expenses,
        'category_labels': category_labels,
        'category_data': category_amounts,
        'monthly_labels': monthly_labels,
        'monthly_data': monthly_amounts,
    }
    return render(request, 'dashboard.html', context)

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})

@login_required
def expense_create(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date = request.POST.get('date')
        
        category = get_object_or_404(Category, id=category_id)
        Expense.objects.create(
            user=request.user,
            category=category,
            amount=amount,
            description=description,
            date=date
        )
        messages.success(request, 'Expense added successfully!')
        return redirect('expense_list')
    
    categories = Category.objects.all()
    return render(request, 'expenses/expense_form.html', {'categories': categories})

@login_required
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        category_id = request.POST.get('category')
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date = request.POST.get('date')
        
        category = get_object_or_404(Category, id=category_id)
        expense.category = category
        expense.amount = amount
        expense.description = description
        expense.date = date
        expense.save()
        
        messages.success(request, 'Expense updated successfully!')
        return redirect('expense_list')
    
    categories = Category.objects.all()
    return render(request, 'expenses/expense_form.html', {
        'expense': expense,
        'categories': categories
    })

@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully!')
        return redirect('expense_list')
    return render(request, 'expenses/expense_confirm_delete.html', {'expense': expense})

# Authentication Views
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')

# API Views
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def total_expenses(self, request):
        total = self.get_queryset().aggregate(total=Sum('amount'))['total'] or 0
        return Response({'total': total})

    @action(detail=False, methods=['get'])
    def expenses_by_category(self, request):
        expenses = self.get_queryset().values('category__name').annotate(total=Sum('amount'))
        return Response(expenses)
