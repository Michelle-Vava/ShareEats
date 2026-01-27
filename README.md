# ShareEats

**A community-driven food marketplace connecting local buyers and sellers in Antigonish.**

## 📍 Demo

Currently, ShareEats is designed for local deployment. See [Local Setup](#-local-setup) and [Running with Docker](#-running-with-docker) for instructions on getting started.

## ✨ Key Features

- **User Authentication & Verification**: Secure registration and login with phone number verification
- **Dual User Roles**: Separate seller and buyer profiles with customized experiences
- **Product Management**: Sellers can list food items with images, pricing, and availability tracking
- **Shopping Cart**: Full cart functionality with quantity management and real-time totals
- **Payment Integration**: Stripe integration for secure online payments
- **Order Management**: Track orders from placement to completion with status updates
- **Membership System**: Premium membership options for both buyers and sellers
- **Responsive Design**: Mobile-friendly interface for seamless browsing on any device

## 🛠 Tech Stack

**Backend:**
- Django 4.0.3 (Python 3.8+)
- PostgreSQL with psycopg2 driver
- Gunicorn WSGI server

**Frontend:**
- Django Templates
- Django Crispy Forms for enhanced form rendering
- Static file management with WhiteNoise

**Infrastructure & DevOps:**
- Docker & Docker Compose for containerization
- Heroku deployment support with django-heroku
- CI/CD configuration (originally Bitbucket Pipelines)

**Third-Party Integrations:**
- Stripe for payment processing
- Twilio for SMS verification
- AWS S3 (via django-storages) for media storage
- Phone number validation with phonenumber-field

**Security:**
- HTTPS enforcement in production
- Secure session management
- Environment-based configuration with python-dotenv

## 📸 Screenshots

![ShareEats Application](__screenshots/img.png)

*Browse the marketplace and discover local food items from community sellers*

## 🏗 Architecture Overview

ShareEats follows a traditional Django MVC (Model-View-Template) architecture:

**Data Models:**
- `User`: Extended Django AbstractUser with phone verification
- `SellerInfo`: Business details for sellers including contact info and membership
- `BuyerInfo`: Buyer profile information
- `Product`: Food items with pricing, availability, and Stripe integration
- `Cart`: Shopping cart items linked to orders
- `Order`: Order tracking with completion status
- `Purchase`: Historical purchase records

**Application Flow:**
1. Users register and verify their phone number via Twilio
2. Users can sign up as buyers, sellers, or both
3. Sellers create product listings with images stored in AWS S3
4. Buyers browse products, add to cart, and checkout via Stripe
5. Orders are tracked through completion with seller notifications

## 🚀 Local Setup

### Prerequisites
- Python 3.8+
- pip
- PostgreSQL
- virtualenv

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/Michelle-Vava/ShareEats.git
cd ShareEats
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables (create a `.env` file):
```bash
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost/shareeats
STRIPE_PUBLIC_KEY=your-stripe-public-key
STRIPE_SECRET_KEY=your-stripe-secret-key
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
```

5. Run database migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Start the development server:
```bash
python manage.py runserver 0.0.0.0:7000
```

8. Navigate to `http://localhost:7000` in your browser.

## 🐳 Running with Docker

ShareEats includes Docker support for easy containerization and deployment.

### Using Docker

1. Build the Docker image:
```bash
docker build -t shareeats .
```

2. Run the container:
```bash
docker run -p 7000:7000 shareeats
```

3. Access the application at `http://localhost:7000`

### Using Docker Compose

For a complete setup with PostgreSQL:

1. Uncomment the services in `docker-compose.yml`

2. Start the services:
```bash
docker-compose up -d
```

3. Run migrations:
```bash
docker-compose exec app python manage.py migrate
```

4. Access the application at `http://localhost:7000`

### Using Pre-built Images

Pull the latest image from Docker Hub:
```bash
docker pull mimivava26/share-eats:latest
```

Run the pulled image:
```bash
docker run --publish 7000:7000 mimivava26/share-eats:latest
```

## 🚢 Deployment Notes

### Heroku Deployment

ShareEats is configured for Heroku deployment with the included `Procfile` and `django-heroku` integration.

1. Create a Heroku app:
```bash
heroku create your-app-name
```

2. Add PostgreSQL addon:
```bash
heroku addons:create heroku-postgresql:hobby-dev
heroku pg:promote DATABASE_URL
```

3. Set environment variables:
```bash
heroku config:set ENVIRONMENT=PRODUCTION
heroku config:set DJANGO_SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
heroku config:set STRIPE_PUBLIC_KEY=your-stripe-public-key
heroku config:set STRIPE_SECRET_KEY=your-stripe-secret-key
heroku config:set TWILIO_ACCOUNT_SID=your-twilio-sid
heroku config:set TWILIO_AUTH_TOKEN=your-twilio-token
```

4. Deploy:
```bash
git push heroku main
```

5. Run migrations:
```bash
heroku run python manage.py migrate
```

### Production Considerations
- Ensure `DEBUG=False` in production
- Use secure secret keys and store them in environment variables
- Configure HTTPS enforcement
- Set up proper static file serving (WhiteNoise is included)
- Configure AWS S3 for media file storage
- Set up monitoring and logging

## 🗺 Roadmap / Next Improvements

**Planned Features:**
- [ ] Advanced search and filtering for products
- [ ] Seller ratings and reviews system
- [ ] Real-time notifications for order updates
- [ ] Mobile app (iOS/Android)
- [ ] Delivery tracking and scheduling
- [ ] Multi-language support
- [ ] Analytics dashboard for sellers
- [ ] Promotional codes and discount system
- [ ] Social media integration
- [ ] Email marketing campaigns

**Technical Improvements:**
- [ ] Upgrade to latest Django LTS version
- [ ] Add comprehensive test coverage
- [ ] Implement API endpoints (REST/GraphQL)
- [ ] Performance optimization and caching
- [ ] Enhanced security measures
- [ ] Automated CI/CD with GitHub Actions
- [ ] Database query optimization

---

**Project maintained by Michelle Vava** | [x2018uxm@stfx.ca](mailto:x2018uxm@stfx.ca)
