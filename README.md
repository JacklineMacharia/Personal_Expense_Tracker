# Personal Expense Tracker

A web-based expense tracking application built with Django that helps users manage and analyze their personal expenses.

## Features

- User Authentication (Register, Login, Logout)
- Dashboard with expense statistics and visualizations
  - Total expenses overview
  - Monthly spending trends
  - Category-wise expense distribution
  - Recent transactions
- Expense Management
  - Add, edit, and delete expenses
  - Categorize expenses
  - Date-based tracking
- Responsive Design
  - Works on desktop and mobile devices
  - Clean and intuitive interface

## Technology Stack

- Backend: Django 4.2.7
- Database: PostgreSQL
- Frontend: 
  - Django Templates
  - Bootstrap 5
  - Chart.js for visualizations
  - Font Awesome icons
- API: Django Rest Framework

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/JacklineMacharia/Personal_Expense_Tracker.git
   cd Personal_Expense_Tracker
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the database in `settings.py`

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Visit http://127.0.0.1:8000/ in your browser

## Project Structure

```
expense_tracker/
├── expense_tracker/      # Project settings
├── expenses/            # Main application
├── static/             # Static files (CSS, JS, Images)
├── templates/          # HTML templates
│   ├── base.html      # Base template
│   ├── dashboard.html # Dashboard template
│   └── expenses/      # Expense management templates
└── requirements.txt    # Project dependencies
```

## Features in Detail

### Dashboard
- Total expense overview
- Monthly spending trends chart
- Category distribution pie chart
- Recent transactions list
- Top spending categories

### Expense Management
- Add new expenses with category and description
- Edit existing expenses
- Delete expenses
- View all expenses in a paginated list

### User Interface
- Responsive Bootstrap design
- Interactive charts and graphs
- User-friendly forms
- Clean and modern layout

## API Endpoints

The application provides REST API endpoints for:
- Expense CRUD operations
- Category management
- Expense statistics

## Future Enhancements

- Budget planning and tracking
- Export expenses to CSV/PDF
- Income tracking
- Financial goals
- Email notifications
- Advanced filtering and search
- Multi-currency support

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License. 