# AnytimeEsim - Django eSIM Store

A complete Django-based eSIM store website with filtering, search, and admin panel functionality.

## Features

- **Responsive Design**: Mobile-friendly interface with orange theme
- **eSIM Plan Management**: Full CRUD operations for eSIM plans
- **Country Filtering**: Browse plans by country
- **Price Filtering**: Filter by price ranges
- **Real-time Search**: Search functionality for plans
- **Admin Panel**: Complete admin interface for managing content
- **Multi-page Site**: Home, Countries, About Us, and FAQ pages

## Project Structure

```
anytimeesim/
├── manage.py              # Django management script
├── anytimeesim/           # Project configuration
│   ├── __init__.py
│   ├── settings.py        # Django settings
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py           # WSGI application
├── esim_store/           # Main application
│   ├── __init__.py
│   ├── admin.py          # Admin configuration
│   ├── models.py         # Database models
│   ├── views.py          # View functions
│   ├── urls.py           # App URL configuration
│   └── management/       # Custom management commands
├── static/               # Static files
│   ├── css/style.css     # Custom styles
│   ├── js/main.js        # JavaScript functionality
│   └── images/          # Image assets
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   └── esim_store/      # App-specific templates
└── media/               # Uploaded files
```

## Models

### ESIMPlan
- Name, price, data amount, validity days
- Many-to-many relationship with countries
- Optional image upload
- Active/inactive status

### Country
- Country name and ISO code
- Optional flag image

### PageContent
- Dynamic page content (About Us, FAQ, etc.)
- Slug-based URL routing

### Order
- Customer information and order details
- Order status tracking

## Installation

1. **Clone and setup**:
   ```bash
   cd anytimeesim
   source venv/bin/activate
   ```

2. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

4. **Populate sample data**:
   ```bash
   python manage.py populate_data
   ```

5. **Start development server**:
   ```bash
   python manage.py runserver
   ```

## Usage

### Website URLs
- **Home**: `http://127.0.0.1:8000/` - Browse all eSIM plans with filtering
- **Countries**: `http://127.0.0.1:8001:8000/countries/` - Browse by country
- **Admin**: `http://127.0.0.1:8000/admin/` - Admin panel for content management

### Admin Panel Features
- **ESIM Plans**: Add, edit, delete eSIM plans
- **Countries**: Manage country list and flags
- **Page Content**: Edit About Us, FAQ, and other pages
- **Orders**: View and manage customer orders

### Filtering Options
- **Country Filter**: Filter plans by specific countries
- **Price Filter**: Filter by price ranges:
  - Under $10
  - $10 - $20
  - $20 - $50
  - Over $50
- **Search**: Real-time search by plan name, data amount, or country

## Customization

### Styling
The website uses a custom orange color scheme defined in CSS variables:
- Primary color: `#ff7f00` (low orange)
- Hover states and accents
- Responsive design for all devices

### Adding New Plans
1. Go to Admin panel
2. Navigate to ESIM Plans
3. Click "Add ESIM Plan"
4. Fill in details and select countries

### Adding New Countries
1. Go to Admin panel
2. Navigate to Countries
3. Click "Add Country"
4. Enter name and ISO code

## Technologies Used

- **Backend**: Django 6.0.2
- **Frontend**: Bootstrap 5, Font Awesome, Custom CSS/JS
- **Database**: SQLite (default)
- **Image Processing**: Pillow
- **Template Engine**: Django Templates

## Future Enhancements

- **Payment Integration**: Stripe or PayPal integration
- **User Registration**: Customer accounts and order history
- **Email Notifications**: Order confirmations and updates
- **API Endpoints**: REST API for mobile apps
- **Caching**: Redis for performance optimization
- **Deployment**: Production deployment configuration

## License

This project is open source and available under the MIT License.