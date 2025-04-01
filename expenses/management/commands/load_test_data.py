from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from expenses.models import Category, Expense
from decimal import Decimal
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Loads test data for the expense tracker'

    def handle(self, *args, **kwargs):
        # Create test categories
        categories = [
            {'name': 'Food & Dining', 'description': 'Groceries, restaurants, and takeout'},
            {'name': 'Transportation', 'description': 'Gas, public transport, and car maintenance'},
            {'name': 'Housing', 'description': 'Rent, utilities, and home maintenance'},
            {'name': 'Entertainment', 'description': 'Movies, games, and leisure activities'},
            {'name': 'Healthcare', 'description': 'Medical expenses and prescriptions'},
            {'name': 'Shopping', 'description': 'Clothing, electronics, and other purchases'},
        ]

        for category_data in categories:
            Category.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )

        # Get or create test user
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'is_staff': True
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created test user'))

        # Create test expenses
        categories = Category.objects.all()
        descriptions = [
            'Grocery shopping', 'Movie tickets', 'Gas refill', 'Restaurant dinner',
            'Utility bill', 'Online shopping', 'Doctor visit', 'Public transport',
            'Home maintenance', 'Entertainment subscription'
        ]

        # Create expenses for the last 30 days
        for i in range(30):
            date = datetime.now().date() - timedelta(days=i)
            num_expenses = random.randint(1, 3)  # 1-3 expenses per day

            for _ in range(num_expenses):
                Expense.objects.create(
                    user=user,
                    category=random.choice(categories),
                    amount=Decimal(random.uniform(10, 500)).quantize(Decimal('0.01')),
                    description=random.choice(descriptions),
                    date=date
                )

        self.stdout.write(self.style.SUCCESS('Successfully loaded test data')) 