# Application Security Programming System

A comprehensive security system built with Django, featuring authentication with 2FA, cipher tools, joke API integration with QR codes, and automation capabilities.

## 📌 Features

### 🔐 Authentication & Security
- **User Registration & Login** with strong password validation
  - Username: minimum 6 characters
  - Password: minimum 8 characters with letters, numbers, and special characters
- **Account Lockout**: Automatic lockout after 3 failed login attempts (30-minute cooldown)
- **Two-Factor Authentication (2FA)** using Google Authenticator
- **Secure Session Management** with HTTPOnly cookies and CSRF protection

### 🔑 Cipher Tools
- **Atbash Cipher**: Reverses the alphabet (A→Z, B→Y)
- **Caesar Cipher**: Shifts letters by a custom value (default: 3)
- **Vigenère Cipher**: Uses a repeating keyword for encryption
- Real-time encryption/decryption with copy functionality

### 😄 JokeAPI Integration
- Fetch random jokes from JokeAPI
- Automatic encryption with all three cipher methods
- QR code generation for:
  - Original joke
  - Atbash encrypted version
  - Caesar encrypted version
  - Vigenère encrypted version
- Download all QR codes feature

### 🤖 Automation Module
- **Email Automation**: Send jokes to multiple recipients
- **SMS Automation**: Send jokes via SMS (Twilio-ready)
- **Scheduled Tasks**:
  - Daily joke emails at 9:00 AM
  - Daily joke SMS at 9:30 AM
  - Weekly session cleanup (Monday 2:00 AM)
- Manual trigger options for immediate sending

### 🎨 UI/UX
- Modern, responsive design with Tailwind CSS
- Glass morphism effects
- Sidebar navigation with collapsible menu
- Real-time clock display
- Toast notifications for user feedback
- Mobile-responsive layout

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- XAMPP (for MySQL)
- Redis (for Celery)
- Node.js (optional, for Tailwind CSS customization)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd project-midterm
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

If requirements.txt doesn't exist, install manually:
```bash
pip install django mysqlclient pillow qrcode django-otp pyotp requests celery redis django-crispy-forms crispy-tailwind
```

### Step 4: Setup MySQL Database

1. Start XAMPP and ensure MySQL is running
2. Open phpMyAdmin (http://localhost/phpmyadmin)
3. Create a new database named `security_system_db`
4. Update database settings in `security_system/settings.py` if needed:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'security_system_db',
        'USER': 'root',
        'PASSWORD': '',  # Default XAMPP password is empty
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Step 5: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 7: Start Redis Server (for Celery)
```bash
# Windows - Download Redis from: https://github.com/microsoftarchive/redis/releases
redis-server

# Linux/Mac
redis-server
```

### Step 8: Start Celery Worker (in a new terminal)
```bash
# Activate virtual environment first
celery -A security_system worker --loglevel=info
```

### Step 9: Start Celery Beat Scheduler (in another terminal)
```bash
# Activate virtual environment first
celery -A security_system beat --loglevel=info
```

### Step 10: Run Development Server
```bash
python manage.py runserver
```

Access the application at: http://localhost:8000

## 📁 Project Structure

```
project-midterm/
├── security_system/        # Main project settings
│   ├── settings.py        # Django settings
│   ├── urls.py           # Main URL configuration
│   └── celery.py         # Celery configuration
├── auth_app/             # Authentication module
│   ├── models.py         # Custom User model with lockout
│   ├── views.py          # Login, register, 2FA views
│   └── forms.py          # Custom authentication forms
├── ciphers/              # Cipher tools module
│   ├── utils.py          # Cipher implementations
│   └── views.py          # Cipher API endpoints
├── jokes/                # JokeAPI integration
│   └── views.py          # Joke fetching and QR generation
├── automation/           # Automation module
│   ├── tasks.py          # Celery tasks
│   └── views.py          # Automation dashboard
├── templates/            # HTML templates
│   ├── base.html         # Base template with sidebar
│   └── ...               # Module-specific templates
└── static/               # Static files (CSS, JS)
```

## 🔧 Configuration

### Email Settings (for automation)
Update in `security_system/settings.py`:
```python
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
```

### Twilio Settings (for SMS - optional)
Add to `security_system/settings.py`:
```python
TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_PHONE_NUMBER = '+1234567890'
```

## 📱 Setting up 2FA

1. Install Google Authenticator on your phone
2. Navigate to "2FA Settings" in the sidebar
3. Scan the QR code with Google Authenticator
4. Enter the 6-digit code to verify setup
5. 2FA is now enabled for your account

## 🧪 Testing the Application

### Test User Registration
1. Go to `/auth/register/`
2. Create account with:
   - Username: testuser (min 6 chars)
   - Password: Test@123! (8+ chars with letters, numbers, special chars)

### Test Cipher Tools
1. Navigate to "Cipher Tools"
2. Enter text to encrypt/decrypt
3. Select cipher type and mode
4. Process and copy results

### Test JokeAPI
1. Navigate to "JokeAPI & QR"
2. Click "Get Random Joke"
3. View encrypted versions and QR codes
4. Download QR codes if needed

### Test Automation
1. Navigate to "Automation"
2. Add email/SMS recipients
3. Trigger manual tasks or wait for scheduled execution

## 🐛 Troubleshooting

### MySQL Connection Error
- Ensure XAMPP MySQL is running
- Check database name and credentials in settings.py
- Create database if it doesn't exist

### Celery Not Working
- Ensure Redis is running
- Check Celery worker and beat are active
- Verify CELERY_BROKER_URL in settings

### 2FA Issues
- Ensure device time is synchronized
- Try removing and re-adding account in authenticator app
- Check that OTP_TOTP_ISSUER matches in settings

### Static Files Not Loading
```bash
python manage.py collectstatic
```

## 🔒 Security Considerations

- Change SECRET_KEY in production
- Set DEBUG = False in production
- Use HTTPS in production (set SECURE_SSL_REDIRECT = True)
- Configure proper ALLOWED_HOSTS
- Use environment variables for sensitive data
- Enable CSRF_COOKIE_SECURE and SESSION_COOKIE_SECURE with HTTPS

## 📄 License

This project is for educational purposes as part of a midterm project.

## 👥 Contributors

- Application Security Programming System Development Team

## 📞 Support

For issues or questions, please create an issue in the repository or contact the development team.

---

**Note**: This is a demonstration project showcasing various security features and should be properly configured for production use.
