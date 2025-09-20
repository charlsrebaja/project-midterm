# Environment Variables Setup

This project uses environment variables to store sensitive information like database credentials and email settings. Follow these steps to set up your environment:

## Setting Up Your .env File

1. Make sure you have a `.env` file in the root directory of the project. If not, create one.
2. Add the following variables to your `.env` file:

```
# Django Secret Key
SECRET_KEY=your_secret_key_here

# Debug Mode
DEBUG=True

# Database Configuration
DB_ENGINE=django.db.backends.mysql
DB_NAME=security_system_db
DB_USER=root
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

## Gmail App Password Setup

To use Gmail for sending emails, you need to set up an App Password:

1. Go to your Google Account settings: https://myaccount.google.com/
2. Navigate to Security > 2-Step Verification (enable it if not already enabled)
3. Scroll down to "App passwords" and click on it
4. Select "Mail" as the app and "Other" as the device (name it "Django Security System")
5. Click "Generate"
6. Copy the 16-character password (without spaces)
7. Paste it as the value for `EMAIL_HOST_PASSWORD` in your `.env` file

## Important Notes

- Never commit your `.env` file to version control
- The `.env` file is already added to `.gitignore` to prevent accidental commits
- For production, use a different set of credentials with stronger security
- Regularly rotate your app passwords for better security
