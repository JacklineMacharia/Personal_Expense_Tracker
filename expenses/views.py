from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from .models import Category, Expense
from .serializers import CategorySerializer, ExpenseSerializer

# Create your views here.

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
